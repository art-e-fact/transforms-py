from transforms_py._core import hello_from_bin, hello_transforms, PyRegistry


def hello() -> str:
    return hello_from_bin()

def hello_t() -> str:
    return hello_transforms()
