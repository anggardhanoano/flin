from abc import ABC, abstractmethod


class Runnable(ABC):
    """
    This class is inspired by java Runnable class.
    https://docs.oracle.com/javase/8/docs/api/java/lang/Runnable.html

    This can be used in single method class (e.g. service class that follow
    1-logic-1-service pattern), to standardize the method name and i/o.
    """

    @classmethod
    @abstractmethod
    def run(cls, **kwargs) -> object:
        pass
