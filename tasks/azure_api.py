import os
import requests

# See link down below to generate your Private Access Token
AZURE_DEVOPS_PAT = "swbsi2y3svlhmnp4i6iowi2a7cftfiokhmtk6pxypa37f6gzmvyq"#os.getenv('AZURE_DEVOPS_PAT')
url = 'https://dev.azure.com/msumanth750/TestProject/_apis/wit/workitems/$Epic?api-version=7.0'



# data = [
#  {
#  "op": "add",
#  "path": "/fields/System.Title",
#  "value": "task 1 by azure api"
#  },
#  {
#  "op": "add",
#  "path": "/fields/System.AssignedTo",
#  "value": "sumanth@starlly.in"
#  }
# ]
#
# r = requests.post(url, json=data,
#     headers={'Content-Type': 'application/json-patch+json'},
#     auth=('', AZURE_DEVOPS_PAT))
#
# print(r.json())


def azure_workitem_create(data,org='msumanth750',project='TestProject',type='Task',assigned_to=None):
    url = f'https://dev.azure.com/{org}/{project}/_apis/wit/workitems/${type}?api-version=7.0'
    r = requests.post(url, json=data,
        headers={'Content-Type': 'application/json-patch+json'},
        auth=('', AZURE_DEVOPS_PAT))

    print(r)
    return r.json()

def azure_workitem_update(id,data,org='msumanth750',project='TestProject'):
    url = f'https://dev.azure.com/{org}/{project}/_apis/wit/workitems/{id}?api-version=7.0'
    r = requests.patch(url, json=data,
        headers={'Content-Type': 'application/json-patch+json'},
        auth=('', AZURE_DEVOPS_PAT))
    return r.json()
