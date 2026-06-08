from __future__ import annotations

import ast
import operator
from dataclasses import dataclass


@dataclass(frozen=True)
class TextAnalysis:
    word_count: int
    character_count: int


class ToolEngine:
    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def calculate(self, expression: str) -> int | float:
        parsed_expression = ast.parse(expression, mode="eval")
        result = self._evaluate_node(parsed_expression.body)

        if isinstance(result, float) and result.is_integer():
            return int(result)

        return result

    def analyze_text(self, text: str) -> TextAnalysis:
        return TextAnalysis(
            word_count=len(text.split()),
            character_count=len(text),
        )

    def _evaluate_node(self, node: ast.AST) -> int | float:
        if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
            return node.value

        if isinstance(node, ast.BinOp):
            operator_function = self._operators.get(type(node.op))
            if operator_function is None:
                raise ValueError("Unsupported calculator operator")

            left = self._evaluate_node(node.left)
            right = self._evaluate_node(node.right)
            return operator_function(left, right)

        if isinstance(node, ast.UnaryOp):
            operator_function = self._operators.get(type(node.op))
            if operator_function is None:
                raise ValueError("Unsupported calculator operator")

            operand = self._evaluate_node(node.operand)
            return operator_function(operand)

        raise ValueError("Unsupported calculator expression")
