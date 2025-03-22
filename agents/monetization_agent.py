"""
Monetization agent for generating ethical and legal monetization strategies.
"""
import os
from typing import Dict, List, Any, Optional
from crewai import Agent, Task
from monetization.strategy_generator import MonetizationStrategyGenerator

class MonetizationAgent:
    """
    Agent specialized in generating ethical and legal monetization strategies for technical content.
    """
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the MonetizationAgent.
        
        Args:
            output_dir: Directory to store output files.
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize components
        self.strategy_generator = MonetizationStrategyGenerator()
    
    def create_agent(self) -> Agent:
        """
        Create a CrewAI agent for monetization strategy generation.
        
        Returns:
            CrewAI Agent configured for monetization strategy generation.
        """
        return Agent(
            role="Monetization Strategist",
            goal="Develop ethical and legal monetization strategies for technical content and applications",
            backstory="You are a business strategist with deep knowledge of digital monetization models. You understand how to create value from technical content and applications while respecting intellectual property rights.",
            verbose=True,
            allow_delegation=False,
            tools=[
                self.generate_content_repurposing_strategies,
                self.generate_educational_product_strategies,
                self.generate_application_development_strategies,
                self.generate_consulting_strategies,
                self.generate_affiliate_marketing_strategies,
                self.evaluate_ethical_considerations,
                self.evaluate_legal_considerations,
                self.create_monetization_plan
            ]
        )
    
    def generate_content_repurposing_strategies(self, video_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate strategies for repurposing content.
        
        Args:
            video_data: Video analysis data.
            
        Returns:
            List of content repurposing strategies.
        """
        try:
            if "error" in video_data:
                return [{"error": video_data["error"]}]
            
            # Extract relevant information from video data
            video_metadata = video_data.get("metadata", {})
            video_transcript = video_data.get("transcript", {})
            content_analysis = video_data.get("content_analysis", {})
            
            # Create a simplified video data structure for the strategy generator
            simplified_video_data = {
                "video_id": video_metadata.get("video_id", ""),
                "title": video_metadata.get("title", ""),
                "description": video_metadata.get("description", ""),
                "transcript_text": video_transcript.get("text", ""),
                "keywords": video_transcript.get("keywords", []),
                "technologies": content_analysis.get("technologies", []),
                "key_concepts": content_analysis.get("key_concepts", [])
            }
            
            # Generate content repurposing strategies
            strategies = self.strategy_generator.generate_content_repurposing_strategies(simplified_video_data)
            
            return strategies
        except Exception as e:
            print(f"Error generating content repurposing strategies: {e}")
            return [{"error": str(e)}]
    
    def generate_educational_product_strategies(self, video_data: Dict[str, Any], repo_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate strategies for educational products.
        
        Args:
            video_data: Video analysis data.
            repo_data: Repository analysis data.
            
        Returns:
            List of educational product strategies.
        """
        try:
            if "error" in video_data or "error" in repo_data:
                return [{"error": "Error in input data"}]
            
            # Extract relevant information from video data
            video_metadata = video_data.get("metadata", {})
            content_analysis = video_data.get("content_analysis", {})
            
            # Extract relevant information from repository data
            repo_info = repo_data.get("repository", {})
            technologies = repo_data.get("technologies", {})
            
            # Create a simplified data structure for the strategy generator
            simplified_data = {
                "video_title": video_metadata.get("title", ""),
                "video_technologies": content_analysis.get("technologies", []),
                "video_key_concepts": content_analysis.get("key_concepts", []),
                "repo_name": repo_info.get("repo", ""),
                "repo_technologies": technologies.get("frameworks", []) + list(technologies.get("languages", {}).keys())
            }
            
            # Generate educational product strategies
            strategies = self.strategy_generator.generate_educational_product_strategies(simplified_data)
            
            return strategies
        except Exception as e:
            print(f"Error generating educational product strategies: {e}")
            return [{"error": str(e)}]
    
    def generate_application_development_strategies(self, repo_data: Dict[str, Any], app_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate strategies for application development.
        
        Args:
            repo_data: Repository analysis data.
            app_data: Application build data.
            
        Returns:
            List of application development strategies.
        """
        try:
            if "error" in repo_data or "error" in app_data:
                return [{"error": "Error in input data"}]
            
            # Extract relevant information from repository data
            repo_info = repo_data.get("repository", {})
            technologies = repo_data.get("technologies", {})
            
            # Extract relevant information from application data
            app_run = app_data.get("application_run", {})
            
            # Create a simplified data structure for the strategy generator
            simplified_data = {
                "repo_name": repo_info.get("repo", ""),
                "repo_url": repo_info.get("url", ""),
                "technologies": technologies.get("frameworks", []) + list(technologies.get("languages", {}).keys()),
                "is_web_app": app_run.get("is_web_app", False)
            }
            
            # Generate application development strategies
            strategies = self.strategy_generator.generate_application_development_strategies(simplified_data)
            
            return strategies
        except Exception as e:
            print(f"Error generating application development strategies: {e}")
            return [{"error": str(e)}]
    
    def generate_consulting_strategies(self, video_data: Dict[str, Any], repo_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate strategies for consulting services.
        
        Args:
            video_data: Video analysis data.
            repo_data: Repository analysis data.
            
        Returns:
            List of consulting strategies.
        """
        try:
            if "error" in video_data or "error" in repo_data:
                return [{"error": "Error in input data"}]
            
            # Extract relevant information from video data
            content_analysis = video_data.get("content_analysis", {})
            
            # Extract relevant information from repository data
            technologies = repo_data.get("technologies", {})
            
            # Create a simplified data structure for the strategy generator
            simplified_data = {
                "technologies": content_analysis.get("technologies", []) + technologies.get("frameworks", []) + list(technologies.get("languages", {}).keys()),
                "key_concepts": content_analysis.get("key_concepts", [])
            }
            
            # Generate consulting strategies
            strategies = self.strategy_generator.generate_consulting_strategies(simplified_data)
            
            return strategies
        except Exception as e:
            print(f"Error generating consulting strategies: {e}")
            return [{"error": str(e)}]
    
    def generate_affiliate_marketing_strategies(self, video_data: Dict[str, Any], repo_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate strategies for affiliate marketing.
        
        Args:
            video_data: Video analysis data.
            repo_data: Repository analysis data.
            
        Returns:
            List of affiliate marketing strategies.
        """
        try:
            if "error" in video_data or "error" in repo_data:
                return [{"error": "Error in input data"}]
            
            # Extract relevant information from video data
            content_analysis = video_data.get("content_analysis", {})
            
            # Extract relevant information from repository data
            technologies = repo_data.get("technologies", {})
            dependencies = repo_data.get("dependencies", {})
            
            # Create a simplified data structure for the strategy generator
            simplified_data = {
                "technologies": content_analysis.get("technologies", []) + technologies.get("frameworks", []) + list(technologies.get("languages", {}).keys()),
                "dependencies": dependencies
            }
            
            # Generate affiliate marketing strategies
            strategies = self.strategy_generator.generate_affiliate_marketing_strategies(simplified_data)
            
            return strategies
        except Exception as e:
            print(f"Error generating affiliate marketing strategies: {e}")
            return [{"error": str(e)}]
    
    def evaluate_ethical_considerations(self, strategies: List[Dict[str, Any]], repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate ethical considerations for monetization strategies.
        
        Args:
            strategies: List of monetization strategies.
            repo_data: Repository analysis data.
            
        Returns:
            Dictionary containing ethical evaluation.
        """
        try:
            if not strategies or "error" in strategies[0] or "error" in repo_data:
                return {"error": "Error in input data"}
            
            # Extract repository license information
            repo_info = repo_data.get("repository", {})
            structure = repo_data.get("structure", {})
            
            # Check for license files
            license_files = structure.get("key_files", {}).get("license", [])
            has_license = len(license_files) > 0
            
            # Ethical considerations
            ethical_evaluation = {
                "has_license": has_license,
                "license_files": license_files,
                "considerations": [],
                "recommendations": []
            }
            
            # Add general ethical considerations
            ethical_evaluation["considerations"].extend([
                "Respect the original creator's intellectual property rights",
                "Give proper attribution to the original creators",
                "Ensure that monetization strategies do not mislead users about the relationship with the original project",
                "Be transparent about any modifications made to the original code",
                "Consider the impact of monetization on the open-source community"
            ])
            
            # Add license-specific considerations
            if has_license:
                ethical_evaluation["considerations"].append("Adhere to the specific terms of the repository's license")
            else:
                ethical_evaluation["considerations"].append("The repository does not have a clear license, which may limit monetization options")
                ethical_evaluation["recommendations"].append("Contact the repository owner to clarify licensing terms before monetization")
            
            # Evaluate each strategy for ethical considerations
            for strategy in strategies:
                strategy_type = strategy.get("type", "")
                
                if strategy_type == "content_repurposing":
                    ethical_evaluation["considerations"].append("Ensure that content repurposing does not misrepresent the original content")
                
                elif strategy_type == "educational_product":
                    ethical_evaluation["considerations"].append("Clearly distinguish between original content and added educational material")
                
                elif strategy_type == "application_development":
                    ethical_evaluation["considerations"].append("Respect the terms of the license for derivative works")
                
                elif strategy_type == "consulting":
                    ethical_evaluation["considerations"].append("Be transparent about the relationship with the original project")
                
                elif strategy_type == "affiliate_marketing":
                    ethical_evaluation["considerations"].append("Disclose affiliate relationships to users")
            
            return ethical_evaluation
        except Exception as e:
            print(f"Error evaluating ethical considerations: {e}")
            return {"error": str(e)}
    
    def evaluate_legal_considerations(self, strategies: List[Dict[str, Any]], repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate legal considerations for monetization strategies.
        
        Args:
            strategies: List of monetization strategies.
            repo_data: Repository analysis data.
            
        Returns:
            Dictionary containing legal evaluation.
        """
        try:
            if not strategies or "error" in strategies[0] or "error" in repo_data:
                return {"error": "Error in input data"}
            
            # Extract repository license information
            repo_info = repo_data.get("repository", {})
            structure = repo_data.get("structure", {})
            
            # Check for license files
            license_files = structure.get("key_files", {}).get("license", [])
            has_license = len(license_files) > 0
            
            # Legal considerations
            legal_evaluation = {
                "has_license": has_license,
                "license_files": license_files,
                "considerations": [],
                "recommendations": []
            }
            
            # Add general legal considerations
            legal_evaluation["considerations"].extend([
                "Comply with the terms of the repository's license",
                "Ensure that monetization strategies do not infringe on trademarks or patents",
                "Adhere to relevant data protection and privacy laws",
                "Comply with platform-specific terms of service for content distribution",
                "Consider tax implications of monetization strategies"
            ])
            
            # Add license-specific considerations
            if has_license:
                # Determine license type
                license_type = "unknown"
                for license_file in license_files:
                    license_path = os.path.join(repo_info.get("local_path", ""), license_file)
                    if os.path.isfile(license_path):
                        with open(license_path, 'r') as f:
                            license_content = f.read().lower()
                            
                            if "mit" in license_content:
                                license_type = "MIT"
                            elif "apache" in license_content:
                                license_type = "Apache"
                            elif "gpl" in license_content:
                                license_type = "GPL"
                            elif "bsd" in license_content:
                                license_type = "BSD"
                            elif "mozilla" in license_content or "mpl" in license_content:
                                license_type = "Mozilla"
                
                legal_evaluation["license_type"] = license_type
                
                # Add license-specific considerations
                if license_type == "MIT":
                    legal_evaluation["considerations"].append("MIT License allows commercial use with attribution")
                    legal_evaluation["recommendations"].append("Include the original license and copyright notice in any distribution")
                
                elif license_type == "Apache":
                    legal_evaluation["considerations"].append("Apache License allows commercial use with attribution")
                    legal_evaluation["considerations"].append("Must include a copy of the license in any distribution")
                    legal_evaluation["considerations"].append("Must state changes made to the original code")
                
                elif license_type == "GPL":
                    legal_evaluation["considerations"].append("GPL requires derivative works to be distributed under the same license")
                    legal_evaluation["considerations"].append("Source code of derivative works must be made available")
                    legal_evaluation["recommendations"].append("Consider consulting with a legal expert before monetizing GPL-licensed code")
                
                elif license_type == "BSD":
                    legal_evaluation["considerations"].append("BSD License allows commercial use with attribution")
                    legal_evaluation["recommendations"].append("Include the original license and copyright notice in any distribution")
                
                elif license_type == "Mozilla":
                    legal_evaluation["considerations"].append("Mozilla Public License requires modifications to be released under the same license")
                    legal_evaluation["considerations"].append("Can combine with proprietary code under certain conditions")
                
                else:
                    legal_evaluation["considerations"].append(f"The repository has a license, but the type could not be determined")
                    legal_evaluation["recommendations"].append("Review the license carefully or consult with a legal expert before monetization")
            else:
                legal_evaluation["considerations"].append("The repository does not have a clear license, which may limit monetization options")
                legal_evaluation["recommendations"].append("Contact the repository owner to clarify licensing terms before monetization")
            
            # Evaluate each strategy for legal considerations
            for strategy in strategies:
                strategy_type = strategy.get("type", "")
                
                if strategy_type == "content_repurposing":
                    legal_evaluation["considerations"].append("Ensure that content repurposing complies with copyright law")
                    legal_evaluation["considerations"].append("Consider fair use/fair dealing provisions for educational content")
                
                elif strategy_type == "educational_product":
                    legal_evaluation["considerations"].append("Comply with educational licensing requirements")
                    legal_evaluation["considerations"].append("Consider trademark issues when referencing technologies")
                
                elif strategy_type == "application_development":
                    legal_evaluation["considerations"].append("Ensure that derivative applications comply with the original license")
                    legal_evaluation["considerations"].append("Consider patent implications for commercial applications")
                
                elif strategy_type == "consulting":
                    legal_evaluation["considerations"].append("Clearly define the scope of consulting services in contracts")
                    legal_evaluation["considerations"].append("Consider non-disclosure agreements for client projects")
                
                elif strategy_type == "affiliate_marketing":
                    legal_evaluation["considerations"].append("Comply with disclosure requirements for affiliate marketing")
                    legal_evaluation["considerations"].append("Adhere to platform-specific affiliate marketing policies")
            
            return legal_evaluation
        except Exception as e:
            print(f"Error evaluating legal considerations: {e}")
            return {"error": str(e)}
    
    def create_monetization_plan(self, content_repurposing_strategies: List[Dict[str, Any]], educational_product_strategies: List[Dict[str, Any]], application_development_strategies: List[Dict[str, Any]], consulting_strategies: List[Dict[str, Any]], affiliate_marketing_strategies: List[Dict[str, Any]], ethical_evaluation: Dict[str, Any], legal_evaluation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a comprehensive monetization plan.
        
        Args:
            content_repurposing_strategies: List of content repurposing strategies.
            educational_product_strategies: List of educational product strategies.
            application_development_strategies: List of application development strategies.
            consulting_strategies: List of consulting strategies.
            affiliate_marketing_strategies: List of affiliate marketing strategies.
            ethical_evaluation: Ethical evaluation.
            legal_evaluation: Legal evaluation.
            
        Returns:
            Dictionary containing the monetization plan.
        """
        try:
            # Check for errors in input data
            for strategies in [content_repurposing_strategies, educational_product_strategies, application_development_strategies, consulting_strategies, affiliate_marketing_strategies]:
                if not strategies or "error" in strategies[0]:
                    return {"error": "Error in strategy data"}
            
            if "error" in ethical_evaluation or "error" in legal_evaluation:
                return {"error": "Error in evaluation data"}
            
            # Combine all strategies
            all_strategies = []
            all_strategies.extend([{**s, "category": "Content Repurposing"} for s in content_repurposing_strategies])
            all_strategies.extend([{**s, "category": "Educational Products"} for s in educational_product_strategies])
            all_strategies.extend([{**s, "category": "Application Development"} for s in application_development_strategies])
            all_strategies.extend([{**s, "category": "Consulting Services"} for s in consulting_strategies])
            all_strategies.extend([{**s, "category": "Affiliate Marketing"} for s in affiliate_marketing_strategies])
            
            # Sort strategies by potential revenue (if available) or priority
            def get_strategy_priority(strategy):
                if "estimated_revenue" in strategy:
                    return float(strategy["estimated_revenue"].replace("$", "").replace(",", "").split("-")[0])
                elif "priority" in strategy:
                    return strategy["priority"]
                else:
                    return 0
            
            sorted_strategies = sorted(all_strategies, key=get_strategy_priority, reverse=True)
            
            # Create the monetization plan
            monetization_plan = {
                "title": "Comprehensive Monetization Plan",
                "strategies": sorted_strategies,
                "ethical_considerations": ethical_evaluation.get("considerations", []),
                "legal_considerations": legal_evaluation.get("considerations", []),
                "recommendations": ethical_evaluation.get("recommendations", []) + legal_evaluation.get("recommendations", [])
            }
            
            # Generate markdown content
            markdown_content = f"# {monetization_plan['title']}\n\n"
            
            # Add ethical and legal considerations
            markdown_content += "## Ethical and Legal Considerations\n\n"
            
            markdown_content += "### Ethical Considerations\n\n"
            for consideration in ethical_evaluation.get("considerations", []):
                markdown_content += f"- {consideration}\n"
            markdown_content += "\n"
            
            markdown_content += "### Legal Considerations\n\n"
            for consideration in legal_evaluation.get("considerations", []):
                markdown_content += f"- {consideration}\n"
            markdown_content += "\n"
            
            # Add recommendations
            if monetization_plan["recommendations"]:
                markdown_content += "### Recommendations\n\n"
                for recommendation in monetization_plan["recommendations"]:
                    markdown_content += f"- {recommendation}\n"
                markdown_content += "\n"
            
            # Add strategies by category
            categories = set(s["category"] for s in sorted_strategies)
            
            for category in categories:
                markdown_content += f"## {category} Strategies\n\n"
                
                category_strategies = [s for s in sorted_strategies if s["category"] == category]
                
                for i, strategy in enumerate(category_strategies, 1):
                    markdown_content += f"### Strategy {i}: {strategy.get('title', 'Untitled Strategy')}\n\n"
                    markdown_content += f"{strategy.get('description', '')}\n\n"
                    
                    if "steps" in strategy:
                        markdown_content += "#### Implementation Steps\n\n"
                        for j, step in enumerate(strategy["steps"], 1):
                            markdown_content += f"{j}. {step}\n"
                        markdown_content += "\n"
                    
                    if "estimated_revenue" in strategy:
                        markdown_content += f"**Estimated Revenue**: {strategy['estimated_revenue']}\n\n"
                    
                    if "time_investment" in strategy:
                        markdown_content += f"**Time Investment**: {strategy['time_investment']}\n\n"
                    
                    if "resources_needed" in strategy:
                        markdown_content += "**Resources Needed**:\n"
                        for resource in strategy["resources_needed"]:
                            markdown_content += f"- {resource}\n"
                        markdown_content += "\n"
            
            # Save markdown content to file
            markdown_filename = os.path.join(self.output_dir, "monetization_plan.md")
            with open(markdown_filename, 'w') as f:
                f.write(markdown_content)
            
            monetization_plan["markdown_file"] = markdown_filename
            monetization_plan["markdown_content"] = markdown_content
            
            return monetization_plan
        except Exception as e:
            print(f"Error creating monetization plan: {e}")
            return {"error": str(e)}
    
    def generate_monetization_strategies(self, video_data: Dict[str, Any], repo_data: Dict[str, Any], app_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive monetization strategies.
        
        Args:
            video_data: Video analysis data.
            repo_data: Repository analysis data.
            app_data: Application build data.
            
        Returns:
            Dictionary containing monetization strategies.
        """
        try:
            # Generate content repurposing strategies
            content_repurposing_strategies = self.generate_content_repurposing_strategies(video_data)
            
            # Generate educational product strategies
            educational_product_strategies = self.generate_educational_product_strategies(video_data, repo_data)
            
            # Generate application development strategies
            application_development_strategies = self.generate_application_development_strategies(repo_data, app_data)
            
            # Generate consulting strategies
            consulting_strategies = self.generate_consulting_strategies(video_data, repo_data)
            
            # Generate affiliate marketing strategies
            affiliate_marketing_strategies = self.generate_affiliate_marketing_strategies(video_data, repo_data)
            
            # Evaluate ethical considerations
            all_strategies = []
            all_strategies.extend(content_repurposing_strategies)
            all_strategies.extend(educational_product_strategies)
            all_strategies.extend(application_development_strategies)
            all_strategies.extend(consulting_strategies)
            all_strategies.extend(affiliate_marketing_strategies)
            
            ethical_evaluation = self.evaluate_ethical_considerations(all_strategies, repo_data)
            
            # Evaluate legal considerations
            legal_evaluation = self.evaluate_legal_considerations(all_strategies, repo_data)
            
            # Create monetization plan
            monetization_plan = self.create_monetization_plan(
                content_repurposing_strategies,
                educational_product_strategies,
                application_development_strategies,
                consulting_strategies,
                affiliate_marketing_strategies,
                ethical_evaluation,
                legal_evaluation
            )
            
            # Combine all information
            monetization_strategies = {
                "content_repurposing": content_repurposing_strategies,
                "educational_products": educational_product_strategies,
                "application_development": application_development_strategies,
                "consulting": consulting_strategies,
                "affiliate_marketing": affiliate_marketing_strategies,
                "ethical_evaluation": ethical_evaluation,
                "legal_evaluation": legal_evaluation,
                "monetization_plan": monetization_plan
            }
            
            return monetization_strategies
        except Exception as e:
            print(f"Error generating monetization strategies: {e}")
            return {"error": str(e)}
