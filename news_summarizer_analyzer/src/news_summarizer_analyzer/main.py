#!/usr/bin/env python
import os
from dotenv import load_dotenv
from crew import NewsSummarizerAnalyzerCrew

# Load environment variables from .env file
load_dotenv()

def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    # Prompt the user for the topic
    topic = input("Please enter the topic you want to research: ")

    crew = NewsSummarizerAnalyzerCrew()
    result = crew.kickoff(topic)
    print(result)

if __name__ == "__main__":
    main()
