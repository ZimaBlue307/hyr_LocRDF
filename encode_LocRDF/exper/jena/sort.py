import os
import pandas as pd


def dataset_query_time(dataset: str, query: int):
    try:
        with open(f'./log/{dataset}/query{query}.txt', 'r') as f:
            lines = f.readlines()
            return float(lines[0])
    except:
        return 0


def get_datasets():
    """
    获取 log 下的测试数据集
    """
    datasets = list(os.listdir('./log'))
    datasets.sort()
    new_index = list(map(lambda dataset: int(dataset[4:]), datasets))
    new_index.sort()
    datasets_new = list(map(lambda index: f'lubm{index}', new_index))
    return datasets_new


if __name__ == '__main__':
    datasets = get_datasets()
    df = pd.DataFrame(columns=['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8'], index=datasets)
    for dataset in datasets:
        for query in range(0, 9):
            df.loc[dataset, f'q{query}'] = dataset_query_time(dataset, query)
    df *= 1000
    print(df)
    df.to_csv('./jena-query.csv')
