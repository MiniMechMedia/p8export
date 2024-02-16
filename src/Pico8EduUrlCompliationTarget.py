from src.ParsedContents import ParsedContents, Config
from textwrap import dedent
from src.TemplateEvaluator import TemplateEvaluator
from pathlib import Path
import os
import subprocess
import base64
from src.P8FileTransformerCompilationTarget import  P8FileTransformerCompilationTarget

class Pico8EduUrlCompilationTarget:

    @classmethod
    def compileToPico8Url(cls, parsedContents: ParsedContents, useMinified: bool):
        targetContents = (
            cls.createMinifiedCartContents(parsedContents)
            if useMinified else
            cls.createClarifiedCartContents(parsedContents)
        )
        fullRom: bytes = cls.writeFullRom(
            parsedContents.config,
            targetContents,
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
    def sanitizeComments(cls, source_code):
        # TODO maybe we wnat to do better wrapping
        # Comments should use proper capitalization, but that looks
        # silly in PICO-8
        env_sentinel = '8372738_env_7639283'
        source_code = source_code.replace('_ENV', env_sentinel)
        source_code = source_code.lower()
        source_code = source_code.replace(env_sentinel, '_ENV')
        return source_code

    @classmethod
    def createClarifiedCartContents(cls, parsedContents: ParsedContents) -> str:
        githubLink = TemplateEvaluator.constructSourceCodeLink(parsedContents).lower()
        header = f'--see more on github\n--{githubLink}\n\n'
        return parsedContents.rawContents.replace(
            parsedContents.sourceCode,
            header +
            cls.sanitizeComments(parsedContents.clarifiedSourceCode)
        )

    @classmethod
    def createMinifiedCartContents(cls, parsedContents: ParsedContents) -> str:
        githubLink = TemplateEvaluator.constructExplainerCodeLink(parsedContents).lower()
        header = f'--see explanation on github\n--{githubLink}\n\n'
        return parsedContents.rawContents.replace(
            parsedContents.sourceCode,
            header +
            parsedContents.minifiedSourceCode
        )

    @classmethod
    def writeFullRom(
            cls,
            config: Config,
            cartContents: str,
            parsedContents: ParsedContents) -> bytes:
        # minifiedCartContents: str = cls.createMinifiedCartContents(parsedContents)
        # cls.writeRom(config, cartContents, parsedContents)

    # @classmethod
    # def writeRom(cls,
    #               config: Config,
    #              cartContents: str,
    #               parsedContents: ParsedContents
    #               ):
        root = (Path(__file__) / ".." / "..").resolve() / "working_tmp"
        # os.m
        # Sure why not?
        root.mkdir(exist_ok=True)
        # print('checkhere',root)
        # TODO fix this naming convention
        temporaryP8FileName = root / 'tweetMinified.p8'
        with open(temporaryP8FileName, "w") as file:
            file.write(cartContents)

        P8FileTransformerCompilationTarget.transformP8File(temporaryP8FileName, parsedContents)
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