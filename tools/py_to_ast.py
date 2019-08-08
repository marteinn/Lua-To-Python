# A simple file for converting python to AST
import ast
import pprint


tree = ast.parse(
"""

a = 2 % 2

"""
)
pprint.pprint(ast.dump(tree))
