function bar(a, b, c)
  print(a, b, c)
  return (1 + 2)
end

v = bar(1, 2, 3)
print(v)

a = function (x, y) return x + y end
print(a(1, 2))
