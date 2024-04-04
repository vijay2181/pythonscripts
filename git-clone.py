from github import Github
import os

# Provide your GitHub personal access token
github_token = os.popen(f"sudo aws ssm get-parameter --name /Git/repo/pw --with-decryption --query Parameter.Value --output text --profile test").read().strip()

repo_to_clone = "vagrant"

# Initialize GitHub instance
server = Github(github_token)

# Get repositories for the user
repos = server.get_user().get_repos()

# Loop through repositories
for repo in repos:
    if repo.name == repo_to_clone:
        # Clone only if repository name matches
        os.system(f"git clone {repo.clone_url.replace('https://', f'https://{github_token}@')}")
        break  # Stop loop after cloning the desired repository
