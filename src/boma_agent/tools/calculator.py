from __future__ import annotations

import ast
import operator


class CalculatorTool:
    name = "calculator"

    _allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
    }

    _allowed_unary = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def run(self, expression: str) -> str:
        expression = expression.strip()
        if not expression:
            raise ValueError("Expression cannot be empty.")

        parsed = ast.parse(expression, mode="eval")
        value = self._eval_node(parsed.body)
        return str(value)

    def _eval_node(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)

        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op_type = type(node.op)
            if op_type not in self._allowed_operators:
                raise ValueError(f"Operator {op_type.__name__} is not allowed.")
            return self._allowed_operators[op_type](left, right)

        if isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op_type = type(node.op)
            if op_type not in self._allowed_unary:
                raise ValueError(f"Unary operator {op_type.__name__} is not allowed.")
            return self._allowed_unary[op_type](operand)

        raise ValueError(f"Unsupported expression node: {type(node).__name__}")
