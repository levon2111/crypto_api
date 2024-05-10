import logging

from dotenv import load_dotenv

from app.common.error import InternalError

load_dotenv()


class Config:
    version = "0.1.0"
    title = "Crypto API"

    app_settings = {
    }

    @classmethod
    def app_settings_validate(cls):
        for k, v in cls.app_settings.items():
            if None is v:
                logging.error(f'Config variable error. {k} cannot be None')
                raise InternalError([{"message": "Server configure error"}])
            else:
                logging.info(f'Config variable {k} is {v}')
