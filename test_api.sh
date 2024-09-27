curl http://10.0.0.4:8080/v1/chat/completions -H "Content-Type: application/json" -d '{
  "model": "/models/Qwen/Qwen2-72B-Instruct-AWQ",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Tell me something about large language models."}
  ],
  "temperature": 0.7,
  "top_p": 0.8,
  "repetition_penalty": 1.05,
  "max_tokens": 512
}'
