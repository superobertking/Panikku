from dataclasses import dataclass
from typing import Dict


@dataclass
class TestBank:
    table: Dict[str, str]
    voice: str = None
    cheatsheet: str = None
