# Does the submission.html
from src.ParsedContents import Config, ParsedContents
from src.CompilationTarget import CompilationTarget
from pathlib import Path
import shutil

# import os
import subprocess
import tempfile
from os.path import exists
import os

class TweetCartCompilationTarget(CompilationTarget):
    @classmethod
    def exportToMinified(cls, parsedContents: ParsedContents):
        pass

    @classmethod
    def exportToClarified(cls, parsedContents: ParsedContents):
        pass