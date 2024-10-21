import multiprocessing
from tqdm import tqdm
import json
import os
from loguru import logger
import re
import time

output_file = '/home/junetheriver/results/huawei/qa.txt'
model = '/home/junetheriver/models/qwen/Qwen1.5-14B-Chat'

# 每个进程运行的函数
def worker(input_queue, output_list, gpu_id, batch_size):
    # 通过环境变量指定使用的GPU
    os.environ['CUDA_VISIBLE_DEVICES'] = str(gpu_id)

    # 设置模型参数
    try:
        from vllm import LLM, SamplingParams
        # model = "/mnt/tenant-home_speed/xz/opsfm-xz/models/Qwen/Qwen1.5-32B-Chat"
        sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=8192, stop_token_ids=[151643, 151645], stop=['<|endoftext|>', '<|im_end|>'])
        llm = LLM(model=model, trust_remote_code=True, max_model_len=8192, tensor_parallel_size=1, gpu_memory_utilization=0.95)
        
        while not input_queue.empty():
            # 从队列中批量获取问题
            batch_questions = []
            for _ in range(batch_size):
                if not input_queue.empty():
                    batch_questions.append(input_queue.get())
                else:
                    break
            
            if batch_questions:
                answers = llm.generate(batch_questions, sampling_params, use_tqdm=False)  # 假设LLM的generate支持批处理
                output_list.extend(answers)
    except Exception as err:
        logger.error(f"[worker {gpu_id}] {err}")
        time.sleep(5)


def get_prompt(content: dict):
    # main prompt
    filename = content['name'].replace('/mnt/home/data/preprocessed_data/zh/zedx/', '').replace('.txt', '')
    filename = re.sub(r"Lib\d+-", "", filename)
    prompt = f"""我正在制作大模型微调语料。其中一个语料的来源的类别为：{content['class']}，语料的内容为：“{content['instruction']}”。现在，请你以问答对的形式，针对上面的语料内容构建出若干个问答对，内容可以包含部分重复。问题可能需要与类别结合，并尽可能根据上下文完整描述完整问题背景，回答需要能够完整地回答问题且不要篡改内容。
    问题应当是self-contain且有意义的，不需要结合语料即可单独回答，错误问题示例：告警是什么级别的？告警的名字是什么？这个告警如何处理？。正确问题示例：发生在核心网部件中的名为503的告警的处置流程是什么？发生在核心网的告警10052应该如何处理？
    如果该语料非常不完整（如语料中缺少关键的图表描述，或语料不完整，则直接输出空列表）。以json格式输出。样例：[{{"question": "在主题中，提取出的问题1", "answer": "问题对应的回答1"}},{{"question": "在主题中，提取出的问题2", "answer": "问题对应的回答2"}}]
    请直接输出json的内容：""".replace('\\n', '\n')

    # apply chat_template
    prompt = f"<|im_start|>system\nYou are a helpful assistant.<|im_end|><|im_start|>user\n{prompt}<|im_end|><|im_start|>assistant\n"
    return prompt

# 主函数
def main(questions, num_gpus=8, batch_size=32):
    manager = multiprocessing.Manager()
    input_queue = manager.Queue()
    output_list = manager.list()
    
    for question in questions:
        input_queue.put(get_prompt(question))

    processes = []
    for gpu_id in range(num_gpus):
        p = multiprocessing.Process(target=worker, args=(input_queue, output_list, gpu_id, batch_size))
        processes.append(p)
        p.start()

    with tqdm(total=len(questions)) as pbar:
        previous_len = 0
        while any(p.is_alive() for p in processes):
            current_len = len(output_list)
            pbar.update(current_len - previous_len)

            # Update file
            with open(output_file, 'at+') as f:
                for line in output_list[previous_len:current_len]:
                    string_text = line.outputs[0].text.replace('\n', '\\n')
                    f.write(f"{string_text}\n")

            previous_len = current_len

    for p in processes:
        p.join()

    return list(output_list)

if __name__ == "__main__":
    # Load questions
    logger.info("Loading file...")
    # questions = json.load(open('/mnt/tenant-home_speed/xz/opsfm-xz/data/ops_data/zh/zedx.json'))

    demo_file = "/home/junetheriver/datasets/huawei/processed/demo.txt"
    with open(demo_file, 'r') as f:
        content = f.read()

    questions = [
        {
            "name": "demo.txt",
            "class": "demo",
            "instruction": content
        }
    ]

    answers = main(questions, num_gpus=4)
    logger.info("Finished!")
