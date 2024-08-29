"""Dimensionality reduction methods.

This module contains functions for dimensionality reduction.
"""

import typing as tp
from abc import ABC, abstractmethod

from sklearn import decomposition


class Reducer(ABC):
    """Abstract base class for reducers."""

    def __init__(self) -> None:
        """Initialise the reducer."""
        super().__init__()
        self.explaination = None

    @abstractmethod
    def fit(self, data: tp.Any) -> None:
        """Fit the reducer to the data."""
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
        """Generate a string representation of the reducer."""
        return ""


class PCA(Reducer):
    """Principal component analysis (PCA) reducer."""

    def __init__(self) -> None:
        """Initialise the PCA reducer."""
        super().__init__()

    def fit(self, data: tp.Any) -> None:
        """Fit the reducer to the data."""
        self.pca = decomposition.PCA()
        self.pca.fit(data.T)

    def transform(self, data: tp.Any) -> tp.Any:
        """Transform the data."""
        return self.pca.transform(data.T)

    def __str__(self) -> str:
        """Generate a string representation of the reducer."""
        return super().__str__() + "PCA"
