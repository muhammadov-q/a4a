"""LoRA fine-tuning of a small chat model on the examples of `a4a train-data`, on one GPU.

    python train_sft.py --data train.jsonl --model Qwen/Qwen3-1.7B --out adapters/sft1 [--epochs 2] [--lr 2e-4] [--rank 16]

Every example is one step of a teacher's run: the conversation so far with its tool list, and the next assistant
message. The prompt is rendered the way vLLM renders it when the student is tested: the model's own chat
template, thinking off, tool-call arguments as objects, and the start of the assistant turn added. The target
is that turn as the template writes it, up to and including <|im_end|>. Prompt and target are tokenized apart,
as at test time, where the server tokenizes the prompt and the model writes the rest. The loss is on the target
only, averaged over the target tokens of each optimizer step.

Writes the adapter (`save_pretrained`, which vLLM serves with --lora-modules) and train_log.json: arguments,
versions, the SHA-256 of the data, examples left out, and the loss of every step.

Needs torch, transformers and peft (the `train` environment of cluster/README.md); nothing from a4a.
"""

import argparse
import hashlib
import json
import math
import random
import time
from pathlib import Path

import peft
import torch
import transformers
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer


def with_objects(messages: list[dict]) -> list[dict]:
    """Tool-call arguments as objects, as vLLM passes them to the template; the template writes them back as JSON."""
    found = []
    for m in messages:
        if m.get("tool_calls"):
            m = {**m, "tool_calls": [{**c, "function": {**c["function"], "arguments": json.loads(c["function"]["arguments"] or "{}")}} for c in m["tool_calls"]]}
        found.append(m)
    return found


def encode(example: dict, tokenizer) -> tuple[list[int], list[int]] | str:
    """Token ids and labels (-100 on the prompt), or why the example cannot be used."""
    messages, tools = with_objects(example["messages"]), example["tools"] or None
    prompt = tokenizer.apply_chat_template(messages, tools=tools, add_generation_prompt=True, tokenize=False, enable_thinking=False)
    full = tokenizer.apply_chat_template([*messages, *with_objects([example["target"]])], tools=tools, tokenize=False, enable_thinking=False)
    if not full.startswith(prompt):
        return "the template renders the history differently once the target is added"
    target = full[len(prompt):].rstrip("\n")  # the model stops at <|im_end|>; the newline after it is the next turn's
    if not target.endswith("<|im_end|>"):
        return "the target does not end the turn"
    prompt_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
    target_ids = tokenizer(target, add_special_tokens=False)["input_ids"]
    return prompt_ids + target_ids, [-100] * len(prompt_ids) + target_ids


def schedule(step: int, steps: int, warmup: int) -> float:
    """Linear warm-up, then cosine down to zero."""
    if step < warmup:
        return (step + 1) / warmup
    return 0.5 * (1 + math.cos(math.pi * (step - warmup) / max(1, steps - warmup)))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--model", default="Qwen/Qwen3-1.7B")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--rank", type=int, default=16)
    parser.add_argument("--batch", type=int, default=16, help="examples per optimizer step (one at a time, gradients added up)")
    parser.add_argument("--warmup", type=float, default=0.05, help="share of the steps with a rising learning rate")
    parser.add_argument("--max-tokens", type=int, default=8192, help="a longer example is left out, not cut")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--check", action="store_true", help="only render and count the examples, and show the first one; no GPU needed")
    args = parser.parse_args()

    random.seed(args.seed)
    torch.manual_seed(args.seed)
    started = time.time()
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    raw = [json.loads(line) for line in args.data.read_text(encoding="utf-8").splitlines()]
    examples, left_out = [], {}
    for example in raw:
        encoded = encode(example, tokenizer)
        if isinstance(encoded, str) or len(encoded[0]) > args.max_tokens:
            why = encoded if isinstance(encoded, str) else f"longer than {args.max_tokens} tokens"
            left_out[why] = left_out.get(why, 0) + 1
            continue
        examples.append(encoded)
    print(f"{len(examples)} of {len(raw)} examples; left out: {left_out or 'none'}", flush=True)
    targets = [sum(label != -100 for label in labels) for _, labels in examples]
    if args.check:
        lengths = sorted(len(ids) for ids, _ in examples)
        print(f"tokens per example: median {lengths[len(lengths) // 2]}, longest {lengths[-1]}; target tokens in all: {sum(targets):,}")
        ids, labels = examples[0]
        first = next(i for i, label in enumerate(labels) if label != -100)
        print("--- prompt of the first example ---\n" + tokenizer.decode(ids[:first]) + "\n--- its target ---\n" + tokenizer.decode(ids[first:]))
        return

    model = AutoModelForCausalLM.from_pretrained(args.model, dtype=torch.bfloat16).cuda()
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.config.use_cache = False
    model = get_peft_model(model, LoraConfig(r=args.rank, lora_alpha=2 * args.rank, lora_dropout=0.05, target_modules="all-linear", task_type="CAUSAL_LM"))
    trainable, total = model.get_nb_trainable_parameters()
    print(f"trainable parameters: {trainable:,} of {total:,}", flush=True)
    optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=args.lr, weight_decay=0.0)

    groups = []
    for _ in range(args.epochs):
        order = list(range(len(examples)))
        random.shuffle(order)
        groups += [order[i:i + args.batch] for i in range(0, len(order), args.batch)]
    warmup = max(1, round(args.warmup * len(groups)))
    log = []
    model.train()
    for step, group in enumerate(groups):
        for g in optimizer.param_groups:
            g["lr"] = args.lr * schedule(step, len(groups), warmup)
        counted = sum(targets[i] for i in group)
        total_loss = 0.0
        for i in group:
            ids, labels = examples[i]
            out = model(input_ids=torch.tensor([ids]).cuda(), labels=torch.tensor([labels]).cuda())
            share = targets[i] / counted  # out.loss is the mean over this example's target tokens
            (out.loss * share).backward()
            total_loss += out.loss.item() * share
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)
        log.append({"step": step + 1, "loss": round(total_loss, 4), "lr": optimizer.param_groups[0]["lr"], "tokens": counted})
        if step % 5 == 0 or step + 1 == len(groups):
            print(f"step {step + 1}/{len(groups)} loss {total_loss:.4f} lr {optimizer.param_groups[0]['lr']:.2e} {time.time() - started:.0f} s", flush=True)

    args.out.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(args.out)
    tokenizer.save_pretrained(args.out)
    record = {"arguments": {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
              "data_sha256": hashlib.sha256(args.data.read_bytes()).hexdigest(), "examples": len(examples), "left_out": left_out,
              "trainable_parameters": trainable, "steps": len(groups), "seconds": round(time.time() - started),
              "versions": {"torch": torch.__version__, "transformers": transformers.__version__, "peft": peft.__version__},
              "gpu": torch.cuda.get_device_name(), "log": log}
    (args.out / "train_log.json").write_text(json.dumps(record, indent=1) + "\n")
    print(f"saved {args.out} after {record['seconds']} s", flush=True)


if __name__ == "__main__":
    main()
