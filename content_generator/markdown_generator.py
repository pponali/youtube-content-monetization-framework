"""
Generate markdown files from processed YouTube video data.
"""
import os
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

class MarkdownGenerator:
    """Class to generate markdown documents from processed video data."""
    
    def __init__(self, output_directory: str = "./knowledge_base"):
        """
        Initialize the MarkdownGenerator.
        
        Args:
            output_directory: Directory to save generated markdown files.
        """
        self.output_directory = output_directory
        os.makedirs(output_directory, exist_ok=True)
    
    def format_duration(self, seconds: int) -> str:
        """
        Format duration in seconds to a readable string.
        
        Args:
            seconds: Duration in seconds.
            
        Returns:
            Formatted duration string.
        """
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    def format_timestamp(self, seconds: int) -> str:
        """
        Format timestamp in seconds to HH:MM:SS.
        
        Args:
            seconds: Timestamp in seconds.
            
        Returns:
            Formatted timestamp string.
        """
        return str(timedelta(seconds=int(seconds))).zfill(8)
    
    def format_date(self, iso_date: str) -> str:
        """
        Format ISO date to a more readable format.
        
        Args:
            iso_date: ISO format date string.
            
        Returns:
            Formatted date string.
        """
        try:
            date = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
            return date.strftime("%B %d, %Y")
        except (ValueError, TypeError):
            return iso_date
    
    def generate_video_metadata_section(self, video_info: Dict[str, Any]) -> str:
        """
        Generate markdown section for video metadata.
        
        Args:
            video_info: Dictionary containing video information.
            
        Returns:
            Markdown string for video metadata section.
        """
        snippet = video_info.get("snippet", {})
        statistics = video_info.get("statistics", {})
        content_details = video_info.get("contentDetails", {})
        
        title = snippet.get("title", "Untitled Video")
        description = snippet.get("description", "No description available.")
        channel_title = snippet.get("channelTitle", "Unknown Channel")
        publish_date = self.format_date(snippet.get("publishedAt", ""))
        
        # Parse duration (in ISO 8601 format)
        duration_str = content_details.get("duration", "PT0S")
        duration_seconds = 0
        
        # Simple ISO 8601 duration parser
        if duration_str.startswith("PT"):
            duration_str = duration_str[2:]
            if "H" in duration_str:
                hours, duration_str = duration_str.split("H")
                duration_seconds += int(hours) * 3600
            if "M" in duration_str:
                minutes, duration_str = duration_str.split("M")
                duration_seconds += int(minutes) * 60
            if "S" in duration_str:
                seconds, duration_str = duration_str.split("S")
                duration_seconds += int(seconds)
        
        duration = self.format_duration(duration_seconds)
        
        # Format statistics
        view_count = statistics.get("viewCount", "0")
        like_count = statistics.get("likeCount", "0")
        comment_count = statistics.get("commentCount", "0")
        
        # Format numbers with commas for readability
        view_count = f"{int(view_count):,}"
        like_count = f"{int(like_count):,}"
        comment_count = f"{int(comment_count):,}"
        
        markdown = f"""# {title}

## Video Metadata

- **Channel**: {channel_title}
- **Published**: {publish_date}
- **Duration**: {duration}
- **Views**: {view_count}
- **Likes**: {like_count}
- **Comments**: {comment_count}

### Description

{description}

"""
        return markdown
    
    def generate_timestamps_section(self, timestamps: List[Dict[str, Any]]) -> str:
        """
        Generate markdown section for video timestamps.
        
        Args:
            timestamps: List of timestamp dictionaries.
            
        Returns:
            Markdown string for timestamps section.
        """
        if not timestamps:
            return ""
        
        markdown = "## Timestamps\n\n"
        
        for ts in timestamps:
            time_seconds = ts.get("time", 0)
            topic = ts.get("topic", "")
            
            formatted_time = self.format_timestamp(time_seconds)
            markdown += f"- [{formatted_time}] {topic}\n"
        
        markdown += "\n"
        return markdown
    
    def generate_summary_section(self, transcript_text: str, keywords: List[str]) -> str:
        """
        Generate markdown section for video summary.
        
        Args:
            transcript_text: Full transcript text.
            keywords: List of extracted keywords.
            
        Returns:
            Markdown string for summary section.
        """
        # In a real implementation, you might use an LLM to generate a proper summary
        # For now, we'll just include a keywords section
        
        markdown = "## Summary\n\n"
        
        # Add keywords section
        if keywords:
            markdown += "### Keywords\n\n"
            keyword_string = ", ".join(keywords)
            markdown += f"{keyword_string}\n\n"
        
        return markdown
    
    def generate_transcript_section(self, paragraphs: List[str]) -> str:
        """
        Generate markdown section for video transcript.
        
        Args:
            paragraphs: List of transcript paragraphs.
            
        Returns:
            Markdown string for transcript section.
        """
        if not paragraphs:
            return ""
        
        markdown = "## Transcript\n\n"
        
        for paragraph in paragraphs:
            markdown += f"{paragraph}\n\n"
        
        return markdown
    
    def generate_code_snippets_section(self, code_snippets: List[str]) -> str:
        """
        Generate markdown section for code snippets.
        
        Args:
            code_snippets: List of detected code snippets.
            
        Returns:
            Markdown string for code snippets section.
        """
        if not code_snippets:
            return ""
        
        markdown = "## Code Snippets\n\n"
        
        for i, snippet in enumerate(code_snippets, 1):
            markdown += f"### Snippet {i}\n\n```\n{snippet}\n```\n\n"
        
        return markdown
    
    def generate_repositories_section(self, repositories: List[Dict[str, Any]]) -> str:
        """
        Generate markdown section for GitHub repositories.
        
        Args:
            repositories: List of repository information dictionaries.
            
        Returns:
            Markdown string for repositories section.
        """
        if not repositories:
            return ""
        
        markdown = "## GitHub Repositories\n\n"
        
        for repo in repositories:
            url = repo.get("url", "")
            owner = repo.get("owner", "")
            repo_name = repo.get("repo", "")
            description = repo.get("github_info", {}).get("description", "No description available.")
            
            # Get repository statistics
            stars = repo.get("github_info", {}).get("stargazers_count", 0)
            forks = repo.get("github_info", {}).get("forks_count", 0)
            issues = repo.get("github_info", {}).get("open_issues_count", 0)
            
            # Get primary language
            languages = repo.get("languages", {})
            primary_language = max(languages.items(), key=lambda x: x[1])[0] if languages else "Unknown"
            
            # Get application type and build system
            app_type = repo.get("application_type", "Unknown")
            build_system = repo.get("build_system", "Unknown")
            
            markdown += f"### [{owner}/{repo_name}]({url})\n\n"
            markdown += f"{description}\n\n"
            markdown += f"- **Stars**: {stars}\n"
            markdown += f"- **Forks**: {forks}\n"
            markdown += f"- **Open Issues**: {issues}\n"
            markdown += f"- **Primary Language**: {primary_language}\n"
            markdown += f"- **Application Type**: {app_type}\n"
            markdown += f"- **Build System**: {build_system}\n\n"
            
            # Add build instructions if available
            build_instructions = repo.get("build_instructions", {})
            if build_instructions:
                markdown += "#### Build Instructions\n\n"
                
                if build_instructions.get("dependencies"):
                    markdown += "Install dependencies:\n\n```bash\n"
                    for cmd in build_instructions["dependencies"]:
                        markdown += f"{cmd}\n"
                    markdown += "```\n\n"
                
                if build_instructions.get("build"):
                    markdown += "Build:\n\n```bash\n"
                    for cmd in build_instructions["build"]:
                        markdown += f"{cmd}\n"
                    markdown += "```\n\n"
                
                if build_instructions.get("run"):
                    markdown += "Run:\n\n```bash\n"
                    for cmd in build_instructions["run"]:
                        markdown += f"{cmd}\n"
                    markdown += "```\n\n"
            
            # Add README section if available
            readme = repo.get("readme", "")
            if readme:
                markdown += "#### README Excerpt\n\n"
                
                # Limit README to first 500 characters
                if len(readme) > 500:
                    markdown += f"{readme[:500]}...\n\n"
                else:
                    markdown += f"{readme}\n\n"
        
        return markdown
    
    def generate_technologies_section(self, technologies: List[str]) -> str:
        """
        Generate markdown section for detected technologies.
        
        Args:
            technologies: List of detected technologies.
            
        Returns:
            Markdown string for technologies section.
        """
        if not technologies:
            return ""
        
        markdown = "## Technologies Mentioned\n\n"
        
        for tech in sorted(technologies):
            markdown += f"- {tech}\n"
        
        markdown += "\n"
        return markdown
    
    def generate_video_markdown(self, processed_data: Dict[str, Any], video_info: Dict[str, Any]) -> str:
        """
        Generate a complete markdown document for a video.
        
        Args:
            processed_data: Dictionary containing processed video data.
            video_info: Dictionary containing video information from YouTube API.
            
        Returns:
            Complete markdown document as a string.
        """
        # Generate each section
        metadata_section = self.generate_video_metadata_section(video_info)
        
        transcript_data = processed_data.get("transcript", {})
        transcript_successful = transcript_data.get("success", False)
        
        if transcript_successful:
            timestamps_section = self.generate_timestamps_section(transcript_data.get("timestamps", []))
            summary_section = self.generate_summary_section(
                transcript_data.get("full_text", ""),
                transcript_data.get("keywords", [])
            )
            transcript_section = self.generate_transcript_section(transcript_data.get("paragraphs", []))
            code_snippets_section = self.generate_code_snippets_section(transcript_data.get("code_snippets", []))
        else:
            timestamps_section = ""
            summary_section = "## Summary\n\nNo transcript available for this video.\n\n"
            transcript_section = ""
            code_snippets_section = ""
        
        repositories_section = self.generate_repositories_section(processed_data.get("repositories", []))
        technologies_section = self.generate_technologies_section(processed_data.get("technologies", []))
        
        # Combine all sections
        markdown = metadata_section
        markdown += summary_section
        markdown += timestamps_section
        markdown += technologies_section
        markdown += repositories_section
        markdown += code_snippets_section
        markdown += transcript_section
        
        return markdown
    
    def save_markdown(self, video_id: str, markdown_content: str) -> str:
        """
        Save markdown content to a file.
        
        Args:
            video_id: YouTube video ID.
            markdown_content: Markdown content to save.
            
        Returns:
            Path to the saved file.
        """
        file_path = os.path.join(self.output_directory, f"{video_id}.md")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        return file_path
    
    def generate_and_save(self, processed_data: Dict[str, Any], video_info: Dict[str, Any]) -> str:
        """
        Generate markdown for a video and save it to a file.
        
        Args:
            processed_data: Dictionary containing processed video data.
            video_info: Dictionary containing video information from YouTube API.
            
        Returns:
            Path to the saved file.
        """
        video_id = processed_data.get("video_id") or video_info.get("id")
        
        if not video_id:
            raise ValueError("Video ID not found in processed data or video info.")
        
        markdown_content = self.generate_video_markdown(processed_data, video_info)
        file_path = self.save_markdown(video_id, markdown_content)
        
        return file_path
    
    def generate_index(self, markdown_files: List[str], video_infos: List[Dict[str, Any]]) -> str:
        """
        Generate an index markdown file linking to all video knowledge base files.
        
        Args:
            markdown_files: List of paths to markdown files.
            video_infos: List of video information dictionaries.
            
        Returns:
            Path to the saved index file.
        """
        index_content = "# YouTube Knowledge Base Index\n\n"
        index_content += "This knowledge base contains information extracted from YouTube videos.\n\n"
        index_content += "## Videos\n\n"
        
        for i, (markdown_file, video_info) in enumerate(zip(markdown_files, video_infos), 1):
            snippet = video_info.get("snippet", {})
            title = snippet.get("title", f"Video {i}")
            channel_title = snippet.get("channelTitle", "Unknown Channel")
            publish_date = self.format_date(snippet.get("publishedAt", ""))
            
            file_name = os.path.basename(markdown_file)
            index_content += f"- [{title}](./{file_name}) - {channel_title} ({publish_date})\n"
        
        index_path = os.path.join(self.output_directory, "index.md")
        
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_content)
        
        return index_path
