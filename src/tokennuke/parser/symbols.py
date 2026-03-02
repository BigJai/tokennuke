"""Symbol and CallEdge data structures."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Symbol:
    """A code symbol extracted from AST (function, class, method, etc.)."""

    name: str
    qualified_name: str
    kind: str  # function, class, method, constant, type, interface
    language: str
    file_path: str
    line: int
    end_line: int
    byte_offset: int
    byte_length: int
    signature: str = ''
    docstring: str = ''
    decorators: list[str] = field(default_factory=list)
    parent_name: str = ''
    children: list[Symbol] = field(default_factory=list, repr=False)
    calls: list[CallEdge] = field(default_factory=list, repr=False)


@dataclass
class CallEdge:
    """A function call expression found inside a symbol body."""

    callee_name: str
    line: int
    caller_qualified_name: str = ''
