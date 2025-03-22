"""
Git operations for cloning and managing repositories.
"""
import os
import subprocess
import shutil
from typing import Dict, List, Any, Optional, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GitOperations:
    """Class to handle Git operations for repositories."""
    
    def __init__(self, base_directory: str = "./repos"):
        """
        Initialize the GitOperations.
        
        Args:
            base_directory: Base directory for cloning repositories.
        """
        self.base_directory = base_directory
        os.makedirs(base_directory, exist_ok=True)
    
    def validate_git_url(self, url: str) -> bool:
        """
        Validate if a URL is a valid Git repository URL.
        
        Args:
            url: Repository URL to validate.
            
        Returns:
            True if valid, False otherwise.
        """
        # Check if URL is a GitHub URL
        if not url.startswith(("https://github.com/", "git@github.com:")):
            return False
        
        # Extract owner and repo name
        parts = url.rstrip("/").split("/")
        if len(parts) < 5 and "github.com" in url:
            return False
        
        return True
    
    def normalize_git_url(self, url: str) -> str:
        """
        Normalize a Git URL to a consistent format.
        
        Args:
            url: Repository URL to normalize.
            
        Returns:
            Normalized URL.
        """
        # Convert SSH URL to HTTPS
        if url.startswith("git@github.com:"):
            url = "https://github.com/" + url[15:]
        
        # Remove .git suffix if present
        if url.endswith(".git"):
            url = url[:-4]
        
        # Ensure URL ends with trailing slash
        if not url.endswith("/"):
            url = url + "/"
        
        return url
    
    def get_repo_name_from_url(self, url: str) -> Tuple[str, str]:
        """
        Extract owner and repository name from a Git URL.
        
        Args:
            url: Repository URL.
            
        Returns:
            Tuple containing (owner, repo_name).
        """
        normalized_url = self.normalize_git_url(url)
        parts = normalized_url.rstrip("/").split("/")
        
        if "github.com" in normalized_url:
            owner = parts[-2]
            repo_name = parts[-1]
            return owner, repo_name
        
        # Default fallback
        return "unknown", "unknown"
    
    def clone_repository(self, url: str, target_directory: Optional[str] = None) -> str:
        """
        Clone a Git repository.
        
        Args:
            url: Repository URL to clone.
            target_directory: Optional directory to clone into. If not provided, a
                directory will be created based on the repository name.
            
        Returns:
            Path to the cloned repository.
        """
        if not self.validate_git_url(url):
            raise ValueError(f"Invalid Git URL: {url}")
        
        owner, repo_name = self.get_repo_name_from_url(url)
        
        if target_directory is None:
            target_directory = os.path.join(self.base_directory, f"{owner}_{repo_name}")
        
        # Check if directory already exists
        if os.path.exists(target_directory):
            logger.info(f"Repository directory already exists: {target_directory}")
            return target_directory
        
        try:
            logger.info(f"Cloning repository: {url} to {target_directory}")
            
            result = subprocess.run(
                ["git", "clone", url, target_directory],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            logger.info(f"Clone successful: {result.stdout}")
            return target_directory
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to clone repository: {e.stderr}")
            raise
    
    def pull_latest_changes(self, repo_directory: str) -> bool:
        """
        Pull the latest changes for a repository.
        
        Args:
            repo_directory: Path to the repository directory.
            
        Returns:
            True if successful, False otherwise.
        """
        if not os.path.isdir(os.path.join(repo_directory, ".git")):
            logger.error(f"Not a Git repository: {repo_directory}")
            return False
        
        try:
            logger.info(f"Pulling latest changes for: {repo_directory}")
            
            result = subprocess.run(
                ["git", "pull"],
                cwd=repo_directory,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            logger.info(f"Pull successful: {result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to pull changes: {e.stderr}")
            return False
    
    def checkout_branch(self, repo_directory: str, branch: str) -> bool:
        """
        Checkout a specific branch in a repository.
        
        Args:
            repo_directory: Path to the repository directory.
            branch: Branch name to checkout.
            
        Returns:
            True if successful, False otherwise.
        """
        if not os.path.isdir(os.path.join(repo_directory, ".git")):
            logger.error(f"Not a Git repository: {repo_directory}")
            return False
        
        try:
            logger.info(f"Checking out branch {branch} in {repo_directory}")
            
            result = subprocess.run(
                ["git", "checkout", branch],
                cwd=repo_directory,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            logger.info(f"Checkout successful: {result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to checkout branch: {e.stderr}")
            return False
    
    def get_branches(self, repo_directory: str) -> List[str]:
        """
        Get list of branches in a repository.
        
        Args:
            repo_directory: Path to the repository directory.
            
        Returns:
            List of branch names.
        """
        if not os.path.isdir(os.path.join(repo_directory, ".git")):
            logger.error(f"Not a Git repository: {repo_directory}")
            return []
        
        try:
            result = subprocess.run(
                ["git", "branch", "-a"],
                cwd=repo_directory,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            branches = []
            for line in result.stdout.splitlines():
                line = line.strip()
                if line.startswith("*"):
                    # Current branch
                    branches.append(line[2:])
                elif line.startswith("remotes/origin/"):
                    # Remote branch
                    branch_name = line.split("remotes/origin/")[1]
                    if branch_name != "HEAD":
                        branches.append(branch_name)
                else:
                    # Local branch
                    branches.append(line)
            
            # Remove duplicates
            branches = list(set(branches))
            
            return branches
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get branches: {e.stderr}")
            return []
    
    def get_commit_history(self, repo_directory: str, max_commits: int = 10) -> List[Dict[str, str]]:
        """
        Get commit history for a repository.
        
        Args:
            repo_directory: Path to the repository directory.
            max_commits: Maximum number of commits to retrieve.
            
        Returns:
            List of commit dictionaries.
        """
        if not os.path.isdir(os.path.join(repo_directory, ".git")):
            logger.error(f"Not a Git repository: {repo_directory}")
            return []
        
        try:
            result = subprocess.run(
                ["git", "log", f"-{max_commits}", "--pretty=format:%H|%an|%ad|%s"],
                cwd=repo_directory,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            commits = []
            for line in result.stdout.splitlines():
                parts = line.split("|", 3)
                if len(parts) == 4:
                    commit = {
                        "hash": parts[0],
                        "author": parts[1],
                        "date": parts[2],
                        "message": parts[3]
                    }
                    commits.append(commit)
            
            return commits
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get commit history: {e.stderr}")
            return []
    
    def remove_repository(self, repo_directory: str) -> bool:
        """
        Remove a cloned repository.
        
        Args:
            repo_directory: Path to the repository directory.
            
        Returns:
            True if successful, False otherwise.
        """
        if not os.path.isdir(repo_directory):
            logger.warning(f"Repository directory does not exist: {repo_directory}")
            return False
        
        try:
            shutil.rmtree(repo_directory)
            logger.info(f"Repository removed successfully: {repo_directory}")
            return True
        except Exception as e:
            logger.error(f"Failed to remove repository: {str(e)}")
            return False
    
    def create_fork(self, repo_directory: str, fork_directory: str) -> bool:
        """
        Create a fork of a repository by copying it.
        
        Args:
            repo_directory: Path to the source repository directory.
            fork_directory: Path to the destination fork directory.
            
        Returns:
            True if successful, False otherwise.
        """
        if not os.path.isdir(os.path.join(repo_directory, ".git")):
            logger.error(f"Not a Git repository: {repo_directory}")
            return False
        
        if os.path.exists(fork_directory):
            logger.error(f"Destination directory already exists: {fork_directory}")
            return False
        
        try:
            # Copy the repository
            shutil.copytree(repo_directory, fork_directory)
            
            # Remove the .git directory to start fresh
            git_dir = os.path.join(fork_directory, ".git")
            if os.path.isdir(git_dir):
                shutil.rmtree(git_dir)
            
            # Initialize a new Git repository
            subprocess.run(
                ["git", "init"],
                cwd=fork_directory,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Add all files
            subprocess.run(
                ["git", "add", "."],
                cwd=fork_directory,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Commit
            subprocess.run(
                ["git", "commit", "-m", "Initial commit from fork"],
                cwd=fork_directory,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            logger.info(f"Fork created successfully: {fork_directory}")
            return True
        except Exception as e:
            logger.error(f"Failed to create fork: {str(e)}")
            return False
