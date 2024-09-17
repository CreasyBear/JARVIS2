# Backend Setup

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Docker (optional, for containerized deployment)

## Installation Steps

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download the spaCy English model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Project Structure
backend/
├── src/
│   ├── multi_agent_workflow.py
│   ├── llm_integration.py
│   └── ...
├── tests/
├── .env
└── requirements.txt

## Running the Backend

1. Start the backend service:
   ```bash
   python src/main.py
   ```

2. The backend will be available at `http://localhost:5000`.

## Running Tests

1. Run the test suite:
   ```bash
   pytest
   ```

## Deployment

1. Build the Docker image:
   ```bash
   docker build -t jarvis-backend .
   ```

2. Run the Docker container:
   ```bash
   docker run -d -p 5000:5000 jarvis-backend
   ```

For more detailed information, refer to the Flask documentation.
