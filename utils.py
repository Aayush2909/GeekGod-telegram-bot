from apiclient.discovery import build
import requests
import json

CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"

API_KEY = "YT_API_KEY"
youtube = build('youtube','v3',developerKey=API_KEY)

def video_links(query='Data Structures'):
    req = youtube.search().list(q=query, part='snippet', type='video', maxResults=3)
    res = req.execute()

    links = []
    for item in res['items']:
        links.append("https://www.youtube.com/watch?v="+item['id']['videoId'])

    return links



default = """#include<iostream>
            using namespace std;
            int main()
            {
                cout<<"Hello World!";
                return 0;
            }"""

def compiler(code=default, input="", lang="cpp14"):
    version = {
        "java": "2",
        "c": "0",
        "cpp14": "0",
        "python3": "3",
        "php": "0"
    }
    
    
    program = {
        "script": code,
        "stdin": input,
        "language" : lang,
        "versionIndex" : version[lang],
        "clientId" : CLIENT_ID,
        "clientSecret" : CLIENT_SECRET
    }

    response = requests.post("https://api.jdoodle.com/v1/execute", json=program)
    items = json.loads(response.text)
    return items

topics_key = [
    ['Arrays', 'Linked list', 'Stack'],
    ['Queue', 'Binary Tree', 'Binary Search Tree'],
    ['Heap', 'Hashing', 'Graph'],
    ['Advance Data Structure', 'Matrix', 'Strings']
]

if __name__ == '__main__':
    print(video_links())