from django.db import connection,transaction
from threading import Thread

def threaded(func):
    def func_close_conn(*args, **kwargs):
        func(*args, **kwargs)
        connection.close()

    """Make a function call async"""

    def wrapper(*args, **kwargs):
        thread = Thread(target=func_close_conn, args=args, kwargs=kwargs)
        transaction.on_commit(lambda: thread.start())
        return thread
 
    return wrapper