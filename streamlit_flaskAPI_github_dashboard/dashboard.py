import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="GitHub Branch Analysis Dashboard",
    page_icon="🔀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:5000/api"

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if 'github_token' not in st.session_state:
    st.session_state.github_token = ""
if 'repo_data' not in st.session_state:
    st.session_state.repo_data = None
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'current_owner' not in st.session_state:
    st.session_state.current_owner = ""
if 'current_repo' not in st.session_state:
    st.session_state.current_repo = ""


def make_api_request(endpoint, method="GET", params=None):
    """Make API request with token"""
    headers = {}
    if st.session_state.github_token:
        headers['X-GitHub-Token'] = st.session_state.github_token

    url = f"{API_BASE_URL}{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None


def display_repository_overview(owner, repo):
    """Display repository overview"""
    repo_info = make_api_request(f"/repository/{owner}/{repo}")

    if repo_info:
        st.session_state.repo_data = repo_info

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("⭐ Stars", repo_info.get('stargazers_count', 0))
        with col2:
            st.metric("🔀 Forks", repo_info.get('forks_count', 0))
        with col3:
            st.metric("👁️ Watchers", repo_info.get('watchers_count', 0))
        with col4:
            st.metric("🐛 Open Issues", repo_info.get('open_issues_count', 0))

        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            st.write(
                f"**Description:** {repo_info.get('description', 'No description')}")
            st.write(f"**Language:** {repo_info.get('language', 'N/A')}")
        with col2:
            st.write(f"**Created:** {repo_info.get('created_at', 'N/A')[:10]}")
            st.write(
                f"**Last Updated:** {repo_info.get('updated_at', 'N/A')[:10]}")


def display_branch_analysis(owner, repo):
    """Display detailed branch analysis"""
    branches = make_api_request(f"/repository/{owner}/{repo}/branches")

    if branches:
        st.subheader(f"📊 Branch Analysis ({len(branches)} branches)")

        # Branch selector with multiple options
        branch_names = [b['name'] for b in branches]

        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            selection_method = st.radio(
                "Selection Method",
                ["Dropdown", "Radio Buttons"],
                horizontal=True,
                key="selection_method"
            )
        with col2:
            if selection_method == "Dropdown":
                selected_branch = st.selectbox(
                    "Select Branch to Analyze",
                    branch_names,
                    index=0,
                    key="branch_select_dropdown"
                )
            else:
                selected_branch = st.radio(
                    "Select Branch to Analyze",
                    branch_names,
                    key="branch_select_radio"
                )
        with col3:
            st.write("")
            st.write("")
            # Removed the refresh button that was causing issues

        st.markdown("---")

        if selected_branch:
            with st.spinner(f"Loading statistics for {selected_branch}..."):
                stats = make_api_request(
                    f"/repository/{owner}/{repo}/branch/{selected_branch}/stats")

                if stats:
                    # Key metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Commits", stats.get(
                            'total_commits', 0))
                    with col2:
                        st.metric("Additions", stats.get('total_additions', 0))
                    with col3:
                        st.metric("Deletions", stats.get('total_deletions', 0))
                    with col4:
                        protected = "🔒 Yes" if stats.get(
                            'is_protected') else "🔓 No"
                        st.metric("Protected", protected)

                    # Activity Timeline
                    if stats.get('activity_timeline'):
                        st.subheader("📈 Commit Activity Timeline")
                        timeline_df = pd.DataFrame([
                            {'Date': k, 'Commits': v}
                            for k, v in stats['activity_timeline'].items()
                        ])
                        timeline_df['Date'] = pd.to_datetime(
                            timeline_df['Date'])
                        timeline_df = timeline_df.sort_values('Date')

                        fig = px.line(timeline_df, x='Date', y='Commits',
                                      title='Daily Commit Activity',
                                      markers=True)
                        fig.update_layout(hovermode='x unified')
                        st.plotly_chart(fig, use_container_width=True)

                    # Top Contributors
                    if stats.get('contributors'):
                        st.subheader("👥 Top Contributors")
                        contributors_df = pd.DataFrame(stats['contributors'])

                        col1, col2 = st.columns(2)

                        with col1:
                            fig = px.bar(contributors_df, x='author', y='commits',
                                         title='Commits by Author',
                                         labels={'author': 'Author', 'commits': 'Commits'})
                            fig.update_layout(xaxis_tickangle=-45)
                            st.plotly_chart(fig, use_container_width=True)

                        with col2:
                            fig = go.Figure(data=[
                                go.Bar(name='Additions', x=contributors_df['author'],
                                       y=contributors_df['additions'], marker_color='green'),
                                go.Bar(name='Deletions', x=contributors_df['author'],
                                       y=contributors_df['deletions'], marker_color='red')
                            ])
                            fig.update_layout(title='Code Changes by Author',
                                              barmode='group',
                                              xaxis_tickangle=-45)
                            st.plotly_chart(fig, use_container_width=True)

                        # Contributors table
                        st.dataframe(contributors_df, use_container_width=True)


