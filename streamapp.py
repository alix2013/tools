import subprocess
import streamlit as st
import shlex

st.set_page_config(page_title="Command Runner", layout="centered")

st.title("🖥️ Hello StreamApp")
command = st.text_input("Input", placeholder="")
timeout = st.slider("Timeout (seconds, only applies to foreground mode)", 1, 60, 10)
background = st.checkbox("Background ")

if st.button("Run"):
    if not command.strip():
        st.warning("Please enter a command.")
    else:
        if background:
            log_file = "output.log"
            final_cmd = f"nohup {command} > {log_file} 2>&1 &"
            try:
                subprocess.Popen(final_cmd, shell=True)
                st.success(f"✅ Background job started. Output will go to `{log_file}`.")
            except Exception as e:
                st.error(f"❌ Failed to start background process: {e}")
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
                st.error("❌ Command failed:")
                st.code(e.output, language="bash")
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")



