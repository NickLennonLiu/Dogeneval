"""
从生成的QA中每类题目都采样一定数量的题目
"""
from dogeneval.utils.mongodb import load_results_as_df
from dogeneval.utils.abbr_mapping import task_to_ability, task_to_abbr, df_col_rename, export_order
from dogeneval.validation.filters import filter_shot, main_filter

def sample_qa_by_group(df, group_col, sample_num):
    # 按group_col分组，每组采样sample_num个题目
    sampled_df = df.groupby(group_col).apply(lambda x: x.sample(min(len(x), sample_num))).reset_index(drop=True)
    return sampled_df

if __name__ == "__main__":
    collection_name = "QA_GEN-11022040"


    df = load_results_as_df(collection_name)

    df = main_filter(df)

    df = filter_shot(df, is_zeroshot=False)

    group_col = "task"
    sample_num = 10
    sampled_df = sample_qa_by_group(df, group_col, sample_num)
    sampled_df['ability'] = task_to_ability(sampled_df)

    export_order = [col for col in export_order if col in sampled_df.columns]
    sampled_df = sampled_df[export_order]
    
    sampled_df['task'] = task_to_abbr(sampled_df)
    sampled_df = df_col_rename(sampled_df)


    print(len(sampled_df))
    sampled_df.to_csv("/home/junetheriver/codes/qa_generation/huawei/outputs/sampled_qa.csv", index=False)
    sampled_df.to_excel("/home/junetheriver/codes/qa_generation/huawei/outputs/sampled_qa.xlsx", index=False)
