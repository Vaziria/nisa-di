import time
from gevent import monkey
monkey.patch_all()
import gevent

import contextvars
from typing import Any, Callable
import threading

map_context = contextvars.ContextVar("context nya semua")
lock_context = contextvars.ContextVar("context untuk locking function")


class SafeWaitable:
    func: Callable
    
    @property
    def lock(self) -> threading.Semaphore:
        key = hash(self.func)
         
        lock_dict = lock_context.get()
        
        lock = lock_dict.get(key, None)
        if not lock:
            lock = threading.Semaphore(1)
            lock_dict[key] = lock
        
        return lock
         
    
    def __init__(self, func: Callable) -> None:
        self.func = func
        
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        with self.lock:
            cache = self.get_cache()
            if cache:
                return cache
            
            cache = self.func(*args, **kwargs)
            self.set_cache(cache)
            
            return cache        
    
    def set_cache(self, data):
        name = hash(self.func)
        data = map_context.get()
        data[name] = data
    
    
    def get_cache(self):
        name = hash(self.func)
        data = map_context.get()
        
        return data.get(name, None)


class FieldInject:
    func: Callable
    
    def __init__(self, func: Callable) -> None:
        self.func = func
    
    def __get__(self, instance, owner):
        return self.func()
    
    def __set__(self, instance, value):
        raise NotImplementedError

class Context:
    name: str = None
    data: dict
    
    def __init__(self) -> None:
        self.data = {}
        
    def get(self, key: str, value = None):
        return self.data.get(key, value)

    def set(self, key: str, value):
        self.data[key] = value

def get_context() -> Context:
    return map_context.get()

def get_dependency(depend):
    context = get_context()
    
    hash = hash(hash)
    
    hasil = context.get(hash)
    if hasil == None:
        hasil = depend()
        context.set(hash, hasil)
    
    return hasil




def run_new_context(func):
    ctx = contextvars.copy_context()

    def run(*arg, **kwarg):
        map_context.set({})
        lock_context.set({})
        return func(*arg, **kwarg)
    
    ctx.run(run)












map_context.set({})
lock_context.set({})


# context = get_context()
# print(context)


# def main():
#     context = get_context()
#     print(context)
    
#     context['name'] = "asdasdasdasd"    
#     print(context)

# run_new_context(main)



# print(context)




# def get_hash(data):
    
#     return hash(data)

# class Blues:
#     test = FieldInject(ssk)


# blue = Blues()

def test():
    print(ssk())


@SafeWaitable
def ssk():
    print("run")
    time.sleep(10)
    return "asdasdasd"




gevent.spawn(test)
gevent.spawn(test)
gevent.spawn(test)
gevent.spawn(test)
    

gevent.wait()


        
        
        
