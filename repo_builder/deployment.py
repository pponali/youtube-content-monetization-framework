"""
Deploy and run applications from GitHub repositories.
"""
import os
import json
import subprocess
import shutil
import time
from typing import Dict, List, Any, Optional, Tuple
import logging
from git_operations import GitOperations

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ApplicationDeployer:
    """Class to deploy and run applications from GitHub repositories."""
    
    def __init__(self, base_directory: str = "./deployments"):
        """
        Initialize the ApplicationDeployer.
        
        Args:
            base_directory: Base directory for deployments.
        """
        self.base_directory = base_directory
        os.makedirs(base_directory, exist_ok=True)
        
        self.git_ops = GitOperations()
    
    def detect_package_manager(self, repo_directory: str) -> str:
        """
        Detect the package manager used in a repository.
        
        Args:
            repo_directory: Path to the repository directory.
            
        Returns:
            Package manager name (npm, pip, etc.).
        """
        # Check for Node.js
        if os.path.exists(os.path.join(repo_directory, "package.json")):
            if os.path.exists(os.path.join(repo_directory, "yarn.lock")):
                return "yarn"
            else:
                return "npm"
        
        # Check for Python
        if os.path.exists(os.path.join(repo_directory, "requirements.txt")):
            return "pip"
        if os.path.exists(os.path.join(repo_directory, "Pipfile")):
            return "pipenv"
        if os.path.exists(os.path.join(repo_directory, "pyproject.toml")):
            if os.path.exists(os.path.join(repo_directory, "poetry.lock")):
                return "poetry"
        
        # Check for Java
        if os.path.exists(os.path.join(repo_directory, "pom.xml")):
            return "maven"
        if os.path.exists(os.path.join(repo_directory, "build.gradle")):
            return "gradle"
        
        # Check for Ruby
        if os.path.exists(os.path.join(repo_directory, "Gemfile")):
            return "bundler"
        
        # Check for Go
        if os.path.exists(os.path.join(repo_directory, "go.mod")):
            return "go"
        
        # Check for Rust
        if os.path.exists(os.path.join(repo_directory, "Cargo.toml")):
            return "cargo"
        
        # Default
        return "unknown"
    
    def detect_project_type(self, repo_directory: str) -> str:
        """
        Detect the type of project in a repository.
        
        Args:
            repo_directory: Path to the repository directory.
            
        Returns:
            Project type (web, cli, library, etc.).
        """
        # Check for Node.js web frameworks
        if os.path.exists(os.path.join(repo_directory, "package.json")):
            with open(os.path.join(repo_directory, "package.json"), "r") as f:
                try:
                    package_data = json.load(f)
                    dependencies = {**package_data.get("dependencies", {}), **package_data.get("devDependencies", {})}
                    
                    if "react" in dependencies:
                        return "react"
                    elif "vue" in dependencies:
                        return "vue"
                    elif "angular" in dependencies:
                        return "angular"
                    elif "express" in dependencies:
                        return "express"
                    elif "next" in dependencies:
                        return "nextjs"
                except json.JSONDecodeError:
                    pass
        
        # Check for Python web frameworks
        if os.path.exists(os.path.join(repo_directory, "requirements.txt")):
            with open(os.path.join(repo_directory, "requirements.txt"), "r") as f:
                content = f.read().lower()
                if "django" in content:
                    return "django"
                elif "flask" in content:
                    return "flask"
                elif "fastapi" in content:
                    return "fastapi"
        
        # Check for common files
        if os.path.exists(os.path.join(repo_directory, "public/index.html")) or os.path.exists(os.path.join(repo_directory, "index.html")):
            return "web"
        
        # Check for ML/Data Science projects
        python_files = [f for f in os.listdir(repo_directory) if f.endswith(".py")]
        for py_file in python_files:
            with open(os.path.join(repo_directory, py_file), "r") as f:
                content = f.read().lower()
                if "import tensorflow" in content or "import torch" in content or "import sklearn" in content:
                    return "machine-learning"
        
        # Default
        return "generic"
    
    def install_dependencies(self, repo_directory: str) -> bool:
        """
        Install dependencies for a repository.
        
        Args:
            repo_directory: Path to the repository directory.
            
        Returns:
            True if successful, False otherwise.
        """
        package_manager = self.detect_package_manager(repo_directory)
        
        try:
            if package_manager == "npm":
                logger.info(f"Installing npm dependencies in {repo_directory}")
                subprocess.run(
                    ["npm", "install"],
                    cwd=repo_directory,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            elif package_manager == "yarn":
                logger.info(f"Installing yarn dependencies in {repo_directory}")
                subprocess.run(
                    ["yarn", "install"],
                    cwd=repo_directory,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            elif package_manager == "pip":
                logger.info(f"Installing pip dependencies in {repo_directory}")
                # Create a virtual environment
                venv_dir = os.path.join(repo_directory, "venv")
                subprocess.run(
                    ["python", "-m", "venv", venv_dir],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                # Install dependencies
                pip_path = os.path.join(venv_dir, "bin", "pip") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "pip.exe")
                subprocess.run(
                    [pip_path, "install", "-r", "requirements.txt"],
                    cwd=repo_directory,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            elif package_manager == "pipenv":
                logger.info(f"Installing pipenv dependencies in {repo_directory}")
                subprocess.run(
                    ["pipenv", "install"],
                    cwd=repo_directory,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            elif package_manager == "poetry":
                logger.info(f"Installing poetry dependencies in {repo_directory}")
                subprocess.run(
                    ["poetry", "install"],
                    cwd=repo_directory,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            elif package_manager == "maven":
                logger.info(f"Installing Maven dependencies in {repo_directory}")
                subprocess.run(
                    ["mvn", "install", "-DskipTests"],
                    cwd=repo_directory,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            elif package_manager == "gradle":
                logger.info(f"Installing Gradle dependencies in {repo_directory}")
                subprocess.run(
                    ["./gradlew", "build", "-x", "test"],
                    cwd=repo_directory,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            elif package_manager == "bundler":
                logger.info(f"Installing Bundler dependencies in {repo_directory}")
                subprocess.run(
                    ["bundle", "install"],
                    cwd=repo_directory,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            elif package_manager == "go":
                logger.info(f"Installing Go dependencies in {repo_directory}")
                subprocess.run(
                    ["go", "mod", "download"],
                    cwd=repo_directory,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            elif package_manager == "cargo":
                logger.info(f"Installing Cargo dependencies in {repo_directory}")
                subprocess.run(
                    ["cargo", "build"],
                    cwd=repo_directory,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            else:
                logger.warning(f"Unknown package manager for {repo_directory}")
                return False
            
            logger.info(f"Dependencies installed successfully for {repo_directory}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e.stderr}")
            return False
    
    def build_project(self, repo_directory: str) -> bool:
        """
        Build a project.
        
        Args:
            repo_directory: Path to the repository directory.
            
        Returns:
            True if successful, False otherwise.
        """
        package_manager = self.detect_package_manager(repo_directory)
        project_type = self.detect_project_type(repo_directory)
        
        try:
            if package_manager == "npm" or package_manager == "yarn":
                # Check if there's a build script in package.json
                with open(os.path.join(repo_directory, "package.json"), "r") as f:
                    package_data = json.load(f)
                    scripts = package_data.get("scripts", {})
                    
                    if "build" in scripts:
                        command = "yarn" if package_manager == "yarn" else "npm"
                        logger.info(f"Building project with {command} in {repo_directory}")
                        subprocess.run(
                            [command, "run", "build"],
                            cwd=repo_directory,
                            check=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        return True
            
            elif package_manager == "maven":
                logger.info(f"Building project with Maven in {repo_directory}")
                subprocess.run(
                    ["mvn", "package", "-DskipTests"],
                    cwd=repo_directory,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                return True
            
            elif package_manager == "gradle":
                logger.info(f"Building project with Gradle in {repo_directory}")
                subprocess.run(
                    ["./gradlew", "build", "-x", "test"],
                    cwd=repo_directory,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                return True
            
            elif package_manager == "cargo":
                logger.info(f"Building project with Cargo in {repo_directory}")
                subprocess.run(
                    ["cargo", "build", "--release"],
                    cwd=repo_directory,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                return True
            
            elif project_type == "django":
                logger.info(f"Preparing Django project in {repo_directory}")
                # Activate virtual environment
                venv_dir = os.path.join(repo_directory, "venv")
                python_path = os.path.join(venv_dir, "bin", "python") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "python.exe")
                
                # Run migrations
                subprocess.run(
                    [python_path, "manage.py", "migrate"],
                    cwd=repo_directory,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                return True
            
            logger.info(f"No specific build step needed for {repo_directory}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to build project: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Error during build: {str(e)}")
            return False
    
    def get_run_command(self, repo_directory: str) -> Optional[List[str]]:
        """
        Get the command to run a project.
        
        Args:
            repo_directory: Path to the repository directory.
            
        Returns:
            List representing the command to run, or None if not determinable.
        """
        package_manager = self.detect_package_manager(repo_directory)
        project_type = self.detect_project_type(repo_directory)
        
        if package_manager == "npm" or package_manager == "yarn":
            with open(os.path.join(repo_directory, "package.json"), "r") as f:
                package_data = json.load(f)
                scripts = package_data.get("scripts", {})
                
                if "start" in scripts:
                    return [package_manager, "start"] if package_manager == "npm" else [package_manager, "run", "start"]
                elif "serve" in scripts:
                    return [package_manager, "run", "serve"]
                elif "dev" in scripts:
                    return [package_manager, "run", "dev"]
        
        elif project_type == "django":
            venv_dir = os.path.join(repo_directory, "venv")
            python_path = os.path.join(venv_dir, "bin", "python") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "python.exe")
            return [python_path, "manage.py", "runserver", "0.0.0.0:8000"]
        
        elif project_type == "flask":
            venv_dir = os.path.join(repo_directory, "venv")
            python_path = os.path.join(venv_dir, "bin", "python") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "python.exe")
            
            # Look for app.py or similar files
            app_files = ["app.py", "main.py", "wsgi.py", "application.py"]
            for app_file in app_files:
                if os.path.exists(os.path.join(repo_directory, app_file)):
                    return [python_path, app_file]
        
        elif project_type == "fastapi":
            venv_dir = os.path.join(repo_directory, "venv")
            python_path = os.path.join(venv_dir, "bin", "python") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "python.exe")
            uvicorn_path = os.path.join(venv_dir, "bin", "uvicorn") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "uvicorn.exe")
            
            # Look for main.py or app.py
            if os.path.exists(os.path.join(repo_directory, "main.py")):
                return [uvicorn_path, "main:app", "--host", "0.0.0.0", "--reload"]
            elif os.path.exists(os.path.join(repo_directory, "app.py")):
                return [uvicorn_path, "app:app", "--host", "0.0.0.0", "--reload"]
        
        return None
    
    def run_application(self, repo_directory: str) -> Optional[subprocess.Popen]:
        """
        Run a deployed application.
        
        Args:
            repo_directory: Path to the repository directory.
            
        Returns:
            Subprocess object for the running application, or None if failed.
        """
        run_command = self.get_run_command(repo_directory)
        
        if not run_command:
            logger.error(f"Could not determine how to run the application in {repo_directory}")
            return None
        
        try:
            logger.info(f"Starting application in {repo_directory} with command: {' '.join(run_command)}")
            
            # Run the application as a subprocess
            process = subprocess.Popen(
                run_command,
                cwd=repo_directory,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a bit to make sure the application starts properly
            time.sleep(3)
            
            if process.poll() is not None:
                # Process has terminated
                stderr = process.stderr.read() if process.stderr else ""
                logger.error(f"Application failed to start: {stderr}")
                return None
            
            logger.info(f"Application started successfully with PID {process.pid}")
            return process
        except Exception as e:
            logger.error(f"Error running application: {str(e)}")
            return None
    
    def deploy_repository(self, repo_url: str) -> Dict[str, Any]:
        """
        Deploy a repository - clone, install dependencies, build, and run.
        
        Args:
            repo_url: URL of the repository to deploy.
            
        Returns:
            Dictionary with deployment information.
        """
        result = {
            "repository_url": repo_url,
            "success": False,
            "steps": []
        }
        
        # Step 1: Clone the repository
        try:
            owner, repo_name = self.git_ops.get_repo_name_from_url(repo_url)
            deploy_dir = os.path.join(self.base_directory, f"{owner}_{repo_name}")
            
            # Clone the repository
            result["steps"].append({"step": "clone", "status": "in_progress"})
            repo_dir = self.git_ops.clone_repository(repo_url, deploy_dir)
            result["steps"][-1] = {"step": "clone", "status": "success", "directory": repo_dir}
            
            # Step 2: Install dependencies
            result["steps"].append({"step": "install_dependencies", "status": "in_progress"})
            if self.install_dependencies(repo_dir):
                result["steps"][-1] = {"step": "install_dependencies", "status": "success"}
            else:
                result["steps"][-1] = {"step": "install_dependencies", "status": "failed"}
                result["error"] = "Failed to install dependencies"
                return result
            
            # Step 3: Build the project
            result["steps"].append({"step": "build", "status": "in_progress"})
            if self.build_project(repo_dir):
                result["steps"][-1] = {"step": "build", "status": "success"}
            else:
                result["steps"][-1] = {"step": "build", "status": "failed"}
                result["error"] = "Failed to build project"
                return result
            
            # Step 4: Get run command
            result["steps"].append({"step": "get_run_command", "status": "in_progress"})
            run_command = self.get_run_command(repo_dir)
            if run_command:
                result["steps"][-1] = {"step": "get_run_command", "status": "success", "command": " ".join(run_command)}
            else:
                result["steps"][-1] = {"step": "get_run_command", "status": "failed"}
                result["error"] = "Could not determine how to run the application"
                result["success"] = True  # We consider this a partial success
                return result
            
            # Optional Step 5: Run the application
            # Note: This step is optional, depending on whether you want to run the application automatically
            
            result["success"] = True
            result["repository_info"] = {
                "owner": owner,
                "name": repo_name,
                "directory": repo_dir,
                "package_manager": self.detect_package_manager(repo_dir),
                "project_type": self.detect_project_type(repo_dir),
                "run_command": run_command
            }
            
            return result
        except Exception as e:
            logger.error(f"Error during deployment: {str(e)}")
            result["error"] = str(e)
            return result
    
    def get_deployment_status(self, repo_dir: str) -> Dict[str, Any]:
        """
        Get the status of a deployed repository.
        
        Args:
            repo_dir: Path to the repository directory.
            
        Returns:
            Dictionary with status information.
        """
        if not os.path.isdir(repo_dir):
            return {"exists": False}
        
        package_manager = self.detect_package_manager(repo_dir)
        project_type = self.detect_project_type(repo_dir)
        run_command = self.get_run_command(repo_dir)
        
        return {
            "exists": True,
            "directory": repo_dir,
            "package_manager": package_manager,
            "project_type": project_type,
            "run_command": run_command
        }
