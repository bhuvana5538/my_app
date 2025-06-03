# main.py
from fastapi import FastAPI
import requests
import json
from bs4 import BeautifulSoup

app = FastAPI(title="LeetCode & Kaggle Reviewer API")

@app.get("/leetcode/{username}")
def fetch_leetcode_profile(username: str):
    url = "https://leetcode.com/graphql"
    query = {
        "operationName": "getUserProfile",
        "variables": {"username": username},
        "query": """
        query getUserProfile($username: String!) {
            matchedUser(username: $username) {
                username
                profile {
                    realName
                    ranking
                    userAvatar
                }
                submitStats {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
            }
        }
        """
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(query))

    if response.status_code == 200:
        user_data = response.json().get("data", {}).get("matchedUser")
        if user_data:
            submissions = user_data["submitStats"]["acSubmissionNum"]
            total_solved = next((item["count"] for item in submissions if item["difficulty"] == "All"), 0)

            return {
                "username": user_data["username"],
                "realName": user_data["profile"]["realName"],
                "ranking": user_data["profile"]["ranking"],
                "totalSolved": total_solved,
            }
    return {"error": "User not found or failed to fetch LeetCode profile."}


@app.get("/kaggle/{username}")
def fetch_kaggle_profile(username: str):
    try:
        url = f"https://www.kaggle.com/{username}"
        response = requests.get(url)

        if response.status_code != 200:
            return {"error": "User not found or page not accessible."}

        return {
            "username": username,
            "datasetLink": f"https://www.kaggle.com/{username}/datasets",
            "notebookLink": f"https://www.kaggle.com/{username}/code",
            "discussionLink": f"https://www.kaggle.com/{username}/discussion",
        }
    except Exception as e:
        return {"error": f"Failed to fetch Kaggle profile: {str(e)}"}
