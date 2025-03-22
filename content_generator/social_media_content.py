"""
Generate social media content based on extracted YouTube video information.
"""
import os
import json
import random
from typing import Dict, List, Any, Optional
import markdown
from bs4 import BeautifulSoup

class SocialMediaContentGenerator:
    """Class to generate social media content from processed video data."""
    
    def __init__(self, output_directory: str = "./social_content"):
        """
        Initialize the SocialMediaContentGenerator.
        
        Args:
            output_directory: Directory to save generated social media content.
        """
        self.output_directory = output_directory
        self.platforms = ["twitter", "linkedin", "instagram", "tiktok", "youtube_shorts"]
        
        # Create directories for each platform
        for platform in self.platforms:
            os.makedirs(os.path.join(output_directory, platform), exist_ok=True)
    
    def extract_key_insights_from_markdown(self, markdown_content: str, max_insights: int = 5) -> List[str]:
        """
        Extract key insights from markdown content.
        
        Args:
            markdown_content: Markdown content to analyze.
            max_insights: Maximum number of insights to extract.
            
        Returns:
            List of insight strings.
        """
        # Convert markdown to HTML for easier parsing
        html = markdown.markdown(markdown_content)
        soup = BeautifulSoup(html, "html.parser")
        
        insights = []
        
        # Extract headings and first paragraph following each heading
        headings = soup.find_all(["h1", "h2", "h3"])
        
        for heading in headings[:max_insights]:
            heading_text = heading.get_text().strip()
            
            # Skip certain headings
            if heading_text.lower() in ["transcript", "video metadata", "timestamps"]:
                continue
            
            # Get the first paragraph after this heading
            next_elem = heading.find_next_sibling()
            if next_elem and next_elem.name == "p":
                paragraph_text = next_elem.get_text().strip()
                
                # Create an insight from heading and paragraph
                insight = f"{heading_text}: {paragraph_text}"
                
                # Limit insight length
                if len(insight) > 280:  # Twitter-like length
                    insight = insight[:277] + "..."
                
                insights.append(insight)
        
        # If we have fewer insights than max_insights, also extract bullet points
        if len(insights) < max_insights:
            list_items = soup.find_all("li")
            for item in list_items:
                item_text = item.get_text().strip()
                
                # Exclude certain items
                if len(item_text) < 20 or ":" not in item_text:
                    continue
                
                if len(insights) >= max_insights:
                    break
                
                insights.append(item_text)
        
        return insights
    
    def extract_code_snippets(self, markdown_content: str) -> List[str]:
        """
        Extract code snippets from markdown content.
        
        Args:
            markdown_content: Markdown content to analyze.
            
        Returns:
            List of code snippet strings.
        """
        # Find all code blocks
        code_blocks = []
        lines = markdown_content.split("\n")
        in_code_block = False
        current_block = []
        
        for line in lines:
            if line.startswith("```"):
                if in_code_block:
                    # End of code block
                    code_blocks.append("\n".join(current_block))
                    current_block = []
                in_code_block = not in_code_block
            elif in_code_block:
                current_block.append(line)
        
        return code_blocks
    
    def extract_technologies(self, markdown_content: str) -> List[str]:
        """
        Extract mentioned technologies from markdown content.
        
        Args:
            markdown_content: Markdown content to analyze.
            
        Returns:
            List of technology strings.
        """
        html = markdown.markdown(markdown_content)
        soup = BeautifulSoup(html, "html.parser")
        
        technologies = []
        
        # Look for technology section
        tech_heading = None
        for heading in soup.find_all(["h2", "h3"]):
            if "technologies" in heading.get_text().lower():
                tech_heading = heading
                break
        
        if tech_heading:
            # Get list items following the tech heading
            list_items = []
            next_elem = tech_heading.find_next_sibling()
            
            while next_elem and next_elem.name in ["ul", "ol"]:
                list_items.extend(next_elem.find_all("li"))
                next_elem = next_elem.find_next_sibling()
            
            for item in list_items:
                technologies.append(item.get_text().strip())
        
        return technologies
    
    def generate_twitter_posts(self, markdown_content: str, video_title: str, video_url: str) -> List[Dict[str, str]]:
        """
        Generate Twitter posts from markdown content.
        
        Args:
            markdown_content: Markdown content to analyze.
            video_title: Title of the video.
            video_url: URL of the video.
            
        Returns:
            List of Twitter post dictionaries.
        """
        insights = self.extract_key_insights_from_markdown(markdown_content)
        technologies = self.extract_technologies(markdown_content)
        
        posts = []
        
        # Create main post
        main_post = {
            "content": f"📺 New Knowledge Drop: {video_title}\n\nCheck out my latest deep dive and learn something new today!\n\n{video_url}"
        }
        posts.append(main_post)
        
        # Create insight posts
        for insight in insights:
            post = {
                "content": f"{insight}\n\nFrom my analysis of \"{video_title}\"\n\n{video_url}"
            }
            posts.append(post)
        
        # Create tech highlight post if technologies are mentioned
        if technologies:
            tech_list = ", ".join(technologies[:5])
            post = {
                "content": f"💻 Tech Spotlight: {tech_list}\n\nThese technologies were featured in \"{video_title}\". Stay updated with the latest tools!\n\n{video_url}"
            }
            posts.append(post)
        
        return posts
    
    def generate_linkedin_posts(self, markdown_content: str, video_title: str, video_url: str) -> List[Dict[str, str]]:
        """
        Generate LinkedIn posts from markdown content.
        
        Args:
            markdown_content: Markdown content to analyze.
            video_title: Title of the video.
            video_url: URL of the video.
            
        Returns:
            List of LinkedIn post dictionaries.
        """
        insights = self.extract_key_insights_from_markdown(markdown_content, max_insights=3)
        technologies = self.extract_technologies(markdown_content)
        
        posts = []
        
        # Create main educational post
        main_post = {
            "content": f"# Key Learnings from \"{video_title}\"\n\n"
        }
        
        for i, insight in enumerate(insights, 1):
            main_post["content"] += f"{i}. {insight}\n\n"
        
        main_post["content"] += f"I've analyzed this tech tutorial and extracted the most valuable insights for you. Check out the full video here: {video_url}\n\n"
        
        if technologies:
            tech_list = ", ".join([f"#{tech.replace(' ', '')}" for tech in technologies[:5]])
            main_post["content"] += f"\n{tech_list}"
        
        posts.append(main_post)
        
        # Create code tutorial post if code snippets are present
        code_snippets = self.extract_code_snippets(markdown_content)
        if code_snippets and len(code_snippets[0]) < 1000:
            code_post = {
                "content": f"# Useful Code Snippet from \"{video_title}\"\n\n"
                           f"Here's a practical example I extracted from a recent tech tutorial:\n\n"
                           f"```\n{code_snippets[0]}\n```\n\n"
                           f"This demonstrates {random.choice(['how to implement', 'a key concept in', 'an important pattern for'])} "
                           f"{random.choice(technologies) if technologies else 'software development'}.\n\n"
                           f"Check out the full tutorial: {video_url}"
            }
            posts.append(code_post)
        
        return posts
    
    def generate_instagram_content(self, markdown_content: str, video_title: str, video_url: str) -> List[Dict[str, Any]]:
        """
        Generate Instagram content ideas from markdown content.
        
        Args:
            markdown_content: Markdown content to analyze.
            video_title: Title of the video.
            video_url: URL of the video.
            
        Returns:
            List of Instagram content idea dictionaries.
        """
        insights = self.extract_key_insights_from_markdown(markdown_content, max_insights=5)
        technologies = self.extract_technologies(markdown_content)
        
        content_ideas = []
        
        # Key insight carousel
        if insights:
            carousel_idea = {
                "type": "carousel",
                "title": f"Key Insights from {video_title}",
                "slides": []
            }
            
            for insight in insights:
                carousel_idea["slides"].append({
                    "text": insight,
                    "background": "gradient",  # In a real implementation, you would generate image designs
                })
            
            content_ideas.append(carousel_idea)
        
        # Technology spotlight
        if technologies:
            tech_spotlight = {
                "type": "image",
                "title": "Technology Spotlight",
                "description": f"Technologies featured in {video_title}: {', '.join(technologies[:5])}",
                "caption": f"Expanding my tech stack with these tools from a recent tutorial I analyzed! Which one interests you the most? Check out the link in bio for the full breakdown. #TechTutorial #CodingJourney #{' #'.join([tech.replace(' ', '') for tech in technologies[:3]])}"
            }
            
            content_ideas.append(tech_spotlight)
        
        return content_ideas
    
    def generate_tiktok_script(self, markdown_content: str, video_title: str, video_url: str) -> List[Dict[str, Any]]:
        """
        Generate TikTok/Shorts script ideas from markdown content.
        
        Args:
            markdown_content: Markdown content to analyze.
            video_title: Title of the video.
            video_url: URL of the video.
            
        Returns:
            List of TikTok script idea dictionaries.
        """
        insights = self.extract_key_insights_from_markdown(markdown_content, max_insights=2)
        technologies = self.extract_technologies(markdown_content)
        code_snippets = self.extract_code_snippets(markdown_content)
        
        script_ideas = []
        
        # Quick Insight Script
        if insights:
            insight_script = {
                "title": f"Key Insight from {video_title}",
                "script": [
                    "👋 Hey devs! Here's a game-changing insight I found while analyzing tech tutorials.",
                    f"💡 {insights[0]}",
                    "That's right. Let me break it down for you...",
                    f"This comes from my deep dive into \"{video_title}\".",
                    "Follow for more tech insights and tutorials breakdown! #CodeTok #TechTutorials"
                ]
            }
            script_ideas.append(insight_script)
        
        # Tech Stack Highlight
        if technologies and len(technologies) >= 3:
            tech_script = {
                "title": "Tech Stack Highlight",
                "script": [
                    "Want to stay relevant in tech? Here are 3 technologies you should know about:",
                    f"1️⃣ {technologies[0]} - This is huge right now!",
                    f"2️⃣ {technologies[1]} - Employers are looking for this skill.",
                    f"3️⃣ {technologies[2]} - Learn this to stand out from the crowd.",
                    f"I found these tech gems in \"{video_title}\" - Follow for more insights! #TechStack #DevLife"
                ]
            }
            script_ideas.append(tech_script)
        
        # Code Walkthrough
        if code_snippets:
            snippet = code_snippets[0]
            if len(snippet) > 150:
                snippet = snippet[:150] + "..."
                
            code_script = {
                "title": "Code Snippet Explained",
                "script": [
                    "Here's a useful code snippet that I found:",
                    f"```\n{snippet}\n```",
                    "Let me explain what's happening here...",
                    f"This shows you how to implement an important pattern in {random.choice(technologies) if technologies else 'programming'}.",
                    "Comment if you want more code explanations like this! #CodingTips #ProgrammingTutorial"
                ]
            }
            script_ideas.append(code_script)
        
        return script_ideas
    
    def generate_youtube_shorts_ideas(self, markdown_content: str, video_title: str, video_url: str) -> List[Dict[str, Any]]:
        """
        Generate YouTube Shorts ideas from markdown content.
        
        Args:
            markdown_content: Markdown content to analyze.
            video_title: Title of the video.
            video_url: URL of the video.
            
        Returns:
            List of YouTube Shorts idea dictionaries.
        """
        # For YouTube Shorts, we'll use similar content as TikTok but with slightly different formatting
        tiktok_scripts = self.generate_tiktok_script(markdown_content, video_title, video_url)
        
        shorts_ideas = []
        
        for script in tiktok_scripts:
            shorts_idea = {
                "title": script["title"],
                "description": f"From my analysis of '{video_title}'",
                "script": script["script"],
                "hashtags": ["TechTips", "CodingTutorial", "LearnToCode", "TechEducation"]
            }
            shorts_ideas.append(shorts_idea)
        
        return shorts_ideas
    
    def process_markdown_file(self, markdown_file_path: str, video_url: str) -> Dict[str, Any]:
        """
        Process a markdown file to generate content for various social media platforms.
        
        Args:
            markdown_file_path: Path to the markdown file.
            video_url: URL of the YouTube video.
            
        Returns:
            Dictionary containing generated content for each platform.
        """
        with open(markdown_file_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()
        
        # Extract video title from markdown (first heading)
        lines = markdown_content.split("\n")
        video_title = ""
        for line in lines:
            if line.startswith("# "):
                video_title = line[2:].strip()
                break
        
        if not video_title:
            video_title = os.path.basename(markdown_file_path).replace(".md", "")
        
        # Generate content for each platform
        twitter_posts = self.generate_twitter_posts(markdown_content, video_title, video_url)
        linkedin_posts = self.generate_linkedin_posts(markdown_content, video_title, video_url)
        instagram_content = self.generate_instagram_content(markdown_content, video_title, video_url)
        tiktok_scripts = self.generate_tiktok_script(markdown_content, video_title, video_url)
        youtube_shorts = self.generate_youtube_shorts_ideas(markdown_content, video_title, video_url)
        
        result = {
            "video_title": video_title,
            "video_url": video_url,
            "twitter": twitter_posts,
            "linkedin": linkedin_posts,
            "instagram": instagram_content,
            "tiktok": tiktok_scripts,
            "youtube_shorts": youtube_shorts
        }
        
        return result
    
    def save_platform_content(self, platform: str, content: List[Dict[str, Any]], video_id: str) -> None:
        """
        Save generated content for a platform to a file.
        
        Args:
            platform: Social media platform name.
            content: List of content dictionaries for the platform.
            video_id: YouTube video ID.
            
        Returns:
            None
        """
        output_dir = os.path.join(self.output_directory, platform)
        file_path = os.path.join(output_dir, f"{video_id}.json")
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2)
    
    def generate_and_save_all(self, markdown_file_path: str, video_id: str, video_url: str) -> Dict[str, str]:
        """
        Generate and save content for all platforms from a markdown file.
        
        Args:
            markdown_file_path: Path to the markdown file.
            video_id: YouTube video ID.
            video_url: URL of the YouTube video.
            
        Returns:
            Dictionary mapping platforms to output file paths.
        """
        all_content = self.process_markdown_file(markdown_file_path, video_url)
        output_files = {}
        
        for platform in self.platforms:
            platform_content = all_content.get(platform, [])
            self.save_platform_content(platform, platform_content, video_id)
            output_files[platform] = os.path.join(self.output_directory, platform, f"{video_id}.json")
        
        return output_files
