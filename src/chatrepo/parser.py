"""chatrepo.parser – Static analysis of Python files."""
import ast
import json
from pathlib import Path
from typing import Any, Dict, List


def signature(node: ast.AST) -> str:
    """Return a readable signature for a function/method node."""
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return node.name
    args = [a.arg for a in node.args.args]
    return f"{node.name}({', '.join(args)})"


def extract_from_file(path: Path) -> List[Dict[str, Any]]:
    """Scan *path* and return a list of symbol dictionaries."""
    tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    symbols: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            symbols.append(
                {
                    "name": node.name,
                    "kind": "class" if isinstance(node, ast.ClassDef) else "function",
                    "signature": signature(node),
                    "lineno": node.lineno,
                    "docstring": ast.get_docstring(node) or "",
                    "path": str(path),
                }
            )
    return symbols


def parse_repo(root: Path) -> list[dict]:
    """Return all symbols found under *root*."""
    results: list[dict] = []
    for file in root.rglob("*.py"):
        results.extend(extract_from_file(file))
    return results


def save_symbols(symbols: list[dict], out_path: Path) -> None:
    """Dump *symbols* as pretty-printed JSON."""
    out_path.write_text(json.dumps(symbols, indent=2), encoding="utf-8")


if __name__ == "__main__":
    from .config import BASE_DIR

    repo = BASE_DIR / "data" / "tmp_repo"
    data = parse_repo(repo)
    save_symbols(data, Path(__file__).with_name("symbols.json"))
    print(f"✅ Parsed {len(data)} symbols")
