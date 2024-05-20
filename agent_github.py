import os
import requests
from git import Repo
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

def create_public_repo(repo_name:str) -> bool:
    url = 'https://api.github.com/user/repos'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'name': repo_name,
        'description': 'Created via script',
        'private': False
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f'Successfully created repository {repo_name}')
        return True
    else:
        print(f'Failed to create repository: {response.json()}')
        return False

def init_local_repo(folder_path:str,repo_name:str) -> bool:
    if not os.path.isdir(folder_path):
        print(f'The folder path {folder_path} does not exist')
        exit(1)

    repo = Repo.init(folder_path)
    repo.git.add(A=True)
    repo.index.commit('Initial commit')

    origin_url = f'https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{repo_name}.git'
    origin = repo.create_remote('origin', origin_url)
    repo.git.push('--set-upstream', origin, 'master')

    print(f'Successfully pushed files to repository {repo_name}')



def commit_files_to_existing_repo(folder_path: str, repo_url: str, commit_message: str) -> bool:
    if not os.path.isdir(folder_path):
        print(f'The folder path {folder_path} does not exist')
        return False

    try:
        repo = Repo(folder_path)
    except Exception as e:
        print(f'Error initializing repository: {e}')
        return False

    repo.git.add(A=True)
    if repo.is_dirty():
        repo.index.commit(commit_message)
        origin = repo.remote(name='origin')
        origin.set_url(repo_url)
        repo.git.push(origin, 'master')
        print(f'Successfully committed and pushed changes: {commit_message}')
        return True
    else:
        print('No changes to commit')
        return False


"""
REPO_NAME="orbidev-test"
FOLDER_PATH="test/"
REPO_URL = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

res = create_public_repo(REPO_NAME)
if res:
    init_local_repo(FOLDER_PATH,REPO_NAME)
else:
    print("Some Error Occured while setting up the public repo")
"""
