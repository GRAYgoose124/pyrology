import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_functor(term):
    try:
        functor, args = term.split('(', 1)
    except ValueError as e:
        print(f"Invalid term: {term}")
        return None

    args = args.split(')')[0].split(',')
    logger.debug(f"Functor: {functor}, Args: {args}")

    return functor, args


def get_name(functor, args):
    arity = len(args)

    return f"{functor}/{arity}"

