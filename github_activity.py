import sys
import urllib.request
import json

# Function to fetch activity from GitHub API
def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"  # GitHub events endpoint
    
    try:
        # Making a request to the GitHub API
        with urllib.request.urlopen(url) as response:
            data = json.load(response)  # Parse the JSON response
            return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Function to display activity
def display_activity(data):
    if data:
        for event in data:
            event_type = event.get('type', 'Unknown')  # Get the type of the event
            repo_name = event.get('repo', {}).get('name', 'Unknown Repo')  # Get repository name
            
            if event_type == 'PushEvent':
                # Display commit information for push events
                commits = event.get('payload', {}).get('commits', [])
                if commits:
                    print(f"Pushed {len(commits)} commit(s) to {repo_name}")
            elif event_type == 'IssuesEvent':
                # Display issue opened/closed information for issue events
                action = event.get('payload', {}).get('action', 'opened')
                issue_title = event.get('payload', {}).get('issue', {}).get('title', 'Unknown')
                print(f"Opened a new issue in {repo_name}: {issue_title}")
            elif event_type == 'StarEvent':
                # Display starred repository information
                print(f"Starred {repo_name}")
            elif event_type == 'CreateEvent':
                # Display created repositories or branches
                creation_type = event.get('payload', {}).get('ref_type', 'Unknown')
                print(f"Created a new {creation_type} in {repo_name}")
            else:
                print(f"Event Type: {event_type} in {repo_name}")
    else:
        print("No activity found or an error occurred.")

# Main function to handle command line arguments and run the script
def main():
    if len(sys.argv) != 2:
        print("Usage: python github_activity.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]  # Get the GitHub username from the command line
    print(f"Fetching activity for GitHub user: {username}")
    
    # Fetch activity data from GitHub API
    activity_data = fetch_github_activity(username)
    
    # Display the fetched activity
    display_activity(activity_data)

# Run the script when executed
if __name__ == "__main__":
    main()

