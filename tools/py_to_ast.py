# A simple file for converting python to AST
import ast
import pprint


tree = ast.parse(
"""

val = True

"""
)
pprint.pprint(ast.dump(tree))
