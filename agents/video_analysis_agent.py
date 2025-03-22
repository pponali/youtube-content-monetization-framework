"""
Video analysis agent for extracting information from YouTube videos.
"""
import os
from typing import Dict, List, Any, Optional
from crewai import Agent, Task
from scraper.youtube_api import YouTubeAPI
from scraper.transcript_extractor import TranscriptExtractor
from scraper.repository_detector import RepositoryDetector

class VideoAnalysisAgent:
    """
    Agent specialized in analyzing YouTube video content to extract valuable information.
    """
    
    def __init__(self, youtube_api_key: Optional[str] = None, output_dir: str = "output"):
        """
        Initialize the VideoAnalysisAgent.
        
        Args:
            youtube_api_key: YouTube API key for accessing video data. If None, loads from environment.
            output_dir: Directory to store output files.
        """
        self.youtube_api_key = youtube_api_key or os.getenv("YOUTUBE_API_KEY")
        if not self.youtube_api_key:
            raise ValueError("YouTube API key is required. Set YOUTUBE_API_KEY environment variable or pass to constructor.")
        
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize components
        self.youtube_api = YouTubeAPI(api_key=self.youtube_api_key)
        self.transcript_extractor = TranscriptExtractor()
        self.repository_detector = RepositoryDetector()
    
    def create_agent(self) -> Agent:
        """
        Create a CrewAI agent for video analysis.
        
        Returns:
            CrewAI Agent configured for video analysis.
        """
        return Agent(
            role="Video Content Analyzer",
            goal="Extract comprehensive information from YouTube videos including technical concepts, code snippets, and key insights",
            backstory="You are an expert in video content analysis with deep knowledge of programming and technical topics. Your specialty is understanding complex technical videos and extracting structured information.",
            verbose=True,
            allow_delegation=False,
            tools=[
                self.extract_video_metadata,
                self.extract_video_transcript,
                self.analyze_transcript_content,
                self.detect_repositories_in_transcript
            ]
        )
    
    def extract_video_metadata(self, video_id: str) -> Dict[str, Any]:
        """
        Extract metadata from a YouTube video.
        
        Args:
            video_id: YouTube video ID.
            
        Returns:
            Dictionary containing video metadata.
        """
        try:
            video_details = self.youtube_api.get_video_details(video_id)
            
            metadata = {
                "video_id": video_id,
                "title": video_details["snippet"]["title"],
                "description": video_details["snippet"]["description"],
                "channel_id": video_details["snippet"]["channelId"],
                "channel_title": video_details["snippet"]["channelTitle"],
                "published_at": video_details["snippet"]["publishedAt"],
                "tags": video_details.get("snippet", {}).get("tags", []),
                "category_id": video_details.get("snippet", {}).get("categoryId", ""),
                "view_count": video_details.get("statistics", {}).get("viewCount", 0),
                "like_count": video_details.get("statistics", {}).get("likeCount", 0),
                "comment_count": video_details.get("statistics", {}).get("commentCount", 0),
                "duration": video_details.get("contentDetails", {}).get("duration", ""),
                "topics": video_details.get("topicDetails", {}).get("topicCategories", [])
            }
            
            return metadata
        except Exception as e:
            print(f"Error extracting video metadata: {e}")
            return {"error": str(e)}
    
    def extract_video_transcript(self, video_id: str) -> Dict[str, Any]:
        """
        Extract and process the transcript from a YouTube video.
        
        Args:
            video_id: YouTube video ID.
            
        Returns:
            Dictionary containing processed transcript information.
        """
        try:
            transcript_data = self.transcript_extractor.process_transcript(video_id)
            return transcript_data
        except Exception as e:
            print(f"Error extracting video transcript: {e}")
            return {"error": str(e)}
    
    def analyze_transcript_content(self, transcript_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze transcript content to extract key concepts, technologies, and code snippets.
        
        Args:
            transcript_data: Transcript data from extract_video_transcript.
            
        Returns:
            Dictionary containing analysis results.
        """
        try:
            if "error" in transcript_data:
                return {"error": transcript_data["error"]}
            
            transcript_text = transcript_data.get("text", "")
            
            # Extract technologies mentioned
            technologies = []
            common_tech_keywords = [
                "Python", "JavaScript", "TypeScript", "Java", "C#", "C++", "Go", "Rust",
                "React", "Angular", "Vue", "Next.js", "Svelte", "Node.js", "Express",
                "Django", "Flask", "FastAPI", "Spring Boot", "ASP.NET",
                "TensorFlow", "PyTorch", "scikit-learn", "Keras",
                "Docker", "Kubernetes", "AWS", "Azure", "GCP",
                "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch"
            ]
            
            for tech in common_tech_keywords:
                if tech.lower() in transcript_text.lower():
                    technologies.append(tech)
            
            # Extract code snippets
            code_snippets = self.transcript_extractor.detect_code_snippets(transcript_text)
            
            # Extract key concepts using keywords
            keywords = transcript_data.get("keywords", [])
            
            return {
                "technologies": technologies,
                "code_snippets": code_snippets,
                "key_concepts": keywords
            }
        except Exception as e:
            print(f"Error analyzing transcript content: {e}")
            return {"error": str(e)}
    
    def detect_repositories_in_transcript(self, transcript_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect GitHub repositories mentioned in the transcript.
        
        Args:
            transcript_data: Transcript data from extract_video_transcript.
            
        Returns:
            List of detected repository information.
        """
        try:
            if "error" in transcript_data:
                return [{"error": transcript_data["error"]}]
            
            transcript_text = transcript_data.get("text", "")
            
            # Use regular expressions to find GitHub URLs
            import re
            github_patterns = [
                r'github\.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)',
                r'github\.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)\.git'
            ]
            
            repositories = []
            
            for pattern in github_patterns:
                matches = re.findall(pattern, transcript_text)
                for match in matches:
                    owner, repo = match
                    repo_url = f"https://github.com/{owner}/{repo}"
                    
                    # Get basic repository information
                    try:
                        repo_info = self.repository_detector.extract_repo_info_from_url(repo_url)
                        repositories.append({
                            "url": repo_url,
                            "owner": repo_info["owner"],
                            "repo": repo_info["repo"]
                        })
                    except Exception as e:
                        print(f"Error processing repository {repo_url}: {e}")
            
            return repositories
        except Exception as e:
            print(f"Error detecting repositories: {e}")
            return [{"error": str(e)}]
    
    def analyze_video(self, video_id: str) -> Dict[str, Any]:
        """
        Analyze a YouTube video to extract all relevant information.
        
        Args:
            video_id: YouTube video ID.
            
        Returns:
            Dictionary containing comprehensive video analysis.
        """
        try:
            # Extract metadata
            metadata = self.extract_video_metadata(video_id)
            
            # Extract transcript
            transcript_data = self.extract_video_transcript(video_id)
            
            # Analyze transcript content
            content_analysis = self.analyze_transcript_content(transcript_data)
            
            # Detect repositories
            repositories = self.detect_repositories_in_transcript(transcript_data)
            
            # Combine all information
            analysis_result = {
                "metadata": metadata,
                "transcript": transcript_data,
                "content_analysis": content_analysis,
                "repositories": repositories
            }
            
            return analysis_result
        except Exception as e:
            print(f"Error analyzing video: {e}")
            return {"error": str(e)}
