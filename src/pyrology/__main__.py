import os
import argparse

from pyrology.utils import get_source, write_tokens
from pyrology.lexer import tokenstream



def main():
    parser = argparse.ArgumentParser(description="Tokenize a source file.")
    parser.add_argument('script', type=str, help="The source file to tokenize.")
    args = parser.parse_args()

    path = args.script
    name = os.path.basename(path).split('.')[0]

    source = get_source(path)
    tokened = tokenstream(source)

    yml = write_tokens(tokened, f"output/{name}.yaml")
    

if __name__ == "__main__":
    main()