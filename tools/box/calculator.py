# calculator.py


class Calculator:

    @staticmethod
    def do_pairwise_arithmetic(num1, num2, operation):
        if operation == '+':
            return num1 + num2
        elif operation == "-":
            return num1 - num2
        elif operation == "*":
            return num1 * num2
        elif operation == "/":
            return num1 / num2
        else:
            return "Error: Operation not supported."

    function_metadata = {
        "type": "function",
        "function": {
            "name": "do_pairwise_arithmetic",
            "description": "Calculator function for doing basic arithmetic. Supports addition, subtraction, multiplication, and division.",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {
                        "type": "number",
                        "description": "First operand (before the operator)",
                    },
                    "num2": {
                        "type": "number",
                        "description": "Second operand (after the operator)",
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["+", "-", "*", "/"],
                        "description": "The operation to perform. Must be either +, -, *, or /",
                    },
                },
                "required": ["num1", "num2", "operation"],
            },
        }
    }