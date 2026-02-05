from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class Stimulus:
    id: str
    rule: str  # e.g. "color.cross_plus_recolor"
    family: str  # e.g. "color" (inferred)
    seed: int
    params: Dict[str, Any]
    difficulty: Optional[Dict[str, Any]] = None  # Hard counting is the only case -> can be a separate method

    def to_json_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d
