from .convert import derive_from_django
from .decorators import method_connect_once, method_redis_once
from .model import Model
from .. import utils


__all__ = [
    'AppModels',
    'Model',
    'derive_from_django',
    'method_connect_once',
    'method_redis_once'
]


class AppModels:
    """
    Class to managing all models of application
    """
    def __init__(self, app):
        self.app = app

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        return KeyError(item)

    def __getattr__(self, item):
        if item in Model.models:
            model_cls = Model.models[item]
            sub_class = model_cls.factory(self.app)
            setattr(self, item, sub_class)
            if hasattr(model_cls, 'relationships'):
                for k, v in model_cls.relationships.items():
                    setattr(sub_class, k, v(self.app))
            return sub_class
        raise AttributeError('%r has no attribute %r' % (self, item))

    @staticmethod
    def import_all_models(apps_path):
        """Imports all the models from apps_path"""
        utils.import_module_from_all_apps(apps_path, 'amodels')

    @staticmethod
    def import_all_models_from_packages(package):
        """Import all the models from package"""
        utils.import_modules_from_packages(package, 'amodels')