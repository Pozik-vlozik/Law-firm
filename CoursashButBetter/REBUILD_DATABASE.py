
argument = " very "


def decorator_factory(deratated_finctoin):
    def decorator(argument):
        def wrapper(*args, **kwargs):
            print("Hello ")
            print(argument)
            deratated_finctoin(*args, **kwargs)
        return wrapper
    return decorator


def decor(func):
    def wrapper(*args, **kwargs):
        print("Hello ", end=" ")
        func(*args, **kwargs)
    return wrapper


@decorator_factory
def func(name):
    print(name)


func(argument)(" Andrey ")
