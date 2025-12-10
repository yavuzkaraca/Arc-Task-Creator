from pathlib import Path

from processing import (
    preprocess, keep_only_real_trials,
    compute_participant_stats, compute_difficulty_stats,
    compute_rule_stats, compute_task_stats, compute_global_stats, compute_duration_stats,
    extract_participant_demographics_from_raw, compute_block_accuracy, compute_confidence_stats,
    compute_reaction_time_stats, compute_confidence_evolution, compute_confidence_correctness_correlation
)
from plots import plot_task_accuracy_hierarchical, plot_task_accuracy_hierarchical_plain, plot_rule_stats, \
    plot_participant_accuracy, plot_participant_scatter, plot_block_accuracy, plot_confidence_histogram, \
    plot_reaction_time_over_time, plot_confidence_over_time, plot_confidence_correctness_correlation


def main():
    ROOT = Path(__file__).resolve().parent.parent  # one level up

    demo = extract_participant_demographics_from_raw("data.csv")
    demo["anon_num"] = demo["anon_id"].str.extract(r"(\d+)").astype(int)
    demo = demo.sort_values("anon_num").drop(columns=["anon_num"])
    demo.to_csv(ROOT / "participant_data.csv", index=False)

    df = preprocess("data.csv")
    df.to_csv(ROOT / "processed_data.csv", index=False)

    real = keep_only_real_trials(df)
    real = real[real["anon_id"] != "t1"]  # Removing myself from the data

    block_stats = compute_block_accuracy(real)
    block_stats.to_csv(ROOT / "block_accuracy.csv", index=False)
    compute_global_stats(real).to_csv(ROOT / "global_stats.csv", index=False)
    compute_duration_stats(real).to_csv(ROOT / "duration_stats.csv", index=False)
    participant_stats = compute_participant_stats(real)
    participant_stats.to_csv(ROOT / "participant_stats.csv", index=False)
    compute_difficulty_stats(real).to_csv(ROOT / "difficulty_stats.csv", index=False)
    rule_stats = compute_rule_stats(real)
    rule_stats.to_csv(ROOT / "rule_stats.csv", index=False)
    task_stats = compute_task_stats(real)
    task_stats.to_csv(ROOT / "task_stats.csv", index=False)

    plot_task_accuracy_hierarchical(task_stats)
    plot_task_accuracy_hierarchical_plain(task_stats)
    plot_block_accuracy(block_stats)
    plot_rule_stats(rule_stats)
    plot_participant_accuracy(participant_stats)
    plot_participant_scatter(participant_stats)

    conf = compute_confidence_stats(real)
    plot_confidence_histogram(conf)
    rt_stats = compute_reaction_time_stats(real)
    plot_reaction_time_over_time(rt_stats)
    conf_stats = compute_confidence_evolution(real)
    plot_confidence_over_time(conf_stats)

    corr_df = compute_confidence_correctness_correlation(real)
    corr_df.to_csv(ROOT / "confidence_correctness_corr.csv", index=False)
    plot_confidence_correctness_correlation(corr_df)

    print("Done.")


if __name__ == "__main__":
    main()
