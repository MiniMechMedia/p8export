from pathlib import Path
from src.ParsedContents import ParsedContents

class P8FileTransformerCompilationTarget:
    @classmethod
    def transformP8File(cls, p8FilePath: Path, parsed: ParsedContents):
        lines = p8FilePath.read_text().split('\n')
        passedLua: bool = False
        commentLineCount = 0
        for index, line in enumerate(lines[:]):
            if passedLua:
                if line.startswith('--'):
                    if commentLineCount == 0:
                        lines[index] = f'--{parsed.metadata.p8FileGameName}'
                    elif commentLineCount == 1:
                        lines[index] = f'--{parsed.config.gameAuthor}'
                    else:
                        raise Exception("that shouldn't happen")
                else:
                    if commentLineCount == 0:
                        lines.insert(index, f'--{parsed.metadata.p8FileGameName}')
                    elif commentLineCount == 1:
                        lines.insert(index, f'--{parsed.config.gameAuthor}')
                    else:
                        raise Exception("that shouldn't happen")
                commentLineCount += 1
                if commentLineCount >= 2:
                    break

            elif line == '__lua__':
                passedLua = True

        contents = '\n'.join(lines)
        p8FilePath.write_text(data=contents)
