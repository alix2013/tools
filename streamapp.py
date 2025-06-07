# cmd_runner_streamlit.py
import subprocess
import streamlit as st

st.set_page_config(page_title="Command Runner", layout="centered")

st.title("🖥️ Shell Command Runner")
st.markdown("Enter a shell command below. The command will run on the server.")

# User input for command
command = st.text_input("command", placeholder="")

# Adjustable timeout
timeout = st.slider("Timeout (seconds)", min_value=1, max_value=60, value=10)

# Run button
if st.button("Run"):
    if not command.strip():
        st.warning("Please enter a command.")
    else:
        try:
            output = subprocess.check_output(
                command,
                shell=True,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=timeout
            )
            st.success("✅ Command executed successfully.")
            st.code(output, language="bash")
        except subprocess.TimeoutExpired:
            st.error(f"❌ Timeout: Command took longer than {timeout} seconds.")
        except subprocess.CalledProcessError as e:
            st.error("❌ Command failed with an error:")
            st.code(e.output, language="bash")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")

