# GitHub Repository Branch Analysis Dashboard

A comprehensive full-stack application for analyzing GitHub repositories with detailed branch metrics, contributor statistics, and visual insights.

## 🌟 Features

### Branch Analysis
- **Branch Statistics**: Total commits, additions, deletions, and protection status
- **Activity Timeline**: Daily commit activity visualization
- **Contributor Metrics**: Top contributors with commit and code change statistics
- **Branch Comparison**: Compare any two branches with detailed diff analysis

### Pull Request Analysis
- **PR Tracking**: View open, closed, or all pull requests
- **State Distribution**: Visual breakdown of PR states
- **Author Statistics**: PRs created by each contributor
- **Branch Information**: Track which branches have active PRs

### Contributor Insights
- **Top Contributors**: Ranked by number of contributions
- **Contribution Charts**: Visual representation of contributor activity
- **Profile Links**: Direct access to contributor profiles

### Activity Metrics
- **Code Frequency**: Track additions and deletions over time
- **Repository Overview**: Stars, forks, watchers, and issues
- **Language Statistics**: Primary programming language

## 🏗️ Architecture

```
┌─────────────────────┐         ┌─────────────────────┐
│  Streamlit Frontend │ ◄─────► │    Flask Backend    │
│   (dashboard.py)    │  HTTP   │      (app.py)       │
└─────────────────────┘         └─────────────────────┘
                                          │
                                          ▼
                                 ┌────────────────────┐
                                 │   GitHub API v3    │
                                 └────────────────────┘
```

## 📋 Prerequisites

- Python 3.8 or higher
- GitHub account (optional: Personal Access Token for higher rate limits)

## 🚀 Installation

### 1. Clone or Create Project Directory

```bash
mkdir github-dashboard
cd github-dashboard
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Project Structure

Ensure your project has the following structure:

```
github-dashboard/
├── app.py                 # Flask backend
├── dashboard.py           # Streamlit frontend
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🎮 Usage

### Step 1: Start the Flask Backend

In your terminal with the virtual environment activated:

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 2: Start the Streamlit Frontend

Open a **new terminal**, activate the virtual environment, and run:

```bash
streamlit run dashboard.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

### Step 3: Analyze a Repository

1. **Optional**: Enter your GitHub Personal Access Token in the sidebar
   - Creates tokens at: https://github.com/settings/tokens
   - Increases rate limit from 60 to 5,000 requests/hour
   - Only needs `public_repo` scope for public repositories

2. **Enter Repository Details**:
   - Owner/Organization: e.g., `facebook`
   - Repository Name: e.g., `react`

3. **Click "Analyze Repository"**

## 📊 API Endpoints

### Backend (Flask) Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/repository/<owner>/<repo>` | GET | Repository information |
| `/api/repository/<owner>/<repo>/branches` | GET | List all branches |
| `/api/repository/<owner>/<repo>/branch/<name>/commits` | GET | Branch commits |
| `/api/repository/<owner>/<repo>/branch/<name>/stats` | GET | Branch statistics |
| `/api/repository/<owner>/<repo>/compare/<base>...<head>` | GET | Compare branches |
| `/api/repository/<owner>/<repo>/contributors` | GET | Repository contributors |
| `/api/repository/<owner>/<repo>/pull-requests` | GET | Pull requests |
| `/api/repository/<owner>/<repo>/code-frequency` | GET | Code frequency stats |

## 🔒 GitHub Token

### Why Use a Token?

- **Without Token**: 60 requests/hour
- **With Token**: 5,000 requests/hour

### How to Create a Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name (e.g., "Dashboard Access")
4. Select scopes: `public_repo` (for public repos)
5. Click "Generate token"
6. Copy the token (you won't see it again!)

### Using the Token

Simply paste it into the "GitHub Personal Access Token" field in the sidebar. It's stored only in your browser session and never saved.

## 📈 Features Explained

### 1. Branch Analysis Tab
- View all repository branches
- Select a branch to analyze
- See commit counts, code additions/deletions
- View daily commit activity chart
- Analyze top contributors

### 2. Branch Comparison Tab
- Compare any two branches
- See commits ahead/behind
- View all changed files
- Visualize code changes

### 3. Pull Requests Tab
- Filter by state (open/closed/all)
- View PR details
- See author statistics
- Analyze PR distribution

### 4. Contributors Tab
- Top 15 contributors chart
- Total contribution metrics
- Contribution distribution

### 5. Activity Tab
- Code frequency over time
- Additions vs deletions visualization
- Historical trends

## 🛠️ Troubleshooting

### "Cannot connect to Flask API"

**Solution**: Make sure the Flask backend is running in a separate terminal:
```bash
python app.py
```

### "Rate limit exceeded"

**Solution**: Add a GitHub Personal Access Token in the sidebar.

### Port Already in Use

**Flask (5000)**:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

**Streamlit (8501)**:
```bash
# Run on different port
streamlit run dashboard.py --server.port 8502
```

### Import Errors

```bash
pip install --upgrade -r requirements.txt
```

## 🔧 Configuration

### Changing API Port

In `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change port here
```

In `dashboard.py`:
```python
API_BASE_URL = "http://localhost:5001/api"  # Update URL
```

### Customizing Streamlit

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
port = 8501
```

## 📝 Example Repositories to Try

- `facebook/react` - Popular React library
- `microsoft/vscode` - VS Code editor
- `tensorflow/tensorflow` - Machine learning framework
- `kubernetes/kubernetes` - Container orchestration
- `nodejs/node` - Node.js runtime

## 🤝 Contributing

Feel free to enhance this dashboard with:
- Additional metrics and visualizations
- Export functionality (CSV, PDF)
- Caching for better performance
- Database integration for historical tracking
- User authentication
- Multi-repository comparison

## 📄 License

This project is open source and available for personal and commercial use.

## 🙏 Acknowledgments

- GitHub API v3 for providing comprehensive repository data
- Streamlit for the amazing dashboard framework
- Plotly for beautiful interactive visualizations
- Flask for the lightweight backend framework