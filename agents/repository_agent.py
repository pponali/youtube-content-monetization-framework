"""
Repository detection and analysis agent for GitHub repositories.
"""
import os
import tempfile
import subprocess
from typing import Dict, List, Any, Optional
from crewai import Agent, Task
from scraper.repository_detector import RepositoryDetector

class RepositoryAgent:
    """
    Agent specialized in detecting, cloning, and analyzing GitHub repositories.
    """
    
    def __init__(self, github_token: Optional[str] = None, output_dir: str = "output"):
        """
        Initialize the RepositoryAgent.
        
        Args:
            github_token: GitHub token for accessing repositories. If None, loads from environment.
            output_dir: Directory to store output files.
        """
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        if not self.github_token:
            raise ValueError("GitHub token is required. Set GITHUB_TOKEN environment variable or pass to constructor.")
        
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize components
        self.repository_detector = RepositoryDetector(github_token=self.github_token)
    
    def create_agent(self) -> Agent:
        """
        Create a CrewAI agent for repository analysis.
        
        Returns:
            CrewAI Agent configured for repository analysis.
        """
        return Agent(
            role="Repository Detective",
            goal="Identify, analyze, and extract valuable information from GitHub repositories mentioned in videos",
            backstory="You are a skilled software developer with expertise in analyzing codebases across various technologies. You can quickly understand repository structures and identify the technologies used.",
            verbose=True,
            allow_delegation=False,
            tools=[
                self.clone_repository,
                self.analyze_repository_structure,
                self.detect_technologies,
                self.analyze_dependencies,
                self.extract_build_instructions
            ]
        )
    
    def clone_repository(self, repo_url: str) -> Dict[str, Any]:
        """
        Clone a GitHub repository to a temporary directory.
        
        Args:
            repo_url: URL of the GitHub repository.
            
        Returns:
            Dictionary containing repository information and local path.
        """
        try:
            # Extract owner and repo name
            repo_info = self.repository_detector.extract_repo_info_from_url(repo_url)
            owner = repo_info["owner"]
            repo = repo_info["repo"]
            
            # Create a temporary directory for the repository
            temp_dir = tempfile.mkdtemp(prefix=f"{owner}_{repo}_")
            
            # Clone the repository
            clone_url = f"https://{self.github_token}@github.com/{owner}/{repo}.git"
            subprocess.run(["git", "clone", clone_url, temp_dir], check=True, capture_output=True)
            
            return {
                "owner": owner,
                "repo": repo,
                "url": repo_url,
                "local_path": temp_dir,
                "success": True
            }
        except Exception as e:
            print(f"Error cloning repository {repo_url}: {e}")
            return {
                "url": repo_url,
                "success": False,
                "error": str(e)
            }
    
    def analyze_repository_structure(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the structure of a cloned repository.
        
        Args:
            repo_data: Repository data from clone_repository.
            
        Returns:
            Dictionary containing repository structure analysis.
        """
        try:
            if not repo_data.get("success", False):
                return {"error": repo_data.get("error", "Unknown error")}
            
            local_path = repo_data["local_path"]
            
            # Get the directory structure
            structure = self._get_directory_structure(local_path)
            
            # Identify key files
            key_files = self._identify_key_files(local_path)
            
            return {
                "structure": structure,
                "key_files": key_files
            }
        except Exception as e:
            print(f"Error analyzing repository structure: {e}")
            return {"error": str(e)}
    
    def _get_directory_structure(self, path: str, max_depth: int = 3) -> Dict[str, Any]:
        """
        Get the directory structure of a repository.
        
        Args:
            path: Path to the repository.
            max_depth: Maximum depth to traverse.
            
        Returns:
            Dictionary representing the directory structure.
        """
        result = {}
        
        def _traverse(current_path, depth, current_dict):
            if depth > max_depth:
                return
            
            for item in os.listdir(current_path):
                item_path = os.path.join(current_path, item)
                
                # Skip hidden files and directories
                if item.startswith('.'):
                    continue
                
                if os.path.isdir(item_path):
                    current_dict[item] = {}
                    _traverse(item_path, depth + 1, current_dict[item])
                else:
                    current_dict[item] = None
        
        _traverse(path, 1, result)
        return result
    
    def _identify_key_files(self, path: str) -> Dict[str, List[str]]:
        """
        Identify key files in the repository.
        
        Args:
            path: Path to the repository.
            
        Returns:
            Dictionary mapping file categories to lists of file paths.
        """
        key_files = {
            "readme": [],
            "license": [],
            "configuration": [],
            "dependency": [],
            "documentation": [],
            "source_code": [],
            "test": [],
            "docker": [],
            "ci_cd": []
        }
        
        # Define patterns for each category
        patterns = {
            "readme": ["README.md", "README.txt", "readme.md"],
            "license": ["LICENSE", "LICENSE.md", "license.txt"],
            "configuration": [".env.example", "config.json", "settings.json", ".gitignore"],
            "dependency": ["requirements.txt", "package.json", "Pipfile", "Gemfile", "build.gradle", "pom.xml"],
            "documentation": ["docs/", "documentation/", "*.md"],
            "source_code": ["src/", "lib/", "app/", "main.py", "index.js"],
            "test": ["test/", "tests/", "*_test.py", "*_spec.js"],
            "docker": ["Dockerfile", "docker-compose.yml"],
            "ci_cd": [".github/workflows/", ".gitlab-ci.yml", ".travis.yml", "Jenkinsfile"]
        }
        
        for category, pattern_list in patterns.items():
            for pattern in pattern_list:
                if pattern.endswith('/'):
                    # It's a directory pattern
                    dir_name = pattern[:-1]
                    if os.path.isdir(os.path.join(path, dir_name)):
                        key_files[category].append(dir_name)
                elif '*' in pattern:
                    # It's a wildcard pattern
                    import glob
                    matches = glob.glob(os.path.join(path, pattern))
                    key_files[category].extend([os.path.basename(m) for m in matches])
                else:
                    # It's a specific file
                    if os.path.isfile(os.path.join(path, pattern)):
                        key_files[category].append(pattern)
        
        return key_files
    
    def detect_technologies(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect technologies used in the repository.
        
        Args:
            repo_data: Repository data from clone_repository.
            
        Returns:
            Dictionary containing detected technologies.
        """
        try:
            if not repo_data.get("success", False):
                return {"error": repo_data.get("error", "Unknown error")}
            
            local_path = repo_data["local_path"]
            
            # Use the repository detector to identify technologies
            technologies = self.repository_detector.detect_technologies(local_path)
            
            return {
                "languages": technologies.get("languages", {}),
                "frameworks": technologies.get("frameworks", []),
                "libraries": technologies.get("libraries", []),
                "tools": technologies.get("tools", [])
            }
        except Exception as e:
            print(f"Error detecting technologies: {e}")
            return {"error": str(e)}
    
    def analyze_dependencies(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze dependencies in the repository.
        
        Args:
            repo_data: Repository data from clone_repository.
            
        Returns:
            Dictionary containing dependency analysis.
        """
        try:
            if not repo_data.get("success", False):
                return {"error": repo_data.get("error", "Unknown error")}
            
            local_path = repo_data["local_path"]
            
            # Check for common dependency files
            dependency_files = {
                "python": ["requirements.txt", "Pipfile", "setup.py", "pyproject.toml"],
                "javascript": ["package.json", "yarn.lock", "package-lock.json"],
                "java": ["pom.xml", "build.gradle", "build.gradle.kts"],
                "ruby": ["Gemfile", "Gemfile.lock"],
                "php": ["composer.json", "composer.lock"],
                "dotnet": ["*.csproj", "*.fsproj", "packages.config"],
                "go": ["go.mod", "go.sum"]
            }
            
            dependencies = {}
            
            for lang, files in dependency_files.items():
                for file in files:
                    if '*' in file:
                        import glob
                        matches = glob.glob(os.path.join(local_path, file))
                        if matches:
                            dependencies[lang] = self._extract_dependencies_from_file(matches[0], lang)
                    else:
                        file_path = os.path.join(local_path, file)
                        if os.path.isfile(file_path):
                            dependencies[lang] = self._extract_dependencies_from_file(file_path, lang)
            
            return dependencies
        except Exception as e:
            print(f"Error analyzing dependencies: {e}")
            return {"error": str(e)}
    
    def _extract_dependencies_from_file(self, file_path: str, language: str) -> List[Dict[str, str]]:
        """
        Extract dependencies from a dependency file.
        
        Args:
            file_path: Path to the dependency file.
            language: Programming language.
            
        Returns:
            List of dependencies.
        """
        dependencies = []
        
        try:
            if language == "python" and file_path.endswith("requirements.txt"):
                with open(file_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            parts = line.split('==')
                            if len(parts) == 2:
                                dependencies.append({
                                    "name": parts[0],
                                    "version": parts[1]
                                })
                            else:
                                dependencies.append({
                                    "name": line,
                                    "version": "latest"
                                })
            
            elif language == "javascript" and file_path.endswith("package.json"):
                import json
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    
                    # Process dependencies
                    if "dependencies" in data:
                        for name, version in data["dependencies"].items():
                            dependencies.append({
                                "name": name,
                                "version": version,
                                "type": "production"
                            })
                    
                    # Process dev dependencies
                    if "devDependencies" in data:
                        for name, version in data["devDependencies"].items():
                            dependencies.append({
                                "name": name,
                                "version": version,
                                "type": "development"
                            })
            
            # Add more language-specific parsers as needed
            
        except Exception as e:
            print(f"Error extracting dependencies from {file_path}: {e}")
        
        return dependencies
    
    def extract_build_instructions(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract build instructions from the repository.
        
        Args:
            repo_data: Repository data from clone_repository.
            
        Returns:
            Dictionary containing build instructions.
        """
        try:
            if not repo_data.get("success", False):
                return {"error": repo_data.get("error", "Unknown error")}
            
            local_path = repo_data["local_path"]
            
            # Check for common build files
            build_files = [
                "Makefile",
                "package.json",
                "setup.py",
                "pom.xml",
                "build.gradle",
                "docker-compose.yml",
                "Dockerfile",
                "README.md"
            ]
            
            instructions = {}
            
            for file in build_files:
                file_path = os.path.join(local_path, file)
                if os.path.isfile(file_path):
                    if file == "README.md":
                        instructions["readme"] = self._extract_instructions_from_readme(file_path)
                    elif file == "package.json":
                        instructions["npm"] = self._extract_npm_scripts(file_path)
                    elif file == "Makefile":
                        instructions["make"] = self._extract_make_targets(file_path)
                    elif file == "docker-compose.yml":
                        instructions["docker_compose"] = ["docker-compose up"]
                    elif file == "Dockerfile":
                        instructions["docker"] = ["docker build -t <image_name> .", "docker run <image_name>"]
            
            return instructions
        except Exception as e:
            print(f"Error extracting build instructions: {e}")
            return {"error": str(e)}
    
    def _extract_instructions_from_readme(self, readme_path: str) -> List[str]:
        """
        Extract build/run instructions from README.md.
        
        Args:
            readme_path: Path to the README.md file.
            
        Returns:
            List of instructions.
        """
        instructions = []
        
        try:
            with open(readme_path, 'r') as f:
                content = f.read()
                
                # Look for common sections
                sections = ["## Installation", "## Getting Started", "## Build", "## Run", "## Usage"]
                
                for section in sections:
                    if section in content:
                        # Extract the section content
                        start_idx = content.find(section)
                        next_section_idx = float('inf')
                        
                        for s in sections:
                            if s != section and s in content[start_idx + len(section):]:
                                idx = content.find(s, start_idx + len(section))
                                next_section_idx = min(next_section_idx, idx)
                        
                        if next_section_idx == float('inf'):
                            section_content = content[start_idx:]
                        else:
                            section_content = content[start_idx:next_section_idx]
                        
                        # Extract code blocks
                        import re
                        code_blocks = re.findall(r'```(?:bash|shell|sh)?\n(.*?)\n```', section_content, re.DOTALL)
                        
                        for block in code_blocks:
                            # Split by lines and filter out empty lines
                            lines = [line.strip() for line in block.split('\n') if line.strip()]
                            instructions.extend(lines)
        
        except Exception as e:
            print(f"Error extracting instructions from README: {e}")
        
        return instructions
    
    def _extract_npm_scripts(self, package_json_path: str) -> List[str]:
        """
        Extract npm scripts from package.json.
        
        Args:
            package_json_path: Path to the package.json file.
            
        Returns:
            List of npm script commands.
        """
        scripts = []
        
        try:
            import json
            with open(package_json_path, 'r') as f:
                data = json.load(f)
                
                if "scripts" in data:
                    for name, command in data["scripts"].items():
                        scripts.append(f"npm run {name}")
        
        except Exception as e:
            print(f"Error extracting npm scripts: {e}")
        
        return scripts
    
    def _extract_make_targets(self, makefile_path: str) -> List[str]:
        """
        Extract make targets from Makefile.
        
        Args:
            makefile_path: Path to the Makefile.
            
        Returns:
            List of make commands.
        """
        targets = []
        
        try:
            with open(makefile_path, 'r') as f:
                content = f.read()
                
                # Extract targets using regex
                import re
                matches = re.findall(r'^([a-zA-Z0-9_-]+):\s*', content, re.MULTILINE)
                
                for match in matches:
                    if not match.startswith('.'):  # Skip internal targets
                        targets.append(f"make {match}")
        
        except Exception as e:
            print(f"Error extracting make targets: {e}")
        
        return targets
    
    def analyze_repository(self, repo_url: str) -> Dict[str, Any]:
        """
        Analyze a GitHub repository to extract all relevant information.
        
        Args:
            repo_url: URL of the GitHub repository.
            
        Returns:
            Dictionary containing comprehensive repository analysis.
        """
        try:
            # Clone the repository
            repo_data = self.clone_repository(repo_url)
            
            if not repo_data.get("success", False):
                return {"error": repo_data.get("error", "Failed to clone repository")}
            
            # Analyze repository structure
            structure_analysis = self.analyze_repository_structure(repo_data)
            
            # Detect technologies
            technology_analysis = self.detect_technologies(repo_data)
            
            # Analyze dependencies
            dependency_analysis = self.analyze_dependencies(repo_data)
            
            # Extract build instructions
            build_instructions = self.extract_build_instructions(repo_data)
            
            # Combine all information
            analysis_result = {
                "repository": {
                    "owner": repo_data["owner"],
                    "repo": repo_data["repo"],
                    "url": repo_data["url"]
                },
                "structure": structure_analysis,
                "technologies": technology_analysis,
                "dependencies": dependency_analysis,
                "build_instructions": build_instructions
            }
            
            return analysis_result
        except Exception as e:
            print(f"Error analyzing repository: {e}")
            return {"error": str(e)}
