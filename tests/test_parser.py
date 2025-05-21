from pathlib import Path
from chatrepo.parser import signature

def test_signature():
    import ast
    node = ast.parse("def foo(a, b): pass").body[0]
    assert signature(node) == "foo(a, b)"

def test_parse_repo(tmp_path):
    pass