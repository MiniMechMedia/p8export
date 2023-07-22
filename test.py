import unittest
import shutil, os
import sys

pattern = sys.argv[1]


try:
    shutil.rmtree("tmp/")
except FileNotFoundError:
    pass

os.makedirs("tmp/")

loader = unittest.TestLoader()

suite = loader.discover("test",
                        pattern='testParsing_.' + pattern
        # pattern='testParsing_.*'
        #                 pattern='*' + pattern + '*'
                        )

runner = unittest.TextTestRunner()
runner.run(suite)
