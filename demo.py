"""
Demo script for the YouTube Content Monetization Framework with Agentic capabilities.
This demo showcases the framework's functionality including the new agentic approach.
"""
import os
import json
import dotenv
from datetime import datetime

# Load environment variables
dotenv.load_dotenv()

# Import monetization components
from monetization.strategy_generator import MonetizationStrategyGenerator
from monetization.trend_analyzer import TrendAnalyzer

# Import agent components
from agents.agent_orchestrator import AgentOrchestrator
from agents.video_analysis_agent import VideoAnalysisAgent
from agents.repository_agent import RepositoryAgent
from agents.app_building_agent import AppBuildingAgent
from agents.trend_analysis_agent import TrendAnalysisAgent
from agents.monetization_agent import MonetizationAgent

def run_traditional_demo():
    """Run the traditional demo without agents."""
    print("=" * 80)
    print("YouTube Content Monetization Framework - Traditional Demo")
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
    print("Traditional demo completed! All output files are saved in the 'demo_output' directory.")
    print("=" * 80)

def run_agentic_demo():
    """Run the agentic demo using CrewAI."""
    print("=" * 80)
    print("YouTube Content Monetization Framework - Agentic Demo with CrewAI")
    print("=" * 80)
    
    # Check for OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("\n⚠️ OPENAI_API_KEY environment variable not set.")
        print("The agentic demo requires an OpenAI API key to function.")
        print("Please set the OPENAI_API_KEY environment variable and try again.")
        return
    
    # Create output directory
    output_dir = "agent_demo_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Demo video ID (real or simulated)
    video_id = "demo_video_456"  # Replace with a real YouTube video ID if available
    
    print(f"\nRunning agentic workflow for video ID: {video_id}")
    print("\nThis process involves multiple AI agents working together:")
    print("1. Video Analysis Agent - Extracts information from the video")
    print("2. Repository Detective - Analyzes GitHub repositories mentioned in the video")
    print("3. Application Builder - Builds applications from the repositories")
    print("4. Trend Analysis Agent - Analyzes technology trends and market opportunities")
    print("5. Monetization Strategist - Develops monetization strategies")
    
    try:
        # Initialize the agent orchestrator
        print("\n[1/5] Initializing agent orchestrator...")
        orchestrator = AgentOrchestrator(openai_api_key=openai_api_key)
        print("✓ Agent orchestrator initialized")
        
        # For demo purposes, we'll simulate the agent workflow
        # In a real scenario, this would call orchestrator.run_monetization_workflow(video_id)
        
        # Simulate video analysis
        print("\n[2/5] Video Analysis Agent is analyzing the video...")
        video_analysis_agent = VideoAnalysisAgent(output_dir=output_dir)
        video_data = {
            "metadata": {
                "video_id": video_id,
                "title": "Building a Modern Web Application with React and FastAPI",
                "description": "In this tutorial, we'll build a full-stack application using React and FastAPI.",
                "channel_id": "UC123456789",
                "channel_title": "Tech Tutorials",
                "published_at": "2023-01-15T12:00:00Z",
                "view_count": 15000,
                "like_count": 1200,
                "comment_count": 150
            },
            "transcript": {
                "text": "In this tutorial, we'll build a full-stack application using React for the frontend and FastAPI for the backend. We'll also use PostgreSQL for the database. The code is available on my GitHub repository: github.com/demo/react-fastapi-app. Let's start by setting up the project...",
                "keywords": ["React", "FastAPI", "PostgreSQL", "web development", "JavaScript", "Python", "full-stack"]
            },
            "content_analysis": {
                "technologies": ["React", "FastAPI", "PostgreSQL", "JavaScript", "Python"],
                "code_snippets": [
                    "npm create vite@latest my-app -- --template react",
                    "pip install fastapi uvicorn sqlalchemy"
                ],
                "key_concepts": ["web development", "API", "database", "frontend", "backend"]
            },
            "repositories": [
                {
                    "url": "https://github.com/demo/react-fastapi-app",
                    "owner": "demo",
                    "repo": "react-fastapi-app"
                }
            ]
        }
        
        # Save video analysis results
        video_analysis_path = os.path.join(output_dir, "video_analysis.json")
        with open(video_analysis_path, "w", encoding="utf-8") as f:
            json.dump(video_data, f, indent=2)
        print(f"✓ Video analysis completed and saved to {video_analysis_path}")
        
        # Simulate repository analysis
        print("\n[3/5] Repository Detective is analyzing the GitHub repository...")
        repository_agent = RepositoryAgent(output_dir=output_dir)
        repo_data = {
            "repository": {
                "owner": "demo",
                "repo": "react-fastapi-app",
                "url": "https://github.com/demo/react-fastapi-app"
            },
            "structure": {
                "key_files": {
                    "readme": ["README.md"],
                    "license": ["LICENSE"],
                    "configuration": [".env.example", ".gitignore"],
                    "dependency": ["requirements.txt", "package.json"],
                    "source_code": ["src/", "backend/", "frontend/"],
                    "docker": ["Dockerfile", "docker-compose.yml"]
                }
            },
            "technologies": {
                "languages": {"JavaScript": 60, "Python": 30, "HTML": 5, "CSS": 5},
                "frameworks": ["React", "FastAPI", "SQLAlchemy"],
                "libraries": ["React Router", "Axios", "Pydantic"],
                "tools": ["Docker", "Vite", "PostgreSQL"]
            },
            "dependencies": {
                "python": [
                    {"name": "fastapi", "version": "0.95.0"},
                    {"name": "sqlalchemy", "version": "2.0.0"},
                    {"name": "pydantic", "version": "1.10.0"},
                    {"name": "uvicorn", "version": "0.21.0"}
                ],
                "javascript": [
                    {"name": "react", "version": "^18.2.0", "type": "production"},
                    {"name": "react-dom", "version": "^18.2.0", "type": "production"},
                    {"name": "axios", "version": "^1.3.4", "type": "production"},
                    {"name": "vite", "version": "^4.2.0", "type": "development"}
                ]
            },
            "build_instructions": {
                "readme": [
                    "# Clone the repository",
                    "git clone https://github.com/demo/react-fastapi-app.git",
                    "cd react-fastapi-app",
                    "# Backend setup",
                    "cd backend",
                    "python -m venv venv",
                    "source venv/bin/activate",
                    "pip install -r requirements.txt",
                    "uvicorn main:app --reload",
                    "# Frontend setup",
                    "cd ../frontend",
                    "npm install",
                    "npm run dev"
                ],
                "docker_compose": ["docker-compose up"]
            }
        }
        
        # Save repository analysis results
        repo_analysis_path = os.path.join(output_dir, "repository_analysis.json")
        with open(repo_analysis_path, "w", encoding="utf-8") as f:
            json.dump(repo_data, f, indent=2)
        print(f"✓ Repository analysis completed and saved to {repo_analysis_path}")
        
        # Simulate application building
        print("\n[4/5] Application Builder is setting up the application...")
        app_building_agent = AppBuildingAgent(output_dir=output_dir)
        app_data = {
            "environment_setup": {
                "working_dir": "/tmp/app_build_123456",
                "detected_languages": {"JavaScript": 60, "Python": 30},
                "detected_frameworks": ["React", "FastAPI"],
                "setup_commands": [
                    "# Python web application detected",
                    "# JavaScript frontend framework detected"
                ]
            },
            "dependency_installation": {
                "installation_commands": [
                    "pip install -r requirements.txt",
                    "npm install"
                ],
                "success": True
            },
            "application_build": {
                "build_commands": ["npm run build"],
                "success": True
            },
            "application_run": {
                "run_commands": [
                    "cd backend && uvicorn main:app --reload",
                    "cd frontend && npm run dev"
                ],
                "is_web_app": True,
                "port": 5173
            },
            "documentation": {
                "markdown_file": os.path.join(output_dir, "application_setup.md"),
                "markdown_content": "# Application Setup Documentation\n\n..."
            }
        }
        
        # Save application build results
        app_build_path = os.path.join(output_dir, "application_build.json")
        with open(app_build_path, "w", encoding="utf-8") as f:
            json.dump(app_data, f, indent=2)
        print(f"✓ Application build process completed and saved to {app_build_path}")
        
        # Simulate trend analysis
        print("\n[5/5] Trend Analysis Agent is analyzing technology trends and market opportunities...")
        trend_analysis_agent = TrendAnalysisAgent(output_dir=output_dir)
        trend_analysis_result = trend_analysis_agent.analyze_trends(video_data, repo_data)
        
        # Save trend analysis results
        trend_analysis_path = os.path.join(output_dir, "trend_analysis_results.json")
        with open(trend_analysis_path, "w", encoding="utf-8") as f:
            json.dump(trend_analysis_result, f, indent=2)
        
        print("✓ Trend analysis completed")
        
        # Display trend analysis summary
        if trend_analysis_result.get("trend_report", {}).get("trend_report", {}).get("summary"):
            summary = trend_analysis_result["trend_report"]["trend_report"]["summary"]
            print("\nTrend Analysis Summary:")
            print(f"Top Technology: {summary.get('top_technology', 'Unknown')}")
            print(f"Content Popularity: {summary.get('content_popularity', 'Unknown')}")
            print(f"Market Fit: {summary.get('market_fit', 'Unknown')}")
            
            # Display key insights
            insights = trend_analysis_result["trend_report"]["trend_report"].get("key_insights", [])
            if insights:
                print("\nKey Insights:")
                for insight in insights[:3]:  # Show up to 3 insights
                    print(f"- {insight}")
        
        # Simulate monetization strategy generation
        print("\n[6/5] Monetization Strategist is developing strategies...")
        monetization_agent = MonetizationAgent(output_dir=output_dir)
        monetization_data = monetization_agent.generate_monetization_strategies(
            video_data, repo_data, app_data, trend_analysis_result
        )
        
        # Save monetization strategies
        strategies_path = os.path.join(output_dir, "monetization_strategies.json")
        with open(strategies_path, "w", encoding="utf-8") as f:
            json.dump(monetization_data, f, indent=2)
        print(f"✓ Monetization strategies generated and saved to {strategies_path}")
        
        # Combine all results
        results = {
            "video_analysis": video_data,
            "repository_analysis": repo_data,
            "application_building": app_data,
            "trend_analysis": trend_analysis_result,
            "monetization_strategies": monetization_data
        }
        
        # Save the combined results
        results_path = os.path.join(output_dir, "agentic_results.json")
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        
        print("\n" + "=" * 80)
        print("Agentic demo completed! All output files are saved in the 'agent_demo_output' directory.")
        print("=" * 80)
    
    except Exception as e:
        print(f"\n❌ Error in agentic demo: {str(e)}")

def main():
    """Run the demo of the YouTube Content Monetization Framework."""
    print("\nYouTube Content Monetization Framework - Demo Options")
    print("\n1. Traditional Demo (No agents)")
    print("2. Agentic Demo with CrewAI")
    
    choice = input("\nSelect demo type (1/2): ").strip()
    
    if choice == "1":
        run_traditional_demo()
    elif choice == "2":
        run_agentic_demo()
    else:
        print("Invalid choice. Please select 1 or 2.")
    
    print("\nNext steps:")
    print("1. Review the generated strategies in the output directories")
    print("2. To use the full framework with real YouTube videos, make sure to:")
    print("   - Set up environment variables (YOUTUBE_API_KEY, GITHUB_TOKEN, OPENAI_API_KEY)")
    print("   - Install all dependencies from requirements.txt")
    print("   - Run the main.py script with appropriate commands")

if __name__ == "__main__":
    main()
