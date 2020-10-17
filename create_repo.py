#!/usr/bin/env python3
import os
import requests
import argparse
import json

# from pprint import pprint
from python_settings import settings
os.environ["SETTINGS_MODULE"] = 'settings'

parser = argparse.ArgumentParser()

parser.add_argument("--name", "-n", type=str, dest="name", required=True)
parser.add_argument("--kind", "-k", type=str, dest="kind", help="kinds: react, python. default: readme.md")
parser.add_argument("--private", "-p", dest="is_private", action="store_true")
parser.add_argument("--dir", "-d", type=str, dest="dir", help="witch dir do you want to repo. default: ./")

args = parser.parse_args()

repo_name = args.name
is_private = args.is_private
repo_kind = args.kind
repo_dir = args.dir

API_URL = "https://api.github.com"

payload = json.dumps({"name": repo_name, "private": is_private})
headers = {
  "Authorization": "token " + settings.USER_TOKEN,
  "Accept": "application/vnd.github.v3+json"
}

def install_project_files_kind():
  result = os.system(f"echo '# {repo_name}' >> README.md")

  if (repo_kind == 'react'):
    result = os.system("npm init react-app client")
    result = os.system("npm i node-sass")
  if (repo_kind == 'python'):
    result = os.system(f"python3 -m venv {repo_name} && touch __init__.py && touch app.py && echo '/{repo_name}' >> .gitignore")
  if (repo_kind == '.net'):
    result = os.system(f"")

  return result

def create_project_files_dir():
  REPO_PATH = "/Users/thor/Projects/"
  os.chdir(REPO_PATH)

  if repo_dir:
    os.system("mkdir " + repo_dir)
    REPO_PATH = f"/Users/thor/Projects/{repo_dir}/"

  os.chdir(REPO_PATH)
  os.system("mkdir " + repo_name)
  os.chdir(REPO_PATH + repo_name)

# create repository
try:
  r = requests.post(API_URL+"/user/repos", data=payload, headers=headers)
  r.raise_for_status()

except requests.exceptions.RequestException as err:
  raise SystemExit(err)

# install on computer and upload
try: 
  create_project_files_dir()
  os.system("git init")
  os.system("git remote add origin https://github.com/RuneDaanen/" + repo_name + ".git")
  install_project_files_kind()
  os.system("git add . && git commit -m 'Initial Commit' && git push origin master")
except FileExistsError as err:
  raise SystemExit(err)

