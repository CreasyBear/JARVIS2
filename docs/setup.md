# JARVIS Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key

## Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/JARVIS.git
   cd JARVIS
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Download the spaCy English model:
   ```
   python -m spacy download en_core_web_sm
   ```

5. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`

6. Initialize the knowledge base:
   - Create a `data` directory in the project root
   - Add your initial documents to the `data` directory

## Project Structure
JARVIS/
├── data/
├── logs/
├── src/
│ ├── action_service.py
│ ├── calculation_service.py
│ ├── cost_estimator.py
│ ├── information_service.py
│ ├── logger.py
│ ├── main.py
│ ├── monitoring.py
│ ├── planner_agent.py
│ ├── report_generator.py
│ ├── summarization_service.py
│ ├── test_system.py
│ ├── web_scraping_service.py
│ └── workflows.py
├── docs/
│ ├── project_status.md
│ └── setup.md
├── .env
└── requirements.txt

## Running JARVIS

1. Start the multi-service system:
   ```
   python src/workflows.py
   ```
   This will deploy all the necessary services using LlamaIndex Deploy.

2. In a separate terminal, run the main JARVIS interface:
   ```
   python src/main.py
   ```

3. Enter your queries when prompted. The system will plan the task, execute it using the appropriate services, and return the result.

## Testing the System

To run the test script and ensure all components are working together:

1. Run the test script:
   ```
   python src/test_system.py
   ```

This script will test the system by sending queries to the main.py interface and checking the responses from the deployed services.

## Extending JARVIS

## Logging

JARVIS uses a logging system to track operations and errors. Log files are stored in the `logs/` directory:

- `main.log`: Main application logs
- `workflow.log`: Workflow-related logs
- `information.log`: Information service logs
- `calculation.log`: Calculation service logs
- `summarization.log`: Summarization service logs
- `action.log`: Action service logs

## Troubleshooting

- If you encounter any issues with service communication, ensure that all services are running and that your network allows the necessary connections.
- For performance issues, consider adjusting the resource allocation for each service in the `deploy` function calls.
- Check the log files in the `logs/` directory for detailed information about any errors or unexpected behavior.

For more detailed information on using LlamaIndex Deploy and Workflows, refer to the [LlamaIndex documentation](https://docs.llamaindex.ai/).

## Running JARVIS

1. Start the multi-service system:
   ```
   python src/workflows.py
   ```
   This will deploy all the necessary services using LlamaIndex Deploy.

2. In a separate terminal, run the main JARVIS interface:
   ```
   python src/main.py
   ```

3. Enter your queries when prompted. The system will classify the task, route it to the appropriate service, and return the result.

## Extending JARVIS

To add new services or modify existing ones:

1. Create a new service file in the `src` directory (e.g., `web_scraping_service.py`).
2. Implement the service logic using LlamaIndex components.
3. In `workflows.py`, add a new deployment for your service:
   ```python
   new_service = deploy(
       NewServiceClass().execute,
       "new_service_name",
       description="Description of the new service",
   )
   ```
4. Update the `route_task` method in `JARVISWorkflow` to include the new service.

## Troubleshooting

- If you encounter any issues with service communication, ensure that all services are running and that your network allows the necessary connections.
- For performance issues, consider adjusting the resource allocation for each service in the `deploy` function calls.

For more detailed information on using LlamaIndex Deploy and Workflows, refer to the [LlamaIndex documentation](https://docs.llamaindex.ai/).

## Setup Instructions

### Frontend (Next.js)

1. Navigate to the frontend directory:
   ```bash
   cd jarvis-frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

### Backend (Python)

1. Navigate to the project root:
   ```bash
   cd ..
   ```
2. Activate the virtual environment:
   ```bash
   source jarvis_env/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the backend service:
   ```bash
   python src/dashboard.py
   ```

### Environment Variables

1. Create a `.env` file in the `WORKING FOLDER` with the following:
   ```env
   LLAMA_INDEX_API_KEY=your_secure_api_key
   NEXT_PUBLIC_API_URL=http://localhost:3000/api
   ```
