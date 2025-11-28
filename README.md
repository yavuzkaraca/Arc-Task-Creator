# ArcTaskCreator

Python-based framework for generating **ARC-like visual tasks**. 
These tasks are used as a dataset for research on **rule inference and rule application** processes in humans.

---

## Overview

The project generates pairs of grids (an **input** and its corresponding **output**) based on specific transformation rules such as:

- **Expansion** (e.g. star, plus, diagonal, single-step / infinite growth)
- **Attraction/repulsion** (e.g. pull, push, fall, float)
- **Occlusion** (e.g. reversal, rotation, mirror)
- **Arithmetic** (e.g. inversion, counting, majority/minority, parity)

Each rule is implemented as a separate function, and families of rules are organized within .py modules.

---

## Repository Structure

```
ArcTaskCreator/
├── experiment/                # Experiment design, data, analysis, Lab.js source files
├── misc/                      # Previous Lab.js demos
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

## ✨ Author & Acknowledgments

**Yavuz Karaca** — University of Tübingen  

Special thanks to **Prof. Dr. Martin V. Butz**, **Dr. Michael Bannert**, and **Prof. Dr. Andreas Bartels**  
for their valuable feedback and discussions on the design and use of these puzzles.



