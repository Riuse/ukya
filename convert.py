import toml
import sys
import re
import argparse
from collections import deque

def convert_to_custom_format(data):
    def convert_value(value, context):
        if isinstance(value, list):
            return f"#( {', '.join(map(str, value))} )"
        elif isinstance(value, dict):
            items = [f"{k} : {convert_value(v, context)}" for k, v in value.items()]
            return "{\n " + ",\n ".join(items) + "\n}"
        elif isinstance(value, str):
            return f'@"{value}"'
        else:
            return str(value)

    def validate_name(name):
        if not re.match(r'^[_a-z]+$', name):
            raise ValueError(f"Invalid name: {name}")

    def evaluate_postfix(expression, context):
        stack = deque()
        tokens = expression.split()
        for token in tokens:
            if token.isdigit():
                stack.append(int(token))
            elif token in context:
                stack.append(context[token])
            elif token == '+':
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
            elif token == 'sort()':
                stack = sorted(stack)
            else:
                raise ValueError(f"Unknown token: {token}")
        return stack.pop()

    def convert_section(section, context, prefix=""):
        for key, value in section.items():
            if isinstance(value, dict):
                converted_items.append(f"{prefix}{key} {{")
                convert_section(value, context, prefix + "  ")
                converted_items.append(f"{prefix}}}")
            else:
                if "problem" in key:
                    value = evaluate_postfix(value, context)
                context[key] = value
                converted_items.append(f"{prefix}{key} := {convert_value(value, context)}")

    context = {}
    converted_items = []
    convert_section(data, context)
    return "{\n " + "\n ".join(converted_items) + "\n}"

def main():
    parser = argparse.ArgumentParser(description="Convert TOML to custom config format.")
    parser.add_argument('input_file', type=str, help="Path to the input TOML file.")
    parser.add_argument('output_file', type=str, help="Path to the output file.")
    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as f:
        data = toml.load(f)

    custom_format_text = convert_to_custom_format(data)
    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(custom_format_text)

if __name__ == "__main__":
    main()
