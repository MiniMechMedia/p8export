from src.ParsedContents import ParsedContents, Config
from textwrap import dedent
from src.TemplateEvaluator import TemplateEvaluator
from pathlib import Path
import os
import subprocess
import base64

class Pico8EduUrlCompilationTarget:

    @classmethod
    def compileToPico8Url(cls, parsedContents: ParsedContents):
        fullRom: bytes = cls.writeFullRomMinified(
            parsedContents.config,
            parsedContents
        )
        code = cls.extractCodeFromRom(fullRom)
        url = cls.createUrlFromCode(code)
        return url


    @classmethod
    def createUrlFromCode(cls, code: bytes):
        encoded = base64.b64encode(code, altchars=b'_-').decode('ascii')
        return f'https://pico-8-edu.com/?c={encoded}'
    #
    # # TODO test if it respects pico8 version number
    # # (probs doesn't)
    # @classmethod
    # def createRomFromSourceCode(cls, raw_contents: str, source: str) -> bytes:
    #     raw_contents.replace(source)

    @classmethod
    def extractCodeFromRom(cls, fullRomContents: bytes):
        return fullRomContents[17152:].rstrip(b'\x00')

    @classmethod
    def createMinifiedCartContents(cls, parsedContents: ParsedContents) -> str:
        githubLink = TemplateEvaluator.constructExplainerCodeLink(parsedContents)
        header = f'-- see explanation on {githubLink}\n'
        return parsedContents.rawContents.replace(
            parsedContents.sourceCode,
            header +
            parsedContents.minifiedSourceCode
        )

    @classmethod
    def writeFullRomMinified(
            cls,
            config: Config,
            parsedContents: ParsedContents) -> bytes:
        minifiedCartContents: str = cls.createMinifiedCartContents(parsedContents)
        root = (Path(__file__) / ".." / "..").resolve() / "tmp"
        # os.m
        # Sure why not?
        root.mkdir(exist_ok=True)
        # print('checkhere',root)
        temporaryP8FileName = root / 'tweetMinified.p8'
        with open(temporaryP8FileName, "w") as file:
            file.write(minifiedCartContents)

        # raise Exception(str(temporaryP8FileName))

        temporaryRomFileName = root / 'tweetMinified.p8.rom'

        args: list[str] = [
            config.pico8ExePath,
            str(temporaryP8FileName.absolute().resolve()),
            '-export',
            str(temporaryRomFileName.name)
        ]

        subprocess.run(args, cwd=temporaryRomFileName.parent, check=True)
        if not temporaryRomFileName.exists():
            raise Exception('rom export failed')

        return temporaryRomFileName.read_bytes()