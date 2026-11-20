#!/bin/bash
# Serve a small model with vLLM (tool calling on), and the LoRA adapters that train_sft.py made for it.
# Free gratis account, one RTX 4090. The base model answers as NAME, each adapter by its own name:
#   cd ~/a4a && sbatch --export=ALL,PORT=8004 serve_student.sbatch
#   sbatch --export=ALL,PORT=8004,ADAPTERS="qwen3-1.7b-sft1=/storage/scratch/users/$USER/a4a/adapters/qwen3-1.7b-sft1" serve_student.sbatch
# Several adapters: ADAPTERS="name1=path1 name2=path2".
#SBATCH --job-name=vllm-student
#SBATCH --account=gratis
#SBATCH --qos=job_gratis
#SBATCH --partition=gpu
#SBATCH --gres=gpu:rtx4090:1
#SBATCH --cpus-per-task=8
#SBATCH --nodes=1
#SBATCH --mem=48G
#SBATCH --time=04:00:00
#SBATCH --output=%x-%j.out

set -euo pipefail
PORT="${PORT:-8004}"
echo "node=$(hostname) port=$PORT start=$(date -Is)"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
export HF_HOME="${HF_HOME:-/storage/scratch/users/$USER/hf}"
export HF_HUB_OFFLINE=1  # weights were downloaded on the login node
export VLLM_USE_FLASHINFER_SAMPLER=0  # its JIT build needs nvcc, which the GPU nodes lack
source "$HOME/envs/vllm/bin/activate"
LORA=()
if [ -n "${ADAPTERS:-}" ]; then
  LORA=(--enable-lora --max-loras 4 --max-lora-rank 64 --lora-modules $ADAPTERS)  # unquoted: one name=path per word
fi
exec vllm serve "${MODEL:-Qwen/Qwen3-1.7B}" \
  --served-model-name "${NAME:-qwen3-1.7b}" \
  --host 0.0.0.0 --port "$PORT" \
  --api-key "$(cat "$HOME/.vllm_api_key")" \
  --max-model-len 16384 \
  --gpu-memory-utilization 0.9 \
  --enable-auto-tool-choice --tool-call-parser hermes \
  "${LORA[@]}"
