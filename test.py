import json

s = "[{\"test\":1}, {\"s\":2}]"

print(type(s))
data = json.loads(s)
print(type(data))
print(data)

prefix = "public/JSON/" + "2014-12"
file = prefix + "-originalCommits.json"
print(file)
with open(file,"r") as f:
    data = f.read()
    print(data)
    print(type(data))
    data = json.loads(data)
