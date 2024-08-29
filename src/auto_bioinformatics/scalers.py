"""Non-linear scaling functions for the data."""

import typing as tp
from abc import ABC, abstractmethod
import numpy as np


class Scaler(ABC):
    """Abstract base class for scalers."""

    def __init__(self) -> None:
        """Initialise the scaler."""
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
        """Fit the scaler to the data and transform it."""
        self.fit(data)
        return self.transform(data)

    def __str__(self) -> str:
        """Generate a string representation of the scaler."""
        return ""


class Log2Scaler(Scaler):
    """Scale the data using log2 scaling."""

    def __init__(self) -> None:
        """Initialise the log2 scaler."""
        super().__init__()

    def fit(self, data: tp.Any) -> None:
        """Log scaling doesn't require fitting."""
        pass

    def transform(self, data: tp.Any) -> tp.Any:
        """Transform the data using log2 scaling."""
        return np.log2(data).replace(-np.inf, 0)

    def __str__(self) -> str:
        """Generate a string representation of the scaler."""
        return super().__str__() + "Log2 Scaler"


class Log10Scaler(Scaler):
    """Log10 scaling for data."""

    def __init__(self) -> None:
        """Initialise the log10 scaler."""
        super().__init__()

    def fit(self, data: tp.Any) -> None:
        """Log scaling doesn't require fitting."""
        pass

    def transform(self, data: tp.Any) -> tp.Any:
        """Trasnform the data using log10 scaling."""
        return np.log10(data).replace(-np.inf, 0)

    def __str__(self) -> str:
        """Generate a string representation of the scaler."""
        return super().__str__() + "Log10 Scaler"


class LogScaler(Scaler):
    """Natural log scaling for data."""

    def __init__(self) -> None:
        """Initialise the natural log scaler."""
        super().__init__()

    def fit(self, data: tp.Any) -> None:
        """Log scaling doesn't require fitting."""
        pass

    def transform(self, data: tp.Any) -> tp.Any:
        """Transform the data using natural log scaling."""
        return np.log(data).replace(-np.inf, 0)

    def __str__(self) -> str:
        """Generate a string representation of the scaler."""
        return super().__str__() + "Natural Log Scaler"


class GeneralisedLogScaler(Scaler):
    """Generalised log scaling for data.

    Generalised log function has the advantage of being able to handle zero/negative values.
    """

    def __init__(self, lambda_value: float = 0.5) -> None:
        """Initalise the glog function.

        The generalised log function takes a lambda value that controls the shape of the function.

        Args:
            lambda_value (float, optional): Shape parameter. Defaults to 0.5.
        """
        super().__init__()
        self.lambda_value = lambda_value

    def fit(self, data: tp.Any) -> None:
        """Generalised log scaling doesn't require fitting."""
        pass

    def transform(self, data: tp.Any) -> tp.Any:
        """Transform the data using generalised log scaling."""
        return np.log(data**self.lambda_value - 1) / self.lambda_value

    def __str__(self) -> str:
        """Generate a string representation of the scaler."""
        return super().__str__() + "Generalised Log Scaler"


class ArcsinhScaler(Scaler):
    """Arcsinh function for scaling data.

    Arcsinh has the advantage of being able to handle zero/negative values.
    """

    def __init__(self) -> None:
        """Initialise the arcsinh scaler."""
        super().__init__()

    def fit(self, data: tp.Any) -> None:
        """Arcsinh scaling doesn't require fitting."""
        pass

    def transform(self, data: tp.Any) -> tp.Any:
        """Transform the data using arcsinh scaling."""
        return np.arcsinh(data)

    def __str__(self) -> str:
        """Generate a string representation of the scaler."""
        return super().__str__() + "Arcsinh Scaler"
