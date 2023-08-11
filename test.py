def decorator(ori):
    print("decorator")

    def wrapper(*args, **kwargs):
        print("wrapper")
        return ori(*args, **kwargs)

    return wrapper


@decorator
def display(hi, hello):
    print("display", hi, hello)


display("hi", "hello")
