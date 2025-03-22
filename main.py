"""
Main application entry point for the YouTube Content Monetization Framework.
"""
import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

from scraper.youtube_api import YouTubeAPI
from scraper.video_processor import VideoProcessor
from scraper.transcript_extractor import TranscriptExtractor
from scraper.repository_detector import RepositoryDetector
from content_generator.markdown_generator import MarkdownGenerator
from content_generator.social_media_content import SocialMediaContentGenerator
from repo_builder.git_operations import GitOperations
from repo_builder.deployment import Deployment
from monetization.strategy_generator import MonetizationStrategyGenerator
from monetization.trend_analyzer import TrendAnalyzer

class YouTubeMonetizationFramework:
    """Main class for the YouTube Content Monetization Framework."""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the YouTube Monetization Framework.
        
        Args:
            output_dir: Directory to store output files.
        """
        # Check for required environment variables
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        self.github_token = os.getenv("GITHUB_TOKEN")
        
        if not self.youtube_api_key:
            print("WARNING: YOUTUBE_API_KEY environment variable not set. YouTube API features will be limited.")
        
        if not self.github_token:
            print("WARNING: GITHUB_TOKEN environment variable not set. GitHub API features will be limited.")
        
        # Initialize output directory
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize components
        self.youtube_api = YouTubeAPI(api_key=self.youtube_api_key)
        self.video_processor = VideoProcessor(output_dir=os.path.join(output_dir, "videos"))
        self.transcript_extractor = TranscriptExtractor()
        self.repository_detector = RepositoryDetector(github_token=self.github_token)
        self.markdown_generator = MarkdownGenerator()
        self.social_media_generator = SocialMediaContentGenerator()
        self.git_operations = GitOperations(github_token=self.github_token)
        self.deployment = Deployment()
        self.strategy_generator = MonetizationStrategyGenerator()
        self.trend_analyzer = TrendAnalyzer(github_token=self.github_token)
    
    def process_video(self, video_id: str) -> Dict[str, Any]:
        """
        Process a single YouTube video.
        
        Args:
            video_id: YouTube video ID.
            
        Returns:
            Dictionary containing all processed data.
        """
        print(f"Processing video ID: {video_id}")
        
        # Create directory for this video
        video_dir = os.path.join(self.output_dir, video_id)
        os.makedirs(video_dir, exist_ok=True)
        
        # Step 1: Get video details from YouTube API
        video_info = self.youtube_api.get_video_details(video_id)
        
        if not video_info:
            print(f"Error: Could not retrieve video information for {video_id}")
            return {}
        
        print(f"Retrieved video information: {video_info['title']}")
        
        # Step 2: Download video for processing
        video_path = self.video_processor.download_video(video_id)
        
        if not video_path:
            print(f"Error: Could not download video {video_id}")
            return video_info
        
        print(f"Downloaded video to: {video_path}")
        
        # Step 3: Extract transcript
        transcript = self.transcript_extractor.get_transcript(video_id)
        
        if not transcript:
            print(f"Warning: Could not extract transcript for {video_id}")
            transcript = {"text": "", "language": "en"}
        else:
            print(f"Extracted transcript of length: {len(transcript['text'])}")
        
        # Process transcript to extract paragraphs and keywords
        processed_transcript = self.transcript_extractor.process_transcript(transcript["text"])
        transcript.update(processed_transcript)
        
        # Step 4: Process video to detect technologies and code
        print("Processing video to detect technologies and code...")
        video_processing_results = self.video_processor.process_video(video_path)
        
        # Step 5: Detect GitHub repositories
        print("Detecting GitHub repositories...")
        repositories = self.repository_detector.detect_repositories(transcript["text"])
        
        for repo in repositories:
            print(f"Detected repository: {repo['repo']}")
            repo.update(self.repository_detector.analyze_repository(repo["repo"]))
        
        # Step 6: Generate markdown knowledge base
        print("Generating markdown knowledge base...")
        markdown_content = self.markdown_generator.generate_markdown(
            video_info=video_info,
            transcript=transcript,
            technologies=video_processing_results.get("technologies", []),
            repositories=repositories
        )
        
        markdown_path = os.path.join(video_dir, f"{video_id}.md")
        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        print(f"Markdown knowledge base saved to: {markdown_path}")
        
        # Step 7: Generate social media content
        print("Generating social media content ideas...")
        social_media_content = self.social_media_generator.generate_content(
            video_info=video_info,
            transcript=transcript,
            technologies=video_processing_results.get("technologies", []),
            repositories=repositories
        )
        
        social_media_path = os.path.join(video_dir, f"{video_id}_social_media.json")
        with open(social_media_path, "w", encoding="utf-8") as f:
            json.dump(social_media_content, f, indent=2)
        
        print(f"Social media content ideas saved to: {social_media_path}")
        
        # Step 8: Generate monetization strategies
        print("Generating monetization strategies...")
        # Prepare video data for strategy generation
        video_data = {
            "video_id": video_id,
            "video_title": video_info["title"],
            "transcript": transcript,
            "technologies": video_processing_results.get("technologies", []),
            "repositories": repositories
        }
        
        monetization_strategies = self.strategy_generator.generate_strategies(video_data)
        
        strategies_path = os.path.join(video_dir, f"{video_id}_monetization_strategies.json")
        with open(strategies_path, "w", encoding="utf-8") as f:
            json.dump(monetization_strategies, f, indent=2)
        
        print(f"Monetization strategies saved to: {strategies_path}")
        
        # Step 9: Analyze technology trends
        if video_processing_results.get("technologies", []):
            print("Analyzing technology trends...")
            tech_trends = self.trend_analyzer.analyze_technology_trends(
                video_processing_results.get("technologies", [])
            )
            
            trends_path = os.path.join(video_dir, f"{video_id}_tech_trends.json")
            with open(trends_path, "w", encoding="utf-8") as f:
                json.dump(tech_trends, f, indent=2)
            
            print(f"Technology trend analysis saved to: {trends_path}")
        
        # Step 10: Analyze repository market fit
        if repositories:
            print("Analyzing repository market fit...")
            for i, repo in enumerate(repositories):
                market_fit = self.trend_analyzer.analyze_repository_market_fit(repo)
                
                market_fit_path = os.path.join(video_dir, f"{video_id}_repo_{i}_market_fit.json")
                with open(market_fit_path, "w", encoding="utf-8") as f:
                    json.dump(market_fit, f, indent=2)
                
                print(f"Repository market fit analysis saved to: {market_fit_path}")
        
        # Compile all the data
        result = {
            "video_id": video_id,
            "video_info": video_info,
            "transcript": transcript,
            "video_processing_results": video_processing_results,
            "repositories": repositories,
            "paths": {
                "markdown": markdown_path,
                "social_media": social_media_path,
                "strategies": strategies_path
            }
        }
        
        # Save the complete result
        result_path = os.path.join(video_dir, f"{video_id}_complete.json")
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        
        print(f"Complete processing results saved to: {result_path}")
        
        return result
    
    def process_channel(self, channel_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Process videos from a YouTube channel.
        
        Args:
            channel_id: YouTube channel ID.
            limit: Maximum number of videos to process.
            
        Returns:
            List of dictionaries containing processed data for each video.
        """
        print(f"Processing channel ID: {channel_id}")
        
        # Get channel information
        channel_info = self.youtube_api.get_channel_info(channel_id)
        
        if not channel_info:
            print(f"Error: Could not retrieve channel information for {channel_id}")
            return []
        
        print(f"Processing channel: {channel_info['title']}")
        
        # Get videos from the channel
        videos = self.youtube_api.get_channel_videos(channel_id, limit=limit)
        
        if not videos:
            print(f"Error: Could not retrieve videos for channel {channel_id}")
            return []
        
        print(f"Retrieved {len(videos)} videos from the channel")
        
        # Process each video
        results = []
        for video in videos:
            result = self.process_video(video["id"])
            if result:
                results.append(result)
        
        # Save overall channel results
        channel_dir = os.path.join(self.output_dir, channel_id)
        os.makedirs(channel_dir, exist_ok=True)
        
        channel_result = {
            "channel_id": channel_id,
            "channel_info": channel_info,
            "processed_videos": [r["video_id"] for r in results],
            "video_count": len(results)
        }
        
        channel_result_path = os.path.join(channel_dir, f"{channel_id}_summary.json")
        with open(channel_result_path, "w", encoding="utf-8") as f:
            json.dump(channel_result, f, indent=2)
        
        print(f"Channel processing summary saved to: {channel_result_path}")
        
        return results
    
    def clone_and_analyze_repository(self, repo_url: str, output_subdir: str = "repos") -> Dict[str, Any]:
        """
        Clone and analyze a GitHub repository.
        
        Args:
            repo_url: GitHub repository URL.
            output_subdir: Subdirectory under output_dir to clone to.
            
        Returns:
            Dictionary containing repository analysis.
        """
        print(f"Cloning and analyzing repository: {repo_url}")
        
        # Create directory for repositories
        repo_dir = os.path.join(self.output_dir, output_subdir)
        os.makedirs(repo_dir, exist_ok=True)
        
        # Clone the repository
        repo_info = self.git_operations.clone_repository(repo_url, repo_dir)
        
        if not repo_info:
            print(f"Error: Could not clone repository {repo_url}")
            return {}
        
        print(f"Repository cloned to: {repo_info['local_path']}")
        
        # Analyze the repository
        repo_analysis = self.repository_detector.analyze_repository(repo_url)
        repo_info.update(repo_analysis)
        
        # Get market fit analysis
        market_fit = self.trend_analyzer.analyze_repository_market_fit(repo_info)
        repo_info["market_fit"] = market_fit
        
        # Generate monetization strategies
        video_data = {
            "video_id": "direct_repo",
            "video_title": repo_info.get("name", repo_url),
            "technologies": repo_info.get("languages", {}).keys(),
            "repositories": [repo_info]
        }
        
        monetization_strategies = self.strategy_generator.generate_strategies(video_data)
        repo_info["monetization_strategies"] = monetization_strategies
        
        # Save the repository analysis
        repo_name = repo_info.get("name", repo_url.split("/")[-1])
        result_path = os.path.join(repo_dir, f"{repo_name}_analysis.json")
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(repo_info, f, indent=2)
        
        print(f"Repository analysis saved to: {result_path}")
        
        return repo_info
    
    def deploy_repository(self, repo_info: Dict[str, Any]) -> bool:
        """
        Deploy a repository application.
        
        Args:
            repo_info: Repository information from clone_and_analyze_repository.
            
        Returns:
            Boolean indicating success.
        """
        if not repo_info or not repo_info.get("local_path"):
            print("Error: Invalid repository information")
            return False
        
        print(f"Deploying repository: {repo_info.get('name', '')}")
        
        # Deploy the repository
        success = self.deployment.deploy_repository(
            repo_path=repo_info["local_path"],
            app_type=repo_info.get("application_type", "unknown")
        )
        
        if success:
            print(f"Repository deployed successfully: {repo_info.get('name', '')}")
        else:
            print(f"Error: Could not deploy repository {repo_info.get('name', '')}")
        
        return success


