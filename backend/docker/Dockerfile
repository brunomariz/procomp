FROM python:3.13.5

RUN python3 -m venv /venv

# Copy requirements file if you have one, or install directly
COPY backend/requirements.txt requirements.txt

RUN . /venv/bin/activate && pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Run the FastAPI application
CMD [".", "/venv/bin/activate", "&&", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
