from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import overload

from app.consciousness.goal_engine import GoalEngine
from app.profile.profile_engine import ProfileEngine
from app.reasoning.reasoning_engine import ReasoningEngine


@dataclass(frozen=True)
class Plan:
    objective: str
    steps: list[str]


class PlanningEngine:
    def __init__(
        self,
        profile_engine: ProfileEngine,
        reasoning_engine: ReasoningEngine,
        goal_engine: GoalEngine,
    ) -> None:
        self._profile_engine = profile_engine
        self._reasoning_engine = reasoning_engine
        self._goal_engine = goal_engine
        self._plans: dict[str, dict[str, Plan]] = {}
        self._lock = Lock()

    @overload
    def create_plan(
        self,
        user_id: str,
        objective: str,
        steps: None = None,
    ) -> list[str]:
        ...

    @overload
    def create_plan(
        self,
        user_id: str,
        objective: str,
        steps: list[str],
    ) -> Plan:
        ...

    def create_plan(
        self,
        user_id: str,
        objective: str,
        steps: list[str] | None = None,
    ) -> Plan | list[str]:
        if steps is None:
            return self._create_contextual_steps(user_id, objective)

        plan = Plan(objective=objective, steps=steps)

        with self._lock:
            user_plans = self._plans.setdefault(user_id, {})
            user_plans[objective.lower()] = plan

        return plan

    def get_plan(self, user_id: str, objective: str) -> Plan | None:
        with self._lock:
            return self._plans.get(user_id, {}).get(objective.lower())

    def get_plans(self, user_id: str) -> list[Plan]:
        with self._lock:
            return list(self._plans.get(user_id, {}).values())

    def _create_contextual_steps(self, user_id: str, objective: str) -> list[str]:
        normalized_objective = objective.lower()

        if "mit" in normalized_objective:
            return [
                "Step 1: Strengthen your English reading, writing, and speaking skills.",
                "Step 2: Build a strong Mathematics foundation with algebra, geometry, and problem solving.",
                "Step 3: Learn Python and use it to solve real programming problems.",
                "Step 4: Create projects that show curiosity, discipline, and technical ability.",
                "Step 5: Start SAT preparation and track your practice scores.",
            ]

        if "python" in normalized_objective:
            return [
                "Step 1: Learn Python syntax, variables, data types, and control flow.",
                "Step 2: Practice functions, modules, files, and error handling.",
                "Step 3: Build small projects to understand programming fundamentals.",
                "Step 4: Learn basic data structures like lists, dictionaries, sets, and tuples.",
                "Step 5: Review your code regularly and improve it with feedback.",
            ]

        return self._build_contextual_plan(user_id, objective)

    def _build_contextual_plan(self, user_id: str, objective: str) -> list[str]:
        profile = self._profile_engine.get_profile(user_id)
        goals = self._goal_engine.get_goals(user_id)
        reasoning = self._reasoning_engine.answer_question(
            user_id=user_id,
            question=f"How should I approach {objective}?",
        )
        active_goals = [goal.title for goal in goals if not goal.completed]

        plan = [
            f"Step 1: Clarify what '{objective}' means and define a measurable outcome.",
            f"Step 2: Use your profile context to focus on {profile.dream or 'your most important long-term direction'}.",
        ]

        if active_goals:
            plan.append(f"Step 3: Connect this objective to your active goal: {active_goals[0]}.")
        else:
            plan.append("Step 3: Create one active goal that supports this objective.")

        plan.append(f"Step 4: Review this reasoning guidance: {reasoning}")
        plan.append("Step 5: Take one small action today and review progress tomorrow.")

        return plan
