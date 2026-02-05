from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

from src.grid import Grid  # IMPORTANT: adjust to your actual module path


@dataclass(frozen=True)
class Stimulus:
    id: str
    rule: str          # e.g. "color.cross_plus_recolor"
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
        d["input_grid"] = self.input_grid.as_list()
        d["output_grid"] = self.output_grid.as_list()
        return d
