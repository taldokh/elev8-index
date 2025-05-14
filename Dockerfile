FROM python:3.11-slim

RUN pip install pipenv

# Set working directory
WORKDIR /app

# Copy only Pipfile first for dependency caching
COPY Pipfile Pipfile.lock* ./

# Install dependencies
RUN pipenv install --system --deploy

# Now copy the rest of the code
COPY main.py InsertEquitiesToDBTopRelative.py insertEquitiesToDB generateEquitiesFileTercile generateEquitiesFile calculateIndexPoints ./
COPY models ./models

# Default command to run the backtest
CMD ["python", "main.py"]
