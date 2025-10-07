"""
Flask Web Service for OpenAI Agents
Provides authenticated access to three different agent demonstrations
"""

import os
import asyncio
from functools import wraps
from flask import Flask, render_template_string, request, session, redirect, url_for, jsonify
from dotenv import load_dotenv
from agent_web_search import run_web_search_agent
from agent_function_tools import run_function_tools_agent
from agent_realtime import run_realtime_simple

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

# Get credentials from environment
USERNAME = os.environ.get("APP_USERNAME", "admin")
PASSWORD = os.environ.get("APP_PASSWORD", "admin")


def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Home page - redirect to login or dashboard"""
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template_string(LOGIN_TEMPLATE, error="Invalid credentials")

    return render_template_string(LOGIN_TEMPLATE)


@app.route('/logout')
def logout():
    """Logout"""
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    return render_template_string(DASHBOARD_TEMPLATE)


@app.route('/run-agent/<agent_type>')
@login_required
def run_agent(agent_type):
    """Run a specific agent"""
    try:
        if agent_type == 'web-search':
            result = asyncio.run(run_web_search_agent())
        elif agent_type == 'function-tools':
            result = asyncio.run(run_function_tools_agent())
        elif agent_type == 'realtime':
            result = asyncio.run(run_realtime_simple())
        else:
            return jsonify({"error": "Invalid agent type"}), 400

        return jsonify({"success": True, "message": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})


# HTML Templates
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login - OpenAI Agents Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
        }
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            width: 300px;
        }
        h1 {
            margin-top: 0;
            color: #333;
            text-align: center;
        }
        input {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #5568d3;
        }
        .error {
            color: red;
            text-align: center;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>🤖 OpenAI Agents</h1>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        {% if error %}
        <p class="error">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - OpenAI Agents Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            margin: 0;
            padding: 20px;
        }
        .header {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        h1 {
            margin: 0;
            color: #333;
        }
        .logout-btn {
            padding: 10px 20px;
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .agents-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .agent-card {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            text-align: center;
        }
        .agent-card h2 {
            color: #667eea;
            margin-top: 0;
        }
        .agent-card p {
            color: #666;
            line-height: 1.6;
        }
        .run-btn {
            padding: 12px 30px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }
        .run-btn:hover {
            background: #5568d3;
        }
        .run-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 5px;
            display: none;
        }
        .result.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .result.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .icon {
            font-size: 48px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 OpenAI Agents Dashboard</h1>
            <a href="/logout" class="logout-btn">Logout</a>
        </div>

        <div class="agents-grid">
            <div class="agent-card">
                <div class="icon">🔍</div>
                <h2>Web Search Agent</h2>
                <p>An agent running in a loop with web search capabilities. Demonstrates how agents can search the internet for current information.</p>
                <button class="run-btn" onclick="runAgent('web-search', this)">Run Agent</button>
                <div class="result" id="result-web-search"></div>
            </div>

            <div class="agent-card">
                <div class="icon">🛠️</div>
                <h2>Function Tools Agent</h2>
                <p>Demonstrates custom function tools including calculator and weather lookup. Shows how to create and use custom tools.</p>
                <button class="run-btn" onclick="runAgent('function-tools', this)">Run Agent</button>
                <div class="result" id="result-function-tools"></div>
            </div>

            <div class="agent-card">
                <div class="icon">⚡</div>
                <h2>Realtime Agent</h2>
                <p>A realtime agent with streaming capabilities. Demonstrates the structure for voice/realtime interactions.</p>
                <button class="run-btn" onclick="runAgent('realtime', this)">Run Agent</button>
                <div class="result" id="result-realtime"></div>
            </div>
        </div>
    </div>

    <script>
        async function runAgent(agentType, button) {
            const resultDiv = document.getElementById(`result-${agentType}`);
            button.disabled = true;
            button.textContent = 'Running...';
            resultDiv.style.display = 'none';

            try {
                const response = await fetch(`/run-agent/${agentType}`);
                const data = await response.json();

                if (data.success) {
                    resultDiv.className = 'result success';
                    resultDiv.textContent = '✓ ' + data.message;
                } else {
                    resultDiv.className = 'result error';
                    resultDiv.textContent = '✗ Error: ' + (data.error || 'Unknown error');
                }
                resultDiv.style.display = 'block';
            } catch (error) {
                resultDiv.className = 'result error';
                resultDiv.textContent = '✗ Error: ' + error.message;
                resultDiv.style.display = 'block';
            } finally {
                button.disabled = false;
                button.textContent = 'Run Agent';
            }
        }
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
