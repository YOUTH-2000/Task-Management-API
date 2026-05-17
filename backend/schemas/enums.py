from enum import Enum

class StatusEnum(str, Enum):
    pending = "pending"
    in_progess = "in_progress"
    completed = "completed"

class PriorityEnum(str, Enum):
    low = "low"
    mwdium = "medium"
    high = "high"