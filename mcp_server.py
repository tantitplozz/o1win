# mcp_server.py
import json
import sys
import traceback

import pygame
import requests
from requests.auth import HTTPBasicAuth

# --- Configuration for the Langgarh API ---
LANGGARH_API_URL = "http://173.208.162.7:8081/api/chat"  # External service
LANGGARH_API_USER = "win"
LANGGARH_API_PASSWORD = "win"
OLLAMA_LOCAL_API_URL = "http://localhost:11434/api/chat"  # Default local Ollama URL

# Global flag to ensure pygame.mixer is initialized only once
PYGAME_MIXER_INITIALIZED = False
PYGAME_MIXER_INIT_ERROR = None


def initialize_pygame_mixer_once():
    """Initializes pygame.mixer only once and stores the result."""
    global PYGAME_MIXER_INITIALIZED, PYGAME_MIXER_INIT_ERROR
    if PYGAME_MIXER_INITIALIZED:
        return True
    if PYGAME_MIXER_INIT_ERROR is not None:  # If it failed before, return failure
        return False
    try:
        pygame.mixer.init()
        PYGAME_MIXER_INITIALIZED = True
        log("Pygame mixer initialized successfully.")
        return True
    except pygame.error as e_pygame_error:
        PYGAME_MIXER_INIT_ERROR = str(e_pygame_error)
        log(
            f"ERROR: Failed to initialize pygame.mixer (pygame.error): {e_pygame_error}"
        )
        return False
    except Exception as e_general_error:
        PYGAME_MIXER_INIT_ERROR = str(e_general_error)
        log(
            f"ERROR: Failed to initialize pygame.mixer (general error): {e_general_error}"
        )
        return False


def call_langgarh_chat_api(
    model_name: str,
    user_message: str,
    use_local_ollama: bool = False,
    local_ollama_url: str | None = None,
) -> dict:
    """
    Calls an Ollama-like chat API.
    Can target the pre-configured external Langgarh service or a local Ollama instance.
    """
    headers = {"Content-Type": "application/json"}

    target_url = OLLAMA_LOCAL_API_URL if use_local_ollama else LANGGARH_API_URL
    if use_local_ollama and local_ollama_url:  # Allow overriding default local URL
        target_url = local_ollama_url

    auth_to_use = (
        HTTPBasicAuth(LANGGARH_API_USER, LANGGARH_API_PASSWORD)
        if not use_local_ollama
        else None
    )

    # Standard Ollama chat payload structure
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": user_message}],
        "stream": False,  # Assuming non-streaming for simplicity with MCP stdio
    }

    log(
        f"Calling Chat API. URL: {target_url}, Model: {model_name}, Local: {use_local_ollama}, Message: {user_message[:50]}..."
    )

    try:
        response = requests.post(
            target_url,
            headers=headers,
            auth=auth_to_use,  # Will be None for local Ollama, which is correct
            data=json.dumps(payload),
            timeout=120,  # 120s timeout
        )
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        log(f"Chat API responded with status: {response.status_code}")
        return response.json()
    except requests.exceptions.Timeout as e_timeout:
        log(f"ERROR: Chat API request timed out: {str(e_timeout)}")
        return {"error": "API request timed out", "details": str(e_timeout)}
    except requests.exceptions.HTTPError as e_http:
        err_response_text = (
            e_http.response.text
            if hasattr(e_http, "response") and e_http.response is not None
            else "No response body from HTTPError"
        )
        err_status_code = (
            e_http.response.status_code
            if hasattr(e_http, "response") and e_http.response is not None
            else "N/A"
        )
        log(f"ERROR: Chat API HTTPError: {err_status_code} - {err_response_text}")
        return {
            "error": f"API HTTPError {err_status_code}",
            "details": err_response_text,
        }
    except requests.exceptions.RequestException as e_req:
        log(f"ERROR: Chat API RequestException: {str(e_req)}")
        return {"error": "API request failed", "details": str(e_req)}
    except json.JSONDecodeError as e_json:
        log(f"ERROR: Failed to decode JSON response from Chat API: {str(e_json)}")
        return {"error": "Invalid JSON response from API", "details": str(e_json)}


def log(message):
    """Helper function to print logs to stderr for MCP stdio server debugging."""
    print(message, file=sys.stderr, flush=True)


