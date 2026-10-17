class TrainingContextError(ValueError):
    """Base error for training-user runtime resolution."""


class InvalidTrainingUserCode(TrainingContextError):
    """Raised when a training user code is not exactly two decimal digits."""


class UnresolvedPlaceholderError(TrainingContextError):
    """Raised when an executable value still contains the ## template marker."""
