# Covert tokens to AST
from pprint import pprint

OPERATORS = [
    "+", "-", "=", "*", ">", "<", "~=", "==", "..", ">=", "<=", "%", "/", "and", "or",
]

fn_name_index = 0


def generate_function_name():
    global fn_name_index

    fn_name_index = fn_name_index + 1
    return "__fn{0}".format(fn_name_index)


def parse_tokens(tokens, in_body=0, in_table_construct=0, in_fn_arguments=0):

    out = []

    while len(tokens) > 0:
        token = tokens.pop(0)

        # Make sure we do not construct tuple when comma list is passed
        # as function arguments/table constructor
        if len(tokens) \
                and is_op(tokens[0], ",") \
                and in_fn_arguments == 0 \
                and in_table_construct == 0:

            tuple_tokens = [token]
            tokens.pop(0)

            # Continue through comma list until the end
            while len(tokens) > 0:
                tuple_tokens.append(tokens.pop(0))

                if len(tokens) == 0:
                    break

                if not is_op(tokens[0], ","):
                    break

                tokens.pop(0)

            out.append({"type": "tuple", "value": parse_tokens(tuple_tokens)})
            continue

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

        if token["type"] == "OP" and token["value"] == "#":
            assignments = extract_assignments(tokens)
            out.append({
                "type": "call",
                "name": "#",
                "args": parse_tokens(assignments),
            })
            continue

        if token["type"] == "OP" and token["value"] == "{":
            table_tokens = extract_table(tokens)
            table_tokens = extract_assignments_by_comma(table_tokens)

            nodes = map(
                lambda x: parse_tokens(x, in_table_construct=1),
                table_tokens
            )

            nodes = [x[0] for x in nodes]

            # print(table_tokens)
            out.append({
                "type": "table",
                "value": nodes,
            })
            continue

        if token["type"] == "OP" and token["value"] == "not":
            assignments = extract_assignments(tokens)
            out.append({
                "type": "call",
                "name": token["value"],
                "args": parse_tokens(assignments),
            })
            continue

        # Ignore [ if beeing used as constructor in table
        if in_table_construct == 1 and is_op(token, "["):
            continue

        # [ is beeing used as a accessor for table
        if in_table_construct == 0 and is_op(token, "["):
            key_tokens = extract_until_end_op(tokens, "]")

            expression = {
                "type": "call",
                "name": "[",
                "args": [out.pop(), parse_tokens(key_tokens)],
            }

            if in_body:  # Do not wrap expression if already running in one
                out.append({
                    "type": "expr",
                    "value": [expression],
                })
            else:
                out.append(expression)
            continue

        if token["type"] == "OP" and token["value"] in OPERATORS:
            assignments = extract_assignments(tokens)

            # Move function outside assignment and declare it in above scope
            # with keyword ref
            if token["value"] == "=" and is_keyword(assignments[0], "function"):
                assignments = inline_anonymous_function(assignments, out)

            out.append({
                "type": "call",
                "name": token["value"],
                "args": [
                    out.pop(),
                    parse_tokens(
                        assignments,
                        in_table_construct=in_table_construct,
                    )
                ],
            })
            continue

        if token["type"] == "NAME" and len(tokens) and is_op(tokens[0], "("):
            args = extract_args(tokens)

            expression = {
                "type": "call",
                "name": token["value"],
                "args": parse_tokens(args, in_fn_arguments=1)
            }

            if in_body:  # Do not wrap expression if already running in one
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
                "body": parse_tokens(body, in_body=1),
            })
            continue

        if token["type"] == "KEYWORD" and token["value"] in ["if", "elseif"]:
            if_nodes = extract_scope_body(tokens)

            test_nodes = extract_to_keyword(if_nodes, "then")
            body = extract_if_body(if_nodes)

            out.append({
                "type": "if",
                "test": parse_tokens(test_nodes),
                "body": parse_tokens(body, in_body=1),
                "else": parse_tokens(if_nodes),
            })
            continue

        if token["type"] == "KEYWORD" and token["value"] == "for":


            body_tokens = extract_scope_body(tokens)
            iteration_tokens = extract_to_keyword(body_tokens, "do")
            if contains_op(iteration_tokens, "="):
                target_tokens = extract_to_op(iteration_tokens, "=")
            else:
                target_tokens = extract_to_keyword(iteration_tokens, "in")

            out.append({
                "type": "for",
                "target": parse_tokens(target_tokens),
                "iteration": parse_tokens(iteration_tokens),
                "body": parse_tokens(body_tokens, in_body=1),
            })
            continue

        if token["type"] == "KEYWORD" and token["value"] == "while":
            while_tokens = extract_scope_body(tokens)
            test_tokens = extract_to_keyword(while_tokens, "do")

            out.append({
                "type": "while",
                "test": parse_tokens(test_tokens),
                "body": parse_tokens(while_tokens, in_body=1),
            })
            continue

        if token["type"] == "KEYWORD" and token["value"] == "return":
            assignments = extract_assignments(tokens)

            if is_keyword(assignments[0], "function"):
                assignments = inline_anonymous_function(assignments, out)

            out.append({
                "type": "return",
                "value": parse_tokens(assignments),
            })
            continue

        if token["type"] == "KEYWORD" and token["value"] == "function":
            function_tokens = extract_scope_body(tokens)
            signature_tokens = extract_fn_signature(function_tokens)
            function_name = ""

            if signature_tokens[0]["type"] == "NAME":
                name_token = signature_tokens.pop(0)
                function_name = name_token["value"]
            else:
                function_name = None

            parameter_tokens = signature_tokens[1:-1]
            # Only accept name as argument
            parameter_tokens = filter(
                lambda x: x["type"] == "NAME",
                parameter_tokens
            )

            parameter_tokens = map(
                lambda x: {"type": "argument", "name": x["value"]},
                parameter_tokens
            )

            out.append({
                "type": "function",
                "name": function_name,
                "args": list(parameter_tokens),
                "body": parse_tokens(function_tokens, in_body=1),
            })
            continue

        if token["type"] == "NAME":
            out.append({
                "type": "name",
                "name": token["value"],
            })
            continue

    return out


