# Lua to Python

This is a project where I attempt to convert Lua to Python, by transforming Lua into Python AST and the running it.

Its only for getting to know the Python AST so please dont do anything serious with it.

## Current status
- Variable assignments, basic datatypes and comparisons, if statements, while loops and functions are working.


## Getting started

- pip install click
- python main.py <path-to.your-lua-file>


## Roadmap
- [x] Single line comments
- [x] Multiline comments
- [x] Numbers
- [x] Strings
- [x] Nil types
- [x] Variable assignments
- [x] Addition
- [x] Multiplication
- [x] If statements
- [x] Nested if statements
- [x] `~=`  operator
- [x] `==`  operator
- [x] `while` keyword
- [x] Concat strings with `..`
- [x] Subtract values
- [x] `>=` operator
- [x] `<=` operator
- [x] Boolean types
- [x] `function` declarations
- [x] `return`
- [x] `not` logical operator
- [ ] `bool` expression in comparison
- [ ] `%` operator
- [ ] `/` operator
- [ ] `or` logical operator
- [ ] `and` logical operator
- [ ] Assign function return to variable
- [ ] Double number support
- [ ] Negative values
- [ ] Anonymous functions
- [ ] Table datatype
- [ ] `_G` for globals access
- [ ] `for` keyword
- [ ] `repeat` keyword
- [ ] Short circuit / tenary operator
- [ ] `local` variables
- [ ] Undefined variables should return nil


## References
- https://drew.ltd/blog/posts/2020-7-18.html - Many thanks for Drew and his excellent articles on how to build a programming language
- https://greentreesnakes.readthedocs.io/en/latest/
- https://github.com/python/cpython/blob/master/Lib/ast.py
- https://learnxinyminutes.com/docs/lua/
