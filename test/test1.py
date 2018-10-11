import datetime,time


def datatiem2strftime(data):
    '''dict数据中的datetime转换成strtime'''
    output = data
    if isinstance(data, datetime):
        output = data.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(data, dict):
        for k, v in data.items():
            data[k] = datatiem2strftime(v)
    if isinstance(data, list):
        for i, v in enumerate(data):
            data[i] = datatiem2strftime(v)
    return output
def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        # return x.isoformat()
        return x.strftime("%Y-%m-%d %H:%M:%S")
    raise TypeError("Unknown type")

a = datetime_handler(datetime.datetime.now())
print (type(a))
print(a)

b = datetime.datetime.now()
print(type(b))

c =  datetime.datetime.date()
print(c)