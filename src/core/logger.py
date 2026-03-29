import logging
import os
from logging.handlers import TimedRotatingFileHandler


def setup_logging(log_filename='app.log'):
    """
    Configures the logging system for the application.

    Logs are written to both a file and the console, with log rotation every midnight.
    The "logs" directory is automatically created if it doesn't exist.
    Older logs are kept for 7 days.

    Args:
        log_filename (str, optional): Log file name (default: "app.log").

    Returns:
        logging.Logger: Configured logger instance.
    """
    log_dir = os.path.join(os.getcwd(), '.temp/logs')
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, log_filename)

    # Create rotating file handler
    file_handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # Configure logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(logging.StreamHandler())

    logging.getLogger('app.utils.some_module').setLevel(logging.WARNING)

    logger.info(f"Logging setup complete. Logs are stored in {log_file}")

    return logger
