from __future__ import annotations

import re
from dataclasses import dataclass

from .errors import InvalidTrainingUserCode


_TRAINING_USER_CODE = re.compile(r"^[0-9]{2}$")


@dataclass(frozen=True)
class TrainingUserContext:
    """Validated training identity used only for runtime template resolution."""

    training_user_code: str

    def __post_init__(self) -> None:
        if not isinstance(self.training_user_code, str) or not _TRAINING_USER_CODE.fullmatch(
            self.training_user_code
        ):
            raise InvalidTrainingUserCode(
                "training_user_code must be a two-character string from 00 through 99"
            )

    @property
    def role(self) -> str:
        return "INSTRUCTOR" if self.training_user_code == "00" else "PARTICIPANT"
