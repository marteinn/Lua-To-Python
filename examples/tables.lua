t = {['@!#'] = 1, [2] = 3, key1 = 'value1', key2 = false, key3 = { subkey = 5 }}
u = {1, 2, [3] = "three"}
v = {[1] = 'qbert', [6.28] = 'tau'}

--print(t["key1"])
--t.key1
--
print(t["@!#"]) -- 1
print(t["key3"]) -- <dict>
print(t)

print(u[1]) -- 3
print(u[3]) -- three
print(u)

--print(t["key3"])
--print(t["1"])
print(v[1])
print(v)
print(v)
