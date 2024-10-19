from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
import sys

# parent_dir = os.path.dirname((os.path.abspath(__file__)))
# sys.path.insert(0, parent_dir)


from news_summarizer_analyzer.agents.news_collector import NewsAPITool
from news_summarizer_analyzer.agents.fact_checker import FactCheckerTool
from news_summarizer_analyzer.agents.summary_writer import SummaryWriterTool
from news_summarizer_analyzer.agents.trend_analyzer import TrendAnalyzerTool

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool

@CrewBase
class NewsSummarizerAnalyzerCrew():
	"""NewsSummarizerAnalyzer crew"""

	@agent
	def news_collector(self) -> Agent:
		return Agent(
			config=self.agents_config['news_collector'],
			tools=[NewsAPITool()],
			verbose=True
		)

	@agent
	def fact_checker(self) -> Agent:
		return Agent(
			config=self.agents_config['fact_checker'],
			tools=[FactCheckerTool()],
			verbose=True
		)

	@task
	def summary_writer(self) -> Task:
		return Task(
			config=self.tasks_config['summary_writer'],
			tools=[SummaryWriterTool()],
		)

	@task
	def trend_analyzer(self) -> Task:
		return Task(
			config=self.tasks_config['trend_analyzer'],
			tools=[TrendAnalyzerTool()],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the NewsSummarizerAnalyzer crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
