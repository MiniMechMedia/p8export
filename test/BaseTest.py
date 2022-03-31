import unittest
import pathlib


class BaseTest(unittest.TestCase):
    def getTestFilePath(self, testFileName: str) -> pathlib.Path:
        return pathlib.Path("test/testFiles/" + testFileName)