def display_branch_comparison(owner, repo):
    """Display branch comparison"""
    branches = make_api_request(f"/repository/{owner}/{repo}/branches")

    if branches:
        st.subheader("🔀 Compare Branches")

        branch_names = [b['name'] for b in branches]

        col1, col2 = st.columns(2)
        with col1:
            base_branch = st.selectbox("Base Branch", branch_names, key="base")
        with col2:
            compare_branch = st.selectbox("Compare Branch",
                                          [b for b in branch_names if b !=
                                              base_branch],
                                          key="compare")

        if st.button("Compare Branches"):
            with st.spinner("Comparing branches..."):
                comparison = make_api_request(
                    f"/repository/{owner}/{repo}/compare/{base_branch}...{compare_branch}"
                )

                if comparison:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Commits Ahead",
                                  comparison.get('ahead_by', 0))
                    with col2:
                        st.metric("Commits Behind",
                                  comparison.get('behind_by', 0))
                    with col3:
                        st.metric("Files Changed", len(
                            comparison.get('files', [])))
                    with col4:
                        st.metric("Total Changes",
                                  comparison.get('total_commits', 0))

                    # File changes
                    if comparison.get('files'):
                        st.subheader("📁 Changed Files")
                        files_data = []
                        for file in comparison['files']:
                            files_data.append({
                                'Filename': file['filename'],
                                'Status': file['status'],
                                'Additions': file['additions'],
                                'Deletions': file['deletions'],
                                'Changes': file['changes']
                            })

                        files_df = pd.DataFrame(files_data)
                        st.dataframe(files_df, use_container_width=True)

                        # Changes visualization
                        fig = px.bar(files_df.head(10), x='Filename',
                                     y=['Additions', 'Deletions'],
                                     title='Top 10 Files by Changes',
                                     barmode='group')
                        fig.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig, use_container_width=True)


def display_pull_requests(owner, repo):
    """Display pull requests analysis"""
    st.subheader("🔄 Pull Requests")

    state = st.radio("PR State", ["open", "closed", "all"], horizontal=True)

    prs = make_api_request(f"/repository/{owner}/{repo}/pull-requests",
                           params={'state': state})

    if prs:
        st.write(f"**Total PRs:** {len(prs)}")

        pr_data = []
        for pr in prs:
            pr_data.append({
                'Number': pr['number'],
                'Title': pr['title'],
                'Author': pr['user']['login'],
                'State': pr['state'],
                'Created': pr['created_at'][:10],
                'Branch': pr['head']['ref']
            })

        pr_df = pd.DataFrame(pr_data)
        st.dataframe(pr_df, use_container_width=True)

        # PR statistics
        col1, col2 = st.columns(2)

        with col1:
            author_counts = pr_df['Author'].value_counts().head(10)
            fig = px.bar(x=author_counts.index, y=author_counts.values,
                         title='PRs by Author',
                         labels={'x': 'Author', 'y': 'Count'})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            state_counts = pr_df['State'].value_counts()
            fig = px.pie(values=state_counts.values, names=state_counts.index,
                         title='PR State Distribution')
            st.plotly_chart(fig, use_container_width=True)


