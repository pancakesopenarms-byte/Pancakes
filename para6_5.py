def checker(var1):
    if type(var1) != str:
        raise TypeError(f"Sorry, we can't work with {type(var1)}")
    else:
        return var1
    

first_car = 10
checker(first_car)