def main():
    """Main function to run the application."""
    parser = argparse.ArgumentParser(description="YouTube Content Monetization Framework")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Video processing command
    video_parser = subparsers.add_parser("video", help="Process a YouTube video")
    video_parser.add_argument("video_id", help="YouTube video ID to process")
    video_parser.add_argument("--output", "-o", default="output", help="Output directory")
    
    # Channel processing command
    channel_parser = subparsers.add_parser("channel", help="Process a YouTube channel")
    channel_parser.add_argument("channel_id", help="YouTube channel ID to process")
    channel_parser.add_argument("--limit", "-l", type=int, default=5, help="Maximum number of videos to process")
    channel_parser.add_argument("--output", "-o", default="output", help="Output directory")
    
    # Repository processing command
    repo_parser = subparsers.add_parser("repo", help="Clone and analyze a GitHub repository")
    repo_parser.add_argument("repo_url", help="GitHub repository URL to analyze")
    repo_parser.add_argument("--output", "-o", default="output", help="Output directory")
    repo_parser.add_argument("--deploy", "-d", action="store_true", help="Deploy the repository application")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    framework = YouTubeMonetizationFramework(output_dir=args.output)
    
    if args.command == "video":
        framework.process_video(args.video_id)
    elif args.command == "channel":
        framework.process_channel(args.channel_id, limit=args.limit)
    elif args.command == "repo":
        repo_info = framework.clone_and_analyze_repository(args.repo_url)
        if args.deploy and repo_info:
            framework.deploy_repository(repo_info)


if __name__ == "__main__":
    main()
