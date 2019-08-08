# A simple file for converting python to AST
import ast
import pprint


tree = ast.parse(
"""

a = False
if not a:
    print("Oh no")


"""
)
pprint.pprint(ast.dump(tree))
