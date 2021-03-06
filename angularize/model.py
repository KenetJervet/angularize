from collections import OrderedDict
from inspect import Signature, Parameter
from .datatypes import *

def make_signature(names):
    sig = Signature(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names)
    return sig
        

class ModelMetaClass(type):
    '''好吧这是从Python 3 Metaprogramming视频中抄袭而来'''
    
    def __prepare__(name, *bases):
        d = OrderedDict()
        return d


    def __new__(cls, name, bases, clsdict):
        clsobj = super().__new__(cls, name, bases, clsdict)
        descriptors = {k: v for k, v in clsdict.items() if isinstance(v, DataTypeDescriptor)}
        for k, v in descriptors.items():
            setattr(v, 'name', k)
            setattr(v, '_containing_class', clsobj)

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
    '''Ngz模型，可从中生成AngularJS代码'''

    @property
    def dict_repr(self):
        dict = {
            k: getattr(self, k)
            for k, v in self.__class__.__dict__.items()
            if isinstance(v, DataTypeDescriptor)
        }

        return dict

    def __str__(self):
        return str(self.dict_repr)

        
