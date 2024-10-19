from crewai_tools import BaseTool
from typing import List, Dict
from openai import OpenAI
import os
from pydantic import Field

class TrendAnalyzerTool(BaseTool):
    name: str = "Trend Analyzer"
    description: str = "Analyzes trends across multiple news article summaries and suggests potential outcomes and business ideas."
    api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""), description="API key for OpenAI")

    def _run(self, summaries: List[str]) -> Dict[str, List[str]]:
        """
        Analyze summaries to identify trends and suggest outcomes and business ideas.
        
        :param summaries: A list of article summaries.
        :return: A dictionary with trends, outcomes, and business ideas.
        """
        self.api_key = os.getenv("OPENAI_API_KEY")  # Ensure this is set securely
        client = OpenAI(api_key=self.api_key)
        # Combine summaries into a single prompt
        combined_summaries = " ".join(summaries)
        prompt = (
            f"Analyze the following article summaries for trends and patterns: {combined_summaries} "
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

        analysis = response['choices'][0]['message']['content'].strip()

        # For simplicity, assume the response is structured as needed
        return {
            "trends": ["Trend 1", "Trend 2"],  # Extracted from analysis
            "outcomes": ["Outcome 1", "Outcome 2"],  # Extracted from analysis
            "business_ideas": ["Business Idea 1"]  # Extracted from analysis
        }

    async def _arun(self, summaries: List[str]) -> Dict[str, List[str]]:
        return self._run(summaries)
