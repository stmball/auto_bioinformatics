"""Errors for the AutoBioinformatics package."""


class AutoBioinformaticsError(Exception):
    """Base class for exceptions in this module."""

    pass


class PlottingError(AutoBioinformaticsError):
    """Exception raised for errors in the plotting module."""

    pass

class AnalysisError(AutoBioinformaticsError):
    """Exception raised for errors in the analysis module."""

    pass    