import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_functor(term):
    try:
        functor, args = term.split("(", 1)
    except ValueError as e:
        print(f"Invalid term: {term}")
        return

    args = args.split(")")[0].split(",")
    args = [arg.strip() for arg in args]
    logger.debug(f"Functor: {functor}, Args: {args}")

    return functor, args


def get_name(functor, args):
    return f"{functor}/{len(args)}"
