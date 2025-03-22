"""
Generate monetization strategies based on extracted video content and repositories.
"""
import os
import json
from typing import Dict, List, Any, Optional

class MonetizationStrategyGenerator:
    """Class to generate monetization strategies from processed video and repository data."""
    
    def __init__(self):
        """Initialize the MonetizationStrategyGenerator."""
        # Define strategy categories
        self.strategy_categories = {
            "content_repurposing": {
                "name": "Content Repurposing",
                "description": "Transform extracted knowledge into different content formats."
            },
            "course_creation": {
                "name": "Educational Products",
                "description": "Create educational content based on technical knowledge."
            },
            "application_development": {
                "name": "Application Development",
                "description": "Build and monetize applications based on repositories."
            },
            "consulting": {
                "name": "Technical Consulting",
                "description": "Offer expertise based on knowledge of specific technologies."
            },
            "affiliate_marketing": {
                "name": "Affiliate Marketing",
                "description": "Promote related products or services with affiliate programs."
            }
        }
    
    def generate_content_repurposing_strategies(self, video_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate content repurposing strategies.
        
        Args:
            video_data: Processed video data.
            
        Returns:
            List of strategy dictionaries.
        """
        strategies = []
        
        # Extract relevant information
        title = video_data.get("video_title", "")
        technologies = video_data.get("technologies", [])
        transcript_data = video_data.get("transcript", {})
        keywords = transcript_data.get("keywords", []) if transcript_data else []
        
        # Strategy 1: Short-form video content
        strategies.append({
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
        })
        
        # Strategy 2: Infographic content
        strategies.append({
            "name": "Technical Infographics",
            "description": "Transform complex concepts into visual learning materials.",
            "platforms": ["Pinterest", "Instagram", "Twitter", "LinkedIn"],
            "potential_revenue": "Low to Medium",
            "time_investment": "Medium",
            "specific_ideas": [
                f"Create a '{technologies[0]} cheat sheet'" if technologies else "Create technology cheat sheets",
                "Design flow diagrams explaining technical processes",
                "Visualize comparisons between similar technologies"
            ]
        })
        
        # Strategy 3: Written content
        strategies.append({
            "name": "Technical Blog Articles",
            "description": "Expand on key concepts in detailed articles for Medium or a personal blog.",
            "platforms": ["Medium", "Dev.to", "Personal blog", "LinkedIn articles"],
            "potential_revenue": "Medium",
            "time_investment": "Medium to High",
            "specific_ideas": [
                f"Write a deep dive on '{keywords[0]}'" if keywords else "Write deep dives on key concepts",
                "Create step-by-step tutorials based on video content",
                "Write comparison articles between technologies"
            ]
        })
        
        return strategies
    
    def generate_course_creation_strategies(self, video_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate educational product strategies.
        
        Args:
            video_data: Processed video data.
            
        Returns:
            List of strategy dictionaries.
        """
        strategies = []
        
        # Extract relevant information
        technologies = video_data.get("technologies", [])
        repositories = video_data.get("repositories", [])
        repo_types = [repo.get("application_type", "unknown") for repo in repositories]
        
        # Strategy 1: Online course
        tech_focus = technologies[0] if technologies else "technology"
        strategies.append({
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
        
        # Strategy 2: Code templates and starter kits
        if repositories:
            repo_type = repo_types[0] if repo_types else "application"
            strategies.append({
                "name": f"{repo_type.capitalize()} Starter Kit",
                "description": f"Create and sell code templates and starter kits for {repo_type} development.",
                "platforms": ["Gumroad", "Personal website", "GitHub Sponsors"],
                "potential_revenue": "Medium",
                "time_investment": "Medium",
                "specific_ideas": [
                    f"Build a premium {repo_type} template with documentation",
                    "Offer different tiers with varying features",
                    "Include video tutorials explaining how to use the template"
                ]
            })
        
        # Strategy 3: Interactive workshops
        strategies.append({
            "name": "Live Technical Workshops",
            "description": f"Host live interactive workshops teaching {tech_focus if technologies else 'technical concepts'}.",
            "platforms": ["Zoom", "Workshop platforms", "Local meetups"],
            "potential_revenue": "Medium to High",
            "time_investment": "Medium",
            "specific_ideas": [
                "Host monthly workshops focused on specific techniques",
                "Create a series of progressive workshops building on each other",
                "Record workshops and sell as on-demand content"
            ]
        })
        
        return strategies
    
    def generate_application_development_strategies(self, video_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate application development strategies.
        
        Args:
            video_data: Processed video data.
            
        Returns:
            List of strategy dictionaries.
        """
        strategies = []
        
        # Extract relevant information
        repositories = video_data.get("repositories", [])
        
        if not repositories:
            # No repositories to build from
            return []
        
        # Get first repository info
        repo = repositories[0]
        repo_name = repo.get("repo", "application")
        app_type = repo.get("application_type", "unknown")
        
        # Strategy 1: SaaS product
        strategies.append({
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
        
        # Strategy The mobile app
        if app_type in ["web", "react", "vue", "angular"]:
            strategies.append({
                "name": f"{repo_name.capitalize()} Mobile App",
                "description": f"Convert the {app_type} application into a mobile app.",
                "platforms": ["App Store", "Google Play Store"],
                "potential_revenue": "Medium to High",
                "time_investment": "High",
                "specific_ideas": [
                    "Use React Native or Flutter to convert the web app",
                    "Add mobile-specific features using device capabilities",
                    "Implement both free and premium versions"
                ]
            })
        
        # Strategy 3: White-label solution
        strategies.append({
            "name": "White-Label Solution",
            "description": f"Offer the {repo_name} application as a customizable solution for businesses.",
            "platforms": ["Direct B2B sales", "Marketplaces"],
            "potential_revenue": "High",
            "time_investment": "Medium",
            "specific_ideas": [
                "Create a customization framework for easy branding",
                "Develop documentation for integration",
                "Offer setup and customization services"
            ]
        })
        
        return strategies
    
    def generate_consulting_strategies(self, video_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate technical consulting strategies.
        
        Args:
            video_data: Processed video data.
            
        Returns:
            List of strategy dictionaries.
        """
        strategies = []
        
        # Extract relevant information
        technologies = video_data.get("technologies", [])
        repositories = video_data.get("repositories", [])
        
        # Strategy 1: Technical consulting
        tech_focus = technologies[0] if technologies else "technology"
        strategies.append({
            "name": f"{tech_focus} Consulting",
            "description": f"Offer consulting services for companies adopting {tech_focus}.",
            "platforms": ["Upwork", "Toptal", "LinkedIn", "Personal website"],
            "potential_revenue": "High",
            "time_investment": "High",
            "specific_ideas": [
                f"Offer {tech_focus} architecture review services",
                f"Provide implementation guidance for {tech_focus} projects",
                "Create a productized consulting package with fixed scope and price"
            ]
        })
        
        # Strategy 2: Implementation services
        if repositories:
            repo_name = repositories[0].get("repo", "solution")
            strategies.append({
                "name": f"{repo_name.capitalize()} Implementation Services",
                "description": f"Help companies implement and customize the {repo_name} solution.",
                "platforms": ["Fiverr", "Upwork", "Direct outreach"],
                "potential_revenue": "Medium to High",
                "time_investment": "Medium",
                "specific_ideas": [
                    "Create standardized implementation packages",
                    "Offer ongoing maintenance and support services",
                    "Develop custom features for clients"
                ]
            })
        
        # Strategy 3: Technical training
        strategies.append({
            "name": "Corporate Technical Training",
            "description": f"Provide specialized training for development teams on {tech_focus if technologies else 'modern technologies'}.",
            "platforms": ["Corporate training programs", "Direct B2B sales"],
            "potential_revenue": "High",
            "time_investment": "Medium",
            "specific_ideas": [
                "Develop customized training curricula for companies",
                "Offer ongoing learning programs with monthly workshops",
                "Create assessment tools to measure team progress"
            ]
        })
        
        return strategies
    
    def generate_affiliate_marketing_strategies(self, video_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate affiliate marketing strategies.
        
        Args:
            video_data: Processed video data.
            
        Returns:
            List of strategy dictionaries.
        """
        strategies = []
        
        # Extract relevant information
        technologies = video_data.get("technologies", [])
        
        # Strategy 1: Technology tool affiliates
        tech_list = ", ".join(technologies[:3]) if technologies else "relevant technologies"
        strategies.append({
            "name": "Technology Tool Affiliates",
            "description": f"Promote tools and services related to {tech_list} through affiliate programs.",
            "platforms": ["Blog posts", "YouTube videos", "Social media"],
            "potential_revenue": "Medium",
            "time_investment": "Low",
            "specific_ideas": [
                "Create honest reviews of tools you actually use",
                "Develop comparison guides for similar products",
                "Create resource pages listing recommended tools"
            ]
        })
        
        # Strategy 2: Learning resource affiliates
        strategies.append({
            "name": "Learning Resource Affiliates",
            "description": "Promote online courses, books, and learning platforms with affiliate programs.",
            "platforms": ["Blog posts", "Email newsletters", "Social media"],
            "potential_revenue": "Medium",
            "time_investment": "Low",
            "specific_ideas": [
                "Create a 'learning path' resource with affiliated course links",
                "Write book reviews with affiliate links",
                "Offer special discounts through affiliate partnerships"
            ]
        })
        
        # Strategy 3: Hosting and service affiliates
        strategies.append({
            "name": "Hosting and Service Affiliates",
            "description": "Promote hosting platforms, development tools, and services.",
            "platforms": ["Tutorial content", "Setup guides", "Social media"],
            "potential_revenue": "Medium to High",
            "time_investment": "Low",
            "specific_ideas": [
                "Create deployment tutorials using specific hosting services",
                "Develop guides for setting up development environments",
                "Showcase how to implement specific features using paid services"
            ]
        })
        
        return strategies
    
    def generate_strategies(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive monetization strategies for video content and repositories.
        
        Args:
            video_data: Processed video data.
            
        Returns:
            Dictionary containing all generated strategies.
        """
        result = {
            "video_id": video_data.get("video_id", ""),
            "video_title": video_data.get("video_title", ""),
            "strategy_categories": {},
            "recommended_strategy": {}
        }
        
        # Generate strategies for each category
        content_strategies = self.generate_content_repurposing_strategies(video_data)
        course_strategies = self.generate_course_creation_strategies(video_data)
        app_strategies = self.generate_application_development_strategies(video_data)
        consulting_strategies = self.generate_consulting_strategies(video_data)
        affiliate_strategies = self.generate_affiliate_marketing_strategies(video_data)
        
        # Add strategies to result
        result["strategy_categories"]["content_repurposing"] = {
            "name": self.strategy_categories["content_repurposing"]["name"],
            "description": self.strategy_categories["content_repurposing"]["description"],
            "strategies": content_strategies
        }
        
        result["strategy_categories"]["course_creation"] = {
            "name": self.strategy_categories["course_creation"]["name"],
            "description": self.strategy_categories["course_creation"]["description"],
            "strategies": course_strategies
        }
        
        result["strategy_categories"]["application_development"] = {
            "name": self.strategy_categories["application_development"]["name"],
            "description": self.strategy_categories["application_development"]["description"],
            "strategies": app_strategies
        }
        
        result["strategy_categories"]["consulting"] = {
            "name": self.strategy_categories["consulting"]["name"],
            "description": self.strategy_categories["consulting"]["description"],
            "strategies": consulting_strategies
        }
        
        result["strategy_categories"]["affiliate_marketing"] = {
            "name": self.strategy_categories["affiliate_marketing"]["name"],
            "description": self.strategy_categories["affiliate_marketing"]["description"],
            "strategies": affiliate_strategies
        }
        
        # Determine recommended strategy
        all_strategies = (
            content_strategies + 
            course_strategies + 
            app_strategies + 
            consulting_strategies + 
            affiliate_strategies
        )
        
        if all_strategies:
            # Simple logic: pick strategy based on whether we have repositories
            has_repositories = len(video_data.get("repositories", [])) > 0
            
            if has_repositories and app_strategies:
                result["recommended_strategy"] = {
                    "category": "application_development",
                    "strategy": app_strategies[0]
                }
            elif course_strategies:
                result["recommended_strategy"] = {
                    "category": "course_creation",
                    "strategy": course_strategies[0]
                }
            elif content_strategies:
                result["recommended_strategy"] = {
                    "category": "content_repurposing",
                    "strategy": content_strategies[0]
                }
        
        return result
    
    def save_strategies(self, strategies: Dict[str, Any], output_file: str) -> None:
        """
        Save generated strategies to a file.
        
        Args:
            strategies: Dictionary of generated strategies.
            output_file: Path to save the strategies to.
            
        Returns:
            None
        """
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(strategies, f, indent=2)
        
        print(f"Strategies saved to {output_file}")
