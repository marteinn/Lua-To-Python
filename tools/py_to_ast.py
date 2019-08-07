# A simple file for converting python to AST
import ast
import pprint


tree = ast.parse(
"""

def bar(a, b, c):
    print(a, b, c)
    return 1


"""
)
pprint.pprint(ast.dump(tree))
