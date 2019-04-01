import threading

def hello():
    print('test')

t = threading.Timer(10.0, hello)
