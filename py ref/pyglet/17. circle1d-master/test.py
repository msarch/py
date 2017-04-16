
from model import *

def test_length():
    assert Vec2(1, 0).length() == 1
    assert Vec2(0, 0).length() == 0

def test_eq():
    assert Vec2(1, 0) == Vec2(1, 0)

def test_neq():
    assert Vec2(0, 1) != Vec2(1, 0)

def test_normalize():
    assert Vec2(2, 0).normalize() == Vec2(1, 0)
    assert Vec2(0, 0).normalize() == Vec2(0, 0)

