try:
    profile  # noqa
except:
    # Create a profile decorator for testing if not running with kernprof
    def profile(func):
        return func


from time import sleep


@profile
def recursive_func(val):
    if val == 0:
        return val
    if val < 1:
        sleep(.30)
        return val + recursive_func(val + 1)
    elif val < 5:
        sleep(.20)
        return val + recursive_func(val * 2)
    elif val < 100:
        sleep(.01)
        return val + recursive_func(val + .2)
    elif val > 1000:
        sleep(.10)
        return val + recursive_func(val / 100)
    else:
        sleep(.10)
        return val


data_array = [0.1, 2, 4, 5, 8, 9, 20, 50, 100, 1000, 5000, 2000, 30000]


@profile
def my_func():
    for val in data_array:
        recursive_func(val)


my_func()
