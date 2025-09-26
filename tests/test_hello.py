import pytest

from transforms_py import hello

def test_hello():
    result = hello()
    assert isinstance(result, str)
    assert len(result) > 0