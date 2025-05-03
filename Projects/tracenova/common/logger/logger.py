import logging
import sys
import os

def get_logger(module_name: str, service_name: str = "default_service") -> logging.Logger:
    logger = logging.getLogger(f"{service_name}.{module_name}")
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Console output
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Optional: File output per service
        log_dir = os.getenv("LOG_DIR", "./logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{service_name}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
