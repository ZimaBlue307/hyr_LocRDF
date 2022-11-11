import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plt_size():
    size_csv: pd.DataFrame = pd.read_csv('./csv/size.csv', index_col=0).iloc[5:]
    plt.figure(-2, figsize=(20, 10))
    wid = 0.2
    for i, column in enumerate(size_csv.columns):
        plt.bar(np.arange(len(size_csv)) + wid * (i - len(size_csv.columns) // 2), size_csv[column], label=column, width=wid)
        for x, y in zip(np.arange(len(size_csv)) + wid * (i - len(size_csv.columns) // 2), size_csv[column]):
            plt.text(x, y, f'{y:.2f}MB', ha='center', va='bottom', fontsize=13)
    plt.title('size (MB)', fontsize=30)
    plt.xticks(np.arange(len(size_csv)), size_csv.index, rotation=0, fontsize=30)
    plt.yticks(np.arange(0, size_csv.max().max() + 200, 200), list(map(lambda x: f'{x} MB', np.arange(0, size_csv.max().max() + 200, 200))), fontsize=20)
    plt.legend(fontsize=20)
    plt.savefig('./img/size.svg')


def plt_insert():
    nebula_csv = pd.read_csv('./csv/nebula.csv', index_col=0).iloc[5:]
    jena_csv = pd.read_csv('./csv/jena.csv', index_col=0).iloc[5:]
    insert_csv = pd.concat([nebula_csv['insert'], jena_csv['insert']], axis=1)
    insert_csv.columns = ['nebula', 'jena']
    insert_csv /= 1000
    tmp = [1000, 20]
    for i, column in enumerate(insert_csv.columns):
        plt.figure(i - 1, figsize=(20, 10))
        plt.bar(np.arange(len(insert_csv)), insert_csv[column])
        for x, y in zip(np.arange(len(insert_csv)), insert_csv[column]):
            plt.text(x, y, f'{y:.2f}s', ha='center', va='bottom', fontsize=20)
        plt.title(f'insert-{column} (s)', fontsize=30)
        plt.xticks(np.arange(len(insert_csv)), insert_csv.index, rotation=0, fontsize=20)
        plt.yticks(np.arange(0, insert_csv.max()[column] + tmp[i], tmp[i]), list(map(lambda x: f'{x:.0f} s', np.arange(0, insert_csv.max()[column] + tmp[i], tmp[i]))), fontsize=20)
        plt.savefig(f'./img/insert-{column}.svg')


def plt_query_template(i: int, title: str):
    nebula_csv = pd.read_csv('./csv/nebula.csv', index_col=0).iloc[5:]
    jena_csv = pd.read_csv('./jena/jena-query.csv', index_col=0).iloc[5:]
    query_csv = pd.concat([nebula_csv[f'q{i}'], jena_csv[f'q{i}']], axis=1)
    query_csv.columns = ['nebula', 'jena']
    query_csv = query_csv.T
    plt.figure(i, figsize=(20, 10))
    wid = 0.15
    for idx, column in enumerate(query_csv.columns):
        plt.bar(np.arange(len(query_csv)) + wid * (idx - len(query_csv.columns) // 2), query_csv[column], label=column, width=wid)
        # 显示 bar 的值
        for x, y in zip(np.arange(len(query_csv)) + wid * (idx - len(query_csv.columns) // 2), query_csv[column]):
            plt.text(x, y, f'{y:.2f}ms', ha='center', va='bottom', fontsize=20)
    plt.title(title, fontsize=30)
    plt.xticks(np.arange(len(query_csv.index)), query_csv.index, rotation=0, fontsize=30)
    plt.yticks(fontsize=20)
    plt.legend(fontsize=20)
    plt.savefig(f'./img/query{i}.svg')


def plt_query_all():
    for i in range(1, 5):
        plt_query_template(i, title=f'lumb5 query Q{i} (ms)')


def plt_query_normal():
    for i in range(5, 9):
        plt_query_template(i, title=f'lumb5 query Q{i} (ms)')


def plt_first_query():
    nebula_csv = pd.read_csv('./csv/nebula.csv', index_col=0).iloc[5:]
    jena_csv = pd.read_csv('./jena/jena-query.csv', index_col=0).iloc[5:]
    query_csv = pd.concat([nebula_csv[f'q1'], jena_csv[f'q0']], axis=1)
    # 给 query_csv 取 log10
    query_csv :pd.DataFrame = np.log10(query_csv)
    query_csv.columns = ['nebula', 'jena']
    query_csv = query_csv.T
    plt.figure(9, figsize=(20, 10))
    wid = 0.15
    for idx, column in enumerate(query_csv.columns):
        plt.bar(np.arange(len(query_csv)) + wid * (idx - len(query_csv.columns) // 2), query_csv[column], label=column, width=wid)
        # 显示 bar 的值
        for x, y in zip(np.arange(len(query_csv)) + wid * (idx - len(query_csv.columns) // 2), query_csv[column]):
            plt.text(x, y, f'$10^{{{y:.2f}}}$ ms', ha='center', va='bottom', fontsize=15)
    plt.title('first query (ms)', fontsize=30)
    plt.xticks(np.arange(len(query_csv.index)), query_csv.index, rotation=0, fontsize=30)
    plt.yticks(np.arange(6), list(map(lambda x: f'$10^{{{x:.0f}}}$ ms', np.arange(6))), fontsize=20)
    plt.legend(fontsize=20)
    plt.savefig(f'./img/first-query.svg')


if __name__ == '__main__':
    if not os.path.exists('./img'):
        os.mkdir('./img')
    plt_size()
    # plt_insert()
    plt_query_all()
    plt_query_normal()
    plt_first_query()
    plt.show()
