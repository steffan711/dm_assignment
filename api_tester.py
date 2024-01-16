import requests

# URL of the Flask API endpoint
url = "http://localhost:5000/api/statistics"

repos = [
    "?repository_name=PyGithub/PyGithub",
    "?repository_name=langchain-ai/langchain",
    "?repository_name=langchain-ai/langchainjs",
    "?repository_name=pinecone-io/examples",
    "?repository_name=diffblue/cbmc",
    "?repository_name=datamole-ai/edvart",
    "?repository_name=nonexistentrepo",
    "?repository_name=",
]

for repo in repos:
    response = requests.get(url + repo)
    if response.status_code == 200:
        # Print the response JSON if successful
        print("Response from API:", response.json())
    else:
        # Print error message if not successful
        print("Failed to fetch data. Status code:", response.status_code)
