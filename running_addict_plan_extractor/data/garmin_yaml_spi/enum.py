from enum import Enum, StrEnum, auto


class StepType(StrEnum):
    WARMUP = "warmup"
    RUN = "run"
    RECOVERY = "recovery"
    REST = "rest"
    COOLDOWN = "cooldown"
    OTHER = "other"
