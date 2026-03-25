from dataclasses import dataclass


@dataclass
class Note:
    path: str
    title: str
    content: str


@dataclass
class Summary:
    note_path: str
    abstract: str


@dataclass
class ContextBundle:
    bundle_id: str
    goal: str
    summary_count: int
