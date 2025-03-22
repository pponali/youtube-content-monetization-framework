"""
Analyze technology trends for monetization opportunities.
"""
import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import requests
from collections import Counter

class TrendAnalyzer:
    """Class to analyze technology trends for monetization opportunities."""
    
    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize the TrendAnalyzer.
        
        Args:
            github_token: GitHub API token for authenticated requests.
        """
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        
        # Set up headers for API requests
        self.headers = {
            "User-Agent": "YouTube-Monetization-Framework/1.0"
        }
        
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"
    
    def get_github_trends(self, language: Optional[str] = None, time_period: str = "daily") -> List[Dict[str, Any]]:
        """
        Get trending repositories from GitHub.
        
        Args:
            language: Optional programming language to filter by.
            time_period: Time period for trends (daily, weekly, monthly).
            
        Returns:
            List of trending repository dictionaries.
        """
        # GitHub Trending API doesn't have an official endpoint
        # This is a workaround using a third-party API
        url = "https://api.gitterapp.com/repositories"
        
        params = {
            "language": language or "",
            "since": time_period
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching GitHub trends: {e}")
            return []
    
    def get_stack_overflow_trends(self, tags: List[str]) -> Dict[str, int]:
        """
        Get question counts for tags on Stack Overflow.
        
        Args:
            tags: List of technology tags to analyze.
            
        Returns:
            Dictionary mapping tags to question counts.
        """
        # Stack Overflow API endpoint for questions
        base_url = "https://api.stackexchange.com/2.3/questions"
        
        # Get questions from the last 30 days
        thirty_days_ago = int((datetime.now() - timedelta(days=30)).timestamp())
        
        results = {}
        
        for tag in tags:
            params = {
                "tagged": tag,
                "site": "stackoverflow",
                "fromdate": thirty_days_ago,
                "filter": "total"
            }
            
            try:
                response = requests.get(base_url, params=params, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                
                results[tag] = data.get("total", 0)
                
                # Respect rate limits
                time.sleep(0.5)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching Stack Overflow trends for {tag}: {e}")
                results[tag] = 0
        
        return results
    
    def get_npm_package_downloads(self, packages: List[str]) -> Dict[str, int]:
        """
        Get download counts for NPM packages.
        
        Args:
            packages: List of NPM package names to analyze.
            
        Returns:
            Dictionary mapping package names to download counts.
        """
        results = {}
        
        for package in packages:
            # NPM API endpoint for package downloads
            url = f"https://api.npmjs.org/downloads/point/last-month/{package}"
            
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                
                downloads = data.get("downloads", 0)
                results[package] = downloads
                
                # Respect rate limits
                time.sleep(0.5)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching NPM downloads for {package}: {e}")
                results[package] = 0
        
        return results
    
    def get_pypi_package_info(self, packages: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Get information about PyPI packages.
        
        Args:
            packages: List of PyPI package names to analyze.
            
        Returns:
            Dictionary mapping package names to information dictionaries.
        """
        results = {}
        
        for package in packages:
            # PyPI API endpoint for package information
            url = f"https://pypi.org/pypi/{package}/json"
            
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                
                info = data.get("info", {})
                results[package] = {
                    "name": info.get("name", ""),
                    "version": info.get("version", ""),
                    "description": info.get("summary", ""),
                    "author": info.get("author", ""),
                    "license": info.get("license", ""),
                    "project_url": info.get("project_url", ""),
                    "release_date": info.get("release_date", "")
                }
                
                # Respect rate limits
                time.sleep(0.5)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching PyPI info for {package}: {e}")
                results[package] = {}
        
        return results
    
    def get_job_market_data(self, technologies: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Get job market data for technologies.
        
        Args:
            technologies: List of technology names to analyze.
            
        Returns:
            Dictionary mapping technology names to job market data.
        """
        # Using a mock implementation since real job APIs typically require authentication
        # In a real implementation, you could use APIs from platforms like LinkedIn, Indeed, etc.
        
        # Mock job counts - in a real implementation, these would come from an API
        mock_job_counts = {
            "python": 50000,
            "javascript": 70000,
            "react": 45000,
            "angular": 25000,
            "vue": 15000,
            "node.js": 30000,
            "django": 12000,
            "flask": 8000,
            "fastapi": 5000,
            "express": 20000,
            "tensorflow": 10000,
            "pytorch": 8000,
            "docker": 35000,
            "kubernetes": 25000,
            "aws": 60000,
            "azure": 40000,
            "gcp": 20000,
            "mongodb": 18000,
            "postgresql": 22000,
            "mysql": 28000
        }
        
        # Mock salary data - in a real implementation, these would come from an API
        mock_salary_data = {
            "python": 120000,
            "javascript": 110000,
            "react": 125000,
            "angular": 115000,
            "vue": 105000,
            "node.js": 115000,
            "django": 115000,
            "flask": 110000,
            "fastapi": 120000,
            "express": 105000,
            "tensorflow": 140000,
            "pytorch": 135000,
            "docker": 125000,
            "kubernetes": 135000,
            "aws": 130000,
            "azure": 125000,
            "gcp": 135000,
            "mongodb": 115000,
            "postgresql": 120000,
            "mysql": 110000
        }
        
        results = {}
        
        for tech in technologies:
            tech_lower = tech.lower()
            
            # Try to find a match in our mock data
            job_count = 0
            avg_salary = 0
            
            for key in mock_job_counts:
                if key in tech_lower or tech_lower in key:
                    job_count = mock_job_counts[key]
                    avg_salary = mock_salary_data[key]
                    break
            
            results[tech] = {
                "job_count": job_count,
                "average_salary": avg_salary,
                "growth_rate": "high" if job_count > 30000 else "medium" if job_count > 15000 else "low"
            }
        
        return results
    
    def get_google_trends_data(self, keywords: List[str]) -> Dict[str, int]:
        """
        Get relative interest from Google Trends.
        
        Args:
            keywords: List of keywords to analyze.
            
        Returns:
            Dictionary mapping keywords to relative interest scores.
        """
        # This is a mock implementation
        # In a real implementation, you would use the pytrends library or similar
        
        # Mock interest scores - in a real implementation, these would come from Google Trends API
        mock_interest_scores = {
            "python": 100,
            "javascript": 90,
            "react": 85,
            "angular": 60,
            "vue": 50,
            "node.js": 70,
            "django": 40,
            "flask": 35,
            "fastapi": 25,
            "express": 45,
            "tensorflow": 65,
            "pytorch": 55,
            "docker": 80,
            "kubernetes": 75,
            "aws": 95,
            "azure": 85,
            "gcp": 65,
            "mongodb": 55,
            "postgresql": 65,
            "mysql": 70
        }
        
        results = {}
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            # Try to find a match in our mock data
            interest_score = 0
            
            for key in mock_interest_scores:
                if key in keyword_lower or keyword_lower in key:
                    interest_score = mock_interest_scores[key]
                    break
            
            results[keyword] = interest_score
        
        return results
    
    def analyze_technology_trends(self, technologies: List[str]) -> Dict[str, Any]:
        """
        Analyze trends for a list of technologies.
        
        Args:
            technologies: List of technology names to analyze.
            
        Returns:
            Dictionary containing trend analysis.
        """
        if not technologies:
            return {"error": "No technologies provided for analysis"}
        
        result = {
            "technologies": technologies,
            "analysis_date": datetime.now().isoformat(),
            "job_market": {},
            "interest_scores": {},
            "stack_overflow": {},
            "package_data": {},
            "overall_ranking": []
        }
        
        # Get job market data
        result["job_market"] = self.get_job_market_data(technologies)
        
        # Get Google Trends data
        result["interest_scores"] = self.get_google_trends_data(technologies)
        
        # Get Stack Overflow data
        result["stack_overflow"] = self.get_stack_overflow_trends(technologies)
        
        # Get package data
        # Determine which technologies might be npm packages or PyPI packages
        npm_packages = []
        pypi_packages = []
        
        for tech in technologies:
            tech_lower = tech.lower()
            if tech_lower in ["react", "angular", "vue", "express", "next.js", "gatsby"]:
                npm_packages.append(tech_lower)
            elif tech_lower in ["django", "flask", "fastapi", "tensorflow", "pytorch", "pandas"]:
                pypi_packages.append(tech_lower)
        
        if npm_packages:
            result["package_data"]["npm"] = self.get_npm_package_downloads(npm_packages)
        
        if pypi_packages:
            result["package_data"]["pypi"] = self.get_pypi_package_info(pypi_packages)
        
        # Calculate overall ranking
        ranking_data = []
        
        for tech in technologies:
            # Factors to consider with different weights
            job_market_score = result["job_market"].get(tech, {}).get("job_count", 0) / 10000  # Scale job count
            interest_score = result["interest_scores"].get(tech, 0) / 20  # Scale interest score
            so_score = result["stack_overflow"].get(tech, 0) / 1000  # Scale Stack Overflow count
            
            # Calculate a weighted score
            overall_score = (job_market_score * 0.5) + (interest_score * 0.3) + (so_score * 0.2)
            
            ranking_data.append({
                "technology": tech,
                "overall_score": overall_score,
                "job_market_score": job_market_score,
                "interest_score": interest_score,
                "stack_overflow_score": so_score
            })
        
        # Sort by overall score (descending)
        ranking_data.sort(key=lambda x: x["overall_score"], reverse=True)
        result["overall_ranking"] = ranking_data
        
        # Identify top technologies for monetization
        if ranking_data:
            top_tech = ranking_data[0]["technology"]
            result["top_technology"] = {
                "name": top_tech,
                "overall_score": ranking_data[0]["overall_score"],
                "job_market": result["job_market"].get(top_tech, {}),
                "monetization_potential": "high" if ranking_data[0]["overall_score"] > 7 else "medium" if ranking_data[0]["overall_score"] > 4 else "low"
            }
        
        return result
    
    def analyze_repository_market_fit(self, repository_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the market fit for a repository.
        
        Args:
            repository_info: Repository information dictionary.
            
        Returns:
            Dictionary containing market fit analysis.
        """
        # Extract relevant information
        repo_name = repository_info.get("repo", "")
        languages = repository_info.get("languages", {})
        primary_language = max(languages.items(), key=lambda x: x[1])[0] if languages else "Unknown"
        app_type = repository_info.get("application_type", "unknown")
        stars = repository_info.get("github_info", {}).get("stargazers_count", 0)
        forks = repository_info.get("github_info", {}).get("forks_count", 0)
        
        # Get trends for the primary language
        language_trends = self.analyze_technology_trends([primary_language]) if primary_language != "Unknown" else {}
        
        # Calculate project popularity score
        popularity_score = (stars * 0.7) + (forks * 0.3)
        popularity_level = "high" if popularity_score > 1000 else "medium" if popularity_score > 100 else "low"
        
        # Determine monetization potential based on app type
        monetization_potential = "low"
        if app_type in ["web", "react", "vue", "angular", "nextjs"]:
            monetization_potential = "high"  # Web apps are easier to monetize
        elif app_type in ["django", "flask", "fastapi", "express"]:
            monetization_potential = "high"  # Backend frameworks can be turned into SaaS
        elif app_type in ["library", "plugin", "extension"]:
            monetization_potential = "medium"  # Libraries can be monetized with premium features
        elif app_type in ["machine-learning", "data-science"]:
            monetization_potential = "high"  # ML models and tools have high monetization potential
        
        # Market gap analysis
        market_gap = "unknown"
        if app_type in ["web", "react", "vue", "angular", "nextjs"] and stars < 100:
            market_gap = "saturated"  # Many web apps available
        elif app_type in ["django", "flask", "fastapi", "express"] and stars > 100:
            market_gap = "opportunity"  # Good backend tools are in demand
        elif app_type in ["machine-learning", "data-science"]:
            market_gap = "growing"  # ML/AI market is growing
        
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
            "language_trends": language_trends,
            "monetization_potential": monetization_potential,
            "market_gap": market_gap,
            "recommendations": []
        }
        
        # Generate recommendations
        if monetization_potential == "high":
            result["recommendations"].append("Consider developing a SaaS product with a freemium model")
            result["recommendations"].append("Create a hosted version with additional features")
        
        if app_type in ["library", "plugin", "extension"]:
            result["recommendations"].append("Offer premium support and consulting services")
            result["recommendations"].append("Create a pro version with advanced features")
        
        if app_type in ["machine-learning", "data-science"]:
            result["recommendations"].append("Develop an API service for the ML models")
            result["recommendations"].append("Create training materials and workshops")
        
        return result
    
    def save_trend_analysis(self, analysis: Dict[str, Any], output_file: str) -> None:
        """
        Save trend analysis to a file.
        
        Args:
            analysis: Dictionary containing trend analysis.
            output_file: Path to save the analysis to.
            
        Returns:
            None
        """
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2)
        
        print(f"Trend analysis saved to {output_file}")
