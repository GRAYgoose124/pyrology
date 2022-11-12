import logging
import os
import argparse

from pyrology.engine.lib import KnowledgeEngine
from pyrology.utils import get_source, load_tokens, write_tokens
from pyrology.lexer import tokenstream

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def argparser():
    parser = argparse.ArgumentParser(description="Tokenize a source file.")
    parser.add_argument('script', nargs='?', type=str, default=None, help="The source file to tokenize.")
    parser.add_argument('--tokens', type=str, default=None, help="The token file to load into the parser-engine.")
    parser.add_argument('--save-tokens', default=True, action='store_true', help="Save the token file.")

    return parser


def pyrology_handle_args(parser):
    args = parser.parse_args()

    if args.tokens is not None:
        path = args.tokens
        source = None

        tokens = load_tokens(path)

        logger.info('Loaded tokens from %s', path)
    elif args.script is not None:
        path = args.script
        source = get_source(path)

        tokens = tokenstream(source)
        logger.info('Tokenized %s', path)
    else:
        logger.error("No script or tokens provided.")
        parser.print_help()
        exit(1)

    if args.save_tokens:
        token_output_file = os.path.basename(path).split('.')[0]
        token_output_file = f"output/{token_output_file}.yml"
        yml = write_tokens(tokens, token_output_file)
    else:
        token_output_file = None
        yml = None

    return {
        'input_file': path,
        'source': source,
        'tokens': tokens, 
        'tokens_yml': yml,
        'tokens_path': token_output_file
    }

def main():
    parser = argparser()

    parsed = pyrology_handle_args(parser)
    tokens = parsed['tokens']

    engine = KnowledgeEngine(tokens)

    

if __name__ == "__main__":
    main()