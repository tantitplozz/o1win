import uvicorn
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

# from fastapi.templating import Jinja2Templates # Not used with embedded HTML

app = FastAPI()

# In a real scenario, you'd have a templates directory. For simplicity, we'll embed HTML.
# However, for a slightly better structure, let's imagine a simple template string.

html_form = """
<!DOCTYPE html>
<html>
<head>
    <title>OpenHands Interface</title>
    <style>
        body { font-family: sans-serif; margin: 20px; background-color: #f4f4f9; color: #333; }
        .container { background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { color: #5a5a5a; }
        label { display: block; margin-bottom: 8px; font-weight: bold; }
        textarea { width: 100%; padding: 10px; margin-bottom: 20px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; min-height: 100px; }
        button { background-color: #007bff; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #0056b3; }
        .response { margin-top: 20px; padding: 15px; background-color: #e9ecef; border: 1px solid #ced4da; border-radius: 4px; }
        .response h2 { margin-top: 0; color: #495057; }
        pre { white-space: pre-wrap; word-wrap: break-word; background-color: #f8f9fa; padding: 10px; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>OpenHands Command Interface</h1>
        <form action="/submit_command" method="post">
            <label for="command_text">Enter your command for OpenHands:</label>
            <textarea id="command_text" name="command_text" rows="4"></textarea>
            <button type="submit">Submit Command</button>
        </form>
        {% if command_received %}
        <div class="response">
            <h2>Command Received:</h2>
            <pre>{{ command_received }}</pre>
            <p><em>(Note: This interface currently only displays the command. Actual execution by OpenHands is not yet implemented here.)</em></p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

# Simulate Jinja2Templates for in-memory HTML
# In a real app, you would use:
# templates = Jinja2Templates(directory="templates")
# and place the html file in a 'templates' folder.


@app.get("/", response_class=HTMLResponse)
async def read_root():
    # This is a simplified way to "render" the template string
    # In a real Jinja2 setup, you'd pass a context dictionary.
    return HTMLResponse(
        content=html_form.replace("{% if command_received %}", "")
        .replace("{% endif %}", "")
        .replace("<pre>{{ command_received }}</pre>", "")
        .replace("<h2>Command Received:</h2>", "")
        .replace(
            """<p><em>(Note: This interface currently only displays the command. Actual execution by OpenHands is not yet implemented here.)</em></p>""",
            "",
        )
    )


@app.post("/submit_command", response_class=HTMLResponse)
async def handle_command(command_text: str = Form(...)):
    # For now, just display the command back.
    # Replace parts of the template to show the command_received block
    response_html = html_form.replace(
        "{% if command_received %}", ""
    )  # Remove the if condition start
    response_html = response_html.replace(
        "{% endif %}", ""
    )  # Remove the if condition end
    response_html = response_html.replace(
        "{{ command_received }}", command_text
    )  # Insert the command
    return HTMLResponse(content=response_html)


@app.get("/submit_command", response_class=HTMLResponse)
async def handle_get_submit_command():
    # Redirect GET requests for /submit_command to the root page or show a message
    return HTMLResponse(
        content='<h1>Please submit commands via the form on the main page.</h1><p><a href="/">Go to main page</a></p>'
    )


def get_vscode_url_for_session(session_id: str):
    # This is a conceptual placeholder.
    # In a real scenario, this would involve:
    # 1. Knowing the OpenHands API endpoint that provides the VSCode URL for a given session.
    #    This endpoint is usually part of the my-openhands-app service.
    #    Let's assume it's something like /api/conversations/{session_id}/vscode-url
    # 2. Making an HTTP GET request to that endpoint.
    #    Since we can't make HTTP requests directly here, we'll simulate.

    # Simulate checking if the runtime container for the session is active
    # and if the vscode plugin is enabled.
    # We know from previous logs that the runtime for c3d16... is 63cf60b63811
    # and it has the vscode plugin.

    print(f"Attempting to get VSCode URL for session: {session_id}")
    # In a real implementation, you would make an API call here.
    # For now, let's assume the my-openhands-app would expose this.
    # The actual URL format is often vscode://all-hands-ai.openhands/...
    # This is a placeholder and might not be the exact live URL.
    if session_id == "c3d168b8e03945109603ccf56e296519":
        # This is a conceptual representation. The actual mechanism involves OpenHands
        # creating a specific token and path for the remote server.
        # The URL would typically be obtained via an API call to the OpenHands backend.
        # The backend (my-openhands-app) usually provides this URL if the 'vscode'
        # plugin is active for the runtime sandbox.

        # Based on logs: "02:41:32 - openhands:DEBUG: docker_runtime.py:181 - [runtime c3d168b8e03945109603ccf56e296519] Container initialized with plugins: ['vscode']. VSCode URL: None"
        # The log shows "VSCode URL: None" initially for the runtime.
        # However, the my-openhands-app (frontend/API) is responsible for generating
        # the actual vscode:// URL when requested by the UI.
        #
        # The UI typically makes a request to an endpoint like:
        # GET /api/conversations/{session_id}/vscode-url
        # And the backend responds with the URL.

        # Let's simulate what the backend might return if the feature is working.
        # The token and specifics would be dynamically generated.
        simulated_url = f"vscode://all-hands-ai.openhands/愁䈯அல்லாஹ்c3d168b8e03945109603ccf56e296519?token=SIMULATED_TOKEN_FOR_{session_id}"
        print(f"Simulated VSCode URL for session {session_id}: {simulated_url}")
        print(
            "Please try opening this URL with VS Code (e.g., via 'Open URI' in Command Palette or by pasting it into a browser that can handle vscode:// links)."
        )
        print(
            "If this doesn't work, it means the VS Code integration feature might not be fully exposed or active in your current OpenHands setup, or the actual URL needs to be retrieved from the OpenHands UI's network requests when clicking the VS Code button."
        )
        return simulated_url
    print(
        f"Cannot determine VSCode URL for session {session_id} through this simulated method."
    )
    return None


# Example of how you might call this (for testing purposes)
# current_session_id = "c3d168b8e03945109603ccf56e296519"
# vscode_url = get_vscode_url_for_session(current_session_id)

if __name__ == "__main__":
    print("Starting OpenHands Interface Server on http://localhost:3001")
    print(
        "Access via ngrok at https://chaichanaomg.ngrok.app if ngrok is running for port 3001."
    )
    uvicorn.run(app, host="0.0.0.0", port=3001)
