from pathlib import Path
import sys
from ParsedContents import ParsedContents
from os.path import exists


class P8Export:
    @classmethod
    def export(cls, targetFile: Path):
        if not exists(targetFile):
            raise Exception("invalid target")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("must provide target")
    P8Export.export(Path(sys.argv[1]))
