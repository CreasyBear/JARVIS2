import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name, log_file, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a rotating file handler
    handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Create loggers for each service
main_logger = setup_logger('main', 'logs/main.log')
workflow_logger = setup_logger('workflow', 'logs/workflow.log')
information_logger = setup_logger('information', 'logs/information.log')
calculation_logger = setup_logger('calculation', 'logs/calculation.log')
summarization_logger = setup_logger('summarization', 'logs/summarization.log')
action_logger = setup_logger('action', 'logs/action.log')