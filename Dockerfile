FROM ubuntu:22.04

# Disable interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv curl wget sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Create a non-root user
ARG USER=appuser
ARG UID=1000
RUN useradd -m -u $UID -s /bin/bash $USER && \
    echo "$USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN chmod 700 /home/$USER
# Set working directory
WORKDIR /home/$USER/app

# Copy the application files (adjust your paths as needed)
COPY --chown=$USER:$USER . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Switch to non-root user
USER $USER

# Expose the Flask default port
EXPOSE 7860

# Start the Flask app (update 'app.py' and 'app' as needed)
CMD ["python3", "app.py"]

