import os
import pytest
import yaml

from future_algebra.tokenizer import tokenizer


@pytest.mark.skip(reason="not implemented yet")
def test_tokenizer():
    queries = ["mortal(socrates).", "human(socrates).", "man(adele)."]

    tokened = None
    with open("assets/script.futa") as f:
        # read script into a string
        script = f.read()
        tokened = tokenizer(script)

    if not os.path.exists('output'):
        os.mkdir('output')
    with open('output/tokened.yaml', 'w') as f:
        f.write(yaml.dump(tokened))