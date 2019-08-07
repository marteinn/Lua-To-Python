# Evaluate AST
from ast import Module, Str, Print, fix_missing_locations


tree = Module([Print(None, [Str("PyCon2010!")], True)])
tree = fix_missing_locations(tree)

exec(compile(tree, filename="<ast>", mode="exec"))
