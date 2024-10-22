# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv

load_dotenv()

project_url = os.getenv('ATLASSIAN_URL') + "/project"
issue_url = os.getenv('ATLASSIAN_URL') + "/issue"
API_TOKEN = os.getenv('ATLASSIAN_API_KEY')
MY_EMAIL = os.getenv('MY_EMAIL')


auth = HTTPBasicAuth(MY_EMAIL, API_TOKEN)

# headers = {
#   "Accept": "application/json"
# }

# response = requests.request(
#    "GET",
#    url,
#    headers=headers,
#    auth=auth
# )

# json_response = json.loads(response.text)

# for project in json_response:
#     print(project['key'] + " --> " + project['name'] + "\n")

# create an issue

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

payload = json.dumps( {
  "fields": {
    "description": {
      "content": [
        {
          "content": [
            {
              "text": "This is my first issue created using the REST API",
              "type": "text"
            }
          ],
          "type": "paragraph"
        }
      ],
      "type": "doc",
      "version": 1
    },
    "issuetype": {
      "id": "10012"
    },
    "project": {
      "key": "DEV"
    },
    "summary": "FIRST ISSUE",
  },
  "update": {}
} )

response = requests.request(
   "POST",
   issue_url,
   data=payload,
   headers=headers,
   auth=auth
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))