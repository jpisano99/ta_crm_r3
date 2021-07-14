def logger(func_to_log):

    import logging, datetime
    now = datetime.datetime.now()
    timestamp = now.strftime("%H:%M:%S")
    func_name = func_to_log.__name__

    logging.basicConfig(filename='{}.log'.format(func_name), level=logging.INFO)

    def wrapper_func(*args, **kwargs):

        logging.info(" Function {} logged args {} with kwargs {} at {}".format(func_name, args, kwargs, timestamp))

        return func_to_log(*args, **kwargs)

    return wrapper_func


@logger
def add_it(a, b):

    print('i added ', a+b)

    return

@logger
def sub_it(a, b):

    print('i subtracted ', a-b)

    return

exit()

jim = add_it
ang = sub_it

print(ang(3, 2))
print(jim(3, 2))
