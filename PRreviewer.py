import requests
import os
from openai import OpenAI

# --- Configuration ---
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Set this in your environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Set this in your environment
REPO_OWNER = "poseidon139"
REPO_NAME = "aiPRReview"
TARGET_BRANCH = os.getenv("TARGET_BRANCH")

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def get_pull_requests(branch):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    params = {"base": branch, "state": "open"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_diff(pr_number):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def get_code_review(diff):
    prompt = f"""You are a code reviewer. Please review the following pull request diff and provide constructive feedback:\n\n{diff}"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert software engineer reviewing code."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

def main():
    print(f"Fetching pull requests targeting branch: {TARGET_BRANCH}")
    prs = get_pull_requests(TARGET_BRANCH)

    if not prs:
        print("No open pull requests found for this branch.")
        return

    for pr in prs:
        print(f"\nReviewing PR #{pr['number']}: {pr['title']}")
        diff = get_diff(pr['number'])

        # Limit diff size for OpenAI input
        if len(diff) > 12000:
            print("Diff is too large to review with OpenAI API. Skipping.")
            continue

        review_comment = get_code_review(diff)
        print("\n--- Review Comment ---\n")
        print(review_comment)
        print("\n----------------------")

if __name__ == "__main__":
    main()
