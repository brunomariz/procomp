FROM python:3.13.5

RUN python3 -m venv /venv

# Copy requirements file if you have one, or install directly
RUN . /venv/bin/activate && pip install "fastapi[standard]"

# Expose port
EXPOSE 8000

# Run the FastAPI application
CMD ["fastapi", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]
