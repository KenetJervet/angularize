from .translator import AstTranslator
from .datatypes import Watched
from .model import NgzModel

class NgzTranslator(AstTranslator):

    def __init__(self, model):
        if not isinstance(model, NgzModel):
            raise TypeError("%s不是一个Ngz模型" % model)

        self.model = model

    def translate(self):
        model_type = type(model)
        watched_fields = [watched
                          for watched in model_type.__dict__
                          if isinstance(watched, Watched)]