#!/bin/bash
# Serve Qwen3-Embedding-4B with vLLM as an OpenAI-compatible embeddings endpoint (/v1/embeddings),
# for `repo2tools corpus-saturation`. Free gratis account, one RTX 4090 (24 GB).
#SBATCH --job-name=vllm-qwen3-embed
#SBATCH --account=gratis
#SBATCH --qos=job_gratis
#SBATCH --partition=gpu
#SBATCH --gres=gpu:rtx4090:1
#SBATCH --cpus-per-task=8
#SBATCH --nodes=1
#SBATCH --mem=48G
#SBATCH --time=02:00:00
#SBATCH --output=%x-%j.out

set -euo pipefail
echo "node=$(hostname) port=8000 start=$(date -Is)"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
export HF_HOME="${HF_HOME:-/storage/scratch/users/$USER/hf}"
export HF_HUB_OFFLINE=1  # weights were downloaded on the login node
source "$HOME/envs/vllm/bin/activate"
exec vllm serve Qwen/Qwen3-Embedding-4B \
  --served-model-name qwen3-embedding-4b \
  --runner pooling \
  --host 0.0.0.0 --port 8000 \
  --api-key "$(cat "$HOME/.vllm_api_key")" \
  --max-model-len 4096 \
  --gpu-memory-utilization 0.90
