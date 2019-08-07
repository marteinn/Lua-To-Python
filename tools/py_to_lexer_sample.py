# A simple tool for cnverting python code to tokens

from tokenize import generate_tokens
from io import StringIO
from pprint import pprint


code = """
# My comment
myvar = 1

def foo(a, b=10):
  return a + b
"""

d = list(generate_tokens(StringIO(code).readline))
pprint(d)
