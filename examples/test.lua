-- From: https://learnxinyminutes.com/docs/lua/
-- Two dashes start a one-line comment.

--[[
     Adding two ['s and ]'s makes it a
     multi-line comment.
--]]

----------------------------------------------------
-- 1. Variables and flow control.
----------------------------------------------------

--num = 12  -- All numbers are doubles.
--numa = 5  -- All numbers are doubles.
-- Don't freak out, 64-bit doubles have 52 bits for
-- storing exact int values; machine precision is
-- not a problem for ints that need < 52 bits.
--
--s = 'walternate'
--t = "double-quotes are also fine"
--t = nil  -- Undefines t; Lua has garbage collection.

num = 42
--t = 2
--numa = 5

aBoolValue = false

while num >= 10 do
  num = num - 1  -- No ++ or += type operators.
  print(num)
end

print('Winter is coming, ' .. 'Hello')
