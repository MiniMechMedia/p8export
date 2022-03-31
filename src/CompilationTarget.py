from abc import ABC, abstractmethod

# from src.ParsedContents import ParsedContents


class CompilationTarget(ABC):
    @abstractmethod
    def compile(self, data: object):
        pass
