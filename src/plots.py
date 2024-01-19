"""Plots for visualizing differential expression analysis results."""
import typing as tp
from pathlib import Path

import gseapy as gp
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import pandas as pd
from adjustText import adjust_text

import src.reducers as reducers
from src.errors import PlottingError


class VolcanoPlot:
    """Volcano plot for visualizing differential expression analysis results."""

    def __init__(
        self,
        log_fold_changes: npt.NDArray,
        p_values: npt.NDArray,
        labels: tp.List[str],
        log_fold_change_threshold: float = 1,
        p_value_threshold: float = 0.05,
        output_file: tp.Optional[Path] = None,
    ) -> None:
        """Initialize a VolcanoPlot object.

        Args:
            log_fold_changes (npt.NDArray): Array of log fold change values.
            p_values (npt.NDArray): Array of p-values for independent t-test.
            labels (tp.List[str]): List of labels for each point to add if a point is significant.
            log_fold_change_threshold (float, optional): Log fold change threshold for significance. Defaults to 1.
            p_value_threshold (float, optional): P-Value threshold for significance. Defaults to 0.05.
            output_file (Path, optional): Path to save the plot to. Defaults to None.
        """
        self.log_fold_changes = log_fold_changes
        self.p_values = p_values
        self.labels = labels

        self.log_fold_change_threshold = log_fold_change_threshold
        self.p_value_threshold = p_value_threshold
        self.output_file = output_file

    def plot(self):
        """Plot the volcano plot."""
        if self.log_fold_changes.shape != self.p_values.shape:
            raise PlottingError(
                "The shape of the log fold changes and p-values must be the same."
            )

        fig, ax = plt.subplots(figsize=(10, 10))

        ax.scatter(self.log_fold_changes, -np.log10(self.p_values), c=-np.log10(self.p_values))

        # Add labels for significant points
        texts = []
        for label, x, y in zip(
            self.labels, self.log_fold_changes, -np.log10(self.p_values)
        ):
            if (
                y > -np.log10(self.p_value_threshold)
                and abs(x) > self.log_fold_change_threshold
            ):
                texts.append(ax.text(x, y, label, fontsize=12))

        # Adjust the labels so they don't overlap
        adjust_text(texts, arrowprops=dict(arrowstyle="-", color="k", lw=0.5))

        # Add axis labels and title
        ax.set_xlabel("Log Fold Change")
        ax.set_ylabel("-log10(p-value)")

        # Set the x-axis to be symmetrical around 0
        ax.set_xlim(-max(abs(self.log_fold_changes)), max(abs(self.log_fold_changes)))

        # Add horizontal lines at the significance thresholds

        ax.axhline(-np.log10(self.p_value_threshold), c="red", ls="--", lw=1)

        # Add vertical lines at the fold change thresholds

        ax.axvline(self.log_fold_change_threshold, c="red", ls="--", lw=1)
        ax.axvline(-self.log_fold_change_threshold, c="red", ls="--", lw=1)

        # Remove the top and right spines
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        plt.tight_layout()

        # Save the plot if an output file is specified
        if self.output_file:
            fig.savefig(self.output_file)

        return fig


class ImputationPlot:
    """Imputation plot for visualizing the effect of imputation on the data."""

    def __init__(
        self,
        pre_imputed_data: pd.DataFrame,
        post_imputed_data: pd.DataFrame,
        output_file: tp.Optional[Path] = None,
    ):
        """Intialize an ImputationPlot object."""
        self.pre_imputed_data = pre_imputed_data
        self.post_imputed_data = post_imputed_data

        self.output_file = output_file

    def plot(self):
        """Plot the imputation plot."""
        # Get the number of samples in the data
        n_samples = max(self.pre_imputed_data.shape[1], 4)
        

        # Create a figure with a subplot for each sample
        fig, axes = plt.subplots(n_samples, 2, figsize=(10, 3 * n_samples))

        # Plot the pre-imputed data
        for i in range(n_samples):

            filtered_pre = self.pre_imputed_data.iloc[:, i][
                self.pre_imputed_data.iloc[:, i] != 0
            ]

            axes[i, 0].hist(filtered_pre, bins=100)
            axes[i, 0].set_title(f"Sample {i+1}")

            # Calculate the difference between the pre and post imputed data
            difference = (
                self.post_imputed_data.iloc[:, i] - self.pre_imputed_data.iloc[:, i]
            )

            # Plot the difference
            axes[i, 1].hist(
                [filtered_pre, difference[difference != 0]], bins=100, stacked=True
            )

            # Add a title
            axes[i, 1].set_title(f"Sample {i+1}")

        plt.tight_layout()

        # Save the plot if an output file is specified
        if self.output_file:
            fig.savefig(self.output_file)

        return fig


class ProjectionPlot:
    """Plot for visualizing a projection of the data, usually a PCA."""

    def __init__(
        self,
        points: npt.NDArray,
        projection: reducers.Reducer,
        output_file: tp.Optional[Path] = None,
        colors: tp.Union[tp.List[int], str] = "black",
    ) -> None:
        """Initialize a ProjectionPlot object."""
        self.points = points
        self.projection = projection
        self.output_file = output_file
        self.colors = colors

    def plot(self):
        """Plot the projection."""
        # Create a figure
        fig, ax = plt.subplots(figsize=(10, 10))

        # Plot the points

        ax.scatter(self.points[:, 0], self.points[:, 1], c=self.colors)

        # Add axis labels and title
        ax.set_xlabel("Dimension 1")
        ax.set_ylabel("Dimension 2")
        ax.set_title(f"{self.projection} Projection")

        plt.tight_layout()

        # Save the plot if an output file is specified
        if self.output_file:
            fig.savefig(self.output_file)

        return fig


class PathwayBarPlot:
    """Pathway bar plot for visualizing pathway analysis results."""

    def __init__(self, enrich: gp.Enrichr, **kwargs) -> None:
        """Initialize a PathwayBarPlot object."""
        self.enrich = enrich
        self.barplot_kwargs = kwargs

    def plot(self):
        """Plot the pathway bar plot."""
        gp.barplot(self.enrich.results, **self.barplot_kwargs)


class PathwayDotPlot:
    """Pathway dot plot for visualizing pathway analysis results."""

    def __init__(self, enrich: gp.Enrichr, **kwargs) -> None:
        """Initialize a PathwayDotPlot object."""
        self.enrich = enrich
        self.dotplot_kwargs = kwargs

    def plot(self):
        """Plot the pathway dot plot."""
        gp.dotplot(self.enrich.results, **self.dotplot_kwargs)
