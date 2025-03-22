"""
Application building agent for setting up and running applications from GitHub repositories.
"""
import os
import subprocess
import tempfile
import shutil
from typing import Dict, List, Any, Optional
from crewai import Agent, Task

class AppBuildingAgent:
    """
    Agent specialized in building and running applications from GitHub repositories.
    """
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the AppBuildingAgent.
        
        Args:
            output_dir: Directory to store output files.
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def create_agent(self) -> Agent:
        """
        Create a CrewAI agent for application building.
        
        Returns:
            CrewAI Agent configured for application building.
        """
        return Agent(
            role="Application Builder",
            goal="Build functional applications from GitHub repositories by understanding their structure and requirements",
            backstory="You are a full-stack developer with experience in multiple programming languages and frameworks. You excel at setting up development environments and getting applications running quickly.",
            verbose=True,
            allow_delegation=False,
            tools=[
                self.setup_environment,
                self.install_dependencies,
                self.build_application,
                self.run_application,
                self.document_setup_process
            ]
        )
    
    def setup_environment(self, repo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Set up the development environment for the repository.
        
        Args:
            repo_analysis: Repository analysis data.
            
        Returns:
            Dictionary containing environment setup information.
        """
        try:
            if "error" in repo_analysis:
                return {"error": repo_analysis["error"]}
            
            # Extract repository information
            repo_url = repo_analysis.get("repository", {}).get("url", "")
            if not repo_url:
                return {"error": "Repository URL not found in analysis data"}
            
            # Create a working directory
            working_dir = tempfile.mkdtemp(prefix="app_build_")
            
            # Clone the repository
            subprocess.run(["git", "clone", repo_url, working_dir], check=True, capture_output=True)
            
            # Determine the programming language and framework
            technologies = repo_analysis.get("technologies", {})
            languages = technologies.get("languages", {})
            frameworks = technologies.get("frameworks", [])
            
            # Set up environment based on detected technologies
            environment_setup = {
                "working_dir": working_dir,
                "detected_languages": languages,
                "detected_frameworks": frameworks,
                "environment_variables": {},
                "setup_commands": []
            }
            
            # Set up language-specific environments
            if "python" in languages:
                # Set up Python virtual environment
                venv_dir = os.path.join(working_dir, "venv")
                subprocess.run(["python", "-m", "venv", venv_dir], check=True, capture_output=True)
                
                # Add activation commands
                if os.name == "nt":  # Windows
                    activate_script = os.path.join(venv_dir, "Scripts", "activate")
                    environment_setup["setup_commands"].append(f"{activate_script}")
                else:  # Unix/Linux/MacOS
                    activate_script = os.path.join(venv_dir, "bin", "activate")
                    environment_setup["setup_commands"].append(f"source {activate_script}")
                
                environment_setup["venv_dir"] = venv_dir
            
            elif "javascript" in languages or "typescript" in languages:
                # Check for Node.js version requirements
                package_json_path = os.path.join(working_dir, "package.json")
                if os.path.isfile(package_json_path):
                    import json
                    with open(package_json_path, 'r') as f:
                        package_data = json.load(f)
                        
                        # Check for engines specification
                        if "engines" in package_data and "node" in package_data["engines"]:
                            environment_setup["node_version"] = package_data["engines"]["node"]
                            environment_setup["setup_commands"].append(f"# Requires Node.js {package_data['engines']['node']}")
            
            # Add framework-specific setup
            for framework in frameworks:
                if framework.lower() in ["django", "flask", "fastapi"]:
                    environment_setup["setup_commands"].append("# Python web application detected")
                    environment_setup["environment_variables"]["PYTHONPATH"] = working_dir
                
                elif framework.lower() in ["react", "vue", "angular"]:
                    environment_setup["setup_commands"].append("# JavaScript frontend framework detected")
                
                elif framework.lower() in ["express", "nest.js", "koa"]:
                    environment_setup["setup_commands"].append("# Node.js backend framework detected")
            
            return environment_setup
        except Exception as e:
            print(f"Error setting up environment: {e}")
            return {"error": str(e)}
    
    def install_dependencies(self, environment_setup: Dict[str, Any]) -> Dict[str, Any]:
        """
        Install dependencies for the application.
        
        Args:
            environment_setup: Environment setup data from setup_environment.
            
        Returns:
            Dictionary containing dependency installation information.
        """
        try:
            if "error" in environment_setup:
                return {"error": environment_setup["error"]}
            
            working_dir = environment_setup["working_dir"]
            detected_languages = environment_setup["detected_languages"]
            
            dependency_results = {
                "working_dir": working_dir,
                "installation_commands": [],
                "success": True,
                "logs": []
            }
            
            # Install Python dependencies
            if "python" in detected_languages:
                requirements_file = os.path.join(working_dir, "requirements.txt")
                setup_py_file = os.path.join(working_dir, "setup.py")
                pipfile = os.path.join(working_dir, "Pipfile")
                
                if os.path.isfile(requirements_file):
                    # Use the virtual environment's pip if available
                    if "venv_dir" in environment_setup:
                        if os.name == "nt":  # Windows
                            pip_path = os.path.join(environment_setup["venv_dir"], "Scripts", "pip")
                        else:  # Unix/Linux/MacOS
                            pip_path = os.path.join(environment_setup["venv_dir"], "bin", "pip")
                        
                        cmd = [pip_path, "install", "-r", requirements_file]
                    else:
                        cmd = ["pip", "install", "-r", requirements_file]
                    
                    dependency_results["installation_commands"].append(" ".join(cmd))
                    try:
                        result = subprocess.run(cmd, check=True, capture_output=True, cwd=working_dir)
                        dependency_results["logs"].append(result.stdout.decode())
                    except subprocess.CalledProcessError as e:
                        dependency_results["success"] = False
                        dependency_results["logs"].append(e.stderr.decode())
                
                elif os.path.isfile(setup_py_file):
                    # Install package in development mode
                    if "venv_dir" in environment_setup:
                        if os.name == "nt":  # Windows
                            pip_path = os.path.join(environment_setup["venv_dir"], "Scripts", "pip")
                        else:  # Unix/Linux/MacOS
                            pip_path = os.path.join(environment_setup["venv_dir"], "bin", "pip")
                        
                        cmd = [pip_path, "install", "-e", "."]
                    else:
                        cmd = ["pip", "install", "-e", "."]
                    
                    dependency_results["installation_commands"].append(" ".join(cmd))
                    try:
                        result = subprocess.run(cmd, check=True, capture_output=True, cwd=working_dir)
                        dependency_results["logs"].append(result.stdout.decode())
                    except subprocess.CalledProcessError as e:
                        dependency_results["success"] = False
                        dependency_results["logs"].append(e.stderr.decode())
                
                elif os.path.isfile(pipfile):
                    # Install using pipenv
                    cmd = ["pipenv", "install"]
                    dependency_results["installation_commands"].append(" ".join(cmd))
                    try:
                        result = subprocess.run(cmd, check=True, capture_output=True, cwd=working_dir)
                        dependency_results["logs"].append(result.stdout.decode())
                    except subprocess.CalledProcessError as e:
                        dependency_results["success"] = False
                        dependency_results["logs"].append(e.stderr.decode())
            
            # Install JavaScript/TypeScript dependencies
            elif "javascript" in detected_languages or "typescript" in detected_languages:
                package_json = os.path.join(working_dir, "package.json")
                
                if os.path.isfile(package_json):
                    # Check for yarn.lock or package-lock.json to determine package manager
                    yarn_lock = os.path.isfile(os.path.join(working_dir, "yarn.lock"))
                    
                    if yarn_lock:
                        cmd = ["yarn", "install"]
                    else:
                        cmd = ["npm", "install"]
                    
                    dependency_results["installation_commands"].append(" ".join(cmd))
                    try:
                        result = subprocess.run(cmd, check=True, capture_output=True, cwd=working_dir)
                        dependency_results["logs"].append(result.stdout.decode())
                    except subprocess.CalledProcessError as e:
                        dependency_results["success"] = False
                        dependency_results["logs"].append(e.stderr.decode())
            
            # Add support for other languages as needed
            
            return dependency_results
        except Exception as e:
            print(f"Error installing dependencies: {e}")
            return {"error": str(e)}
    
    def build_application(self, dependency_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build the application.
        
        Args:
            dependency_results: Dependency installation data from install_dependencies.
            
        Returns:
            Dictionary containing build information.
        """
        try:
            if "error" in dependency_results:
                return {"error": dependency_results["error"]}
            
            if not dependency_results.get("success", False):
                return {"error": "Dependency installation failed", "logs": dependency_results.get("logs", [])}
            
            working_dir = dependency_results["working_dir"]
            
            build_results = {
                "working_dir": working_dir,
                "build_commands": [],
                "success": True,
                "logs": []
            }
            
            # Check for common build files
            package_json = os.path.join(working_dir, "package.json")
            makefile = os.path.join(working_dir, "Makefile")
            setup_py = os.path.join(working_dir, "setup.py")
            
            # Build JavaScript/TypeScript application
            if os.path.isfile(package_json):
                import json
                with open(package_json, 'r') as f:
                    package_data = json.load(f)
                    
                    # Check for build script
                    if "scripts" in package_data and "build" in package_data["scripts"]:
                        # Check for yarn.lock or package-lock.json to determine package manager
                        yarn_lock = os.path.isfile(os.path.join(working_dir, "yarn.lock"))
                        
                        if yarn_lock:
                            cmd = ["yarn", "build"]
                        else:
                            cmd = ["npm", "run", "build"]
                        
                        build_results["build_commands"].append(" ".join(cmd))
                        try:
                            result = subprocess.run(cmd, check=True, capture_output=True, cwd=working_dir)
                            build_results["logs"].append(result.stdout.decode())
                        except subprocess.CalledProcessError as e:
                            build_results["success"] = False
                            build_results["logs"].append(e.stderr.decode())
            
            # Build using Makefile
            elif os.path.isfile(makefile):
                cmd = ["make", "build"]
                build_results["build_commands"].append(" ".join(cmd))
                try:
                    result = subprocess.run(cmd, check=True, capture_output=True, cwd=working_dir)
                    build_results["logs"].append(result.stdout.decode())
                except subprocess.CalledProcessError as e:
                    # Try make without arguments
                    try:
                        cmd = ["make"]
                        build_results["build_commands"].append(" ".join(cmd))
                        result = subprocess.run(cmd, check=True, capture_output=True, cwd=working_dir)
                        build_results["logs"].append(result.stdout.decode())
                    except subprocess.CalledProcessError as e2:
                        build_results["success"] = False
                        build_results["logs"].append(e2.stderr.decode())
            
            # Build Python package
            elif os.path.isfile(setup_py):
                cmd = ["python", "setup.py", "build"]
                build_results["build_commands"].append(" ".join(cmd))
                try:
                    result = subprocess.run(cmd, check=True, capture_output=True, cwd=working_dir)
                    build_results["logs"].append(result.stdout.decode())
                except subprocess.CalledProcessError as e:
                    build_results["success"] = False
                    build_results["logs"].append(e.stderr.decode())
            
            # If no build command was found, mark as skipped
            if not build_results["build_commands"]:
                build_results["build_commands"].append("# No build step detected")
                build_results["skipped"] = True
            
            return build_results
        except Exception as e:
            print(f"Error building application: {e}")
            return {"error": str(e)}
    
    def run_application(self, build_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the application.
        
        Args:
            build_results: Build data from build_application.
            
        Returns:
            Dictionary containing run information.
        """
        try:
            if "error" in build_results:
                return {"error": build_results["error"]}
            
            if not build_results.get("success", False) and not build_results.get("skipped", False):
                return {"error": "Build failed", "logs": build_results.get("logs", [])}
            
            working_dir = build_results["working_dir"]
            
            run_results = {
                "working_dir": working_dir,
                "run_commands": [],
                "success": True,
                "logs": [],
                "port": None,
                "is_web_app": False
            }
            
            # Check for common run files
            package_json = os.path.join(working_dir, "package.json")
            procfile = os.path.join(working_dir, "Procfile")
            manage_py = os.path.join(working_dir, "manage.py")
            app_py = os.path.join(working_dir, "app.py")
            main_py = os.path.join(working_dir, "main.py")
            docker_compose = os.path.join(working_dir, "docker-compose.yml")
            
            # Run JavaScript/TypeScript application
            if os.path.isfile(package_json):
                import json
                with open(package_json, 'r') as f:
                    package_data = json.load(f)
                    
                    # Check for start script
                    if "scripts" in package_data:
                        start_script = None
                        
                        # Look for start scripts in order of preference
                        for script_name in ["start", "serve", "dev", "develop"]:
                            if script_name in package_data["scripts"]:
                                start_script = script_name
                                break
                        
                        if start_script:
                            # Check for yarn.lock or package-lock.json to determine package manager
                            yarn_lock = os.path.isfile(os.path.join(working_dir, "yarn.lock"))
                            
                            if yarn_lock:
                                cmd = ["yarn", start_script]
                            else:
                                cmd = ["npm", "run", start_script]
                            
                            run_results["run_commands"].append(" ".join(cmd))
                            
                            # Don't actually run the command, just provide the command
                            # as it might be a long-running process
                            
                            # Check if it's likely a web app
                            if "dependencies" in package_data:
                                web_frameworks = ["react", "vue", "angular", "next", "nuxt", "express", "koa", "hapi", "fastify"]
                                for framework in web_frameworks:
                                    if any(framework in dep.lower() for dep in package_data["dependencies"]):
                                        run_results["is_web_app"] = True
                                        run_results["port"] = 3000  # Default for many JS frameworks
                                        break
            
            # Run Django application
            elif os.path.isfile(manage_py):
                cmd = ["python", "manage.py", "runserver", "0.0.0.0:8000"]
                run_results["run_commands"].append(" ".join(cmd))
                run_results["is_web_app"] = True
                run_results["port"] = 8000
            
            # Run Flask/FastAPI application
            elif os.path.isfile(app_py) or os.path.isfile(main_py):
                target_file = "app.py" if os.path.isfile(app_py) else "main.py"
                cmd = ["python", target_file]
                run_results["run_commands"].append(" ".join(cmd))
                run_results["is_web_app"] = True
                run_results["port"] = 5000  # Default for Flask
            
            # Run using Docker Compose
            elif os.path.isfile(docker_compose):
                cmd = ["docker-compose", "up"]
                run_results["run_commands"].append(" ".join(cmd))
                run_results["is_web_app"] = True
                run_results["port"] = 80  # Assuming default HTTP port
            
            # Run using Procfile (Heroku-style)
            elif os.path.isfile(procfile):
                with open(procfile, 'r') as f:
                    for line in f:
                        if line.startswith("web:"):
                            web_command = line[4:].strip()
                            run_results["run_commands"].append(web_command)
                            run_results["is_web_app"] = True
                            run_results["port"] = 8000  # Common default
                            break
            
            # If no run command was found
            if not run_results["run_commands"]:
                # Look for README for instructions
                readme_paths = [
                    os.path.join(working_dir, "README.md"),
                    os.path.join(working_dir, "README"),
                    os.path.join(working_dir, "readme.md")
                ]
                
                for readme_path in readme_paths:
                    if os.path.isfile(readme_path):
                        with open(readme_path, 'r') as f:
                            content = f.read().lower()
                            
                            # Look for run instructions
                            run_sections = ["## running", "## run", "## usage", "## how to run", "## start"]
                            
                            for section in run_sections:
                                if section in content:
                                    run_results["run_commands"].append(f"# See {readme_path} for run instructions")
                                    run_results["readme_instructions"] = True
                                    break
                
                if not run_results.get("readme_instructions"):
                    run_results["run_commands"].append("# No run command detected")
                    run_results["skipped"] = True
            
            return run_results
        except Exception as e:
            print(f"Error running application: {e}")
            return {"error": str(e)}
    
    def document_setup_process(self, environment_setup: Dict[str, Any], dependency_results: Dict[str, Any], build_results: Dict[str, Any], run_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Document the setup process for the application.
        
        Args:
            environment_setup: Environment setup data.
            dependency_results: Dependency installation data.
            build_results: Build data.
            run_results: Run data.
            
        Returns:
            Dictionary containing documentation.
        """
        try:
            # Check for errors in any step
            for step_result in [environment_setup, dependency_results, build_results, run_results]:
                if "error" in step_result:
                    return {"error": step_result["error"]}
            
            working_dir = environment_setup["working_dir"]
            
            # Create documentation
            documentation = {
                "title": "Application Setup Documentation",
                "working_directory": working_dir,
                "steps": []
            }
            
            # Environment setup step
            env_step = {
                "name": "Environment Setup",
                "commands": environment_setup.get("setup_commands", []),
                "environment_variables": environment_setup.get("environment_variables", {})
            }
            documentation["steps"].append(env_step)
            
            # Dependency installation step
            dep_step = {
                "name": "Dependency Installation",
                "commands": dependency_results.get("installation_commands", []),
                "success": dependency_results.get("success", False)
            }
            documentation["steps"].append(dep_step)
            
            # Build step
            build_step = {
                "name": "Application Build",
                "commands": build_results.get("build_commands", []),
                "success": build_results.get("success", False),
                "skipped": build_results.get("skipped", False)
            }
            documentation["steps"].append(build_step)
            
            # Run step
            run_step = {
                "name": "Application Execution",
                "commands": run_results.get("run_commands", []),
                "success": run_results.get("success", False),
                "skipped": run_results.get("skipped", False),
                "is_web_app": run_results.get("is_web_app", False)
            }
            
            if run_results.get("is_web_app", False) and run_results.get("port"):
                run_step["access_url"] = f"http://localhost:{run_results['port']}"
            
            documentation["steps"].append(run_step)
            
            # Generate markdown documentation
            markdown_content = f"# {documentation['title']}\n\n"
            markdown_content += f"Working directory: `{documentation['working_directory']}`\n\n"
            
            for step in documentation["steps"]:
                markdown_content += f"## {step['name']}\n\n"
                
                if "skipped" in step and step["skipped"]:
                    markdown_content += "This step was skipped as it was not applicable.\n\n"
                
                if "environment_variables" in step and step["environment_variables"]:
                    markdown_content += "### Environment Variables\n\n"
                    for var, value in step["environment_variables"].items():
                        markdown_content += f"- `{var}={value}`\n"
                    markdown_content += "\n"
                
                if "commands" in step and step["commands"]:
                    markdown_content += "### Commands\n\n"
                    markdown_content += "```bash\n"
                    for cmd in step["commands"]:
                        markdown_content += f"{cmd}\n"
                    markdown_content += "```\n\n"
                
                if "access_url" in step:
                    markdown_content += f"### Access URL\n\n"
                    markdown_content += f"Once the application is running, access it at: {step['access_url']}\n\n"
            
            # Save documentation to file
            doc_filename = os.path.join(self.output_dir, "application_setup.md")
            with open(doc_filename, 'w') as f:
                f.write(markdown_content)
            
            documentation["markdown_file"] = doc_filename
            documentation["markdown_content"] = markdown_content
            
            return documentation
        except Exception as e:
            print(f"Error documenting setup process: {e}")
            return {"error": str(e)}
    
    def build_application_from_repository(self, repo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build an application from a repository analysis.
        
        Args:
            repo_analysis: Repository analysis data.
            
        Returns:
            Dictionary containing application build information.
        """
        try:
            # Set up environment
            environment_setup = self.setup_environment(repo_analysis)
            
            if "error" in environment_setup:
                return {"error": environment_setup["error"]}
            
            # Install dependencies
            dependency_results = self.install_dependencies(environment_setup)
            
            if "error" in dependency_results:
                return {"error": dependency_results["error"]}
            
            # Build application
            build_results = self.build_application(dependency_results)
            
            if "error" in build_results and not build_results.get("skipped", False):
                return {"error": build_results["error"]}
            
            # Run application
            run_results = self.run_application(build_results)
            
            if "error" in run_results and not run_results.get("skipped", False):
                return {"error": run_results["error"]}
            
            # Document setup process
            documentation = self.document_setup_process(
                environment_setup,
                dependency_results,
                build_results,
                run_results
            )
            
            # Combine all information
            build_info = {
                "repository": repo_analysis.get("repository", {}),
                "environment_setup": environment_setup,
                "dependency_installation": dependency_results,
                "application_build": build_results,
                "application_run": run_results,
                "documentation": documentation
            }
            
            return build_info
        except Exception as e:
            print(f"Error building application from repository: {e}")
            return {"error": str(e)}
