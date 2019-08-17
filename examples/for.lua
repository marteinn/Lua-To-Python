print("-- 1")
for i = 1, 5 do -- 1, 2, 3, 4, 5
  print(i)
end

print("-- 1")
for i = 1, 6, 2 do -- 1, 3, 5
  print(i)
end

print("-- 3")
for i = 5, 1, -2 do -- 5, 3, 1
  print(i)
end

print("-- 4")
v = {a=1, b=2}
for key, val in pairs(v) do -- 1, 2, 3
  print(key)
end

print("-- 5")
v = {1, 2, 3, 4}
for key, val in pairs(v) do -- 1, 2, 3
  print(key)
end
