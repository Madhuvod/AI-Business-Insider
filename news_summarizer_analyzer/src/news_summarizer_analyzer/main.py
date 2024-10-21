#!/usr/bin/env python
import os
from dotenv import load_dotenv
from crew import NewsSummarizerAnalyzerCrew

# Load environment variables from .env file
load_dotenv()

def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    topic = "Artificial Intelligence"  # You can change this or get it from command line arguments
    crew = NewsSummarizerAnalyzerCrew()
    result = crew.kickoff(topic)
    print(result)

if __name__ == "__main__":
    main()
