# OpenAI Agents Demo

A Flask web service demonstrating three different OpenAI Agent SDK implementations:

1. **Web Search Agent** - Agent running in a loop with web search capabilities
2. **Function Tools Agent** - Agent with custom function tools (calculator, weather)
3. **Realtime Agent** - Realtime streaming agent structure

## Features

- 🔐 Secure login authentication
- 🌐 Web-based dashboard to run agents
- 🚀 One-click deployment to Render
- 🔑 Environment variable configuration

## Project Structure

```
.
├── app.py                    # Flask web service with authentication
├── agent_web_search.py       # Web search agent implementation
├── agent_function_tools.py   # Custom function tools agent
├── agent_realtime.py         # Realtime agent implementation
├── requirements.txt          # Python dependencies
├── render.yaml              # Render deployment configuration
├── .env.example             # Environment variables template
└── README.md                # This file
```

## Local Development

### Prerequisites

- Python 3.9+
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd "Underwriting AI"
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from template:
```bash
cp .env.example .env
```

5. Edit `.env` and add your credentials:
```env
OPENAI_API_KEY=your_actual_openai_api_key
APP_USERNAME=your_username
APP_PASSWORD=your_password
SECRET_KEY=your_random_secret_key
```

6. Run the application:
```bash
python app.py
```

7. Open browser to `http://localhost:5000`

## Testing Individual Agents

You can test each agent separately:

```bash
# Test web search agent
python agent_web_search.py

# Test function tools agent
python agent_function_tools.py

# Test realtime agent
python agent_realtime.py
```

## Deployment to Render

### Method 1: Using render.yaml (Recommended)

1. Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit: OpenAI Agents Demo"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. Go to [Render Dashboard](https://dashboard.render.com/)

3. Click "New +" → "Blueprint"

4. Connect your GitHub repository

5. Render will automatically detect `render.yaml`

6. Set the following environment variables in Render:
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `APP_USERNAME` - Username for login
   - `APP_PASSWORD` - Password for login
   - `SECRET_KEY` - Auto-generated or set your own

7. Click "Apply" to deploy

### Method 2: Manual Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)

2. Click "New +" → "Web Service"

3. Connect your GitHub repository

4. Configure:
   - **Name**: `openai-agents-demo`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

5. Add environment variables:
   - `OPENAI_API_KEY`
   - `APP_USERNAME`
   - `APP_PASSWORD`
   - `SECRET_KEY`

6. Click "Create Web Service"

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `APP_USERNAME` | Login username | Yes |
| `APP_PASSWORD` | Login password | Yes |
| `SECRET_KEY` | Flask secret key for sessions | Yes |
| `PORT` | Port to run on (default: 5000) | No |

## Usage

1. Navigate to your deployed URL (e.g., `https://openai-agents-demo.onrender.com`)

2. Login with your configured username and password

3. Click on any agent card to run demonstrations:
   - **Web Search Agent**: Runs queries with web search
   - **Function Tools Agent**: Demonstrates calculator and weather tools
   - **Realtime Agent**: Shows realtime agent structure

## Security Notes

- Always use strong passwords in production
- Never commit `.env` file to version control
- Generate a secure random string for `SECRET_KEY`
- Rotate your OpenAI API key regularly

## Agent Details

### 1. Web Search Agent (`agent_web_search.py`)

Demonstrates an agent running in a loop with web search capabilities using the `WebSearchTool`.

**Features:**
- Searches the web for current information
- Runs multiple queries in sequence
- Streams responses in real-time

### 2. Function Tools Agent (`agent_function_tools.py`)

Shows how to create custom function tools with Pydantic models.

**Included Tools:**
- **Calculator**: Performs basic arithmetic (add, subtract, multiply, divide)
- **Weather**: Mock weather lookup by location

**Features:**
- Custom function definitions
- Pydantic schema validation
- Error handling
- JSON response parsing

### 3. Realtime Agent (`agent_realtime.py`)

Demonstrates the structure for realtime voice/text agents.

**Features:**
- Realtime streaming capabilities
- Text mode demonstration
- Voice assistant configuration structure

## Troubleshooting

### Import Errors

If you get import errors for `openai-agents`, make sure you have the latest version:
```bash
pip install --upgrade openai-agents
```

### Authentication Issues

If login doesn't work, verify your `.env` file has the correct credentials and restart the app.

### OpenAI API Errors

- Verify your API key is valid
- Check you have sufficient credits
- Ensure you're using a supported model

## License

MIT

## Contributing

Pull requests welcome! Please ensure all agents run successfully before submitting.

## Support

For issues, please open a GitHub issue or contact the maintainer.
