import unittest
import shutil, os


try:
    shutil.rmtree("tmp/")
except FileNotFoundError:
    pass

os.makedirs("tmp/")

loader = unittest.TestLoader()

suite = loader.discover("test")

runner = unittest.TextTestRunner()
runner.run(suite)
