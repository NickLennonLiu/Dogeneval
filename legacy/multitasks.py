import multiprocessing
from tqdm import tqdm
import os
from codes.qa_generation.huawei.llm import get_vllm_model, get_qwen_answer
from loguru import logger
from time import sleep
import json



def worker(input_queue, output_list, gpu_id, batch_size):
    os.environ['CUDA_VISIBLE_DEVICES'] = str(gpu_id)

    try:
        llm = get_vllm_model()

        while not input_queue.empty():
            # 从队列中批量获取问题
            batch_questions = []
            for _ in range(batch_size):
                if not input_queue.empty():
                    batch_questions.append(input_queue.get())
                else:
                    break
            if batch_questions:
                prompts = [question['prompt'] for question in batch_questions]
                answers = get_qwen_answer(llm, prompts)
                generated_qas = [question.update({'generated_qa': answer.outputs[0].text}) for question, answer in zip(batch_questions, answers)]
                generated_qas = batch_questions

                logger.info(f"[worker {gpu_id}] Generated {len(generated_qas)} answers")
                # print(generated_qas)

                # 假设LLM的generate支持批处理
                output_list.extend(generated_qas)
    except Exception as err:
        logger.error(f"[worker {gpu_id}] {err}")
        sleep(5)


def multi_process(questions, output_file, category, num_gpus=4, batch_size=32):
    manager = multiprocessing.Manager()
    input_queue = manager.Queue()
    output_list = manager.list()
    
    for question in questions:
        input_queue.put(question)

    gpu_choices = [
        '0,1,2,3'
    ]

    processes = []
    # for gpu_id in range(num_gpus):
    for gpu_id in gpu_choices:
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
                for question in output_list[previous_len:current_len]:
                    f.write(json.dumps(question, ensure_ascii=False) + '\n')

            previous_len = current_len

    for p in processes:
        p.join()

    return list(output_list)