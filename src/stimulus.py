from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

from grid import Grid


@dataclass(frozen=True)
class Stimulus:
    id: str
    family: str
    rule: str
    seed: int
    params: Dict[str, Any]
    input_grid: Grid
    output_grid: Grid
    forced_tags: Optional[List[str]] = None
    observed_tags: Optional[List[str]] = None
    difficulty: Optional[Dict[str, Any]] = None
    provenance: Optional[Dict[str, Any]] = None

    def to_json_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # Replace Grid objects with raw matrices for JSON
        d["input_grid"] = self.input_grid.as_list()
        d["output_grid"] = self.output_grid.as_list()
        return d