"""Normalisers for data preprocessing.

Normalisers are used to scale data to a given range. This is useful for
preprocessing data before analysis. For example, some machine learning
algorithms require data to be scaled to a mean of 0 and variance of 1.
"""

from abc import ABC, abstractmethod
import numpy as np
import typing as tp
from sklearn.preprocessing import PowerTransformer


class Normaliser(ABC):
    """Abstract base class for normalisers."""

    def __init__(self) -> None:
        """Initialise the normaliser."""
        super().__init__()
        self.explaination = None

    @abstractmethod
    def fit(self, data: tp.Any) -> None:
        """Fit the scaler to the data."""
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
        """Generate a string representation of the object."""
        return ""


class StandardScaler(Normaliser):
    """Standard scaling scales the data to a mean of 0 and variance of 1."""

    def __init__(self) -> None:
        """Initialise the standard scaler."""
        super().__init__()

    def fit(self, data: tp.Any) -> None:
        """Fit the scaler to the data."""
        self.mean = np.mean(data)
        self.std = np.std(data)

    def transform(self, data: tp.Any) -> tp.Any:
        """Transform the data."""
        return (data - self.mean) / self.std

    def __str__(self) -> str:
        """Generate a string representation of the object."""
        return super().__str__() + "Standard Scaler"


class MinMaxScaler(Normaliser):
    """MinMax scaling scales the data to a range between 0 and 1."""

    def __init__(self) -> None:
        """Initialise the min-max scaler."""
        super().__init__()

    def fit(self, data: tp.Any) -> None:
        """Figt the scaler to the data."""
        self.min = np.min(data)
        self.max = np.max(data)

    def transform(self, data: tp.Any) -> tp.Any:
        """Transform the data."""
        return (data - self.min) / (self.max - self.min)

    def __str__(self) -> str:
        """Generate a string representation of the object."""
        return super().__str__() + "Min-Max Scaler"


class PowerScaler(Normaliser):
    """Power scaling scales the data to a normal distribution."""

    def __init__(self) -> None:
        """Initialise the power scaler."""
        super().__init__()

    def fit(self, data: tp.Any) -> None:
        """Fit the scaler to the data."""
        self.transformer = PowerTransformer()
        self.transformer.fit(data)

    def transform(self, data: tp.Any) -> tp.Any:
        """Transform the data."""
        return self.transformer.transform(data)

    def __str__(self) -> str:
        """Generate a string representation of the object."""
        return super().__str__() + "Power Scaler"
