"""Placeholder code to test things are working properly."""
import argparse
import typing as tp

import pandas as pd

import src.imputers as imputers
import src.normalisers as normalisers
import src.reducers as reducers
import src.scalers as scalers
from src.analysis import AutoAnalysis, AutoAnalysisConfig
from src.reporting import Reporter
from src.ui.root import run_ui


def main() -> bool:
    """Run a simple function that returns True."""
    return True


def run_with_cli(args: argparse.Namespace) -> None:
    """Run the program with a CLI interface."""

    config = get_config(args)
    data = get_data(args)

    analysis = AutoAnalysis(config)

    analysis.run(data)

    if args.generate_report:
        reporter = Reporter(analysis, config.output_dir)

        reporter.generate_report()



def run_with_ui(args: argparse.Namespace) -> None:
    """Run the program with a GUI interface."""
    run_ui()


def get_config(args: argparse.Namespace) -> AutoAnalysisConfig:

    if args.groups:
        groups = args.groups.split(",")
    else:
        raise ValueError("No groups given.")

    if args.gene_sets:
        gene_sets = args.gene_sets.split(",")
    else:
        gene_sets = ["KEGG_2019_Human", "MSigDB_Hallmark_2020"]

    if args.scaler:
        scaler = get_preprocessor(args.scaler, scalers.Scaler)
    else:
        scaler = scalers.Log2Scaler()

    if args.imputer:
        imputer = get_preprocessor(args.imputer, imputers.Imputer)
    else:
        imputer = imputers.KNN_Imputer()

    if args.normaliser:
        normaliser = get_preprocessor(args.normaliser, normalisers.Normaliser)
    else:
        normaliser = normalisers.PowerScaler()

    if args.reducer:
        reducer = get_preprocessor(args.reducer, reducers.Reducer)
    else:
        reducer = reducers.PCA_Reducer()



    return AutoAnalysisConfig(
        groups=groups,
        gene_name_col=args.gene_col if args.gene_col else "Gene",
        p_value_threshold=args.p_value_threshold if args.p_value_threshold else 0.05,
        log_fold_change_threshold=args.log_fold_change_threshold
        if args.log_fold_change_threshold
        else 1,
        gene_sets=gene_sets,
        organism=args.organism if args.organism else "Human",
        plot_dir=args.plot_dir if args.plot_dir else "./img",
        output_dir=args.output_dir if args.output_dir else "./out",
        scaler=scaler,
        imputer=imputer,
        normaliser=normaliser,
        reducer=reducer
    )

def get_data(args: argparse.Namespace) -> tp.Any:
    """Return the data in the given file."""
    if args.file:
        return pd.read_excel(args.file)
    else:
        raise ValueError("No file given.")

def get_preprocessor(
    name: str,
    baseclass: tp.Union[
        scalers.Scaler, imputers.Imputer, normalisers.Normaliser, reducers.Reducer
    ],
) -> scalers.Scaler:
    """Return the scaler with the given name."""
    classes = baseclass.__subclasses__()
    for preprocessor in classes:
        if preprocessor.name == name:
            return preprocessor()

    raise ValueError(f"{name} not found. Options are: {[c.name for c in classes]}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Placeholder code to test things are working properly."
    )

    # Datafile
    parser.add_argument(
        "file", type=argparse.FileType("r"), help="The file to run the analysis on."
    )

    # Group names
    parser.add_argument(
        "-g", "--groups", type=str, help="The names of the groups in the data file, separated by commas."
    )

    # Gene name column
    parser.add_argument(
        "-c", "--gene-col", type=str, help="The name of the column containing the gene names."
    )

    # P value threshold
    parser.add_argument(
        "-p",
        "--p-value-threshold",
        type=float,
        help="The threshold for the p value. Defaults to 0.05",
    )

    # Fold change threshold
    parser.add_argument(
        "-f",
        "--log-fold-change-threshold",
        type=float,
        help="The threshold for the log fold change. Defaults to 1",
    )

    # Gene sets
    parser.add_argument(
        "-s",
        "--gene-sets",
        type=str,
        help="The gene sets to use for the enrichment analysis, separated by commas.",
    )

    # Organism
    parser.add_argument(
        "-o",
        "--organism",
        type=str,
        help="The organism to use for the enrichment analysis. Defaults to Human.",
    )

    # Plot directory
    parser.add_argument(
        "-i",
        "--plot-dir",
        type=str,
        help="The directory to save the plots to. Defaults to ./img",
    )

    # Output directory
    parser.add_argument(
        "-d",
        "--output-dir",
        type=str,
        help="The directory to save the output files to. Defaults to ./out",
    )

    # Scaler
    parser.add_argument(
        "--scaler",
        type=str,
        help="The scaler to use. Defaults to Log2Scaler.",
    )

    # Imputer
    parser.add_argument(
        "--imputer",
        type=str,
        help="The imputer to use. Defaults to KNN_Imputer.",
    )

    # Normaliser
    parser.add_argument(
        "--normaliser",
        type=str,
        help="The normaliser to use. Defaults to PowerScaler.",
    )

    # Reducer
    parser.add_argument(
        "--reducer",
        type=str,
        help="The reducer to use. Defaults to PCA_Reducer.",
    )

    # Generate report
    parser.add_argument(
        "--generate-report",
        action="store_true",
        help="Generate a report after running the analysis.",
    )

    # GUI or CLI
    parser.add_argument(
        "--gui", action="store_true", help="Run the GUI version of the program."
    )


    args = parser.parse_args()

    if args.gui:
        run_with_ui(args)
    else:
        run_with_cli(args)

    main()