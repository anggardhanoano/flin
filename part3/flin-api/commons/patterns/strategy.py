# https://refactoring.guru/design-patterns/strategy/python/example

from abc import ABC, abstractmethod

class Strategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """
    @classmethod
    def execute(self, **kwargs):
        pass

class StrategyContext(ABC):
    """
    The Context defines the interface of interest to clients.
    """
    def __init__(self, strategy: Strategy = None) -> None:
        if(strategy is not None):
            self._strategy = strategy

    def set_strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def execute(self, **kwargs):
        return self._strategy.execute(**kwargs)