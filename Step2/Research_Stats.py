# Allows for abstract classes
import abc  # abc.ABCMeta, @abc.abstractmethod

class Research_Stats(metaclass=abc.ABCMeta):
    AP  = "All-Languages"
    SLP = "Single-Languages"
    MLP = "Multiple-Languages"
    Project_Types = [AP, SLP, MLP]

    @abc.abstractmethod
    def create_row(self, key):
        print("Abstract Method that is implemented by inheriting classes")
