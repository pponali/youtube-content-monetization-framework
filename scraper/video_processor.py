"""
Process YouTube videos to extract valuable information.
"""
import os
import re
import json
from typing import Dict, List, Any, Optional
import yt_dlp
import cv2
import numpy as np
from PIL import Image
import pytesseract
from transformers import pipeline

class VideoProcessor:
    """Class to process YouTube videos and extract information."""
    
    def __init__(self, download_path: str = "./downloads"):
        """
        Initialize the VideoProcessor.
        
        Args:
            download_path: Directory to store downloaded videos.
        """
        self.download_path = download_path
        os.makedirs(download_path, exist_ok=True)
        
        # Initialize the text detection model for frames
        self.text_detector = pipeline("text-detection", model="Xenova/layoutlmv3-base")
        
    def download_video(self, video_id: str) -> str:
        """
        Download a YouTube video.
        
        Args:
            video_id: YouTube video ID.
            
        Returns:
            Path to the downloaded video file.
        """
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        ydl_opts = {
            'format': 'best[height<=720]',  # Limit to 720p for processing efficiency
            'outtmpl': os.path.join(self.download_path, f'{video_id}.%(ext)s'),
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_path = ydl.prepare_filename(info_dict)
            
        return video_path
    
    def extract_frames(self, video_path: str, frequency: int = 30) -> List[np.ndarray]:
        """
        Extract frames from a video at a specified frequency.
        
        Args:
            video_path: Path to the video file.
            frequency: Extract one frame every 'frequency' seconds.
            
        Returns:
            List of extracted frames as numpy arrays.
        """
        frames = []
        video = cv2.VideoCapture(video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * frequency)
        
        success, frame = video.read()
        count = 0
        
        while success:
            if count % frame_interval == 0:
                # Convert from BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(rgb_frame)
            
            success, frame = video.read()
            count += 1
        
        video.release()
        return frames
    
    def detect_text_in_frame(self, frame: np.ndarray) -> List[str]:
        """
        Detect and extract text from a video frame.
        
        Args:
            frame: Video frame as numpy array.
            
        Returns:
            List of detected text strings.
        """
        # Convert numpy array to PIL Image
        pil_image = Image.fromarray(frame)
        
        # Extract text using pytesseract
        text = pytesseract.image_to_string(pil_image)
        
        # Split text into lines and filter out empty lines
        text_lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        return text_lines
    
    def detect_github_repositories(self, text_lines: List[str]) -> List[str]:
        """
        Detect GitHub repository URLs in text.
        
        Args:
            text_lines: List of text strings.
            
        Returns:
            List of detected GitHub repository URLs.
        """
        github_patterns = [
            r'https?://(?:www\.)?github\.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)',
            r'github\.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)',
            r'([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+) on GitHub'
        ]
        
        repositories = []
        
        for line in text_lines:
            for pattern in github_patterns:
                matches = re.findall(pattern, line)
                for match in matches:
                    if isinstance(match, tuple):
                        owner, repo = match
                        repo_url = f"https://github.com/{owner}/{repo}"
                        repositories.append(repo_url)
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(repositories))
    
    def detect_technologies(self, text_lines: List[str]) -> List[str]:
        """
        Detect mentioned technologies in text.
        
        Args:
            text_lines: List of text strings.
            
        Returns:
            List of detected technologies.
        """
        # Common programming languages, frameworks, and tools
        tech_keywords = [
            'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'C#', 'Ruby', 'Go', 'Rust',
            'React', 'Angular', 'Vue', 'Node.js', 'Express', 'Django', 'Flask', 'Spring Boot',
            'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'Pandas', 'NumPy',
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Firebase',
            'MongoDB', 'PostgreSQL', 'MySQL', 'SQLite', 'Redis', 'Elasticsearch',
            'Git', 'GitHub', 'GitLab', 'Bitbucket',
            'REST API', 'GraphQL', 'WebSocket', 'gRPC',
            'CI/CD', 'Jenkins', 'Travis CI', 'GitHub Actions',
            'Agile', 'Scrum', 'Kanban',
            'AI', 'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision'
        ]
        
        detected_tech = set()
        
        for line in text_lines:
            for tech in tech_keywords:
                # Case-insensitive matching for technology names
                if re.search(r'\b' + re.escape(tech) + r'\b', line, re.IGNORECASE):
                    detected_tech.add(tech)
        
        return list(detected_tech)
    
    def process_video(self, video_id: str, download: bool = True) -> Dict[str, Any]:
        """
        Process a YouTube video to extract information.
        
        Args:
            video_id: YouTube video ID.
            download: Whether to download the video for processing.
            
        Returns:
            Dictionary containing extracted information.
        """
        result = {
            'video_id': video_id,
            'github_repositories': [],
            'technologies': [],
            'detected_text': []
        }
        
        if download:
            try:
                video_path = self.download_video(video_id)
                frames = self.extract_frames(video_path)
                
                all_text_lines = []
                
                for frame in frames:
                    text_lines = self.detect_text_in_frame(frame)
                    all_text_lines.extend(text_lines)
                    result['detected_text'].extend(text_lines)
                
                # Detect GitHub repositories and technologies
                result['github_repositories'] = self.detect_github_repositories(all_text_lines)
                result['technologies'] = self.detect_technologies(all_text_lines)
                
                # Clean up the downloaded video
                os.remove(video_path)
            except Exception as e:
                print(f"Error processing video {video_id}: {e}")
        
        return result
