"""
YouTube API connector for extracting video and channel data.
"""
import os
from typing import Dict, List, Optional, Any
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class YouTubeAPI:
    """Class to interact with the YouTube Data API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the YouTube API client.
        
        Args:
            api_key: YouTube Data API key. If None, loads from environment variables.
        """
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YouTube API key is required. Set YOUTUBE_API_KEY environment variable or pass to constructor.")
        
        self.youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=self.api_key
        )
    
    def get_channel_info(self, channel_id: str) -> Dict[str, Any]:
        """
        Get information about a YouTube channel.
        
        Args:
            channel_id: The YouTube channel ID.
            
        Returns:
            Dictionary containing channel information.
        """
        try:
            request = self.youtube.channels().list(
                part="snippet,contentDetails,statistics",
                id=channel_id
            )
            response = request.execute()
            
            if "items" in response and response["items"]:
                return response["items"][0]
            else:
                raise ValueError(f"Channel ID not found: {channel_id}")
        except HttpError as e:
            print(f"Error retrieving channel info: {e}")
            raise
    
    def get_channel_id_from_username(self, username: str) -> str:
        """
        Get channel ID from a YouTube username.
        
        Args:
            username: YouTube channel username.
            
        Returns:
            YouTube channel ID.
        """
        try:
            request = self.youtube.channels().list(
                part="id",
                forUsername=username
            )
            response = request.execute()
            
            if "items" in response and response["items"]:
                return response["items"][0]["id"]
            else:
                raise ValueError(f"Username not found: {username}")
        except HttpError as e:
            print(f"Error retrieving channel ID: {e}")
            raise
    
    def get_videos_from_channel(self, channel_id: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Get videos from a YouTube channel.
        
        Args:
            channel_id: YouTube channel ID.
            max_results: Maximum number of videos to retrieve.
            
        Returns:
            List of video information dictionaries.
        """
        try:
            # First, get the channel's uploads playlist
            request = self.youtube.channels().list(
                part="contentDetails",
                id=channel_id
            )
            response = request.execute()
            
            uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            
            # Now, get the videos from the uploads playlist
            videos = []
            next_page_token = None
            
            while len(videos) < max_results:
                playlist_request = self.youtube.playlistItems().list(
                    part="snippet,contentDetails",
                    playlistId=uploads_playlist_id,
                    maxResults=min(50, max_results - len(videos)),
                    pageToken=next_page_token
                )
                playlist_response = playlist_request.execute()
                
                videos.extend(playlist_response["items"])
                next_page_token = playlist_response.get("nextPageToken")
                
                if not next_page_token:
                    break
            
            return videos[:max_results]
        except HttpError as e:
            print(f"Error retrieving videos: {e}")
            raise
    
    def get_video_details(self, video_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific video.
        
        Args:
            video_id: YouTube video ID.
            
        Returns:
            Dictionary containing video details.
        """
        try:
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics,topicDetails",
                id=video_id
            )
            response = request.execute()
            
            if "items" in response and response["items"]:
                return response["items"][0]
            else:
                raise ValueError(f"Video ID not found: {video_id}")
        except HttpError as e:
            print(f"Error retrieving video details: {e}")
            raise
    
    def get_video_transcript(self, video_id: str) -> str:
        """
        Get the transcript of a YouTube video.
        Note: This is a placeholder as the YouTube Data API doesn't provide transcripts.
        You'll need to use a library like youtube_transcript_api to get actual transcripts.
        
        Args:
            video_id: YouTube video ID.
            
        Returns:
            Video transcript as text.
        """
        # This is a placeholder - YouTube Data API doesn't provide transcripts
        # In a real implementation, you would use youtube_transcript_api or another solution
        return f"Transcript retrieval not implemented for video ID: {video_id}"

    def search_videos(self, query: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Search for YouTube videos matching a query.
        
        Args:
            query: Search query string.
            max_results: Maximum number of results to return.
            
        Returns:
            List of video information dictionaries.
        """
        try:
            request = self.youtube.search().list(
                part="snippet",
                q=query,
                type="video",
                maxResults=min(50, max_results)
            )
            response = request.execute()
            
            return response.get("items", [])
        except HttpError as e:
            print(f"Error searching videos: {e}")
            raise
            
    def get_video_comments(self, video_id: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Get comments for a YouTube video.
        
        Args:
            video_id: YouTube video ID.
            max_results: Maximum number of comments to retrieve.
            
        Returns:
            List of comment dictionaries.
        """
        try:
            comments = []
            next_page_token = None
            
            while len(comments) < max_results:
                request = self.youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=min(100, max_results - len(comments)),
                    pageToken=next_page_token
                )
                response = request.execute()
                
                comments.extend(response["items"])
                next_page_token = response.get("nextPageToken")
                
                if not next_page_token:
                    break
            
            return comments[:max_results]
        except HttpError as e:
            # Comments might be disabled for the video
            if e.resp.status == 403:
                print(f"Comments are disabled for video ID: {video_id}")
                return []
            else:
                print(f"Error retrieving comments: {e}")
                raise
