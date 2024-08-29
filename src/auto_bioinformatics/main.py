"""Placeholder code to test things are working properly."""

import argparse
from pathlib import Path
from auto_bioinformatics.ui.root import run_ui
from auto_bioinformatics.analysis import AutoAnalysis


def run_with_cli(args: argparse.Namespace) -> None:
    """Run the program with a CLI interface."""
    print("Running with CLI interface.")

    data = AutoAnalysis.load_data(Path(args.data))
    groups = args.groups
    gene_name_col = args.gene_name_col
    p_value_threshold = args.p_value_threshold
    log_fold_change_threshold = args.log_fold_change_threshold
    gene_sets = args.gene_sets
    organism = args.organism
    plot_dir = Path(args.plot_dir)
    output_dir = Path(args.output_dir)

    # Run the analysis
    AutoAnalysis(
        data,
        groups,
        gene_name_col,
        p_value_threshold,
        log_fold_change_threshold,
        gene_sets,
        organism,
        plot_dir,
        output_dir,
    ).run()


def run_with_ui(args: argparse.Namespace) -> None:
    """Run the program with a GUI interface."""
    print("Running with GUI interface.")
    run_ui()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Placeholder code to test things are working properly."
    )

    parser.add_argument(
        "--cli", action="store_true", help="Run the CLI version of the program."
    )

    args = parser.parse_args()

    if args.cli:
        run_with_cli(args)
    else:
        run_with_ui(args)

    main()
