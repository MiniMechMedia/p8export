from src.ParsedContents import Metadata, ControlEnum, ParsedContents, CartType

# from File
from src.FileRegistry import TemplateFileEnum
from pathlib import Path
from markdown import markdown
from enum import Enum, auto


class RenderType(Enum):
    # just a basic string replacement
    BASIC = auto()
    HTML = auto()


class TemplateEvaluator:
    @classmethod
    def getRenderTypeFromTemplate(cls, template: TemplateFileEnum) -> RenderType:
        if template.value.endswith(".html.md"):
            return RenderType.HTML
        return RenderType.BASIC

    @classmethod
    def evaluateTemplateToString(
        cls, parsedContents: ParsedContents, template: TemplateFileEnum
    ) -> str:
        strTemplate: str = template.readText()
        return cls.evaluateStringTemplateToString(
            parsedContents=parsedContents,
            strTemplate=strTemplate,
            renderType=cls.getRenderTypeFromTemplate(template=template),
        )

    # @classmethod
    # def chooseTemplate(cls, cartType: CartType) -> TemplateFileEnum:
    #     return {
    #         CartType.GAME: TemplateFileEnum.ITCH_GAME_DESCRIPTION_MD,
    #         CartType.UNKNOWN: TemplateFileEnum.ITCH_GAME_DESCRIPTION_MD,
    #         CartType.TWEET: TemplateFileEnum.ITCH_TWEET_DESCRIPTION_MD,
    #     }[parsedContents.metadata.stronglyTypedCartType]

    @classmethod
    def evaluateStringTemplateToString(
        cls, parsedContents: ParsedContents, strTemplate: str, renderType: RenderType
    ) -> str:
        ret: str = strTemplate.format(
            **cls.constructEvaluationDictionary(parsedContents=parsedContents)
        )

        if renderType == RenderType.HTML:
            ret = markdown(ret)

        return ret

    @classmethod
    def evaluateTemplateToFile(
        cls,
        parsedContents: ParsedContents,
        template: TemplateFileEnum,
        outputFile: Path,
    ) -> None:

        with open(outputFile, "w") as file:
            file.write(
                cls.evaluateStringTemplateToString(
                    parsedContents=parsedContents,
                    strTemplate=template.readText(),
                    renderType=cls.getRenderTypeFromTemplate(template=template),
                )
            )

    @classmethod
    def constructEvaluationDictionary(
        cls, parsedContents: ParsedContents
    ) -> dict[str, str]:
        return {
            "description": parsedContents.metadata.description,
            "controls": cls.constructControlDescription(
                metadata=parsedContents.metadata
            ),
            "hints": '' if not parsedContents.metadata.hints else f'## Hints\n{parsedContents.metadata.hints}',
            "jam_info": cls.constructJamInfo(metadata=parsedContents.metadata),
            "about_extra": parsedContents.metadata.about_extra,
            "source_code_link": cls.constructSourceCodeLink(
                parsedContents=parsedContents
            ),
            "char_count": parsedContents.sourceCodeP8sciiCharCount,
            "source_code": parsedContents.sourceCode,
            "game_name": parsedContents.metadata.game_name,
            "itch_link": cls.constructItchLink(parsedContents=parsedContents),
            "alt_text": parsedContents.metadata.img_alt,
            "hints": parsedContents.metadata.hints,
            "tag_line": parsedContents.metadata.tagline,
            "cover_path": parsedContents.coverPath,
            "cover_path_abs": parsedContents.coverPathAbs,
            "folder_relative_path": parsedContents.folderRelativePath
            # 'itch_link': cls.constructItchLink(parsedContents=parsedContents)
        }

    # @classmethod
    # def constructDescription(cls, parsedContents: ParsedContents):
    #     template: str = parsedContents.metadata.description
    #     template = template.replace(
    #         "$charCount$", str(parsedContents.sourceCodeP8sciiCharCount)
    #     )
    #     template = template.replace(
    #         "$sourceCode$", f"<pre><code>{parsedContents.sourceCode}</code></pre>"
    #     )
    #     return template

    # TODO should maybe provide target like XML, HTML, MD, TXT
    @classmethod
    def constructControlDescription(cls, metadata: Metadata) -> str:
        ret: str = ''
        for control in metadata.controls:
            controlInputs: str = ' / '.join(cls.controlToDescription(inp) for inp in control.inputs)
            ret += f'* {controlInputs} - {control.desc}\n'

        return ret.removesuffix('\n')

    @classmethod
    def controlToDescription(cls, controlEnum: ControlEnum):
        return {
            ControlEnum.ARROW_KEYS: "Arrow Keys",
            ControlEnum.X: "X",
            ControlEnum.Z: 'Z',
            ControlEnum.MOUSE: 'Mouse',
            ControlEnum.LEFT_CLICK: 'Left Click',
            ControlEnum.RIGHT_CLICK: 'Right Click',
        }[controlEnum]

    @classmethod
    def constructJamInfo(cls, metadata: Metadata) -> str:
        ret: str = ""
        jam: Metadata.JamInfo
        isFirst = True
        for jam in metadata.jam_info:
            if not isFirst:
                ret += "\n"
            verb = "Created for" if isFirst else "Also submitted to"
            jamName = (
                jam.jam_name
                if jam.jam_number is None
                else f"{jam.jam_name} {jam.jam_number}"
            )
            ret += f"{verb} [{jamName}]({jam.correctedJamUrl})  \n"

            ret += f"Theme: {jam.jam_theme}  \n"
            if jam.jam_name == "TriJam":
                ret += f"Development Time: {metadata.develop_time}  \n"
            elif jam.jam_name == 'MiniJam':
                ret += f'Limitation: {jam.minijam_limitation}  \n'
            isFirst = False

        return ret

    @classmethod
    def constructSourceCodeLink(cls, parsedContents: ParsedContents) -> str:
        baseUrl: str = parsedContents.config.sourceControlRootUrl
        if not baseUrl.endswith("/"):
            baseUrl += "/"

        return baseUrl + parsedContents.metadata.correctedGameSlug

    @classmethod
    def constructItchLink(cls, parsedContents):
        return f"https://{parsedContents.config.itchAuthor}.itch.io/{parsedContents.metadata.correctedGameSlug}"
