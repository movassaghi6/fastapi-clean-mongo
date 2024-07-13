FROM python:3.12.4-bullseye

# Install poetry and dependencies
RUN python3 -m venv /opt/poetry-venv \
    && /opt/poetry-venv/bin/pip install -U pip setuptools \
    && /opt/poetry-venv/bin/pip install poetry==1.8.3

# Set the working directory
WORKDIR /my-clean-DI

# Copy the dependency files and install dependencies
COPY ./poetry.lock ./pyproject.toml ./
# Install dependencies
RUN . /opt/poetry-venv/bin/activate \
    && /opt/poetry-venv/bin/poetry config virtualenvs.create false \
    && /opt/poetry-venv/bin/poetry install --no-root \
    && /opt/poetry-venv/bin/poetry update


# Copy the rest of the application
COPY . .

# Ensure uvicorn is installed
RUN /opt/poetry-venv/bin/pip install uvicorn

# Verify uvicorn installation
RUN /opt/poetry-venv/bin/uvicorn --version

# Expose port 8000
EXPOSE 8000

# Define the command to run the application
CMD ["/opt/poetry-venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
