from abc import ABCMeta, abstractmethod


class Singleton(object):
    """ A generic base class to derive any singleton class from. """
    __metaclass__ = ABCMeta
    __instance = None

    def __new__(new_singleton, *arguments, **keyword_arguments):
        """Override the __new__ method so that it is a singleton."""
        if new_singleton.__instance is None:
            new_singleton.__instance = object.__new__(new_singleton)
            new_singleton.__instance.init(*arguments, **keyword_arguments)
        return new_singleton.__instance

    @abstractmethod
    def init(self, *arguments, **keyword_arguments):
        """ 
        as __init__ will be called on every new instance of a base class of 
        Singleton we need a function for initialisation. This will only be 
        called once regardless of how many instances of Singleton are made.
        """
        raise
