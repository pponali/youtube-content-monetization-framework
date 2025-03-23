"""
Agent orchestrator using CrewAI to coordinate the YouTube content monetization process.
"""
import os
from typing import Dict, List, Any, Optional
from crewai import Agent, Task, Crew, Process

class AgentOrchestrator:
    """
    Orchestrates the AI agents that handle different aspects of the YouTube content monetization process.
    Uses CrewAI to manage agent interactions and workflows.
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the AgentOrchestrator.
        
        Args:
            openai_api_key: OpenAI API key for agent operations. If None, loads from environment.
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass to constructor.")
        
        # Initialize agents
        self.video_analysis_agent = self._create_video_analysis_agent()
        self.repo_detection_agent = self._create_repo_detection_agent()
        self.app_building_agent = self._create_app_building_agent()
        self.trend_analysis_agent = self._create_trend_analysis_agent()
        self.monetization_agent = self._create_monetization_agent()
    
    def _create_video_analysis_agent(self) -> Agent:
        """Create an agent specialized in analyzing YouTube video content."""
        return Agent(
            role="Video Content Analyzer",
            goal="Extract comprehensive information from YouTube videos including technical concepts, code snippets, and key insights",
            backstory="You are an expert in video content analysis with deep knowledge of programming and technical topics. Your specialty is understanding complex technical videos and extracting structured information.",
            verbose=True,
            allow_delegation=True
        )
    
    def _create_repo_detection_agent(self) -> Agent:
        """Create an agent specialized in detecting and analyzing GitHub repositories."""
        return Agent(
            role="Repository Detective",
            goal="Identify, analyze, and extract valuable information from GitHub repositories mentioned in videos",
            backstory="You are a skilled software developer with expertise in analyzing codebases across various technologies. You can quickly understand repository structures and identify the technologies used.",
            verbose=True,
            allow_delegation=True
        )
    
    def _create_app_building_agent(self) -> Agent:
        """Create an agent specialized in building applications from repositories."""
        return Agent(
            role="Application Builder",
            goal="Build functional applications from GitHub repositories by understanding their structure and requirements",
            backstory="You are a full-stack developer with experience in multiple programming languages and frameworks. You excel at setting up development environments and getting applications running quickly.",
            verbose=True,
            allow_delegation=True
        )
    
    def _create_trend_analysis_agent(self) -> Agent:
        """Create an agent specialized in analyzing technology trends and market opportunities."""
        return Agent(
            role="Technology Trend Analyst",
            goal="Analyze technology trends, market opportunities, and content popularity to inform monetization strategies",
            backstory="You are an expert in technology trends and market analysis. You can identify emerging technologies, analyze market opportunities, and provide insights that can inform monetization strategies.",
            verbose=True,
            allow_delegation=True
        )
    
    def _create_monetization_agent(self) -> Agent:
        """Create an agent specialized in monetization strategies."""
        return Agent(
            role="Monetization Strategist",
            goal="Develop ethical and legal monetization strategies for technical content and applications",
            backstory="You are a business strategist with deep knowledge of digital monetization models. You understand how to create value from technical content and applications while respecting intellectual property rights.",
            verbose=True,
            allow_delegation=True
        )
    
    def create_video_analysis_task(self, video_id: str) -> Task:
        """
        Create a task for analyzing a YouTube video.
        
        Args:
            video_id: YouTube video ID to analyze.
            
        Returns:
            Task for video analysis.
        """
        return Task(
            description=f"Analyze YouTube video with ID {video_id}. Extract the transcript, identify key technical concepts, detect code snippets, and identify any GitHub repositories mentioned.",
            agent=self.video_analysis_agent,
            expected_output="A comprehensive analysis of the video content including transcript, key concepts, code snippets, and repository URLs."
        )
    
    def create_repo_detection_task(self, video_analysis_result: Dict[str, Any]) -> Task:
        """
        Create a task for detecting and analyzing repositories from video analysis.
        
        Args:
            video_analysis_result: Result from the video analysis task.
            
        Returns:
            Task for repository detection and analysis.
        """
        return Task(
            description="Identify and analyze GitHub repositories mentioned in the video. Clone the repositories, analyze their structure, and determine the technologies used.",
            agent=self.repo_detection_agent,
            context=[video_analysis_result],
            expected_output="A detailed analysis of each repository including structure, technologies, and build instructions."
        )
    
    def create_app_building_task(self, repo_analysis_result: Dict[str, Any]) -> Task:
        """
        Create a task for building applications from repositories.
        
        Args:
            repo_analysis_result: Result from the repository analysis task.
            
        Returns:
            Task for application building.
        """
        return Task(
            description="Build a functional application from the analyzed repository. Set up the development environment, install dependencies, and get the application running.",
            agent=self.app_building_agent,
            context=[repo_analysis_result],
            expected_output="A working application built from the repository, with documentation on how to run it."
        )
    
    def create_trend_analysis_task(self, video_analysis_result: Dict[str, Any], repo_analysis_result: Dict[str, Any]) -> Task:
        """
        Create a task for analyzing technology trends and market opportunities.
        
        Args:
            video_analysis_result: Result from the video analysis task.
            repo_analysis_result: Result from the repository analysis task.
            
        Returns:
            Task for trend analysis.
        """
        return Task(
            description="Analyze technology trends, market opportunities, and content popularity based on the video content and repository data. Identify emerging technologies, evaluate market potential, and provide insights to inform monetization strategies.",
            agent=self.trend_analysis_agent,
            context=[video_analysis_result, repo_analysis_result],
            expected_output="A comprehensive trend analysis report with insights on technology trends, market opportunities, and content popularity."
        )
    
    def create_monetization_task(self, video_analysis_result: Dict[str, Any], repo_analysis_result: Dict[str, Any], app_building_result: Dict[str, Any], trend_analysis_result: Dict[str, Any]) -> Task:
        """
        Create a task for developing monetization strategies.
        
        Args:
            video_analysis_result: Result from the video analysis task.
            repo_analysis_result: Result from the repository analysis task.
            app_building_result: Result from the application building task.
            trend_analysis_result: Result from the trend analysis task.
            
        Returns:
            Task for monetization strategy development.
        """
        return Task(
            description="Develop ethical and legal monetization strategies for the technical content and application. Consider content repurposing, educational products, application development, consulting, and affiliate marketing. Use the trend analysis to inform your strategy recommendations.",
            agent=self.monetization_agent,
            context=[video_analysis_result, repo_analysis_result, app_building_result, trend_analysis_result],
            expected_output="A comprehensive monetization strategy with specific recommendations for generating revenue from the content and application, informed by trend analysis."
        )
    
    def run_monetization_workflow(self, video_id: str, output_dir: str = "output", verbose: bool = False) -> Dict[str, Any]:
        """
        Run the complete monetization workflow for a YouTube video.
        
        Args:
            video_id: YouTube video ID to process.
            output_dir: Directory to save output files.
            verbose: Whether to print verbose output.
            
        Returns:
            Dictionary containing the results of each task in the workflow.
        """
        # Create tasks
        video_analysis_task = self.create_video_analysis_task(video_id)
        
        # Create a crew with sequential process
        crew = Crew(
            agents=[
                self.video_analysis_agent,
                self.repo_detection_agent,
                self.app_building_agent,
                self.trend_analysis_agent,
                self.monetization_agent
            ],
            tasks=[video_analysis_task],
            verbose=2 if verbose else 0,
            process=Process.sequential
        )
        
        # Run the crew
        result = crew.kickoff()
        
        # After video analysis, create and add repository detection task
        video_analysis_result = result
        repo_detection_task = self.create_repo_detection_task(video_analysis_result)
        crew.tasks.append(repo_detection_task)
        repo_analysis_result = crew.kickoff()
        
        # After repository analysis, create and add application building task
        app_building_task = self.create_app_building_task(repo_analysis_result)
        crew.tasks.append(app_building_task)
        app_building_result = crew.kickoff()
        
        # After application building, create and add trend analysis task
        trend_analysis_task = self.create_trend_analysis_task(video_analysis_result, repo_analysis_result)
        crew.tasks.append(trend_analysis_task)
        trend_analysis_result = crew.kickoff()
        
        # After trend analysis, create and add monetization task
        monetization_task = self.create_monetization_task(
            video_analysis_result,
            repo_analysis_result,
            app_building_result,
            trend_analysis_result
        )
        crew.tasks.append(monetization_task)
        final_result = crew.kickoff()
        
        return {
            "video_analysis": video_analysis_result,
            "repo_analysis": repo_analysis_result,
            "app_building": app_building_result,
            "trend_analysis": trend_analysis_result,
            "monetization": final_result
        }
