from load_document import iter_folder

def _form_docs_prompt(docs):
    merged = ""
    for doc in docs:
        merged += f"path: {doc['path']}\n"
        merged += "=========================\n"
        merged += f"{doc['content']}\n"
        merged += "=========================\n"
    return merged

root_path = '/home/junetheriver/codes/qa_generation/huawei/data/UNC_20.9.5/'


def get_max_token_paths(root_path, max_token_num):
    recorded_paths = []

    save_recorded_path = f"data/paths/{max_token_num}_paths_tmp.txt"

    def record_docs(path):
        with open(save_recorded_path, "a") as f:
            f.write(path + "\n")
        recorded_paths.append(path)

    iter_folder(root_path, max_token_num, record_docs, merge_method=_form_docs_prompt)
    
    with open(f"data/paths/{max_token_num}_paths.txt", 'w') as f:
        f.write("\n".join(recorded_paths))


get_max_token_paths(root_path, 2000)
get_max_token_paths(root_path, 4000)
get_max_token_paths(root_path, 6000)
get_max_token_paths(root_path, 8000)
get_max_token_paths(root_path, 10000)