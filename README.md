## News Summarizer and Analyst - CrewAI 


This project is a web-based tool that helps users research a news topic, fact-check information, summarize key findings, and analyze trends. It leverages multiple AI agents to collect, verify, and analyze news, enabling users to extract insights and identify key opportunities across various news articles. The application uses [CrewAI](https://crewai.com/) to orchestrate these tasks and provide an interactive experience.

## Features

- **User Prompt**: Users can input a topic of interest for research.
- **News Collection**: The system gathers recent news articles based on the topic provided.
- **Fact Verification**: Key facts from collected news articles are verified using trusted tools.
- **Summary Generation**: Concise summaries of verified information are generated.
- **Trend Analysis**: The system identifies trends and patterns across the analyzed news stories, providing deeper insights.

## Architecture

This tool comprises four key agents:

### 1. News Collector
- **Task**: Collects recent news articles on the given topic.
- **Tools**: 
  - Web Scrapers
  - News APIs (like [NewsAPI](https://newsapi.org/))
  
### 2. Fact Checker
- **Task**: Verifies key facts from collected articles.
- **Tools**: 
  - Google Fact-Check Tools API
  
### 3. Summary Writer
- **Task**: Produces concise summaries of the verified information.
- **Tools**: 
  - Hugging Face's [BART](https://huggingface.co/facebook/bart-large-cnn) / GPT 4o (now)

### 4. Trend Analyzer
- **Task**: Analyzes trends and patterns across collected and summarized news stories.
- **Tools**: 
  - OpenAI's GPT
  - Periscope for Sentiment Analysis

## Project Flow

1. **Step 1**: User enters a topic in the input field on the frontend.
2. **Step 2**: The system fetches recent news articles related to the topic using the News Collector agent.
3. **Step 3**: The Fact Checker agent verifies the accuracy of key facts from the news articles.
4. **Step 4**: The Summary Writer agent generates a concise summary of the news.
5. **Step 5**: The Trend Analyzer agent examines the news for trends and patterns.
6. **Step 6**: Results are presented to the user, showing collected news, verified facts, a summary, and trend analysis.

## Technologies Used

- **Frontend**: Streamlit (underdevelopment)
- **Backend**: 
  - Python (with FastAPI for the API backend)
- **AI/ML Tools**: 
  - CrewAI for orchestrating AI agents
  - Hugging Face for NLP-based models
  - Google Fact-Check Tools API
  - OpenAI for trend analysis
- **Web Scraping**: Custom web scrapers and external APIs (News API)

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/news_summarizer_analyzer.git
   cd news_summarizer_analyzer
   ```

2. Set up your environment variables:
   ```bash
   NEWS_API_KEY=your_news_api_key
   GOOGLE_FACT_CHECK_KEY=your_google_fact_check_key
   OPENAI_API_KEY=your_openai_api_key
   ```

3. Run the application:
   ```
   python src/news_summarizer_analyzer/main.py
   ```
**TODO**: Thinking of using A voice agent for this tooo
![image](IMG_3530.heic)
