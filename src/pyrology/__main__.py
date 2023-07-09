import logging
import os
import argparse

from pyrology.engine.core import KnowledgeEngine
from pyrology.engine.interactive import InteractiveKernel
from pyrology.engine.lexer.utils import get_source, write_tokens, load_tokens
from pyrology.engine.lexer.__main__ import IgnisTokenizer

logger = logging.getLogger(__name__)


def argparser():
    parser = argparse.ArgumentParser(description="Tokenize a source file.")
    parser.add_argument(
        "script", nargs="?", type=str, default=None, help="The source file to tokenize."
    )
    parser.add_argument(
        "--tokens",
        type=str,
        default=None,
        help="The token file to load into the parser-engine.",
    )
    parser.add_argument(
        "--save-tokens", default=True, action="store_true", help="Save the token file."
    )
    parser.add_argument(
        "--no-save-tokens",
        dest="save_tokens",
        action="store_false",
        help="Don't save the token file.",
    )

    parser.add_argument(
        "--debug", default=False, action="store_true", help="Enable debug mode."
    )
    parser.add_argument(
        "--info",
        default=False,
        action="store_true",
    )

    return parser


def pyrology_handle_args(tokenizer):
    parser = argparser()
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.info:
        logging.basicConfig(level=logging.INFO, format="%(message)s", force=True)
    else:
        logging.getLogger().setLevel(logging.CRITICAL + 1)

    if args.tokens is not None:
        path = args.tokens
        source = None
        load_tokens(path)

        logger.info("Loaded tokens from %s", path)
    elif args.script is not None:
        path = args.script
        source = get_source(path)
        tokenizer.prepare(source)

        logger.debug("\tTokenized %s", path)
    else:
        logger.error("No script or tokens provided.")
        parser.print_help()
        exit(1)

    if args.save_tokens:
        token_output_file = os.path.basename(path).split(".")[0]
        token_output_file = f"output/{token_output_file}.yml"
        yml = write_tokens(tokenizer.get_tokens(), token_output_file)
        logger.debug("\tSaved `%s` tokens to `%s`", path, token_output_file)
    else:
        token_output_file = None
        yml = None

    return {
        "input_file": path,
        "source": source,
        "tokens_yml": yml,
        "tokens_path": token_output_file,
    }


def main():
    tokenizer = IgnisTokenizer()
    metadata = pyrology_handle_args(tokenizer)

    engine = KnowledgeEngine(tokenizer=tokenizer, interactive=True)
    cli = InteractiveKernel(engine)

    cli.run()


if __name__ == "__main__":
    main()
