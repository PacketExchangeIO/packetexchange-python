#!/usr/bin/env python3
"""Generate typed models and the operations table from the OpenAPI document.

    python3 scripts/generate.py [path/to/openapi.json]

Reads ``openapi.json`` at the repository root (a copy of the document the API serves
at https://packetexchange.io/api/v1/docs/json) and writes
``src/packetexchange/_generated/models.py`` and ``operations.py``.

A small purpose-built generator keeps the output buildable offline with the standard
library only, importable on Python 3.9, and free of runtime dependencies beyond httpx.
The document uses a small, predictable subset of JSON Schema; anything outside it
degrades to ``Any`` rather than failing.
"""

from __future__ import annotations

import json
import keyword
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "openapi.json"
OUT = HERE.parent / "src" / "packetexchange" / "_generated"


def ident(name: str) -> str:
    """A component name as a Python identifier."""
    s = re.sub(r"[^A-Za-z0-9_]", "_", name)
    return f"_{s}" if s[:1].isdigit() else s


def py_type(s: object) -> str:
    """JSON Schema (OpenAPI 3.0 dialect) -> a Python type expression (as a string)."""
    if not isinstance(s, dict):
        return "Any"
    if "$ref" in s:
        t = f'"{ident(s["$ref"].split("/")[-1])}"'
    elif isinstance(s.get("enum"), list):
        t = "Literal[" + ", ".join(json.dumps(v) if not isinstance(v, bool) else str(v) for v in s["enum"]) + "]"
    elif "anyOf" in s or "oneOf" in s:
        t = "Union[" + ", ".join(py_type(x) for x in s.get("anyOf") or s.get("oneOf")) + "]"
    elif "allOf" in s:
        # TypedDicts cannot be intersected inline; the first member is the useful one.
        t = py_type(s["allOf"][0]) if s["allOf"] else "Any"
    else:
        ty = s.get("type")
        if ty == "string":
            t = "str"
        elif ty == "integer":
            t = "int"
        elif ty == "number":
            t = "float"
        elif ty == "boolean":
            t = "bool"
        elif ty == "array":
            t = f"List[{py_type(s.get('items'))}]"
        elif ty == "object" or (ty is None and "properties" in s):
            # Nested objects stay loose; named components carry the precise shapes.
            t = "Dict[str, Any]"
        else:
            t = "Any"
    if s.get("nullable"):
        t = f"Optional[{t}]"
    return t


def doc(text: object, indent: str = "    ") -> str:
    if not text:
        return ""
    body = str(text).replace('"""', "'''").replace("\\", "\\\\")
    return f'{indent}"""{body}"""\n'


def emit_model(name: str, s: dict) -> str:
    """One TypedDict per object component; a type alias for anything else."""
    cls = ident(name)
    if s.get("type") != "object" and "properties" not in s:
        comment = f"  # {s['description']}" if s.get("description") else ""
        return f"{cls} = {py_type(s)}{comment}\n\n"
    props: dict = s.get("properties") or {}
    required = set(s.get("required") or [])
    req = {k: v for k, v in props.items() if k in required}
    opt = {k: v for k, v in props.items() if k not in required}

    def plain(k: str) -> bool:
        return k.isidentifier() and not keyword.iskeyword(k)

    out = ""
    if all(plain(k) for k in props):
        # Two-class pattern: required keys in a total base, optional keys total=False.
        # (NotRequired would be neater but needs typing_extensions below 3.11.)
        base = f"_{cls}Required"
        out += f"class {base}(TypedDict):\n"
        out += "".join(f"    {k}: {py_type(v)}\n" for k, v in req.items()) or "    pass\n"
        out += f"\n\nclass {cls}({base}, total=False):\n"
        out += doc(s.get("description")) or ""
        for k, v in opt.items():
            out += f"    {k}: {py_type(v)}\n"
            if v.get("description") if isinstance(v, dict) else None:
                out += f"    # {str(v['description']).splitlines()[0]}\n"
        if not opt and not s.get("description"):
            out += "    pass\n"
        return out + "\n\n"
    # A key that is not a Python identifier: functional form, every key optional.
    fields = ", ".join(f"{json.dumps(k)}: {py_type(v)}" for k, v in props.items())
    return f"{cls} = TypedDict({json.dumps(cls)}, {{{fields}}}, total=False)\n\n"


def main() -> None:
    spec = json.loads(SPEC.read_text())
    schemas: dict = spec.get("components", {}).get("schemas", {})
    header = (
        "# Do not edit by hand: produced by scripts/generate.py.\n"
        f"# Source: openapi.json (PacketExchange API {spec.get('info', {}).get('version', '')}).\n"
        "# Regenerate with: python3 scripts/generate.py\n"
    )

    models = header + (
        '"""Typed shapes of the API\'s documented schemas.\n\n'
        "Money fields are USD decimal strings with 6 places (\"0.012500\"): use\n"
        "decimal.Decimal for arithmetic, never float.\n"
        '"""\n\n'
        "from __future__ import annotations\n\n"
        "from typing import Any, Dict, List, Literal, Optional, TypedDict, Union\n\n\n"
    )
    for name, s in schemas.items():
        models += emit_model(name, s)
    models += "__all__ = [" + ", ".join(json.dumps(ident(n)) for n in schemas) + "]\n"

    ops = []
    for path, item in (spec.get("paths") or {}).items():
        for method, op in item.items():
            if isinstance(op, dict) and op.get("operationId"):
                ops.append((op["operationId"], method.upper(), path, (op.get("tags") or [""])[0], op.get("summary", "")))
    ops.sort()
    operations = header + (
        '"""Every operation in the spec, keyed by operationId.\n\n'
        "Use with PacketExchange.call_operation(operation_id, ...) to reach an endpoint\n"
        "that has no convenience method yet. Paths include the /api/v1 prefix.\n"
        '"""\n\n'
        "from typing import Dict, NamedTuple\n\n\n"
        "class Operation(NamedTuple):\n"
        "    method: str\n"
        "    path: str\n"
        "    tag: str\n"
        "    summary: str\n\n\n"
        "OPERATIONS: Dict[str, Operation] = {\n"
    )
    for oid, m, p, tag, summ in ops:
        operations += f"    {json.dumps(oid)}: Operation({json.dumps(m)}, {json.dumps(p)}, {json.dumps(tag)}, {json.dumps(summ)}),\n"
    operations += "}\n"

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "models.py").write_text(models)
    (OUT / "operations.py").write_text(operations)
    (OUT / "__init__.py").write_text(
        header + '"""Code generated from the OpenAPI spec (models + operations table)."""\n\n'
        "from .models import *  # noqa: F401,F403\n"
        "from .operations import OPERATIONS, Operation  # noqa: F401\n"
    )
    print(f"{len(schemas)} models + {len(ops)} operations -> {OUT}")


if __name__ == "__main__":
    main()