def display_contributors(owner, repo):
    """Display contributors analysis"""
    st.subheader("👥 Contributors Analysis")

    contributors = make_api_request(f"/repository/{owner}/{repo}/contributors")

    if contributors:
        contrib_data = []
        for contrib in contributors:
            contrib_data.append({
                'Username': contrib['login'],
                'Contributions': contrib['contributions'],
                'Profile': contrib['html_url']
            })

        contrib_df = pd.DataFrame(contrib_data)

        col1, col2 = st.columns([2, 1])

        with col1:
            fig = px.bar(contrib_df.head(15), x='Username', y='Contributions',
                         title='Top 15 Contributors',
                         labels={'Contributions': 'Number of Contributions'})
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.metric("Total Contributors", len(contrib_df))
            st.metric("Total Contributions", contrib_df['Contributions'].sum())
            st.metric("Average Contributions",
                      int(contrib_df['Contributions'].mean()))

        st.dataframe(contrib_df, use_container_width=True)

# Main Application


def main():
    st.markdown('<div class="main-header">🔀 GitHub Branch Analysis Dashboard</div>',
                unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        # GitHub Token
        github_token = st.text_input(
            "GitHub Personal Access Token (Optional)",
            type="password",
            help="Increases API rate limits. Create at: https://github.com/settings/tokens"
        )

        if github_token:
            st.session_state.github_token = github_token
            st.success("✅ Token configured")

        st.markdown("---")

        # Repository Input
        st.header("📦 Repository")
        owner = st.text_input(
            "Owner/Organization", placeholder="facebook", value=st.session_state.current_owner)
        repo = st.text_input(
            "Repository Name", placeholder="react", value=st.session_state.current_repo)

        analyze_button = st.button("🔍 Analyze Repository", type="primary")

        if analyze_button:
            st.session_state.analyzed = True
            st.session_state.current_owner = owner
            st.session_state.current_repo = repo

        st.markdown("---")
        st.info(
            "💡 **Tip:** Use a GitHub token to increase API rate limits from 60 to 5000 requests/hour")

    # Main Content
    if (analyze_button or st.session_state.analyzed) and owner and repo:
        # Update session state
        st.session_state.current_owner = owner
        st.session_state.current_repo = repo

        # Health check
        health = make_api_request("/health")
        if not health:
            st.error(
                "❌ Cannot connect to Flask API. Make sure it's running on port 5000")
            st.code("python app.py", language="bash")
            return

        # Repository Overview
        with st.container():
            display_repository_overview(owner, repo)

        # Tabs for different analyses
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Branch Analysis",
            "🔀 Branch Comparison",
            "🔄 Pull Requests",
            "👥 Contributors",
            "📈 Activity"
        ])

        with tab1:
            display_branch_analysis(owner, repo)

        with tab2:
            display_branch_comparison(owner, repo)

        with tab3:
            display_pull_requests(owner, repo)

        with tab4:
            display_contributors(owner, repo)

        with tab5:
            st.subheader("📈 Code Frequency")
            code_freq = make_api_request(
                f"/repository/{owner}/{repo}/code-frequency")
            if code_freq:
                df = pd.DataFrame(code_freq, columns=[
                                  'Week', 'Additions', 'Deletions'])
                df['Week'] = pd.to_datetime(df['Week'], unit='s')

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df['Week'], y=df['Additions'],
                                         name='Additions', fill='tozeroy',
                                         line=dict(color='green')))
                fig.add_trace(go.Scatter(x=df['Week'], y=df['Deletions'],
                                         name='Deletions', fill='tozeroy',
                                         line=dict(color='red')))
                fig.update_layout(title='Code Additions vs Deletions Over Time',
                                  xaxis_title='Date', yaxis_title='Lines of Code')
                st.plotly_chart(fig, use_container_width=True)

    elif not analyze_button and not st.session_state.analyzed:
        # Welcome screen
        st.info(
            "👈 Enter repository details in the sidebar and click 'Analyze Repository' to begin")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### 📊 Features")
            st.markdown("""
            - Branch statistics
            - Commit analysis
            - Contributor metrics
            - Activity timelines
            """)
        with col2:
            st.markdown("### 🔀 Comparison")
            st.markdown("""
            - Branch comparison
            - File diff analysis
            - Commit differences
            - Change statistics
            """)
        with col3:
            st.markdown("### 🔄 Pull Requests")
            st.markdown("""
            - PR tracking
            - State analysis
            - Author statistics
            - Branch insights
            """)


if __name__ == "__main__":
    main()
