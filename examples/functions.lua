function bar(a, b, c)
  print(a, b, c)
  return (1 + 2)
end

v = bar(1, 2, 3)
print(v)

a = function (x, y) return x + y end
print(a(1, 2))

function fib(n)
  if n < 2 then return 1 end
  return fib(5)
end

-- Closures and anonymous functions are ok:
function adder(x)
  -- The returned function is created when adder is
  -- called, and remembers the value of x:
  return function (y) return x + y end
end


v = adder(5)
print(v(2))

a1 = adder(9)
a2 = adder(36)
print(a1(16))  --> 25
print(a2(64))  --> 100
