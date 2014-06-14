from collections import OrderedDict
from inspect import Signature, Parameter
from .datatypes import *

def make_signature(names):
    sig = Signature(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names)
    return sig
        

class ModelMetaClass(type):
    def __prepare__(name, *bases):
        d = OrderedDict()
        return d


    def __new__(cls, name, bases, clsdict):
        clsobj = super().__new__(cls, name, bases, clsdict)
        descriptors = {k: v for k, v in clsdict.items() if isinstance(v, DataTypeDescriptor)}
        for k, v in descriptors.items():
            setattr(v, 'name', k)

        sig = make_signature(descriptors)
        clsobj.__signature__ = sig
        def _init(self, *args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            for n, v in bound.arguments.items():
                setattr(self, n, v)
        clsobj.__init__ = _init
        return clsobj


    def __init__(self, name, bases, clsdict):
        pass


class NgzModel(metaclass=ModelMetaClass):
    '''没想好'''
    pass