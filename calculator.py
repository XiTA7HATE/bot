"""
handlers/calculator.py — safe math expression evaluator
"""

import ast
import operator
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

# Allowed operations — no eval(), no security issues
ALLOWED_OPS = {
    ast.Add:  operator.add,
    ast.Sub:  operator.sub,
    ast.Mult: operator.mul,
    ast.Div:  operator.truediv,
    ast.Pow:  operator.pow,
    ast.Mod:  operator.mod,
    ast.USub: operator.neg,
}


def safe_eval(expression: str) -> float:
    """Parse and evaluate a math expression safely using AST."""

    def _eval(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPS:
            left  = _eval(node.left)
            right = _eval(node.right)
            if isinstance(node.op, ast.Div) and right == 0:
                raise ZeroDivisionError
            return ALLOWED_OPS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_OPS:
            return ALLOWED_OPS[type(node.op)](_eval(node.operand))
        raise ValueError(f"Unsupported operation: {ast.dump(node)}")

    tree = ast.parse(expression.strip(), mode="eval")
    return _eval(tree.body)


@router.message(Command("calc"))
@router.message(lambda m: m.text == "🧮 Calculator")
async def cmd_calc(message: Message) -> None:
    # If it's the keyboard button — show usage hint
    if message.text == "🧮 Calculator":
        await message.answer(
            "Send me a math expression:\n"
            "<code>/calc 2 + 2</code>\n"
            "<code>/calc (100 - 32) / 1.8</code>\n"
            "<code>/calc 2 ** 10</code>"
        )
        return

    expression = message.text.removeprefix("/calc").strip()
    if not expression:
        await message.answer("Usage: <code>/calc 2 + 2 * 5</code>")
        return

    try:
        result = safe_eval(expression)
        # Clean up float display
        display = int(result) if result == int(result) else round(result, 10)
        await message.answer(
            f"<code>{expression}</code>\n"
            f"= <b>{display}</b>"
        )
    except ZeroDivisionError:
        await message.answer("❌ Division by zero.")
    except Exception:
        await message.answer("❌ Invalid expression. Example: <code>/calc 10 * (3 + 4)</code>")
