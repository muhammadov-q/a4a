#!/bin/bash
# LoRA fine-tuning of a small model on the examples of `a4a train-data` (train_sft.py, in the folder sbatch is run from).
# Free gratis account, one RTX 4090; a 1.7B model with 1,000 short examples takes minutes.
#   cd ~/a4a && sbatch --export=ALL,DATA=/storage/scratch/users/$USER/a4a/data/sft1/train.jsonl,OUT=/storage/scratch/users/$USER/a4a/adapters/qwen3-1.7b-sft1 train_sft.sbatch
#   another model or other settings: add MODEL=Qwen/Qwen3-4B or EXTRA="--epochs 3 --rank 32" to --export
#SBATCH --job-name=a4a-train
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
echo "node=$(hostname) start=$(date -Is)"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
export HF_HOME="${HF_HOME:-/storage/scratch/users/$USER/hf}"
export HF_HUB_OFFLINE=1  # weights were downloaded on the login node
source "$HOME/envs/train/bin/activate"
# EXTRA is left unquoted on purpose: it holds several options
exec python "$SLURM_SUBMIT_DIR/train_sft.py" --data "$DATA" --out "$OUT" --model "${MODEL:-Qwen/Qwen3-1.7B}" ${EXTRA:-}
