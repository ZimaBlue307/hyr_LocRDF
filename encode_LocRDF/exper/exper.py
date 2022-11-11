import os
import re
import pandas as pd


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


def get_insert_time(log_path: str) -> float:
    """
    从 insert.txt 的最后一行获取 数据导入时间 (单位: ms)
    """
    try:
        with open(log_path, 'r') as f:
            time_line = f.readlines()[-1]
            second = re.search(r'\d+\.?\d*s', time_line)[0][:-1]
            return float(second) * 1000
    except:
        return 0


def get_query_times(log_path: str):
    """
    从 query.txt 中提取 几种查询语句 分别的用时 (单位: ms)
    """
    try:
        with open(log_path, 'r') as f:
            content = f.read()
            time_strs = re.findall(r'time spent \d+/', content)
            times = list(map(lambda str: (float(str[len('time spent '):-1]) / 1000), time_strs))
            return times
    except:
        return [0] * 10


def get_message(dataset: str):
    return [get_insert_time(f'./log/{dataset}/insert.txt')] + get_query_times(f'./log/{dataset}/query.txt')


if __name__ == '__main__':
    lubm_list = get_datasets()

    df = pd.DataFrame(columns=['insert', 'USE', 'use', 'Q1', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8'], index=lubm_list)
    for i, dataset in enumerate(lubm_list):
        message = get_message(dataset)
        try:
            df.iloc[i] = message
        except:
            print(len(message), message)
    os.system('mkdir -p csv')
    df.to_csv('csv/nebula.csv')

    test_read = pd.read_csv('csv/nebula.csv', index_col=0)
    print(test_read)
