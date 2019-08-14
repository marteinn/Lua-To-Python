u = {cat = "Fluffy", dog="Bob", horse="Sr speedalot"}

for key, val in pairs(u) do  -- Table iteration.
  print(key, val)
end

for item in pairs(u) do
  print(item)
end
