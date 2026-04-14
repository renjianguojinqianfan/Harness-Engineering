"""Workflow stage definitions and transitions."""
from enum import Enum


class Stage(Enum):
    FEEDBACK = "feedback"
    TRIAGE = "triage"
    CLARIFY = "clarify"
    PLAN = "plan"
    EXECUTE = "execute"
    EVALUATE = "evaluate"
    DONE = "done"


TRANSITIONS = {
    Stage.FEEDBACK: [Stage.TRIAGE],
    Stage.TRIAGE: [Stage.CLARIFY, Stage.PLAN],
    Stage.CLARIFY: [Stage.PLAN],
    Stage.PLAN: [Stage.EXECUTE],
    Stage.EXECUTE: [Stage.EVALUATE],
    Stage.EVALUATE: [Stage.DONE, Stage.PLAN],
    Stage.DONE: [Stage.DONE],
}


def get_next_stage(current: Stage) -> Stage:
    """Return the default next stage for a given stage."""
    next_stages = TRANSITIONS.get(current, [current])
    return next_stages[0]


def get_allowed_transitions(current: Stage) -> list[Stage]:
    """Return all allowed next stages."""
    return list(TRANSITIONS.get(current, [current]))
