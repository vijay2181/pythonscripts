import requests
import os
import json
import optparse

parser = optparse.OptionParser()

parser.add_option("-t", "--token", dest="GITHUB_TOKEN", help="Enter your Github Personal Access Token")
parser.add_option("-r", "--repo", dest="REPO_NAME", help="Enter Github Repo name you want to create")
parser.add_option("-a", "--add-user", dest="USER_NAME", help="Enter Github username you want to add as collaborator")
parser.add_option("-l", "--list-repos-for-user", dest="REPO_LIST", help="List repos for a given user")

(options, arguments) = parser.parse_args()

#token = os.environ.get("GITHUB_TOKEN")
#REPO_NAME = input("Please enter the repo name you want to create : ")

GITHUB_TOKEN = options.GITHUB_TOKEN
REPO_NAME = options.REPO_NAME

GITHUB_API_URL = "https://api.github.com/"
headers = {"Authorization": "token {}".format(GITHUB_TOKEN)}
data = {"name": "{}".format(REPO_NAME)}

r = requests.post(GITHUB_API_URL +"user/repos" + "", data=json.dumps(data), headers=headers)
print(r)
