import argparse
import os
import yaml


from future_algebra.tokenizer import tokenizer


def main(args):
    pass
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('script', type=str, help='The script to run')
    args = parser.parse_args()

    main(args)