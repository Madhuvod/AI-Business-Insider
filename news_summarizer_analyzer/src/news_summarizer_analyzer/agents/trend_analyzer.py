from crewai_tools import BaseTool
from typing import Dict, List, Union
from openai import OpenAI
import os
from pydantic import Field, BaseModel

class TrendAnalyzerTool(BaseTool):
    name: str = "Trend Analyzer"
    description: str = "Analyzes trends across multiple news article summaries and suggests potential outcomes and business ideas."
    api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""), description="API key for OpenAI")

    def _run(self, input_data: Union[str, Dict]) -> Dict[str, list]:
        """
        Analyze summaries to identify trends and suggest outcomes and business ideas.
        
        :param input_data: A string or dictionary containing the summary to analyze.
        :return: A dictionary with trends, outcomes, and business ideas.
        """
        self.api_key = os.getenv("OPENAI_API_KEY")  # Ensure this is set securely
        client = OpenAI(api_key=self.api_key)

        if isinstance(input_data, dict):
            summary_data = input_data.get('summary', input_data)
        else:
            summary_data = input_data

        prompt = (
            f"Analyze the following news summary for trends and patterns:\n\n"
            f"{summary_data}\n\n"
            "Based on these trends, suggest potential outcomes and a business idea."
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful business consultant that gives advice on market trends and business ideas."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )

        analysis = response.choices[0].message.content.strip()

        # Parse the analysis to extract trends, outcomes, and business ideas
        lines = analysis.split('\n')
        trends = [line.strip() for line in lines if line.startswith('Trend:')]
        outcomes = [line.strip() for line in lines if line.startswith('Outcome:')]
        business_ideas = [line.strip() for line in lines if line.startswith('Business Idea:')]

        return {
            "trends": trends,
            "outcomes": outcomes,
            "business_ideas": business_ideas
        }

    async def _arun(self, input_data: Union[str, Dict]) -> Dict[str, list]:
        return self._run(input_data)
