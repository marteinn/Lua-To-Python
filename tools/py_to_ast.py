# A simple file for converting python to AST
import ast
import pprint


tree = ast.parse(
"""
globals()["a"] = 1
"""
)
pprint.pprint(ast.dump(tree))

