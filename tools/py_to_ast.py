# A simple file for converting python to AST
import ast
import pprint


tree = ast.parse(
"""
a = lambda x, y: cat(x)
def main():
    def sub_func():
        return 1
    return sub_func

"""
)
pprint.pprint(ast.dump(tree))

