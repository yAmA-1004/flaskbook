import pytest


def test_func1():
    assert 1 == 1


def test_func2():
    assert 2 == 2

@pytest.fixture
def app_data():
    return 3

def test_func3(app_data):
    assert app_data == 3


"""
def fact(n):
    if n <= 1:
        return 1
    else:
        return m * fact(n - 1)
    
def func
"""
