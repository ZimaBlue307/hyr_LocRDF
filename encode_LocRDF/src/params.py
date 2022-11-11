import argparse


def get_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='lubm')
    args = parser.parse_args()
    return args
