from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
from collections import defaultdict
import base64

app = Flask(__name__)
CORS(app)

# GitHub API base URL
GITHUB_API_URL = "https://api.github.com"


def get_headers(token=None):
    """Get headers for GitHub API requests"""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "API is running"})


@app.route('/api/repository/<owner>/<repo>', methods=['GET'])
def get_repository_info(owner, repo):
    """Get basic repository information"""
    token = request.headers.get('X-GitHub-Token')
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}"

    try:
        response = requests.get(url, headers=get_headers(token))
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/repository/<owner>/<repo>/branches', methods=['GET'])
def get_branches(owner, repo):
    """Get all branches in the repository"""
    token = request.headers.get('X-GitHub-Token')
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/branches"

    try:
        response = requests.get(url, headers=get_headers(
            token), params={'per_page': 100})
        response.raise_for_status()
        branches = response.json()

        # Get detailed info for each branch
        detailed_branches = []
        for branch in branches:
            branch_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/branches/{branch['name']}"
            branch_response = requests.get(
                branch_url, headers=get_headers(token))
            if branch_response.status_code == 200:
                detailed_branches.append(branch_response.json())

        return jsonify(detailed_branches)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/repository/<owner>/<repo>/branch/<path:branch_name>/commits', methods=['GET'])
def get_branch_commits(owner, repo, branch_name):
    """Get commits for a specific branch"""
    token = request.headers.get('X-GitHub-Token')
    since = request.args.get('since', None)
    per_page = request.args.get('per_page', 100)

    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits"
    params = {'sha': branch_name, 'per_page': per_page}

    if since:
        params['since'] = since

    try:
        response = requests.get(url, headers=get_headers(token), params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/repository/<owner>/<repo>/branch/<path:branch_name>/stats', methods=['GET'])
def get_branch_stats(owner, repo, branch_name):
    """Get comprehensive statistics for a branch"""
    token = request.headers.get('X-GitHub-Token')

    try:
        # Get commits
        commits_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits"
        commits_response = requests.get(
            commits_url,
            headers=get_headers(token),
            params={'sha': branch_name, 'per_page': 100}
        )
        commits_response.raise_for_status()
        commits = commits_response.json()

        # Analyze commits
        contributor_stats = defaultdict(
            lambda: {'commits': 0, 'additions': 0, 'deletions': 0})
        commit_dates = []
        total_additions = 0
        total_deletions = 0

        for commit in commits[:50]:  # Limit to avoid rate limiting
            if commit.get('author'):
                author = commit['author'].get('login', 'Unknown')
                contributor_stats[author]['commits'] += 1

            commit_date = commit['commit']['author']['date']
            commit_dates.append(commit_date)

            # Get commit details for file changes
            commit_sha = commit['sha']
            commit_detail_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits/{commit_sha}"
            commit_detail = requests.get(
                commit_detail_url, headers=get_headers(token))

            if commit_detail.status_code == 200:
                stats = commit_detail.json().get('stats', {})
                additions = stats.get('additions', 0)
                deletions = stats.get('deletions', 0)

                total_additions += additions
                total_deletions += deletions

                if commit.get('author'):
                    author = commit['author'].get('login', 'Unknown')
                    contributor_stats[author]['additions'] += additions
                    contributor_stats[author]['deletions'] += deletions

        # Calculate activity timeline
        activity_timeline = defaultdict(int)
        for date_str in commit_dates:
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            day = date.strftime("%Y-%m-%d")
            activity_timeline[day] += 1

        # Sort contributors by commits
        top_contributors = sorted(
            [{'author': k, **v} for k, v in contributor_stats.items()],
            key=lambda x: x['commits'],
            reverse=True
        )[:10]

        # Get branch protection status
        protection_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/branches/{branch_name}/protection"
        protection_response = requests.get(
            protection_url, headers=get_headers(token))
        is_protected = protection_response.status_code == 200

        return jsonify({
            'total_commits': len(commits),
            'total_additions': total_additions,
            'total_deletions': total_deletions,
            'contributors': top_contributors,
            'activity_timeline': dict(sorted(activity_timeline.items())),
            'is_protected': is_protected,
            'last_commit_date': commits[0]['commit']['author']['date'] if commits else None
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/repository/<owner>/<repo>/compare/<base>...<head>', methods=['GET'])
def compare_branches(owner, repo, base, head):
    """Compare two branches"""
    token = request.headers.get('X-GitHub-Token')
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/compare/{base}...{head}"

    try:
        response = requests.get(url, headers=get_headers(token))
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/repository/<owner>/<repo>/contributors', methods=['GET'])
def get_contributors(owner, repo):
    """Get repository contributors"""
    token = request.headers.get('X-GitHub-Token')
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contributors"

    try:
        response = requests.get(url, headers=get_headers(
            token), params={'per_page': 100})
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/repository/<owner>/<repo>/pull-requests', methods=['GET'])
def get_pull_requests(owner, repo):
    """Get pull requests"""
    token = request.headers.get('X-GitHub-Token')
    state = request.args.get('state', 'open')
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"

    try:
        response = requests.get(url, headers=get_headers(
            token), params={'state': state, 'per_page': 50})
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/repository/<owner>/<repo>/code-frequency', methods=['GET'])
def get_code_frequency(owner, repo):
    """Get code frequency statistics"""
    token = request.headers.get('X-GitHub-Token')
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/stats/code_frequency"

    try:
        response = requests.get(url, headers=get_headers(token))
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
