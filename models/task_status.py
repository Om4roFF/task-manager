import enum


class TaskStatus(enum.Enum):
    todo = 1
    in_process = 2
    done = 3
