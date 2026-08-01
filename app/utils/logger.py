import logging
import os

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/app.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ShareMindAI")