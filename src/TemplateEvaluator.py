from src.ParsedContents import Metadata, ControlEnum, ParsedContents, CartType

# from File
from src.FileRegistry import TemplateFileEnum
from pathlib import Path


class TemplateEvaluator:
    # @classmethod
    # def evaluateTemplateToString(
    #     cls, parsedContents: ParsedContents, template: TemplateFileEnum
    # ) -> str:
    #     strTemplate: str = template.readText()
    #     return cls.evaluateStringTemplateToString(
    #         parsedContents=parsedContents, strTemplate=strTemplate
    #     )

    @classmethod
    def chooseTemplate(cls, parsedContents: ParsedContents) -> TemplateFileEnum:
        return {
            CartType.GAME: TemplateFileEnum.ITCH_GAME_DESCRIPTION_MD,
            CartType.UNKNOWN: TemplateFileEnum.ITCH_GAME_DESCRIPTION_MD,
            CartType.TWEET: TemplateFileEnum.ITCH_TWEET_DESCRIPTION_MD,
        }[parsedContents.metadata.stronglyTypedCartType]

    @classmethod
    def evaluateStringTemplateToString(
        cls, parsedContents: ParsedContents, strTemplate: str
    ) -> str:
        return strTemplate.format(
            **cls.constructEvaluationDictionary(parsedContents=parsedContents)
        )

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
                    parsedContents=parsedContents, strTemplate=template.readText()
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
            "hints": parsedContents.metadata.hints,
            "jam_info": cls.constructJamInfo(metadata=parsedContents.metadata),
            "about_extra": parsedContents.metadata.about_extra,
            "source_code_link": cls.constructSourceCodeLink(
                parsedContents=parsedContents
            ),
            "char_count": parsedContents.sourceCodeP8sciiCharCount,
            "source_code": parsedContents.sourceCode
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
        return "\n".join(
            f"* {cls.controlToDescription(control.key)} - {control.desc}"
            for control in metadata.controls
        )

    @classmethod
    def controlToDescription(cls, controlEnum: ControlEnum):
        return {ControlEnum.ARROW_KEYS: "Arrow Keys", ControlEnum.X: "X"}[controlEnum]

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
            isFirst = False

        return ret

    @classmethod
    def constructSourceCodeLink(cls, parsedContents: ParsedContents) -> str:
        baseUrl: str = parsedContents.config.sourceControlRootUrl
        if not baseUrl.endswith("/"):
            baseUrl += "/"

        return baseUrl + parsedContents.metadata.correctedGameSlug