def process_tool_call(tool_request: dict) -> dict:
    """Processes a single tool call request from OpenHands."""
    tool_name = tool_request.get("tool_name")
    args = tool_request.get("args", {})

    log(f"Received tool call: {tool_name} with args: {args}")

    if tool_name == "langgarh_chat":
        model = args.get("model")
        message = args.get("message")
        use_local = args.get("use_local_ollama", False)
        custom_local_url = args.get("local_ollama_url")

        if not model or not message:
            log("ERROR: 'model' and 'message' are required for langgarh_chat")
            return {"error": "Missing 'model' or 'message' argument for langgarh_chat"}
        return call_langgarh_chat_api(
            model,
            message,
            use_local_ollama=use_local,
            local_ollama_url=custom_local_url,
        )
    if tool_name == "play_pygame_sound":
        if not initialize_pygame_mixer_once():
            return {
                "error": "Pygame mixer could not be initialized.",
                "details": PYGAME_MIXER_INIT_ERROR,
            }

        sound_file_path = args.get("file_path")
        if not sound_file_path:
            log("ERROR: 'file_path' is required for play_pygame_sound")
            return {"error": "Missing 'file_path' argument for play_pygame_sound"}
        try:
            log(f"Attempting to play sound: {sound_file_path}")
            sound = pygame.mixer.Sound(sound_file_path)
            sound.play()
            log(f"Successfully started playing sound: {sound_file_path}")
            return {
                "status": "success",
                "message": f"Sound '{sound_file_path}' started playing.",
            }
        except pygame.error as e_pygame:
            log(
                f"ERROR: Pygame error playing sound '{sound_file_path}': {str(e_pygame)}"
            )
            return {"error": "Pygame error playing sound", "details": str(e_pygame)}
        except Exception as e:
            log(f"ERROR: Generic error playing sound '{sound_file_path}': {str(e)}")
            return {"error": "Generic error playing sound", "details": str(e)}
    else:
        log(f"ERROR: Unknown tool_name: {tool_name}")
        return {"error": f"Unknown tool: {tool_name}"}


def main_loop():
    """
    Main loop for the MCP stdio server.
    Reads JSON requests from stdin and writes JSON responses to stdout.
    """
    log("MCP Server (stdio) started. Waiting for requests...")
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            log(f"Received line from stdin: {line[:200]}...")  # Log truncated line
            try:
                request_json = json.loads(line)
            except json.JSONDecodeError as e_json_main:
                log(
                    f"ERROR: Invalid JSON received in main_loop: {line}. Error: {str(e_json_main)}"
                )
                # According to MCP spec, if unparseable, might need specific error response
                # For now, just log and continue or send a generic error
                error_response = {
                    "error": "Invalid JSON input",
                    "details": str(e_json_main),
                }
                print(json.dumps(error_response), flush=True)
                continue

            # Assuming the request is a tool call (OpenHands might send other message types)
            # A robust server would check message types (e.g., tool_listing, tool_call)
            if isinstance(request_json, dict) and "tool_name" in request_json:
                response_data = process_tool_call(request_json)
            else:
                # Handle other potential MCP messages or errors if needed
                log(
                    f"WARNING: Received non-tool_call message or malformed request: {request_json}"
                )
                response_data = {
                    "error": "Unsupported request format or not a tool call"
                }

            response_str = json.dumps(response_data)
            log(f"Sending response to stdout: {response_str[:200]}...")
            print(response_str, flush=True)
            log("Waiting for next request...")

    except EOFError:
        log("EOF received, MCP server shutting down.")
    except KeyboardInterrupt:
        log("KeyboardInterrupt received, MCP server shutting down.")
    except (IOError, OSError) as e_io:  # More specific exceptions for IO/OS issues
        log(f"IO/OS ERROR in MCP main loop: {str(e_io)}\n{traceback.format_exc()}")
        fatal_error_response = {"error": "IO/OS server error", "details": str(e_io)}
        try:
            print(json.dumps(fatal_error_response), flush=True)
        except (
            OSError,
            TypeError,
        ):  # Catch specific errors for print during fatal error reporting
            pass
    except (
        Exception
    ) as e_fatal:  # noqa: E722 # pylint: disable=broad-except # General Exception as the very last resort
        log(
            f"UNHANDLED FATAL ERROR in MCP main loop: {str(e_fatal)}\n{traceback.format_exc()}"
        )
        fatal_error_response = {
            "error": "Unhandled fatal server error",
            "details": str(e_fatal),
        }
        try:
            print(json.dumps(fatal_error_response), flush=True)
        except (
            OSError,
            TypeError,
        ):  # Catch specific errors for print during fatal error reporting
            pass
    finally:
        if PYGAME_MIXER_INITIALIZED:  # Quit pygame mixer if it was initialized
            pygame.mixer.quit()
            log("Pygame mixer quit successfully.")
        log("MCP Server exited.")


if __name__ == "__main__":
    main_loop()
