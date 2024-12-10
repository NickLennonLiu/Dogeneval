cd /home/junetheriver/codes/qa_generation/huawei/llama-factory
TRITON_CACHE_DIR=/tmp llamafactory-cli train /home/junetheriver/codes/qa_generation/huawei/dogeneval/finetune/scripts/qwen2.5_lora_sft_awq.yaml \
&& \
TRITON_CACHE_DIR=/tmp llamafactory-cli train /home/junetheriver/codes/qa_generation/huawei/dogeneval/finetune/scripts/qwen2.5_lora_predict.yaml