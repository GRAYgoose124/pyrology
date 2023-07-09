import yaml
import os
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# <, =, =.., =@=, \=@=, =:=, =<, ==, =\=, >, >=, @<, @=<, @>, @>=, \=, \==, as, is, >:<, :<
BIN_TOKENS = ["<", "=", "=<", "==", ">", ">=", r"\=", r"\=="]
TOKENS = ["(", ")", ",", ";", ":-", "."] + BIN_TOKENS


def load_tokens(path):
    with open(path) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def write_tokens(tokens, filename):
    """Write tokens to a file and returns the YAML object."""
    if not os.path.exists("output"):
        os.mkdir("output")

    with open(filename, "w") as f:
        yml = yaml.dump(tokens)
        f.write(yml)

    return yml


def get_source(path):
    if os.path.exists(path):
        with open(path) as f:
            logger.info(" - Loaded source from `%s`.", path)
            return f.read()
    else:
        print(f"No such file: {path}")


def sanitize_src(source):
    # Filter comments
    source = "\n".join(
        [
            notcomment
            for notcomment in filter(
                lambda s: not s.startswith("%"), source.split("\n")
            )
        ]
    )

    # Filter non-whitelisted characters.
    sanitized = "".join(
        [c for c in source if c.isalpha() or c.isdigit() or c in "".join(TOKENS)]
    )

    return sanitized


def get_first_token_not_in_parens(string):
    """Get the index of the first binary operator not in parentheses."""
    return get_all_tokens_not_in_parens(string)[0]


def get_all_tokens_not_in_parens(string):
    """Get the indices of all binary operators not in parentheses."""
    return get_all_delims_not_in_parens(string, TOKENS)


def get_first_comma_not_in_parens(string):
    """Get the index of the first comma not in parentheses."""
    parens = 0
    for i, c in enumerate(string):
        if c == "(":
            parens += 1
        elif c == ")":
            parens -= 1
        elif c == "," and parens == 0:
            return i


def get_all_commas_not_in_parens(string):
    """Get the indices of all commas not in parentheses."""
    return get_all_delims_not_in_parens(string, ",")


def get_all_delims_not_in_parens(string, delims: str | list):
    """Get the indices of all delimiters not in parentheses."""
    parens = 0
    delims = list(delims)
    indices = []
    for i, c in enumerate(string):
        if c == "(":
            parens += 1
        elif c == ")":
            parens -= 1
        elif c in delims and parens == 0:
            indices.append((i, c))

    return indices
