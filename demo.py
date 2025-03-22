"""
Demo script for the YouTube Content Monetization Framework.
This demo simulates the framework's functionality without requiring external API calls.
"""
import os
import json
from datetime import datetime

# Import only the monetization components which don't have external dependencies
from monetization.strategy_generator import MonetizationStrategyGenerator
from monetization.trend_analyzer import TrendAnalyzer

def main():
    """Run a demo of the YouTube Content Monetization Framework."""
    print("=" * 80)
    print("YouTube Content Monetization Framework - Demo")
    print("=" * 80)
    
    # Create output directory
    output_dir = "demo_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create simulated video data
    print("\n[1/4] Simulating video data extraction...")
    video_data = {
        "video_id": "demo_video_123",
        "video_title": "Building a Modern Web Application with React and FastAPI",
        "transcript": {
            "text": "In this tutorial, we'll build a full-stack application using React for the frontend and FastAPI for the backend. We'll also use PostgreSQL for the database. The code is available on my GitHub repository: github.com/demo/react-fastapi-app. Let's start by setting up the project...",
            "language": "en",
            "keywords": ["React", "FastAPI", "PostgreSQL", "web development", "JavaScript", "Python", "full-stack"],
            "paragraphs": [
                "In this tutorial, we'll build a full-stack application using React for the frontend and FastAPI for the backend.",
                "We'll also use PostgreSQL for the database.",
                "The code is available on my GitHub repository: github.com/demo/react-fastapi-app.",
                "Let's start by setting up the project..."
            ]
        },
        "technologies": ["React", "FastAPI", "PostgreSQL", "JavaScript", "Python"],
        "repositories": [
            {
                "repo": "demo/react-fastapi-app",
                "url": "https://github.com/demo/react-fastapi-app",
                "name": "react-fastapi-app",
                "application_type": "web",
                "languages": {
                    "JavaScript": 60,
                    "Python": 30,
                    "HTML": 5,
                    "CSS": 5
                },
                "github_info": {
                    "stargazers_count": 250,
                    "forks_count": 45,
                    "subscribers_count": 15,
                    "description": "A modern full-stack web application template using React and FastAPI"
                }
            }
        ]
    }
    
    # Save the simulated video data
    video_data_path = os.path.join(output_dir, "video_data.json")
    with open(video_data_path, "w", encoding="utf-8") as f:
        json.dump(video_data, f, indent=2)
    
    print(f"✓ Simulated video data saved to {video_data_path}")
    
    # Generate monetization strategies
    print("\n[2/4] Generating monetization strategies...")
    strategy_generator = MonetizationStrategyGenerator()
    strategies = strategy_generator.generate_strategies(video_data)
    
    # Save the strategies
    strategies_path = os.path.join(output_dir, "monetization_strategies.json")
    with open(strategies_path, "w", encoding="utf-8") as f:
        json.dump(strategies, f, indent=2)
    
    print(f"✓ Monetization strategies saved to {strategies_path}")
    
    # Print the top recommended strategy
    if strategies.get("recommended_strategy"):
        recommended = strategies["recommended_strategy"]
        category = recommended.get("category", "")
        strategy = recommended.get("strategy", {})
        
        print("\nTop Recommended Strategy:")
        print(f"Category: {strategies['strategy_categories'][category]['name']}")
        print(f"Strategy: {strategy.get('name', '')}")
        print(f"Description: {strategy.get('description', '')}")
        print(f"Potential Revenue: {strategy.get('potential_revenue', '')}")
        print(f"Platforms: {', '.join(strategy.get('platforms', []))}")
        
        if strategy.get("specific_ideas"):
            print("\nSpecific Ideas:")
            for idea in strategy.get("specific_ideas", []):
                print(f"- {idea}")
    
    # Analyze technology trends
    print("\n[3/4] Analyzing technology trends...")
    trend_analyzer = TrendAnalyzer()
    tech_trends = trend_analyzer.analyze_technology_trends(video_data["technologies"])
    
    # Save the trends
    trends_path = os.path.join(output_dir, "technology_trends.json")
    with open(trends_path, "w", encoding="utf-8") as f:
        json.dump(tech_trends, f, indent=2)
    
    print(f"✓ Technology trend analysis saved to {trends_path}")
    
    # Print the top technology
    if tech_trends.get("top_technology"):
        top_tech = tech_trends["top_technology"]
        print("\nTop Technology for Monetization:")
        print(f"Technology: {top_tech.get('name', '')}")
        print(f"Overall Score: {top_tech.get('overall_score', '')}")
        print(f"Monetization Potential: {top_tech.get('monetization_potential', '')}")
        print(f"Job Market: {tech_trends['job_market'].get(top_tech.get('name', ''), {}).get('job_count', '')} positions")
        print(f"Average Salary: ${tech_trends['job_market'].get(top_tech.get('name', ''), {}).get('average_salary', '')}")
    
    # Analyze repository market fit
    print("\n[4/4] Analyzing repository market fit...")
    if video_data.get("repositories"):
        repo = video_data["repositories"][0]
        market_fit = trend_analyzer.analyze_repository_market_fit(repo)
        
        # Save the market fit analysis
        market_fit_path = os.path.join(output_dir, "repository_market_fit.json")
        with open(market_fit_path, "w", encoding="utf-8") as f:
            json.dump(market_fit, f, indent=2)
        
        print(f"✓ Repository market fit analysis saved to {market_fit_path}")
        
        # Print market fit summary
        print("\nRepository Market Fit Summary:")
        print(f"Repository: {market_fit.get('repository', '')}")
        print(f"Application Type: {market_fit.get('application_type', '')}")
        print(f"Monetization Potential: {market_fit.get('monetization_potential', '')}")
        print(f"Market Gap: {market_fit.get('market_gap', '')}")
        
        if market_fit.get("recommendations"):
            print("\nRecommendations:")
            for recommendation in market_fit.get("recommendations", []):
                print(f"- {recommendation}")
    
    print("\n" + "=" * 80)
    print("Demo completed! All output files are saved in the 'demo_output' directory.")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Review the generated strategies in demo_output/monetization_strategies.json")
    print("2. Check technology trends in demo_output/technology_trends.json")
    print("3. Examine repository market fit in demo_output/repository_market_fit.json")
    print("\nTo use the full framework with real YouTube videos, make sure to:")
    print("- Set up environment variables (YOUTUBE_API_KEY, GITHUB_TOKEN)")
    print("- Install all dependencies from requirements.txt")
    print("- Run the main.py script with appropriate commands")

if __name__ == "__main__":
    main()
