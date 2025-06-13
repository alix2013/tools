from flask import Flask, request, render_template_string
import subprocess
import os

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Command Runner</title>
    <style>
        body { font-family: sans-serif; padding: 20px; max-width: 800px; margin: auto; }
        textarea { width: 100%%; height: 200px; }
        input[type="text"] { width: 70%%; padding: 5px; }
    </style>
</head>
<body>
    <h1> Input </h1>
    <form method="POST">
        <input name="command" placeholder="" />
        <p>
        <label><input type="checkbox" name="background" {% if background %}checked{% endif %}/> Run in background</label>
        <button type="submit">Run</button>
    </form>

    {% if output %}
        <h3>Output:</h3>
        <textarea readonly>{{ output }}</textarea>
    {% endif %}

    {% if background %}
        <h3>Last Background Output (output.log):</h3>
        <form method="GET">
            <button name="view_log" value="1"> Refresh output.log</button>
        </form>
        <textarea readonly>{{ log_output }}</textarea>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    return "hello"

@app.route("/cmd", methods=["GET", "POST"])
def index():
    output = ""
    log_output = ""
    background = False

    if request.method == "POST":
        command = request.form.get("command", "")
        background = request.form.get("background") == "on"

        if not command.strip():
            output = "⚠️ Please enter a command."
        else:
            if background:
                try:
                    full_cmd = f"nohup {command} > output.log 2>&1 &"
                    subprocess.Popen(full_cmd, shell=True)
                    output = f"✅ Background job started: `{command}`.\nOutput will be written to `output.log`."
                except Exception as e:
                    output = f"❌ Failed to start background command: {e}"
            else:
                try:
                    result = subprocess.check_output(
                        command, shell=True, stderr=subprocess.STDOUT, text=True, timeout=30
                    )
                    output = result
                except subprocess.TimeoutExpired:
                    output = "❌ Command timed out after 30 seconds."
                except subprocess.CalledProcessError as e:
                    output = f"❌ Command failed:\n{e.output}"
                except Exception as e:
                    output = f"❌ Error: {e}"

    # For viewing log content after background job
    if request.method == "GET" and request.args.get("view_log") == "1":
        background = True
        try:
            with open("output.log", "r") as f:
                log_output = f.read()
        except FileNotFoundError:
            log_output = "output.log not found yet."

    return render_template_string(TEMPLATE, output=output, background=background, log_output=log_output)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

