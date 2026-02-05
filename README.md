# ArcTaskCreator

Python-based framework for generating **ARC-like visual tasks**. 
These tasks are used as a dataset for research on **rule inference and rule application** processes in humans.

---

## Overview

The project generates pairs of grids (an **input** and its corresponding **output**) based on specific transformation rules such as:

- **Expansion** (e.g. star, plus, diagonal, single-step / infinite growth)
- **Attraction/repulsion** (e.g. pull, push, fall, float)
- **Occlusion** (e.g. reversal, rotation, mirror)
- **Color** (e.g. shape based recoloring)
- **Arithmetic** (e.g. inversion, counting, majority/minority, parity)

Each rule is implemented as a separate function, and families of rules are organized within .py modules.

---

## Repository Structure

```
ArcTaskCreator/
├── experiment/                # Pilot experiment design, data, analysis, Lab.js source files
├── out/                       # Generated examples organized by rule type
└── src/
    ├── tasks/
    │   ├── arithmetic.py
    │   ├── attraction.py
    │   ├── color.py
    │   ├── expansion.py
    │   └── occlusion.py
    ├── grid.py                # Grid logic and data structure
    ├── stimulus.py            # Stimulus dataclass for JSON dataset overview
    ├── util.py                # Helper functions
    ├── visualize.py           # Visualization i.e. figure generation
    └── main.py                # Main entry point for task generation
```

## Author & Acknowledgments

**Yavuz Karaca** — University of Tübingen  

Special thanks to **Prof. Dr. Martin V. Butz**, **Dr. Michael Bannert**, and **Prof. Dr. Andreas Bartels** for designing the experimental paradigm in which these tasks are used, but also for their constructive feedback and ideas during the development.



