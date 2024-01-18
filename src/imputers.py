"""Imputer classes for missing data imputation.

Imputers are used to fill in missing data in a dataset. They are used in the
preprocessing stage of an analysis.

"""

import typing as tp
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer, SimpleImputer


class Imputer(ABC):
    """Abstract base class for imputers."""

    def __init__(self) -> None:
        """Initialise the imputer."""
        self.explaination = None
        super().__init__()

    @abstractmethod
    def fit(self, data: tp.Any) -> None:
        """Fit the imputer to the data."""
        pass

    @abstractmethod
    def transform(self, data: tp.Any) -> tp.Any:
        """Transform the data."""
        pass

    def fit_transform(self, data: tp.Any) -> tp.Any:
        """Fit and transform the data."""
        self.fit(data)
        return self.transform(data)

    def __str__(self) -> str:
        """Generate a string representation of the imputer."""
        return ""


class MeanImputer(Imputer):
    """Mean imputer."""

    def __init__(self) -> None:
        """Initialise the mean imputer."""
        super().__init__()

    def fit(self, data: tp.Any) -> None:
        """Fit the imputer to the data."""
        self.imputer = SimpleImputer(strategy="mean")
        self.imputer.fit(data)

    def transform(self, data: tp.Any) -> tp.Any:
        """Transform the data."""
        return self.imputer.transform(data)

    def __str__(self) -> str:
        """Generate a string representation of the imputer."""
        return super().__str__() + "Mean Imputation"


class KNN_Imputer(Imputer):
    """KNN imputer."""

    def __init__(self, sample_threshold: float = 0.5):
        """Initialise the KNN imputer."""
        super().__init__()
        self.sample_threshold = sample_threshold

    def fit(self, data: tp.Any) -> None:
        """Fit the imputer to the data."""
        clean_data = data.replace(0, np.nan)
        clean_data = clean_data.dropna(thresh=self.sample_threshold * data.shape[1])
        self.imputer = KNNImputer()
        self.imputer.fit(clean_data)

    def transform(self, data: tp.Any) -> pd.DataFrame:
        """Transform the data."""
        clean_data = data.replace(0, np.nan)
        clean_data = clean_data.dropna(
            thresh=self.sample_threshold * clean_data.shape[1]
        )
        clean_data = pd.DataFrame(
            self.imputer.transform(clean_data),
            columns=clean_data.columns,
            index=clean_data.index,
        )

        return clean_data.reindex(data.index, fill_value=np.nan)

    def __str__(self) -> str:
        """Generate a string representation of the imputer."""
        return super().__str__() + "KNN Imputation"
