#!/usr/bin/env python3
"""
Agentic Monetization Framework - Main Entry Point

This script provides a command-line interface to run the agentic monetization workflow
using CrewAI agents to analyze YouTube videos, detect repositories, build applications,
and generate monetization strategies.
"""

import os
import sys
import argparse
import logging
import json
import dotenv
from datetime import datetime

# Load environment variables
dotenv.load_dotenv()

# Import agent components
from agents.agent_orchestrator import AgentOrchestrator
from agents.video_analysis_agent import VideoAnalysisAgent
from agents.repository_agent import RepositoryAgent
from agents.app_building_agent import AppBuildingAgent
from agents.trend_analysis_agent import TrendAnalysisAgent
from agents.monetization_agent import MonetizationAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("agentic_monetization.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def check_environment():
    """Check if all required environment variables are set."""
    required_vars = {
        "YOUTUBE_API_KEY": "YouTube Data API key for video analysis",
        "GITHUB_TOKEN": "GitHub API token for repository analysis",
        "OPENAI_API_KEY": "OpenAI API key for CrewAI agents"
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"{var} ({description})")
    
    if missing_vars:
        logger.error("Missing required environment variables:")
        for var in missing_vars:
            logger.error(f"  - {var}")
        logger.error("Please set these variables in your .env file or environment.")
        return False
    
    return True

def process_video(video_id, output_dir="output", verbose=False):
    """
    Process a YouTube video through the agentic workflow.
    
    Args:
        video_id (str): YouTube video ID
        output_dir (str): Directory to save output files
        verbose (bool): Whether to print verbose output
    
    Returns:
        dict: Results of the processing
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_output_dir = os.path.join(output_dir, f"{video_id}_{timestamp}")
    os.makedirs(video_output_dir, exist_ok=True)
    
    logger.info(f"Processing video {video_id}")
    logger.info(f"Output will be saved to {video_output_dir}")
    
    # Initialize the agent orchestrator
    openai_api_key = os.getenv("OPENAI_API_KEY")
    orchestrator = AgentOrchestrator(openai_api_key=openai_api_key)
    
    try:
        # Run the full monetization workflow
        results = orchestrator.run_monetization_workflow(
            video_id=video_id,
            output_dir=video_output_dir,
            verbose=verbose
        )
        
        # Save the final results
        results_path = os.path.join(video_output_dir, "results.json")
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Processing completed. Results saved to {results_path}")
        
        # Generate a summary report
        summary = {
            "video_id": video_id,
            "processing_timestamp": timestamp,
            "output_directory": video_output_dir,
            "video_title": results.get("video_data", {}).get("metadata", {}).get("title", "Unknown"),
            "detected_repositories": len(results.get("repository_data", {}).get("repositories", [])),
            "trend_analysis": {
                "top_technology": results.get("trend_analysis", {}).get("technology_trends", {}).get("top_technology", {}).get("name", "Unknown"),
                "content_popularity": results.get("trend_analysis", {}).get("content_popularity", {}).get("popularity_level", "Unknown"),
                "market_opportunities": len(results.get("trend_analysis", {}).get("market_opportunities", {}).get("emerging_opportunities", []))
            },
            "monetization_strategies": len(results.get("monetization_strategies", {}).get("strategies", [])),
            "top_strategy": results.get("monetization_strategies", {}).get("top_strategy", "None")
        }
        
        summary_path = os.path.join(video_output_dir, "summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        
        return results
    
    except Exception as e:
        logger.error(f"Error processing video {video_id}: {str(e)}")
        error_path = os.path.join(video_output_dir, "error.json")
        with open(error_path, "w", encoding="utf-8") as f:
            json.dump({"error": str(e)}, f, indent=2)
        return {"error": str(e)}

def process_channel(channel_id, max_videos=5, output_dir="output", verbose=False):
    """
    Process videos from a YouTube channel through the agentic workflow.
    
    Args:
        channel_id (str): YouTube channel ID
        max_videos (int): Maximum number of videos to process
        output_dir (str): Directory to save output files
        verbose (bool): Whether to print verbose output
    
    Returns:
        dict: Results of the processing
    """
    from scraper.youtube_api import YouTubeAPI
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    channel_output_dir = os.path.join(output_dir, f"{channel_id}_{timestamp}")
    os.makedirs(channel_output_dir, exist_ok=True)
    
    logger.info(f"Processing channel {channel_id}")
    logger.info(f"Output will be saved to {channel_output_dir}")
    
    try:
        # Get videos from the channel
        youtube_api = YouTubeAPI(api_key=os.getenv("YOUTUBE_API_KEY"))
        channel_info = youtube_api.get_channel_info(channel_id)
        videos = youtube_api.get_channel_videos(channel_id, max_results=max_videos)
        
        logger.info(f"Found {len(videos)} videos in channel {channel_info.get('title', channel_id)}")
        
        # Save channel info
        channel_info_path = os.path.join(channel_output_dir, "channel_info.json")
        with open(channel_info_path, "w", encoding="utf-8") as f:
            json.dump(channel_info, f, indent=2)
        
        # Process each video
        results = []
        for video in videos:
            video_id = video.get("id", {}).get("videoId")
            if video_id:
                logger.info(f"Processing video {video_id}: {video.get('snippet', {}).get('title', 'Unknown')}")
                video_result = process_video(
                    video_id=video_id,
                    output_dir=os.path.join(channel_output_dir, "videos"),
                    verbose=verbose
                )
                results.append({
                    "video_id": video_id,
                    "title": video.get("snippet", {}).get("title", "Unknown"),
                    "result": video_result
                })
        
        # Save the final results
        results_path = os.path.join(channel_output_dir, "results.json")
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Channel processing completed. Results saved to {results_path}")
        
        return {
            "channel_id": channel_id,
            "channel_title": channel_info.get("title", channel_id),
            "videos_processed": len(results),
            "results": results
        }
    
    except Exception as e:
        logger.error(f"Error processing channel {channel_id}: {str(e)}")
        error_path = os.path.join(channel_output_dir, "error.json")
        with open(error_path, "w", encoding="utf-8") as f:
            json.dump({"error": str(e)}, f, indent=2)
        return {"error": str(e)}

def main():
    """Main entry point for the agentic monetization framework."""
    parser = argparse.ArgumentParser(
        description="YouTube Content Monetization Framework with Agentic Capabilities"
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Video command
    video_parser = subparsers.add_parser("video", help="Process a single YouTube video")
    video_parser.add_argument("video_id", help="YouTube video ID")
    video_parser.add_argument(
        "--output-dir", "-o", 
        default="output",
        help="Directory to save output files"
    )
    video_parser.add_argument(
        "--verbose", "-v", 
        action="store_true",
        help="Print verbose output"
    )
    
    # Channel command
    channel_parser = subparsers.add_parser("channel", help="Process videos from a YouTube channel")
    channel_parser.add_argument("channel_id", help="YouTube channel ID")
    channel_parser.add_argument(
        "--max-videos", "-m", 
        type=int, 
        default=5,
        help="Maximum number of videos to process"
    )
    channel_parser.add_argument(
        "--output-dir", "-o", 
        default="output",
        help="Directory to save output files"
    )
    channel_parser.add_argument(
        "--verbose", "-v", 
        action="store_true",
        help="Print verbose output"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check if command is provided
    if not args.command:
        parser.print_help()
        return
    
    # Check environment variables
    if not check_environment():
        return
    
    # Process command
    if args.command == "video":
        process_video(
            video_id=args.video_id,
            output_dir=args.output_dir,
            verbose=args.verbose
        )
    elif args.command == "channel":
        process_channel(
            channel_id=args.channel_id,
            max_videos=args.max_videos,
            output_dir=args.output_dir,
            verbose=args.verbose
        )

if __name__ == "__main__":
    main()
