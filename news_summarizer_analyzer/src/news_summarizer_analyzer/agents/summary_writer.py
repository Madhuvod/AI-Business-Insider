from crewai_tools import BaseTool
from typing import Dict
from pydantic import Field
from openai import OpenAI

class SummaryWriterTool(BaseTool):
    name: str = "Summary Writer"
    description: str = "Generates concise summaries of news articles."
    api_key: str = Field(..., description="API key for OpenAI")

    def _run(self, article: Dict[str, str]) -> str:
        """
        Generate a summary for the given article using OpenAI API.
        
        :param article: A dictionary containing article details.
        :return: A summary of the article.
        """
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Summarize the following article: {article['snippet']}"}
            ],
            max_tokens=150
        )
        summary = response.choices[0].message.content.strip()
        return summary

    async def _arun(self, article: Dict[str, str]) -> str:
        return self._run(article)
