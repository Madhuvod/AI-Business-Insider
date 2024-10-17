from crewai_tools import BaseTool
from typing import Dict, List, Any
from pydantic import Field
import requests

class FactCheckerTool(BaseTool):
    name: str = "Fact Checker"
    description: str = "Verifies the factual accuracy of news articles using Google Fact Check API."
    api_key: str = Field(..., description="API key for the Google Fact Check API")
    base_url: str = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

    def _run(self, article: Dict[str, str]) -> Dict[str, Any]:
        """Checks the factual accuracy of a news article"""
        query = f"{article['title']} {article['snippet']}"
        params = {
            'key': self.api_key,
            'query': query
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            fact_checks = response.json().get('claims', [])
            
            if not fact_checks:
                return {"is_accurate": "Unknown", "confidence": 0, "fact_checks": []}
            
            # Process fact check results
            processed_checks = []
            for check in fact_checks:
                processed_checks.append({
                    "claim": check.get('text', ''),
                    "rating": check.get('claimReview', [{}])[0].get('textualRating', ''),
                    "url": check.get('claimReview', [{}])[0].get('url', '')
                })
            
            # Determine overall accuracy based on fact checks
            # Extract lowercase ratings from processed checks
            ratings: List[str] = [check['rating'].lower() for check in processed_checks]
            
            # Determine if the article is accurate based on all ratings
            # An article is considered accurate if all ratings contain 'true' or 'accurate'
            is_accurate: str = "True" if all('true' in r or 'accurate' in r for r in ratings) else "False"
            
            # Calculate confidence as the proportion of ratings that are true or accurate
            # If there are no ratings, confidence is 0
            confidence: float = len([r for r in ratings if 'true' in r or 'accurate' in r]) / len(ratings) if ratings else 0

            return {
                "is_accurate": is_accurate,
                "confidence": confidence,
                "fact_checks": processed_checks
            }

        except requests.RequestException as e:
            raise Exception(f"Error checking facts: {str(e)}")

    async def _arun(self, article: Dict[str, str]) -> Dict[str, Any]:
        """Async implementation of the tool"""
        return self._run(article)