def is_op(token, op):
    return token.get("type", None) == "OP" and token["value"] == op


def is_keyword(token, keyword):
    return token["type"] == "KEYWORD" and token["value"] == keyword


def extract_table(tokens):
    out = []
    depth = 0

    while len(tokens) > 0:
        token = tokens.pop(0)
        out.append(token)

        if depth > 0 and is_op(token, "}"):
            depth = depth +1
            continue

        if is_op(token, "}"):
            break

    return out


def extract_fn_signature(tokens):
    out = []

    while len(tokens) > 0:
        token = tokens.pop(0)
        out.append(token)
        if is_op(token, ")"):
            break
    return out


def extract_scope_body(tokens):
    out = []

    depth = 0

    while len(tokens) > 0:
        token = tokens.pop(0)
        out.append(token)

        if token["type"] == "KEYWORD" and token["value"] in ["if", "function"]:
            depth = depth + 1
            continue

        if depth > 0 and token["type"] == "KEYWORD" and token["value"] in ["if", "end"]:
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

        if is_keyword(token, "if"):
            out.append(token)
            tokens.pop(0)
            depth = depth + 1
            continue

        if depth > 0 and is_keyword(token, "end"):
            out.append(token)
            tokens.pop(0)
            depth = depth - 1
            continue

        if depth == 0 and is_keyword(token, "elseif"):
            break

        if depth == 0 and is_keyword(token, "else"):
            break

        if depth == 0 and is_keyword(token, "end"):
            break

        out.append(token)
        tokens.pop(0)

    return out

def extract_until_end_op(tokens, exit_op="]"):
    out = []

    while len(tokens) > 0:
        token = tokens.pop(0)

        if is_op(token, exit_op):
            break

        out.append(token)

    return out

def extract_until_end_op(tokens, exit_op="]"):
    out = []

    while len(tokens) > 0:
        token = tokens.pop(0)

        if is_op(token, exit_op):
            break

        out.append(token)

    return out


def extract_to_op(tokens, exit_op="="):
    out = []

    while len(tokens) > 0:
        token = tokens.pop(0)

        if is_op(token, exit_op):
            break

        out.append(token)

    return out

def extract_to_keyword(tokens, exit_keyword="then"):
    out = []

    while len(tokens) > 0:
        token = tokens.pop(0)

        if is_keyword(token, exit_keyword):
            break

        out.append(token)

    return out


def extract_assignments(tokens):
    out = []
    depth = 0

    while len(tokens) > 0:
        token = tokens.pop(0)

        if is_keyword(token, "function"):
            out.append(token)
            depth = depth + 1
            continue

        if is_op(token, "("):
            out.append(token)
            depth = depth + 1
            continue

        if is_op(token, "{"):
            out.append(token)
            depth = depth + 1
            continue

        if is_op(token, ")"):
            out.append(token)
            depth = depth - 1
            continue

        if is_keyword(token, "end"):
            out.append(token)
            depth = depth - 1
            continue

        if is_op(token, "}"):
            out.append(token)
            depth = depth - 1
            continue

        if token["type"] == "NL" and depth == 0:
            break

        out.append(token)

    return out

def inline_anonymous_function(tokens, out):
    fn_name = generate_function_name()

    fn_tokens = parse_tokens(tokens)
    fn_tokens[0]["name"] = fn_name
    out.insert(-1, fn_tokens[0])
    assignments = [{"type": "NAME", "value": fn_name}]
    return assignments


def extract_args(tokens):
    depth = 1
    args = []

    tokens.pop(0)  # Drop (

    while depth != 0:
        token = tokens.pop(0)

        if is_op(token, "("):
            depth = depth+1

        if is_op(token, ")"):
            depth = depth-1

        args.append(token)

    args = args[:-1]  # Drop )
    return args


def extract_assignments_by_comma(tokens):
    pairs = [[]]
    depth = 0

    while len(tokens) > 0:
        token = tokens.pop(0)

        if is_op(token, "{"):
            depth = depth + 1

        if is_op(token, "("):
            depth = depth + 1

        if is_op(token, "}"):
            depth = depth - 1

        if is_op(token, ")"):
            depth = depth - 1

        if depth == 0 and is_op(token, ","):
            pairs.append([])
            continue

        pairs[-1].append(token)

    return pairs


def contains_op(tokens, op):
    for token in tokens:
        if is_op(token, op):
            return True
    return False


def parse(tokens):
    ast_ = parse_tokens(tokens, in_body=1)
    return ast_
