"""Full analysis pipeline for AutoBioinformatics."""

import typing as tp
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import gseapy as gp
import numpy as np
import numpy.typing as npt
import pandas as pd
from scipy.stats import ttest_ind
from tqdm import tqdm

import src.imputers as imputers
import src.normalisers as normalisers
import src.plots as plots
import src.reducers as reducers
import src.scalers as scalers


class AutoAnalysis:
    """AutoAnalysis class for running a full analysis pipeline.

    The AutoAnalysis class is used to run a full analysis pipeline. It is
    designed to be used with the AutoBioinformatics package for generation of
    reports, but can be used independently with inner functions and classes.
    """

    def __init__(
        self,
        data: pd.DataFrame,
        groups: tp.List[str],
        gene_name_col: str = "Gene",
        p_value_threshold: float = 0.05,
        log_fold_change_threshold: float = 1,
        gene_sets: tp.List[str] = ["KEGG_2019_Human", "MSigDB_Hallmark_2020"],
        organism: str = "Human",
        plot_dir: Path = Path("img"),
        output_dir: Path = Path("out"),
    ) -> None:
        """Initialise an AutoAnalysis object.

        Args:
            data (pd.DataFrame): Data to be analysed.
            groups (tp.Optional[tp.List[str]], optional): Groups to split data by. Defaults to None.
            p_value_threshold (float, optional): p-value threshold for significance. Defaults to 0.05.
            log_fold_change_threshold (float, optional): Log fold change threshold for significane. Defaults to 1.
            gene_sets (tp.List[str], optional): Gene sets for pathway analysis. Defaults to ["KEGG_2019_Human"].
            organism (str, optional): Organism to lookup in pathway analysis. Defaults to "Human".
            plot_dir (Path, optional): Directory for plots to go. Defaults to Path("img").
            output_dir (Path, optional): Directory for output excel files to go. Defaults to Path("out").
        """
        self.data = data
        self.groups = groups
        self.gene_name_col = gene_name_col

        self.missing_data_percentage = self._calculate_missing_data()

        self.p_value_threshold = p_value_threshold
        self.log_fold_change_threshold = log_fold_change_threshold

        self.gene_sets = gene_sets
        self.organism = organism

        self.plot_dir = plot_dir
        self.output_dir = output_dir

        self.imputer: tp.Optional[imputers.Imputer] = None
        self.reducer: tp.Optional[reducers.Reducer] = None
        self.normaliser: tp.Optional[normalisers.Normaliser] = None
        self.de_paths: tp.Optional[tp.Dict[str, tp.Dict]] = None

    def run(self):
        """Run the full analysis pipeline."""
        self._check_dirs_exist()

        self._clean_gene_names()

        self._scale_data()

        self._impute_data()

        self._normalise_data()

        self._save_data(output_file="imputed_and_normalised.xlsx")

        self._run_pca(plot=True, output_file="pca.png")

        self._run_all_de_analysis()

    def _scale_data(self, scaler: scalers.Scaler = scalers.Log2Scaler()) -> None:
        """Scale the data using a scaler object.

        Args:
            scaler (scalers.Scaler, optional): Scales the data for analysis. Defaults to scalers.Log2Scaler().
        """
        data_cols = self._get_group_cols(self.groups)

        data = self.data.loc[:, data_cols]

        self.scaler = scaler

        self.data.loc[:, data_cols] = scaler.fit_transform(data)

    def _impute_data(
        self,
        imputer: imputers.Imputer = imputers.KNN_Imputer(),
        plot: bool = True,
        output_file: Path = Path("imputation.png"),
    ) -> None:
        """Imute the data using an imputer object.

        Args:
            imputer (imputers.Imputer, optional): Imputer strategy to use. Defaults to imputers.KNNImputer().
            plot (bool, optional): Whether or not to plot the imputation plot. Defaults to True.
            output_file (Path, optional): File to save imputation plot to. Defaults to "imputation.png".
        """
        self.imputer = imputer

        for group in tqdm(self.groups, desc="Imputing data..."):
            data_cols = self._get_group_cols(group)

            data = self.data.loc[:, data_cols]

            if plot:
                # Set an attribute to store the path to the imputation plot
                self.imputation_plot_path = self.plot_dir / (
                    output_file.stem + f"_{group}" + output_file.suffix
                )
                new_data = imputer.fit_transform(data)
                plots.ImputationPlot(
                    data,
                    new_data,
                    self.imputation_plot_path,
                ).plot()
                self.data.loc[:, data_cols] = imputer.fit_transform(data)

    def _normalise_data(
        self, normaliser: normalisers.Normaliser = normalisers.PowerScaler()
    ) -> None:
        """Normalise the data using a normaliser object.

        Args:
            normaliser (normalisers.Normaliser): Algorithm to use for normalisation. Defaults to PowerScaler.
        """
        data_cols = self._get_group_cols(self.groups)

        data = self.data.loc[:, data_cols]

        self.normaliser = normaliser

        self.data.loc[:, data_cols] = normaliser.fit_transform(data)

    def _run_pca(
        self,
        dim_reducer: reducers.Reducer = reducers.PCA(),
        plot: bool = True,
        output_file: Path = Path("pca.png"),
    ) -> npt.NDArray:
        """Reduce the dimensionality of the data using a dimensionality reduction algorithm.

        Args:
            dim_reducer (reducers.Reducer): Dimensionality reduction algorithm to use. Defaults to PCA
            plot (bool, optional): Whether or not to plot and save the PCA data. Defaults to True.
            output_file (Path, optional): Where to save the PCA plot. Defaults to "pca.png".
        """
        data_cols = self._get_group_cols(self.groups)

        data = self.data.loc[:, data_cols].dropna()

        self.reducer = dim_reducer

        pca_data = dim_reducer.fit_transform(data)


        if plot:
            self.dim_reducer_plot_path = self.plot_dir / output_file
            plots.ProjectionPlot(
                pca_data,
                dim_reducer,
                self.dim_reducer_plot_path,
                data_cols,
                self.groups
            ).plot()

        return pca_data

    def _run_all_de_analysis(self) -> None:
        """Run differential expression analysis for all combinations of groups."""
        self.de_paths = defaultdict(dict)

        for group1_name, group2_name in combinations(self.groups, 2):
            fig_path = self.plot_dir / (
                "_".join([group1_name, group2_name]) + "_volcano.png"
            )

            self.de_paths[f"{group1_name}_{group2_name}"]["volcano_fig"] = fig_path

            output_path = self.output_dir / (
                "_".join([group1_name, group2_name]) + "_de_analysis.xlsx"
            )

            sig_genes = self._run_single_de_anaylsis(
                group1_name,
                group2_name,
                fig_path,
                output_path,
            )

            if sig_genes:
                fig_path = self.plot_dir / (
                    "_".join([group1_name, group2_name]) + "_pathways.png"
                )

                self.de_paths[f"{group1_name}_{group2_name}"]["pathway_fig"] = fig_path

                output_path = self.output_dir / (
                    "_".join([group1_name, group2_name]) + "_pathways.xlsx"
                )

                self._run_pathway_analysis(
                    sig_genes,
                    fig_path,
                    output_path,
                )

    def _run_single_de_anaylsis(
        self, group1_name: str, group2_name: str, fig_path: Path, output_path: Path
    ) -> pd.DataFrame:
        """Run single differential expression analysis for two groups.

        Args:
            group1_name (str): Column names of group 1
            group2_name (str): Column names of group 2
            fig_path (Path): Path for figure to go into
            output_path (Path): Path for output excel file to go into

        Returns:
            pd.DataFrame: _description_
        """
        group_1_cols = self._get_group_cols(group1_name)
        group_2_cols = self._get_group_cols(group2_name)

        grouped_data = self.data.loc[
            :, [self.gene_name_col] + group_1_cols + group_2_cols
        ]

        group_1_mean = self.data.loc[:, group_1_cols].mean(axis=1)
        group_2_mean = self.data.loc[:, group_2_cols].mean(axis=1)

        grouped_data["log_fold_change"] = group_2_mean - group_1_mean

        grouped_data["p_value"] = ttest_ind(
            self.data[group_1_cols], self.data[group_2_cols], axis=1
        )[1]

        # Drop na values
        grouped_data = grouped_data.dropna()

        # Save the data
        grouped_data.to_excel(output_path)

        # Plot the volcano plot
        plots.VolcanoPlot(
            grouped_data["log_fold_change"],
            grouped_data["p_value"],
            grouped_data[self.gene_name_col],
            p_value_threshold=self.p_value_threshold,
            log_fold_change_threshold=self.log_fold_change_threshold,
            output_file=fig_path,
        ).plot()

        # Return significant genes
        return grouped_data.loc[
            (grouped_data["p_value"] < self.p_value_threshold)
            & (grouped_data["log_fold_change"].abs() > self.log_fold_change_threshold)
        ][self.gene_name_col].to_list()

    def _run_pathway_analysis(
        self,
        significant_genes: tp.List[str],
        figure_path: Path,
        output_path: Path,
    ):
        """Run pathway analysis for a list of significant genes.

        Args:
            significant_genes (tp.List[str]): List of significant genes.
            figure_path (Path): Path for figure to go into
            output_path (Path): Path for output excel file to go into
        """

        print(significant_genes)
        enriched = gp.enrichr(
            gene_list=significant_genes,
            organism=self.organism,
            gene_sets=self.gene_sets,
            cutoff=0.5,
        )

        enriched.results.to_excel(output_path)

        try:
            plots.PathwayBarPlot(
                enriched,
                group="Gene_set",
                color={a: b for a, b in zip(self.gene_sets, ["red", "blue"])},
                ofname=figure_path,
            ).plot()
        except:
            print("Could not plot pathway bar plot.")
            pass

    def _get_group_cols(self, group_name: tp.Union[tp.List[str], str]) -> tp.List[str]:
        """Get the columns for a group.

        Args:
            group_name (str): Group name

        Returns:
            tp.List[str]: List of columns for the group.
        """
        if isinstance(group_name, str):
            return self.data.columns[
                self.data.columns.str.contains(group_name)
            ].to_list()

        else:
            return self.data.columns[
                self.data.columns.str.contains("|".join(group_name))
            ].to_list()

    def _calculate_missing_data(self) -> float:
        """Calculate the percentage of zeros in the dataset.

        Returns:
            float: Percentage of zeros in the dataset.
        """
        cols = self._get_group_cols(self.groups)
        num_zeros = (self.data.loc[:, cols] == 0).astype(int).sum().sum()
        num_total = self.data.loc[:, cols].shape[0] * self.data.loc[:, cols].shape[1]

        return num_zeros / num_total * 100

    def _save_data(self, output_file: Path) -> None:
        """Save the data to an excel file."""
        self.data.to_excel(self.output_dir / output_file)

    def _check_dirs_exist(self) -> None:
        if not self.plot_dir.exists():
            self.plot_dir.mkdir()

        if not self.output_dir.exists():
            self.output_dir.mkdir()

    def _clean_gene_names(self) -> None:
        """Clean the gene names to remove version numbers."""
        self.data[self.gene_name_col] = (
            self.data[self.gene_name_col].str.split(";").str[0]
        )