# ArcTaskCreator

**ArcTaskCreator** is a Python-based framework for generating **ARC-like visual puzzles**. 
These puzzles are used as a dataset for research on **rule inference and rule application** processes in humans.

---

## Overview

The project generates pairs of grids (an **input** and its corresponding **output**) based on specific transformation rules such as:

- **Arithmetic** (e.g. inversion, parity, majority/minority recolor)
- **Attraction/repulsion** (e.g. gravity, fall, float, repulsion)
- **Expansion** (e.g. star, plus, diagonal growth)
- **Occlusion** (e.g. reversal, rotation, mirror)

Each rule is implemented as a distinct generator, producing both input/output grids.

---

## Repository Structure

```
ArcTaskCreator/
├── misc/                      # Lab.js demo configurations
├── out/                       # Generated examples organized by rule type
└── src/
    ├── tasks/
    │   ├── arithmetic.py
    │   ├── attraction.py
    │   ├── expansion.py
    │   └── occlusion.py
    ├── grid.py                # Grid logic and data structure
    ├── util.py                # Helper functions
    ├── visualize.py           # Visualization and figure generation
    └── main.py                # Main entry point for task generation
```

## Author

**Yavuz Karaca**  
University of Tübingen


