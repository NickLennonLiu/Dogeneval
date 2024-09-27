from transformers import AutoTokenizer

qwen_tokenizer = AutoTokenizer.from_pretrained("/home/junetheriver/models/Qwen/Qwen2-72B-Instruct-AWQ")

def get_qwen_token_num(text: str):
    return len(qwen_tokenizer.encode(text))

def get_openai_token_num(text: str):
    import tiktoken
    return len(tiktoken.encode(text))

def load_tokenizer(model_path: str):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return tokenizer

def get_token_num(text: str, tokenizer: AutoTokenizer):
    return len(tokenizer.encode(text))

if __name__ == "__main__":
    model_path = "/home/junetheriver/models/Qwen/Qwen2-72B-Instruct-AWQ"
    tokenizer = load_tokenizer(model_path)
    text = "你好，世界！"
    print(get_token_num(text, tokenizer))