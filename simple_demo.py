"""
Simplified demo script for the YouTube Content Monetization Framework.
This script simulates the key functionality without any external dependencies.
"""
import os
import json
from datetime import datetime

def generate_monetization_strategies(video_data):
    """Simulate the MonetizationStrategyGenerator.generate_strategies method."""
    
    # Extract data from video_data
    video_id = video_data.get("video_id", "")
    video_title = video_data.get("video_title", "")
    technologies = video_data.get("technologies", [])
    repositories = video_data.get("repositories", [])
    
    # Generate content repurposing strategies
    content_strategies = [
        {
            "name": "Short-form Video Content",
            "description": "Create concise educational shorts focusing on specific concepts.",
            "platforms": ["TikTok", "YouTube Shorts", "Instagram Reels"],
            "potential_revenue": "Medium",
            "time_investment": "Low",
            "specific_ideas": [
                f"Create a '{technologies[0]} in 60 seconds' series" if technologies else "Create a 'Tech Concept in 60 seconds' series",
                "Highlight code snippets with explanations",
                "Demonstrate quick technical tips and tricks"
            ]
        },
        {
            "name": "Technical Blog Articles",
            "description": "Expand on key concepts in detailed articles for Medium or a personal blog.",
            "platforms": ["Medium", "Dev.to", "Personal blog", "LinkedIn articles"],
            "potential_revenue": "Medium",
            "time_investment": "Medium to High",
            "specific_ideas": [
                f"Write a deep dive on '{technologies[0]}'" if technologies else "Write deep dives on key concepts",
                "Create step-by-step tutorials based on video content",
                "Write comparison articles between technologies"
            ]
        }
    ]
    
    # Generate course strategies
    course_strategies = []
    if technologies:
        tech_focus = technologies[0]
        course_strategies.append({
            "name": f"{tech_focus} Mastery Course",
            "description": f"Create a comprehensive online course teaching {tech_focus}.",
            "platforms": ["Udemy", "Teachable", "Podia", "Skillshare"],
            "potential_revenue": "High",
            "time_investment": "High",
            "specific_ideas": [
                f"Build a '{tech_focus} from Zero to Hero' course",
                f"Create a project-based course using {tech_focus}",
                "Include hands-on exercises and projects"
            ]
        })
    
    # Generate app development strategies
    app_strategies = []
    if repositories:
        repo = repositories[0]
        repo_name = repo.get("repo", "application").split("/")[-1]
        app_type = repo.get("application_type", "unknown")
        
        app_strategies.append({
            "name": f"{repo_name.capitalize()} as a Service",
            "description": f"Develop the repository into a SaaS product with a freemium model.",
            "platforms": ["AWS", "Heroku", "DigitalOcean", "Vercel"],
            "potential_revenue": "High",
            "time_investment": "High",
            "specific_ideas": [
                "Identify core functionality that can be offered as a service",
                "Create a tiered pricing model with free and premium features",
                "Add monitoring, analytics, and user management features"
            ]
        })
    
    # Determine recommended strategy
    recommended_strategy = {}
    if app_strategies:
        recommended_strategy = {
            "category": "application_development",
            "strategy": app_strategies[0]
        }
    elif course_strategies:
        recommended_strategy = {
            "category": "course_creation",
            "strategy": course_strategies[0]
        }
    elif content_strategies:
        recommended_strategy = {
            "category": "content_repurposing",
            "strategy": content_strategies[0]
        }
    
    # Build result
    result = {
        "video_id": video_id,
        "video_title": video_title,
        "strategy_categories": {
            "content_repurposing": {
                "name": "Content Repurposing",
                "description": "Transform extracted knowledge into different content formats.",
                "strategies": content_strategies
            },
            "course_creation": {
                "name": "Educational Products",
                "description": "Create educational content based on technical knowledge.",
                "strategies": course_strategies
            },
            "application_development": {
                "name": "Application Development",
                "description": "Build and monetize applications based on repositories.",
                "strategies": app_strategies
            }
        },
        "recommended_strategy": recommended_strategy
    }
    
    return result

