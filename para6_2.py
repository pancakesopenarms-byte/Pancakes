try:
    print("Start")
    print(10/0)
    print("No errors")
except NameError:
    print("We have an error")
except ZeroDivisionError:
    print("We have an error")

print("code after capsule")