# from pydantic import BaseModel

# from app.core.config import settings

# class LogConfig(BaseModel):
#     """Logging configuration to be set for the server"""

#     LOGGER_NAME: str = "app"
#     # LOG_FORMAT: str = "%(asctime)s - %(process)s - %(name)s - %(levelname)s - %(message)s"
#     LOG_FORMAT: str = '%(asctime)s,%(msecs)d %(levelname)-8s [%(pathname)s:%(lineno)d] %(message)s'
#     LOG_LEVEL: str = settings.LOG_LEVEL

#     # Logging config
#     version = 1
#     disable_existing_loggers = False
#     formatters = {
#         "default": {
#             "()": "uvicorn.logging.DefaultFormatter",
#             "fmt": LOG_FORMAT,
#             "datefmt": "%Y-%m-%d %H:%M:%S",
#         },
#     }
#     handlers = {
#         "default": {
#             "formatter": "default", 
#             "class": "logging.StreamHandler",
#             "stream": "ext://sys.stdout", 
#             "level": "DEBUG"
#         },
#     }
#     loggers = {
#         "gunicorn": {
#             "propagate": True
#         },
#         "uvicorn": {
#             "propagate": True
#         },
#         "uvicorn.access": {
#             "propagate": True
#         },
#         "app": {
#             "handlers": ["default"],
#             "level": LOG_LEVEL
#         },
#     }


# from logging.config import dictConfig
# import logging
# # from .config import LogConfig

# dictConfig(LogConfig().dict())
# logger = logging.getLogger("app")

# logger.info("Dummy Info")
# logger.error("Dummy Error")
# logger.debug("Dummy Debug")
# logger.warning("Dummy Warning")








# import logging

# from fastapi.logger import logger

# logger.setLevel(logging.DEBUG)

# logger.debug("Debug message")

# from fastapi.logger import logger as fastapi_logger

# gunicorn_error_logger = logging.getLogger("gunicorn.error")
# gunicorn_logger = logging.getLogger("gunicorn")
# uvicorn_access_logger = logging.getLogger("uvicorn.access")
# uvicorn_access_logger.handlers = gunicorn_error_logger.handlers

# fastapi_logger.handlers = gunicorn_error_logger.handlers

# fastapi_logger.setLevel(gunicorn_logger.level)

# if __name__ != "__main__":
#     fastapi_logger.setLevel(gunicorn_logger.level)
# else:
# fastapi_logger.setLevel(logging.DEBUG)

# fastapi_logger.debug('Logging initialized')
