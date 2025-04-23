import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

class GitHubAPI:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.owner = os.getenv('GITHUB_OWNER')
        self.repo = os.getenv('GITHUB_REPO')
        self.github = Github(self.token)

    def get_commits(self):
        repo = self.github.get_repo(f"{self.owner}/{self.repo}")
        return repo.get_commits()

    def get_commit_details(self, commit_sha):
        repo = self.github.get_repo(f"{self.owner}/{self.repo}")
        commit = repo.get_commit(sha=commit_sha)
        return commit

    def get_pull_requests(self, state='all'):
        repo = self.github.get_repo(f"{self.owner}/{self.repo}")
        return repo.get_pulls(state=state)

if __name__ == "__main__":
    github = GitHubAPI()
    commits = github.get_commits()
    for commit in list(commits)[:5]:
        print(f"\nCommit: {commit.sha[:7]} - {commit.commit.message}")
        print(f"Author: {commit.commit.author.name}")
        print(f"Date: {commit.commit.author.date}")
        
        commit_details = github.get_commit_details(commit.sha)
        print("\nFiles changed:")
        for file in commit_details.files:
            print(f"- {file.filename}")
            print(f"  Status: {file.status}")
            print(f"  Changes: +{file.additions} -{file.deletions}")
            if file.patch:
                print("  Patch preview:")
                print(f"  {file.patch[:200]}...")

    prs = github.get_pull_requests()
    for pr in list(prs)[:5]:
        print(f"PR #{pr.number}: {pr.title}")