def analyze_technology_trends(technologies):
    """Simulate the TrendAnalyzer.analyze_technology_trends method."""
    
    # Mock job market data
    mock_job_market = {
        "python": {"job_count": 50000, "average_salary": 120000, "growth_rate": "high"},
        "react": {"job_count": 45000, "average_salary": 125000, "growth_rate": "high"},
        "javascript": {"job_count": 70000, "average_salary": 110000, "growth_rate": "high"},
        "fastapi": {"job_count": 5000, "average_salary": 120000, "growth_rate": "high"},
        "postgresql": {"job_count": 22000, "average_salary": 120000, "growth_rate": "medium"}
    }
    
    # Mock interest scores
    mock_interest_scores = {
        "python": 100,
        "react": 85,
        "javascript": 90,
        "fastapi": 25,
        "postgresql": 65
    }
    
    result = {
        "technologies": technologies,
        "analysis_date": datetime.now().isoformat(),
        "job_market": {},
        "interest_scores": {},
        "overall_ranking": []
    }
    
    # Fill in job market data and interest scores
    for tech in technologies:
        tech_lower = tech.lower()
        if tech_lower in mock_job_market:
            result["job_market"][tech] = mock_job_market[tech_lower]
        else:
            result["job_market"][tech] = {"job_count": 10000, "average_salary": 100000, "growth_rate": "medium"}
            
        if tech_lower in mock_interest_scores:
            result["interest_scores"][tech] = mock_interest_scores[tech_lower]
        else:
            result["interest_scores"][tech] = 50
    
    # Calculate overall ranking
    ranking_data = []
    for tech in technologies:
        job_market_score = result["job_market"].get(tech, {}).get("job_count", 0) / 10000
        interest_score = result["interest_scores"].get(tech, 0) / 20
        
        overall_score = (job_market_score * 0.6) + (interest_score * 0.4)
        
        ranking_data.append({
            "technology": tech,
            "overall_score": overall_score,
            "job_market_score": job_market_score,
            "interest_score": interest_score
        })
    
    # Sort by overall score (descending)
    ranking_data.sort(key=lambda x: x["overall_score"], reverse=True)
    result["overall_ranking"] = ranking_data
    
    # Identify top technology for monetization
    if ranking_data:
        top_tech = ranking_data[0]["technology"]
        result["top_technology"] = {
            "name": top_tech,
            "overall_score": ranking_data[0]["overall_score"],
            "job_market": result["job_market"].get(top_tech, {}),
            "monetization_potential": "high" if ranking_data[0]["overall_score"] > 7 else "medium" if ranking_data[0]["overall_score"] > 4 else "low"
        }
    
    return result

def analyze_repository_market_fit(repository_info):
    """Simulate the TrendAnalyzer.analyze_repository_market_fit method."""
    
    # Extract relevant information
    repo_name = repository_info.get("repo", "").split("/")[-1]
    languages = repository_info.get("languages", {})
    primary_language = max(languages.items(), key=lambda x: x[1])[0] if languages else "Unknown"
    app_type = repository_info.get("application_type", "unknown")
    stars = repository_info.get("github_info", {}).get("stargazers_count", 0)
    forks = repository_info.get("github_info", {}).get("forks_count", 0)
    
    # Calculate project popularity score
    popularity_score = (stars * 0.7) + (forks * 0.3)
    popularity_level = "high" if popularity_score > 1000 else "medium" if popularity_score > 100 else "low"
    
    # Determine monetization potential based on app type
    monetization_potential = "low"
    if app_type in ["web", "react", "vue", "angular", "nextjs"]:
        monetization_potential = "high"  # Web apps are easier to monetize
    elif app_type in ["django", "flask", "fastapi", "express"]:
        monetization_potential = "high"  # Backend frameworks can be turned into SaaS
    
    # Market gap analysis
    market_gap = "unknown"
    if app_type in ["web", "react", "vue", "angular", "nextjs"] and stars < 100:
        market_gap = "saturated"  # Many web apps available
    elif app_type in ["django", "flask", "fastapi", "express"] and stars > 100:
        market_gap = "opportunity"  # Good backend tools are in demand
    
    result = {
        "repository": repo_name,
        "primary_language": primary_language,
        "application_type": app_type,
        "popularity": {
            "stars": stars,
            "forks": forks,
            "score": popularity_score,
            "level": popularity_level
        },
        "monetization_potential": monetization_potential,
        "market_gap": market_gap,
        "recommendations": []
    }
    
    # Generate recommendations
    if monetization_potential == "high":
        result["recommendations"].append("Consider developing a SaaS product with a freemium model")
        result["recommendations"].append("Create a hosted version with additional features")
    
    if app_type in ["web", "react", "vue", "angular", "nextjs"]:
        result["recommendations"].append("Offer white-label solutions for businesses")
        result["recommendations"].append("Create premium UI component libraries or templates")
    
    return result

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
    strategies = generate_monetization_strategies(video_data)
    
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
    tech_trends = analyze_technology_trends(video_data["technologies"])
    
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
        market_fit = analyze_repository_market_fit(repo)
        
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
    print("\nNext steps to use the full framework:")
    print("1. Set up environment variables (YOUTUBE_API_KEY, GITHUB_TOKEN)")
    print("2. Install all dependencies from requirements.txt")
    print("3. Run the main.py script with appropriate commands:")
    print("   - python main.py video <VIDEO_ID> --output output_directory")
    print("   - python main.py channel <CHANNEL_ID> --limit 10 --output output_directory")
    print("   - python main.py repo <REPOSITORY_URL> --output output_directory --deploy")

if __name__ == "__main__":
    main()
