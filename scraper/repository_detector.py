"""
Detect and analyze GitHub repositories mentioned in YouTube videos.
"""
import os
import re
import json
import subprocess
from typing import Dict, List, Any, Optional
import requests
from urllib.parse import urlparse

class RepositoryDetector:
    """Class to detect and analyze GitHub repositories."""
    
    def __init__(self, github_token: Optional[str] = None, clone_path: str = "./repositories"):
        """
        Initialize the RepositoryDetector.
        
        Args:
            github_token: GitHub API token for authenticated requests.
            clone_path: Directory to clone repositories to.
        """
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.clone_path = clone_path
        os.makedirs(clone_path, exist_ok=True)
        
        # Set up headers for GitHub API requests
        self.headers = {}
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"
    
    def extract_repo_info_from_url(self, url: str) -> Dict[str, str]:
        """
        Extract owner and repository name from a GitHub URL.
        
        Args:
            url: GitHub repository URL.
            
        Returns:
            Dictionary with 'owner' and 'repo' keys.
        """
        parsed_url = urlparse(url)
        
        if parsed_url.netloc not in ["github.com", "www.github.com"]:
            raise ValueError(f"Not a GitHub URL: {url}")
        
        path_parts = parsed_url.path.strip("/").split("/")
        
        if len(path_parts) < 2:
            raise ValueError(f"Invalid GitHub repository URL: {url}")
        
        return {
            "owner": path_parts[0],
            "repo": path_parts[1]
        }
    
    def get_repository_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        Get information about a GitHub repository using the GitHub API.
        
        Args:
            owner: Repository owner (username or organization).
            repo: Repository name.
            
        Returns:
            Dictionary containing repository information.
        """
        url = f"https://api.github.com/repos/{owner}/{repo}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repository info: {e}")
            return {}
    
    def get_repository_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """
        Get languages used in a GitHub repository.
        
        Args:
            owner: Repository owner (username or organization).
            repo: Repository name.
            
        Returns:
            Dictionary mapping language names to byte counts.
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/languages"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repository languages: {e}")
            return {}
    
    def get_repository_readme(self, owner: str, repo: str) -> str:
        """
        Get the README content of a GitHub repository.
        
        Args:
            owner: Repository owner (username or organization).
            repo: Repository name.
            
        Returns:
            README content as text.
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        
        try:
            response = requests.get(url, headers=self.headers, params={"accept": "application/vnd.github.raw"})
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repository README: {e}")
            return ""
    
    def clone_repository(self, url: str) -> str:
        """
        Clone a GitHub repository.
        
        Args:
            url: GitHub repository URL.
            
        Returns:
            Path to the cloned repository.
        """
        try:
            repo_info = self.extract_repo_info_from_url(url)
            owner, repo = repo_info["owner"], repo_info["repo"]
            
            clone_dir = os.path.join(self.clone_path, f"{owner}_{repo}")
            
            # Clone the repository
            subprocess.run(
                ["git", "clone", url, clone_dir],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            return clone_dir
        except (ValueError, subprocess.CalledProcessError) as e:
            print(f"Error cloning repository: {e}")
            return ""
    
    def analyze_repository_structure(self, repo_path: str) -> Dict[str, Any]:
        """
        Analyze the structure of a cloned repository.
        
        Args:
            repo_path: Path to the cloned repository.
            
        Returns:
            Dictionary containing repository structure information.
        """
        if not os.path.isdir(repo_path):
            return {}
        
        result = {
            "files": [],
            "directories": [],
            "file_count": 0,
            "directory_count": 0,
            "file_types": {},
            "has_package_json": False,
            "has_requirements_txt": False,
            "has_pipfile": False,
            "has_dockerfile": False,
            "has_docker_compose": False,
            "has_ci_config": False
        }
        
        for root, dirs, files in os.walk(repo_path):
            # Skip hidden directories and __pycache__
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            # Get relative path from repo root
            rel_path = os.path.relpath(root, repo_path)
            if rel_path != '.':
                result["directories"].append(rel_path)
                result["directory_count"] += 1
            
            for file in files:
                # Skip hidden files
                if file.startswith('.'):
                    continue
                
                file_path = os.path.join(rel_path, file)
                result["files"].append(file_path)
                result["file_count"] += 1
                
                # Track file extensions
                _, ext = os.path.splitext(file)
                if ext:
                    ext = ext[1:]  # Remove the leading dot
                    result["file_types"][ext] = result["file_types"].get(ext, 0) + 1
                
                # Check for special files
                lower_file = file.lower()
                if lower_file == 'package.json':
                    result["has_package_json"] = True
                elif lower_file == 'requirements.txt':
                    result["has_requirements_txt"] = True
                elif lower_file == 'pipfile':
                    result["has_pipfile"] = True
                elif lower_file == 'dockerfile':
                    result["has_dockerfile"] = True
                elif lower_file in ('docker-compose.yml', 'docker-compose.yaml'):
                    result["has_docker_compose"] = True
                elif lower_file in ('.travis.yml', '.github/workflows', '.gitlab-ci.yml', 'jenkinsfile'):
                    result["has_ci_config"] = True
        
        return result
    
    def detect_build_system(self, repo_path: str) -> str:
        """
        Detect the build system used in a repository.
        
        Args:
            repo_path: Path to the cloned repository.
            
        Returns:
            Name of the detected build system.
        """
        build_systems = {
            "npm": os.path.exists(os.path.join(repo_path, "package.json")),
            "yarn": os.path.exists(os.path.join(repo_path, "yarn.lock")),
            "pip": os.path.exists(os.path.join(repo_path, "requirements.txt")),
            "pipenv": os.path.exists(os.path.join(repo_path, "Pipfile")),
            "poetry": os.path.exists(os.path.join(repo_path, "pyproject.toml")),
            "gradle": os.path.exists(os.path.join(repo_path, "build.gradle")),
            "maven": os.path.exists(os.path.join(repo_path, "pom.xml")),
            "cargo": os.path.exists(os.path.join(repo_path, "Cargo.toml")),
            "go": os.path.exists(os.path.join(repo_path, "go.mod")),
            "make": os.path.exists(os.path.join(repo_path, "Makefile")),
            "cmake": os.path.exists(os.path.join(repo_path, "CMakeLists.txt")),
        }
        
        for system, exists in build_systems.items():
            if exists:
                return system
        
        return "unknown"
    
    def detect_application_type(self, repo_path: str) -> str:
        """
        Detect the type of application in a repository.
        
        Args:
            repo_path: Path to the cloned repository.
            
        Returns:
            Type of application.
        """
        # Check for web frameworks
        if os.path.exists(os.path.join(repo_path, "package.json")):
            with open(os.path.join(repo_path, "package.json"), "r") as f:
                try:
                    package_json = json.load(f)
                    dependencies = {**package_json.get("dependencies", {}), **package_json.get("devDependencies", {})}
                    
                    if "react" in dependencies:
                        return "react"
                    elif "vue" in dependencies:
                        return "vue"
                    elif "angular" in dependencies:
                        return "angular"
                    elif "express" in dependencies:
                        return "express"
                    elif "next" in dependencies:
                        return "next.js"
                except json.JSONDecodeError:
                    pass
        
        # Check for Python frameworks
        requirements_path = os.path.join(repo_path, "requirements.txt")
        if os.path.exists(requirements_path):
            with open(requirements_path, "r") as f:
                requirements = f.read().lower()
                
                if "django" in requirements:
                    return "django"
                elif "flask" in requirements:
                    return "flask"
                elif "fastapi" in requirements:
                    return "fastapi"
                elif "pytorch" in requirements or "torch" in requirements:
                    return "pytorch"
                elif "tensorflow" in requirements:
                    return "tensorflow"
        
        # Check for Java frameworks
        if os.path.exists(os.path.join(repo_path, "pom.xml")):
            with open(os.path.join(repo_path, "pom.xml"), "r") as f:
                pom_content = f.read().lower()
                
                if "spring-boot" in pom_content:
                    return "spring-boot"
        
        return "unknown"
    
    def generate_build_instructions(self, repo_path: str) -> Dict[str, List[str]]:
        """
        Generate build instructions for a repository.
        
        Args:
            repo_path: Path to the cloned repository.
            
        Returns:
            Dictionary with 'dependencies' and 'build' instructions.
        """
        build_system = self.detect_build_system(repo_path)
        app_type = self.detect_application_type(repo_path)
        
        instructions = {
            "dependencies": [],
            "build": [],
            "run": []
        }
        
        if build_system == "npm" or build_system == "yarn":
            instructions["dependencies"] = [
                f"{build_system} install"
            ]
            
            # Check package.json for scripts
            if os.path.exists(os.path.join(repo_path, "package.json")):
                with open(os.path.join(repo_path, "package.json"), "r") as f:
                    try:
                        package_json = json.load(f)
                        scripts = package_json.get("scripts", {})
                        
                        if "build" in scripts:
                            instructions["build"] = [f"{build_system} run build"]
                        
                        if "start" in scripts:
                            instructions["run"] = [f"{build_system} start"]
                        elif "dev" in scripts:
                            instructions["run"] = [f"{build_system} run dev"]
                    except json.JSONDecodeError:
                        pass
        
        elif build_system == "pip":
            instructions["dependencies"] = [
                "pip install -r requirements.txt"
            ]
            
            # Check for common Python entry points
            if os.path.exists(os.path.join(repo_path, "manage.py")) and app_type == "django":
                instructions["run"] = [
                    "python manage.py migrate",
                    "python manage.py runserver"
                ]
            elif os.path.exists(os.path.join(repo_path, "app.py")) or os.path.exists(os.path.join(repo_path, "main.py")):
                entry_point = "app.py" if os.path.exists(os.path.join(repo_path, "app.py")) else "main.py"
                instructions["run"] = [f"python {entry_point}"]
        
        elif build_system == "gradle":
            instructions["dependencies"] = [
                "./gradlew build"
            ]
            instructions["run"] = [
                "./gradlew run"
            ]
        
        elif build_system == "maven":
            instructions["dependencies"] = [
                "mvn clean install"
            ]
            instructions["run"] = [
                "mvn spring-boot:run" if app_type == "spring-boot" else "java -jar target/*.jar"
            ]
        
        elif build_system == "make":
            instructions["dependencies"] = [
                "make"
            ]
            instructions["run"] = [
                "./bin/main" if os.path.exists(os.path.join(repo_path, "bin/main")) else "./main"
            ]
        
        return instructions
    
    def process_repository(self, repo_url: str) -> Dict[str, Any]:
        """
        Process a GitHub repository to extract information.
        
        Args:
            repo_url: GitHub repository URL.
            
        Returns:
            Dictionary containing extracted repository information.
        """
        try:
            repo_info = self.extract_repo_info_from_url(repo_url)
            owner, repo = repo_info["owner"], repo_info["repo"]
            
            result = {
                "url": repo_url,
                "owner": owner,
                "repo": repo,
                "github_info": self.get_repository_info(owner, repo),
                "languages": self.get_repository_languages(owner, repo),
                "readme": self.get_repository_readme(owner, repo)
            }
            
            # Clone the repository for further analysis
            clone_path = self.clone_repository(repo_url)
            if clone_path:
                result["structure"] = self.analyze_repository_structure(clone_path)
                result["build_system"] = self.detect_build_system(clone_path)
                result["application_type"] = self.detect_application_type(clone_path)
                result["build_instructions"] = self.generate_build_instructions(clone_path)
            
            return result
        except Exception as e:
            print(f"Error processing repository {repo_url}: {e}")
            return {
                "url": repo_url,
                "error": str(e)
            }
