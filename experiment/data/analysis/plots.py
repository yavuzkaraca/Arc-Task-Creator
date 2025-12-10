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


def plot_confidence_histogram(conf_series):
    plt.figure(figsize=(8, 5))
    plt.hist(conf_series, bins=[-0.05, 0.1, 0.5, 0.9, 1.1],
             edgecolor="black", color="#666688")

    plt.xticks([0, 0.30, 0.70, 1.0],
               ["Very Unsure", "Unsure", "Sure", "Very Sure"],
               rotation=20)

    plt.ylabel("Count")
    plt.title("Distribution of Confidence Ratings")
    plt.tight_layout()
    plt.show()


def plot_confidence_over_time(conf_stats):
    import matplotlib.pyplot as plt

    x = conf_stats["task_int"]
    y = conf_stats["mean"]
    sem = conf_stats["sem"]

    plt.figure(figsize=(10, 5))
    plt.plot(x, y, marker="o", color="#8c1f1f", linewidth=2)
    plt.fill_between(x, y - sem, y + sem, color="#8c1f1f", alpha=0.25)

    plt.xlabel("Task ID")
    plt.ylabel("Confidence")
    plt.title("Confidence Over Experiment Progression")
    plt.ylim(0, 1)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_confidence_correctness_correlation(corr_df):
    df = corr_df.copy().sort_values("corr")

    plt.figure(figsize=(8, 6))
    plt.barh(df["anon_id"], df["corr"],
             color="#666688", edgecolor="black")

    plt.xlabel("Correlation (Confidence ↔ Correctness)")
    plt.title("Metacognitive Accuracy per Participant")
    plt.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_reaction_time_over_time(rt_stats):
    x = rt_stats["task_int"]
    y = rt_stats["mean"]
    sem = rt_stats["sem"]

    plt.figure(figsize=(10, 5))
    plt.plot(x, y, marker="o", color="#335f87", linewidth=2)
    plt.fill_between(x, y - sem, y + sem, color="#335f87", alpha=0.2)

    plt.xlabel("Task ID")
    plt.ylabel("Reaction Time (ms)")
    plt.title("Reaction Time Over Experiment Progression")
    plt.grid(alpha=0.3)
    plt.tight_layout()
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

    ordered = []
    for sr in rs["super_rule"].unique():
        ordered.append(rs[rs["super_rule"] == sr])
    rs = pd.concat(ordered, ignore_index=True)

    labels = [
        row["super_rule"] if row["sub_rule"] == "" else "   " + row["sub_rule"]
        for _, row in rs.iterrows()
    ]
    colors = ["#333333" if row["sub_rule"] == "" else "#888888"
              for _, row in rs.iterrows()]

    x = range(len(rs))

    plt.figure(figsize=(12, 6))
    ax = plt.gca()

    ax.bar(
        x,
        rs["accuracy"],
        yerr=rs["sem"],
        capsize=5,
        color=colors,
        edgecolor="black"
    )

    ax.axhline(0.5, color="black", linestyle="--", linewidth=1.2)
    ax.axhline(0.7, color="green", linestyle="--", linewidth=1.2)

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


def plot_block_accuracy(block_stats):
    import matplotlib.pyplot as plt
    import numpy as np

    bs = block_stats.copy()

    block_labels = {
        1: "Expansion",
        2: "Attraction",
        3: "Occlusion",
        4: "Arithmetic"
    }
    order = ["Expansion", "Attraction", "Occlusion", "Arithmetic"]

    bs["block_name"] = bs["block"].map(block_labels)
    bs["block_name"] = pd.Categorical(bs["block_name"], categories=order, ordered=True)

    type_order = ["inference", "application"]
    bs["block_type"] = pd.Categorical(bs["block_type"], categories=type_order, ordered=True)

    bs = bs.sort_values(["block_name", "block_type"])

    pivot_mean = bs.pivot(index="block_name", columns="block_type", values="mean_acc")
    pivot_sem = bs.pivot(index="block_name", columns="block_type", values="sem")

    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(order))
    width = 0.35

    colors = {"inference": "#1f77b4",
              "application": "#d62728"}

    ax.bar(
        x - width / 2,
        pivot_mean["inference"],
        width,
        label="Inference",
        color=colors["inference"],
        edgecolor="black",
        yerr=pivot_sem["inference"],
        capsize=5
    )

    ax.bar(
        x + width / 2,
        pivot_mean["application"],
        width,
        label="Application",
        color=colors["application"],
        edgecolor="black",
        yerr=pivot_sem["application"],
        capsize=5
    )

    ax.axhline(0.5, color="black", linestyle="--", linewidth=1.2)
    ax.axhline(0.7, color="green", linestyle="--", linewidth=1.2)

    ax.set_ylabel("Accuracy")
    ax.set_ylim(0, 1)
    ax.set_xticks(x)
    ax.set_xticklabels(order)

    ax.set_title("Accuracy per Block (Inference vs Application)", fontsize=14)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.show()
