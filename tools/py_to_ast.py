# A simple file for converting python to AST
import ast
import pprint


tree = ast.parse(
"""
a = True
b = False
if a or b:
    print("YES")

"""
)
pprint.pprint(ast.dump(tree))

