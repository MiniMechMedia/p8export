from abc import ABC, abstractmethod

# from src.ParsedContents import ParsedContents


class CompilationTarget(ABC):
    pass
    # Does disk/network IO stuff
    # @abstractmethod
    # def compileToIo(self, data: object) -> None:
    #     raise NotImplemented
    #
    # @abstractmethod
    # def compileToString(self, data: object) -> str:
    #     raise NotImplemented
    #
    # @abstractmethod
    # def compileToBinary(self, data: object) -> bytes:
    #     raise NotImplemented
