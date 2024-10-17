from crewai_tools import BaseTool
from typing import Dict
from pydantic import Field

class SummaryWriterTool(BaseTool):
    name: str = "Summary Writer"
    description: str = "Generates concise summaries of news articles."

    def _run(self, article: Dict[str, str]) -> str:
        # Implement summary writing logic here
        # This is a placeholder implementation
        return f"Summary of article: {article['title']}"

    async def _arun(self, article: Dict[str, str]) -> str:
        return self._run(article)
