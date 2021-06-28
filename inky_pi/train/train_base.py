"""Base class for train model"""
from abc import ABC, abstractmethod


class TrainBase(ABC):
    """Abstract base class for all train models"""
    @abstractmethod
    def fetch_train(self, num: int) -> str:
        """Return requested train data"""
        ...
