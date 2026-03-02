"""Call graph utilities — callee/caller traversal with depth control."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CallGraphNode:
    """A node in the call graph traversal result."""

    qualified_name: str
    kind: str
    file_path: str
    line: int
    depth: int
    calls: list[str] = field(default_factory=list)
    called_by: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            'qualified_name': self.qualified_name,
            'kind': self.kind,
            'file_path': self.file_path,
            'line': self.line,
            'depth': self.depth,
            'calls': self.calls,
            'called_by': self.called_by,
        }
