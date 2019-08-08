# Covert AST to Python AST

import ast


def ast_to_py_ast(nodes):
    ast_ = parse_nodes(nodes)

    tree = ast.Module(ast_)
    tree = ast.fix_missing_locations(tree)
    return tree


def parse_nodes(nodes):
    out = []
    while len(nodes) > 0:
        node = nodes.pop(0)

        if node["type"] == "string":
            out.append(ast.Str(s=node["value"]))
            continue

        if node["type"] == "boolean":
            value = node["value"]
            value = True if value == "true" else value
            value = False if value == "false" else value
            out.append(out.append(ast.NameConstant(value=value)))
            continue

        if node["type"] == "number":
            out.append(ast.Num(n=int(node["value"])))
            continue

        if node["type"] == "nil":
            out.append(ast.NameConstant(value=None))
            continue

        if node["type"] == "return":
            out.append(
                ast.Return(value=parse_nodes(node["value"])[0])
            )
            continue

        if node["type"] == "assign":
            out.append(
                ast.Assign(
                    targets=[
                        ast.Name(id=node["name"], ctx=ast.Store())
                    ],
                    value=parse_nodes(node["value"])[0],
                )
            )
            continue

        if node["type"] == "name":
            out.append(
                ast.Name(id=node["name"], ctx=ast.Load())
            )
            continue

        if node["type"] == "expr":
            out.append(
                ast.Expr(
                    value=parse_nodes(node["value"])[0]
                )
            )
            continue

        if node["type"] == "function":
            body_nodes = parse_nodes(node["body"])
            out.append(
                ast.FunctionDef(
                    name=node["name"],
                    args=ast.arguments(
                        args=[
                            ast.arg(
                                arg=x["name"],
                                annotation=None,
                            ) for x in node["args"]
                        ],
                        vararg=None,
                        kwonlyargs=[],
                        kw_defaults=[],
                        kwarg=None,
                        defaults=[]
                    ),
                    body=body_nodes,
                    decorator_list=[],
                )
            )
            continue

        if node["type"] == "if":
            test_nodes = parse_nodes(node["test"])
            body_nodes = parse_nodes(node["body"])
            else_nodes = parse_nodes(node["else"])

            out.append(
                ast.If(
                    test=test_nodes[0],
                    body=body_nodes,
                    orelse=else_nodes,
                )
            )
            continue

        if node["type"] == "while":
            test_nodes = parse_nodes(node["test"])
            body_nodes = parse_nodes(node["body"])

            out.append(
                ast.While(
                    test=test_nodes[0],
                    body=body_nodes,
                    orelse=[],
                )
            )

        if node["type"] == "else":
            body_nodes = parse_nodes(node["body"])
            out = out + body_nodes
            continue

        if node["type"] == "call":
            if node["name"] == "=":
                name_arg = node["args"][0]

                out.append(
                    ast.Assign(
                        targets=[
                            ast.Name(id=name_arg["name"], ctx=ast.Store())
                        ],
                        value=parse_nodes(node["args"][1])[0],
                    )
                )
                continue

            if node["name"] in ["-"]:
                arg_left = parse_nodes([node["args"][0]])
                arg_right = parse_nodes(node["args"][1])

                out.append(
                    ast.BinOp(
                        left=arg_left[0],
                        op=ast.Sub(),
                        right=arg_right[0],
                    )
                )
                continue

            if node["name"] in ["+"] or node["name"] == "..":
                arg_left = parse_nodes([node["args"][0]])
                arg_right = parse_nodes(node["args"][1])

                out.append(
                    ast.BinOp(
                        left=arg_left[0],
                        op=ast.Add(),
                        right=arg_right[0],
                    )
                )
                continue

            if node["name"] in ["*"]:
                arg_left = parse_nodes([node["args"][0]])
                arg_right = parse_nodes(node["args"][1])

                out.append(
                    ast.BinOp(
                        left=arg_left[0],
                        op=ast.Mult(),
                        right=arg_right[0],
                    )
                )
                continue

            if node["name"] in [">", "<", "~=", "==", "<=", ">="]:
                ops = node["name"]

                arg_left = parse_nodes([node["args"][0]])
                arg_right = parse_nodes(node["args"][1])

                ops_ref = {
                    ">": ast.Gt,
                    ">=": ast.GtE,
                    "<": ast.Lt,
                    "<=": ast.LtE,
                    "~=": ast.NotEq,
                    "==": ast.Eq,
                }

                out.append(
                    ast.Compare(
                        left=arg_left[0],
                        ops=[ops_ref[ops]()],
                        comparators=arg_right,
                    )
                )
                continue

            out.append(
                ast.Call(
                    func=ast.Name(id=node["name"], ctx=ast.Load()),
                    args=parse_nodes(node["args"]),
                    keywords=[]
                )
            )
            continue

    return out
