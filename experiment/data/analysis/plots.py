import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
import pandas as pd


def plot_task_accuracy_hierarchical_plain(task_stats):
    ts = task_stats.copy()
    ts["task_id"] = ts["task_id"].astype(int)
    ts = ts.sort_values("task_id")

    fig, ax = plt.subplots(figsize=(14, 6))

    # --- plain bars ---
    ax.bar(ts["task_id"], ts["accuracy"], color="#aaa6c4", edgecolor="black")

    ax.set_ylim(0, 1)
    ax.set_ylabel("Accuracy")
    ax.set_xticks(ts["task_id"])
    ax.set_xticklabels(ts["task_id"])

    # --- CHANCE LINE ---
    ax.axhline(0.5, color="black", linestyle="--", linewidth=1.2)
    # --- Good ---
    ax.axhline(0.7, color="green", linestyle="--", linewidth=1.2)

    plt.subplots_adjust(bottom=0.25)
    plt.title("Task Accuracy")
    plt.grid(axis="y", alpha=0.3)
    plt.show()


def plot_task_accuracy_hierarchical(task_stats):
    ts = task_stats.copy()
    ts["task_id"] = ts["task_id"].astype(int)
    ts = ts.sort_values("task_id")

    colors = {
        1: "#e6e1ff",
        2: "#aaa6c4",
        3: "#646982",
    }
    bar_colors = ts["difficulty"].map(colors)

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(ts["task_id"], ts["accuracy"], color=bar_colors, edgecolor="black")

    ax.set_ylim(0, 1)
    ax.set_ylabel("Accuracy")
    ax.set_xticks(ts["task_id"])
    ax.set_xticklabels(ts["task_id"])

    for x in [9.5, 19.5, 29.5]:
        ax.axvline(x, color="#252440", linewidth=5, linestyle="--")

    ax.axhline(0.5, color="black", linestyle="--", linewidth=1.2)
    ax.axhline(0.7, color="green", linestyle="--", linewidth=1.2)

    for i in range(0, 40, 5):
        label = "Inf" if (i % 10) < 5 else "App"
        x0, x1 = i - .4, i + 4 + .4
        y = -0.08
        ax.plot([x0, x1], [y, y], transform=ax.get_xaxis_transform())
        ax.text((x0 + x1) / 2, y - .02, label, ha="center", va="top",
                transform=ax.get_xaxis_transform())

    families = ["Expansion", "Attraction", "Occlusion", "Arithmetic"]
    for i, fam in zip(range(0, 40, 10), families):
        x0, x1 = i - .4, i + 9 + .4
        y = -0.20
        ax.plot([x0, x1], [y, y], transform=ax.get_xaxis_transform())
        ax.text((x0 + x1) / 2, y - .02, fam, ha="center", va="top",
                transform=ax.get_xaxis_transform())

    legend = [
        Patch(facecolor="#e6e1ff", edgecolor="black", label="Difficulty 1"),
        Patch(facecolor="#aaa6c4", edgecolor="black", label="Difficulty 2"),
        Patch(facecolor="#646982", edgecolor="black", label="Difficulty 3"),
    ]
    ax.legend(handles=legend, loc="upper right")

    plt.subplots_adjust(bottom=0.25)
    plt.title("Task Accuracy")
    plt.grid(axis="y", alpha=0.3)
    plt.show()


def plot_rule_stats(rule_stats):
    rs = rule_stats.copy()

    # enforce grouping order by super_rule
    ordered_rows = []
    for sr in rs["super_rule"].unique():
        ordered_rows.append(rs[rs["super_rule"] == sr])
    rs = pd.concat(ordered_rows, ignore_index=True)

    # labels + colors
    labels = []
    colors = []
    for _, row in rs.iterrows():
        if pd.isna(row["sub_rule"]) or row["sub_rule"] == "":
            labels.append(row["super_rule"])          # super
            colors.append("#333333")                  # dark
        else:
            labels.append("   " + row["sub_rule"])    # indented sub
            colors.append("#888888")                  # lighter

    x = range(len(rs))

    plt.figure(figsize=(12, 6))
    ax = plt.gca()

    # ---- BARS ----
    ax.bar(x, rs["accuracy"], color=colors, edgecolor="black")

    # ---- HORIZONTAL LINES ----
    ax.axhline(0.5, color="black", linestyle="--", linewidth=1.2)   # chance
    ax.axhline(0.7, color="green", linestyle="--", linewidth=1.2)   # threshold

    # ---- AXIS & LABELS ----
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_ylabel("Accuracy")
    ax.set_ylim(0, 1)

    plt.title("Rule Accuracy (Super + Sub Rules)")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()



def plot_participant_scatter(stats):
    ps = stats.copy()

    plt.figure(figsize=(7, 6))

    plt.scatter(ps["mean_duration"], ps["accuracy"],
                s=80, color="#6666aa", edgecolor="black")

    for _, row in ps.iterrows():
        plt.text(row["mean_duration"] + 100, row["accuracy"], row["anon_id"],
                 fontsize=9, va="center")

    plt.xlabel("Mean Duration (ms)")
    plt.ylabel("Accuracy")
    plt.title("Participant Performance: Speed vs Accuracy")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_participant_accuracy(stats):
    ps = stats.copy().sort_values("accuracy")

    plt.figure(figsize=(10, 6))
    plt.barh(ps["anon_id"], ps["accuracy"], color="#fff7ff", edgecolor="black")
    plt.xlabel("Accuracy")
    plt.title("Accuracy per Participant")
    plt.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.show()
