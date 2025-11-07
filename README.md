# ArcTaskCreator

**ArcTaskCreator** is a Python-based framework for generating **ARC-like visual puzzles**. 
These puzzles are used as a dataset for reseach on **rule inference and rule application** processes in humans.

---

## Overview

The project generates pairs of grids (an **input** and its corresponding **output**) based on specific transformation rules such as:

- **Arithmetic transformations** (e.g. inversion, parity, majority/minority recolor)
- **Attraction/repulsion rules** (e.g. gravity, fall, float, repulsion)
- **Expansion rules** (e.g. star, plus, diagonal growth)
- **Occlusion transformations** (e.g. reversal, rotation, mirror)

Each rule type is implemented as a distinct generator, producing both input/output matrices and visualized examples.

---

## 📁 Repository Structure
ArcTaskCreator/
├── misc/ # Lab.js demo configurations
├── out/ # Generated examples organized by rule type
├── src/
│ ├── tasks/
│ │ ├── arithmetic.py
│ │ ├── attraction.py
│ │ ├── expansion.py
│ │ └── occlusion.py
│ ├── grid.py # Grid logic and data structure
│ ├── util.py # Helper functions
│ ├── visualize.py # Visualization and figure generation
│ └── main.py # Main entry point for task generation
├── LICENSE
└── .gitignore

---

## Output

Generated puzzles are saved as **PNG image files** in subfolders under `/out/`, named according to their rule type.

**Example directory structure:**

out/
├── arithmetic_majority_recolor/
│ ├── task_01_input.png
│ ├── task_01_output.png
│ └── task_01_combined.png
└── occlusion_transform/
├── task_07_input.png
├── task_07_output.png
└── task_07_combined.png

Each folder contains:
- `*_input.png`: input grid before transformation  
- `*_output.png`: resulting grid after applying the rule  
- `*_combined.png`: side-by-side visualization of both

---

## ✨ Author

**Yavuz Karaca**  
Cognitive Science M.Sc. — University of Tübingen


