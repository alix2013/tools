# cmd_runner_streamlit.py
import subprocess
import streamlit as st

st.set_page_config(page_title="Command Runner", layout="centered")

st.title("🖥️ Shell Command Runner")
st.write("Enter a command below. It will be executed on the server.")

command = st.text_input("Shell command", placeholder="e.g. ls -la")

if st.button("Run"):
    if command:
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True, timeout=5)
            st.code(output, language="bash")
        except subprocess.CalledProcessError as e:
            st.error(f"Command failed with error:\n{e.output}")
        except Exception as e:
            st.error(f"Exception: {str(e)}")
    else:
        st.warning("Please enter a command.")

