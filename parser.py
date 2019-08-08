# Covert tokens to AST

OPERATORS = [
    "+", "-", "=", "*", ">", "<", "~=", "==", "..", ">=", "<=", "%", "/",
]


def parse_tokens(tokens, in_expr=0):
    out = []

    while len(tokens) > 0:
        token = tokens.pop(0)

        if token["type"] == "NUMBER":
            out.append({"type": "number", "value": token["value"]})
            continue

        if token["type"] == "STRING":
            out.append({"type": "string", "value": token["value"]})
            continue

        if token["type"] == "BOOLEAN":
            out.append({"type": "boolean", "value": token["value"]})
            continue

        if token["type"] == "NIL":
            out.append({"type": "nil", "value": None})
            continue

        if token["type"] == "OP" and token["value"] == "not":
            assignments = extract_assignments(tokens)
            out.append({
                "type": "call",
                "name": token["value"],
                "args": parse_tokens(assignments),
            })
            continue

        if token["type"] == "OP" and token["value"] in OPERATORS:
            assignments = extract_assignments(tokens)
            out.append({
                "type": "call",
                "name": token["value"],
                "args": [out.pop(), parse_tokens(assignments)],
            })
            continue

        if token["type"] == "NAME" and len(tokens) and is_op(tokens[0], "("):
            args = extract_args(tokens)

            expression = {
                "type": "call",
                "name": token["value"],
                "args": parse_tokens(args, in_expr=1)
            }

            if not in_expr:  # Do not wrap expression if already running in one
                out.append({
                    "type": "expr",
                    "value": [expression],
                })
            else:
                out.append(expression)

            continue

        if token["type"] == "KEYWORD" and token["value"] == "else":
            body = extract_if_body(tokens)

            out.append({
                "type": "else",
                "body": parse_tokens(body),
            })
            continue

        if token["type"] == "KEYWORD" and token["value"] in ["if", "elseif"]:
            if_nodes = extract_scope_body(tokens)

            test_nodes = extract_test_statement(if_nodes, "then")
            body = extract_if_body(if_nodes)

            out.append({
                "type": "if",
                "test": parse_tokens(test_nodes),
                "body": parse_tokens(body),
                "else": parse_tokens(if_nodes),
            })
            continue

        if token["type"] == "KEYWORD" and token["value"] == "while":
            while_tokens = extract_scope_body(tokens)
            test_tokens = extract_test_statement(while_tokens, "do")

            out.append({
                "type": "while",
                "test": parse_tokens(test_tokens),
                "body": parse_tokens(while_tokens),
            })
            continue

        if token["type"] == "KEYWORD" and token["value"] == "return":
            assignments = extract_assignments(tokens)
            out.append({
                "type": "return",
                "value": parse_tokens(assignments),
            })
            continue

        if token["type"] == "KEYWORD" and token["value"] == "function":
            function_tokens = extract_scope_body(tokens)
            signature_tokens = extract_fn_signature(function_tokens)
            name_token = signature_tokens.pop(0)  # TODO: Add anonymous support

            parameter_tokens = signature_tokens[1:-1]
            parameter_tokens = map(
                lambda x: {"type": "argument", "name": x["value"]},
                parameter_tokens
            )

            out.append({
                "type": "function",
                "name": name_token["value"],
                "args": list(parameter_tokens),
                "body": parse_tokens(function_tokens),
            })
            continue

        if token["type"] == "NAME":
            out.append({
                "type": "name", "name": token["value"],
            })
            continue

    return out


def is_op(token, op):
    return token["type"] == "OP" and token["value"] == op


def extract_fn_signature(tokens):
    out = []

    while len(tokens) > 0:
        token = tokens.pop(0)
        out.append(token)
        if token["type"] == "OP" and token["value"] == ")":
            break
    return out


def extract_scope_body(tokens):
    out = []

    depth = 0

    while len(tokens) > 0:
        token = tokens.pop(0)
        out.append(token)

        if token["type"] == "KEYWORD" and token["value"] == "if":
            depth = depth + 1
            continue

        if depth > 0 and token["type"] == "KEYWORD" and token["value"] == "if":
            depth = depth - 1
            continue

        if depth == 0 and token["type"] == "KEYWORD" and token["value"] == "end":
            break

    return out


def extract_if_body(tokens):
    out = []
    depth = 0

    while len(tokens) > 0:
        token = tokens[0]

        if token["type"] == "KEYWORD" and token["value"] == "if":
            out.append(token)
            tokens.pop(0)
            depth = depth + 1
            continue

        if depth > 0 and token["type"] == "KEYWORD" and token["value"] == "end":
            out.append(token)
            tokens.pop(0)
            depth = depth - 1
            continue

        if depth == 0 and token["type"] == "KEYWORD" and token["value"] == "elseif":
            break

        if depth == 0 and token["type"] == "KEYWORD" and token["value"] == "else":
            break

        if depth == 0 and token["type"] == "KEYWORD" and token["value"] == "end":
            break

        out.append(token)
        tokens.pop(0)

    return out


def extract_test_statement(tokens, exit_keyword="then"):
    out = []

    while len(tokens) > 0:
        token = tokens.pop(0)

        if token["type"] == "KEYWORD" and token["value"] == exit_keyword:
            break

        out.append(token)

    return out


def extract_assignments(tokens):
    out = []
    depth = 0

    while len(tokens) > 0:
        token = tokens.pop(0)

        if token["type"] == "OP" and token["value"] == "(":
            out.append(token)
            depth = depth + 1
            continue

        if token["type"] == "OP" and token["value"] == ")":
            out.append(token)
            depth = depth - 1
            continue

        if token["type"] == "NL" and depth == 0:
            break

        out.append(token)

    return out


def extract_args(tokens):
    depth = 1
    args = []

    tokens.pop(0)  # Drop (

    while depth != 0:
        token = tokens.pop(0)
        # print(token)

        if is_op(token, "("):
            depth = depth+1

        if is_op(token, ")"):
            depth = depth-1

        args.append(token)

    args = args[:-1]  # Drop )
    return args


def parse(tokens):
    ast_ = parse_tokens(tokens)
    return ast_
