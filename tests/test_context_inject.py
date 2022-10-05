import asyncio
import pytest
from collections import OrderedDict
from contextvars import copy_context
from nisa_di.context_inject import get_context_dependency, inject_context, run_in_new_context


class Abaca:
    msg: str = 'asdasd'

class WithVar:
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs



async def running():
    inject_context.set({})
    
    cc = get_context_dependency(Abaca)
    assert cc.msg == 'asdasd'
    cc2 = get_context_dependency(Abaca)
    
    assert cc == cc2
    
    return cc


async def context_var_run():
    
    inject_context.set({})
    
    cc = get_context_dependency(WithVar, 12, "asd", 3, name="dasd")
    cc2 = get_context_dependency(WithVar, 12, "asd", 3, name="dasd")
    
    assert cc == cc2
    
    return cc


async def diff_run():
    
    inject_context.set({})
    
    cc = get_context_dependency(WithVar, 12, "asd", 3, name="dasd")
    cc2 = get_context_dependency(WithVar, 12, 3, name="dasd")
    
    assert cc != cc2
    
    return cc
    
    

@pytest.mark.asyncio
async def test_context_inject():

    cc1 = await run_in_new_context(running)
    cc2 = await run_in_new_context(running)
    
    
    assert cc1 != cc2
    
    
    
    cc1 = run_in_new_context(context_var_run)
    cc2 = run_in_new_context(context_var_run)
    
    
    await asyncio.gather(cc1, cc2)
    
    assert cc1 != cc2
    
    
    cc1 = await run_in_new_context(diff_run)
    cc2 = await run_in_new_context(diff_run)
    
    assert cc1 != cc2
    
    
def test_hash():
    def cc(*arg, **kwawg):
        
        data = frozenset(OrderedDict(kwawg).items())
        cc = (arg, data)
        print(hash(cc))
        # print(hash((arg, kwawg)))
        
    cc(2,3,"ada", he="asd", cs="asdasd")
    cc(2,3,"ada", cs="asdasd", he="asd")