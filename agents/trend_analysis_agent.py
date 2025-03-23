"""
Trend Analysis Agent for the YouTube Content Monetization Framework.

This agent analyzes technology trends, market opportunities, and content popularity
to provide insights that can inform monetization strategies.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from crewai import Agent, Task, Crew
from crewai.tasks import TaskOutput

# Import trend analyzer from the monetization module
from monetization.trend_analyzer import TrendAnalyzer

class TrendAnalysisAgent:
    """
    Agent responsible for analyzing technology trends, market opportunities,
    and content popularity to inform monetization strategies.
    """

    def __init__(self, openai_api_key: Optional[str] = None, output_dir: str = "output"):
        """
        Initialize the TrendAnalysisAgent.
        
        Args:
            openai_api_key (str, optional): OpenAI API key for CrewAI agents
            output_dir (str): Directory to save output files
        """
        self.openai_api_key = openai_api_key
        self.output_dir = output_dir
        self.trend_analyzer = TrendAnalyzer()
        self.logger = logging.getLogger(__name__)
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

    def create_agent(self) -> Agent:
        """
        Create a CrewAI agent for trend analysis.
        
        Returns:
            Agent: CrewAI agent for trend analysis
        """
        return Agent(
            role="Technology Trend Analyst",
            goal="Analyze technology trends and market opportunities to inform monetization strategies",
            backstory="""You are an expert in technology trends and market analysis.
            Your job is to identify emerging technologies, analyze market opportunities,
            and provide insights that can inform monetization strategies.""",
            verbose=True,
            allow_delegation=False,
            tools=[
                self.analyze_technology_trends,
                self.analyze_content_popularity,
                self.analyze_market_opportunities,
                self.generate_trend_report
            ]
        )

    def analyze_technology_trends(self, technologies: List[str]) -> Dict[str, Any]:
        """
        Analyze technology trends for the given technologies.
        
        Args:
            technologies (List[str]): List of technologies to analyze
            
        Returns:
            Dict[str, Any]: Analysis of technology trends
        """
        self.logger.info(f"Analyzing technology trends for: {', '.join(technologies)}")
        
        try:
            # Use the TrendAnalyzer to analyze technology trends
            trends = self.trend_analyzer.analyze_technology_trends(technologies)
            
            # Save the trends to a file
            trends_path = os.path.join(self.output_dir, "technology_trends.json")
            with open(trends_path, "w", encoding="utf-8") as f:
                json.dump(trends, f, indent=2)
            
            self.logger.info(f"Technology trend analysis saved to {trends_path}")
            
            return trends
        
        except Exception as e:
            self.logger.error(f"Error analyzing technology trends: {str(e)}")
            return {"error": str(e)}

    def analyze_content_popularity(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze content popularity based on video data.
        
        Args:
            video_data (Dict[str, Any]): Video data including metadata and engagement metrics
            
        Returns:
            Dict[str, Any]: Analysis of content popularity
        """
        self.logger.info("Analyzing content popularity")
        
        try:
            # Extract relevant metrics from video data
            metadata = video_data.get("metadata", {})
            view_count = metadata.get("view_count", 0)
            like_count = metadata.get("like_count", 0)
            comment_count = metadata.get("comment_count", 0)
            
            # Calculate engagement rate
            engagement_rate = 0
            if view_count > 0:
                engagement_rate = ((like_count + comment_count) / view_count) * 100
            
            # Determine popularity level
            popularity_level = "low"
            if engagement_rate > 5:
                popularity_level = "high"
            elif engagement_rate > 2:
                popularity_level = "medium"
            
            # Create popularity analysis
            popularity_analysis = {
                "metrics": {
                    "view_count": view_count,
                    "like_count": like_count,
                    "comment_count": comment_count,
                    "engagement_rate": round(engagement_rate, 2)
                },
                "popularity_level": popularity_level,
                "insights": []
            }
            
            # Add insights based on popularity level
            if popularity_level == "high":
                popularity_analysis["insights"].append(
                    "High engagement indicates strong audience interest in this content."
                )
                popularity_analysis["insights"].append(
                    "Consider creating more content on this topic or related technologies."
                )
            elif popularity_level == "medium":
                popularity_analysis["insights"].append(
                    "Moderate engagement suggests potential interest in this content."
                )
                popularity_analysis["insights"].append(
                    "Consider optimizing content to increase engagement."
                )
            else:
                popularity_analysis["insights"].append(
                    "Low engagement may indicate limited audience interest in this content."
                )
                popularity_analysis["insights"].append(
                    "Consider focusing on more popular topics or improving content quality."
                )
            
            # Save the popularity analysis to a file
            popularity_path = os.path.join(self.output_dir, "content_popularity.json")
            with open(popularity_path, "w", encoding="utf-8") as f:
                json.dump(popularity_analysis, f, indent=2)
            
            self.logger.info(f"Content popularity analysis saved to {popularity_path}")
            
            return popularity_analysis
        
        except Exception as e:
            self.logger.error(f"Error analyzing content popularity: {str(e)}")
            return {"error": str(e)}

    def analyze_market_opportunities(self, 
                                    technologies: List[str], 
                                    repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze market opportunities based on technologies and repository data.
        
        Args:
            technologies (List[str]): List of technologies to analyze
            repo_data (Dict[str, Any]): Repository data
            
        Returns:
            Dict[str, Any]: Analysis of market opportunities
        """
        self.logger.info("Analyzing market opportunities")
        
        try:
            # Extract repository information
            repo_info = repo_data.get("repository", {})
            repo_name = repo_info.get("repo", "")
            repo_url = repo_info.get("url", "")
            
            # Get repository structure and technologies
            structure = repo_data.get("structure", {})
            tech_info = repo_data.get("technologies", {})
            
            # Use the TrendAnalyzer to analyze repository market fit
            market_fit = self.trend_analyzer.analyze_repository_market_fit({
                "repo": repo_name,
                "url": repo_url,
                "name": repo_name.split("/")[-1] if "/" in repo_name else repo_name,
                "application_type": "web",  # Default to web, could be more sophisticated
                "languages": tech_info.get("languages", {}),
                "github_info": {
                    "stargazers_count": 0,
                    "forks_count": 0,
                    "subscribers_count": 0,
                    "description": ""
                }
            })
            
            # Enhance market fit with additional opportunities
            market_opportunities = {
                "repository_market_fit": market_fit,
                "emerging_opportunities": [],
                "competitive_landscape": {
                    "saturation_level": "unknown",
                    "key_competitors": [],
                    "differentiators": []
                },
                "target_audience": {
                    "segments": [],
                    "needs": [],
                    "pain_points": []
                }
            }
            
            # Analyze each technology for opportunities
            for tech in technologies:
                # Get technology trend data
                tech_trend = self.trend_analyzer.get_technology_trend(tech)
                
                # Add emerging opportunities based on technology trends
                if tech_trend.get("growth_rate", "unknown") == "high":
                    market_opportunities["emerging_opportunities"].append({
                        "technology": tech,
                        "opportunity": f"Rapidly growing demand for {tech} solutions",
                        "recommendation": f"Prioritize {tech} features in monetization strategy"
                    })
                elif tech_trend.get("growth_rate", "unknown") == "medium":
                    market_opportunities["emerging_opportunities"].append({
                        "technology": tech,
                        "opportunity": f"Steady growth in {tech} adoption",
                        "recommendation": f"Include {tech} as part of broader monetization strategy"
                    })
            
            # Save the market opportunities to a file
            opportunities_path = os.path.join(self.output_dir, "market_opportunities.json")
            with open(opportunities_path, "w", encoding="utf-8") as f:
                json.dump(market_opportunities, f, indent=2)
            
            self.logger.info(f"Market opportunities analysis saved to {opportunities_path}")
            
            return market_opportunities
        
        except Exception as e:
            self.logger.error(f"Error analyzing market opportunities: {str(e)}")
            return {"error": str(e)}

    def generate_trend_report(self, 
                             tech_trends: Dict[str, Any], 
                             popularity_analysis: Dict[str, Any],
                             market_opportunities: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive trend report based on all analyses.
        
        Args:
            tech_trends (Dict[str, Any]): Technology trends analysis
            popularity_analysis (Dict[str, Any]): Content popularity analysis
            market_opportunities (Dict[str, Any]): Market opportunities analysis
            
        Returns:
            Dict[str, Any]: Comprehensive trend report
        """
        self.logger.info("Generating comprehensive trend report")
        
        try:
            # Extract key insights from each analysis
            top_tech = tech_trends.get("top_technology", {})
            popularity_level = popularity_analysis.get("popularity_level", "unknown")
            market_fit = market_opportunities.get("repository_market_fit", {})
            
            # Create trend report
            trend_report = {
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "top_technology": top_tech.get("name", "unknown"),
                    "content_popularity": popularity_level,
                    "market_fit": market_fit.get("monetization_potential", "unknown")
                },
                "key_insights": [],
                "recommendations": []
            }
            
            # Add key insights based on analyses
            if top_tech:
                trend_report["key_insights"].append(
                    f"{top_tech.get('name', 'unknown')} has the highest monetization potential "
                    f"with an overall score of {top_tech.get('overall_score', 0)}"
                )
            
            if popularity_level != "unknown":
                trend_report["key_insights"].append(
                    f"Content has {popularity_level} popularity with an engagement rate of "
                    f"{popularity_analysis.get('metrics', {}).get('engagement_rate', 0)}%"
                )
            
            if market_fit:
                trend_report["key_insights"].append(
                    f"Repository has {market_fit.get('monetization_potential', 'unknown')} "
                    f"monetization potential as a {market_fit.get('application_type', 'unknown')} application"
                )
            
            # Add recommendations based on insights
            for opportunity in market_opportunities.get("emerging_opportunities", []):
                trend_report["recommendations"].append(opportunity.get("recommendation", ""))
            
            for recommendation in market_fit.get("recommendations", []):
                trend_report["recommendations"].append(recommendation)
            
            # Add recommendations based on content popularity
            if popularity_level == "high":
                trend_report["recommendations"].append(
                    "Leverage high content popularity to maximize monetization potential"
                )
            elif popularity_level == "medium":
                trend_report["recommendations"].append(
                    "Improve content to increase popularity and monetization potential"
                )
            else:
                trend_report["recommendations"].append(
                    "Consider focusing on more popular topics to increase monetization potential"
                )
            
            # Generate markdown report
            markdown_report = f"""# Trend Analysis Report

## Summary

- **Top Technology**: {trend_report['summary']['top_technology']}
- **Content Popularity**: {trend_report['summary']['content_popularity'].capitalize()}
- **Market Fit**: {trend_report['summary']['market_fit'].capitalize()}

## Key Insights

{chr(10).join(['- ' + insight for insight in trend_report['key_insights']])}

## Recommendations

{chr(10).join(['- ' + recommendation for recommendation in trend_report['recommendations']])}

## Technology Trends

| Technology | Overall Score | Monetization Potential | Growth Rate |
|------------|---------------|------------------------|-------------|
"""
            
            # Add technology trends to markdown report
            for tech_name, tech_data in tech_trends.get("technologies", {}).items():
                markdown_report += f"| {tech_name} | {tech_data.get('overall_score', 0)} | {tech_data.get('monetization_potential', 'unknown')} | {tech_data.get('growth_rate', 'unknown')} |\n"
            
            # Add market opportunities to markdown report
            markdown_report += f"""
## Market Opportunities

### Emerging Opportunities

{chr(10).join(['- **' + opportunity.get('technology', '') + '**: ' + opportunity.get('opportunity', '') for opportunity in market_opportunities.get('emerging_opportunities', [])])}

### Repository Market Fit

- **Application Type**: {market_fit.get('application_type', 'unknown')}
- **Monetization Potential**: {market_fit.get('monetization_potential', 'unknown').capitalize()}
- **Market Gap**: {market_fit.get('market_gap', 'unknown').capitalize()}

## Content Popularity

- **View Count**: {popularity_analysis.get('metrics', {}).get('view_count', 0)}
- **Like Count**: {popularity_analysis.get('metrics', {}).get('like_count', 0)}
- **Comment Count**: {popularity_analysis.get('metrics', {}).get('comment_count', 0)}
- **Engagement Rate**: {popularity_analysis.get('metrics', {}).get('engagement_rate', 0)}%
- **Popularity Level**: {popularity_level.capitalize()}

"""
            
            # Save the trend report to files
            report_path = os.path.join(self.output_dir, "trend_report.json")
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(trend_report, f, indent=2)
            
            markdown_path = os.path.join(self.output_dir, "trend_report.md")
            with open(markdown_path, "w", encoding="utf-8") as f:
                f.write(markdown_report)
            
            self.logger.info(f"Trend report saved to {report_path} and {markdown_path}")
            
            return {
                "trend_report": trend_report,
                "markdown_report": markdown_path
            }
        
        except Exception as e:
            self.logger.error(f"Error generating trend report: {str(e)}")
            return {"error": str(e)}

    def analyze_trends(self, 
                      video_data: Dict[str, Any], 
                      repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the complete trend analysis workflow.
        
        Args:
            video_data (Dict[str, Any]): Video data including metadata and content analysis
            repo_data (Dict[str, Any]): Repository data
            
        Returns:
            Dict[str, Any]: Results of the trend analysis
        """
        self.logger.info("Starting trend analysis workflow")
        
        try:
            # Extract technologies from video data
            technologies = video_data.get("content_analysis", {}).get("technologies", [])
            
            # Create CrewAI agent and tasks
            agent = self.create_agent()
            
            # Analyze technology trends
            tech_trends = self.analyze_technology_trends(technologies)
            
            # Analyze content popularity
            popularity_analysis = self.analyze_content_popularity(video_data)
            
            # Analyze market opportunities
            market_opportunities = self.analyze_market_opportunities(technologies, repo_data)
            
            # Generate trend report
            trend_report = self.generate_trend_report(
                tech_trends, popularity_analysis, market_opportunities
            )
            
            # Combine all results
            results = {
                "technology_trends": tech_trends,
                "content_popularity": popularity_analysis,
                "market_opportunities": market_opportunities,
                "trend_report": trend_report
            }
            
            # Save the combined results
            results_path = os.path.join(self.output_dir, "trend_analysis_results.json")
            with open(results_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
            
            self.logger.info(f"Trend analysis workflow completed. Results saved to {results_path}")
            
            return results
        
        except Exception as e:
            self.logger.error(f"Error in trend analysis workflow: {str(e)}")
            return {"error": str(e)}
