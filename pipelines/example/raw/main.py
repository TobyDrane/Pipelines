from dagster import asset

from utils.utils import test_func

@asset
def main():
    test_func()

@asset
def func1():
    print('HELLO WORLD')