x = list(range(10))
x.extend(list(reversed(x[:-1])))
print(x)
