# n = 0.0

# if n:
#     print("True")
# else:
#     print("False")

# import json

# # dic = '''{"name" : "moaad", "age": 21}'''

# # with open("scores.json", "w") as f:
# #     json.dump(dic, f)


# # m = json.dumps(dic)
# # print(type(m))

# with open("scores.json", "r") as f:
#     res = json.loads(f)

# print(res)
scores = {"moaad": 20, "bilal": 10, "ayoub": 30}
# scores = scores[:2]
# print(scores)

scores = sorted(scores.items(), key=lambda x : x[1], reverse=True)

print(dict(list(scores)[:2]))

# print(scores)