class Laptop:

    object_counter = 0

    def __init__(self, brand):
        object_counter += 1

print(f'Class.class_variable = {Laptop.object_counter}')
obj = Laptop("dell")
print(f'inst.class_variable = {Laptop.object_counter}')