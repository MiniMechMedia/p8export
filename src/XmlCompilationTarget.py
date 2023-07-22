from xml.sax.saxutils import escape
from src.ParsedContents import Metadata
from src.CompilationTarget import CompilationTarget
from pathlib import Path
from src.TemplateEvaluator import TemplateEvaluator


class XmlCompilationTarget(CompilationTarget):
    @classmethod
    def compileToXml(cls, xmlDestination: Path, metadata: Metadata):
        controlDesc: str = TemplateEvaluator.constructControlDescription(metadata)

        with open(xmlDestination, "w") as file:
            file.write(
                f"""
                <game>
                    <path>./{metadata.correctedGameSlug}.p8.png</path>
                    <name>{metadata.game_name}</name>
                    <image>./{metadata.correctedGameSlug}.p8.png</image>
                    <players>{metadata.numberPlayersDesc}</players>
                    <desc>
                        Description: {escape(metadata.tagline)}
                        Controls: {escape(controlDesc)}
                    </desc>
                </game>
            """
            )
