import os
import subprocess
import sys

# Auto-install Flask if not present
try:
    from flask import Flask, request, jsonify, render_template_string
except ImportError:
    print("Flask not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_PAGE = '''
<!doctype html>
<title>Command Runner</title>
<h2>Enter a shell command:</h2>
<form method="post" action="/run">
  <input type="text" name="command" style="width: 300px;">
  <input type="submit" value="Run">
</form>
<pre>{{ result }}</pre>
'''

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_PAGE, result="")

@app.route("/run", methods=["POST"])
def run_command():
    cmd = request.form.get("command")
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True, timeout=5)
    except subprocess.CalledProcessError as e:
        output = f"Error:\n{e.output}"
    except Exception as e:
        output = f"Exception: {str(e)}"
    return render_template_string(HTML_PAGE, result=output)

@app.route("/api/run", methods=["POST"])
def api_run_command():
    data = request.json
    cmd = data.get("command")
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True, timeout=5)
        return jsonify({"output": output})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.output}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)



