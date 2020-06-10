import json
import logging
import os
import sys
from pprint import pprint


class Logger:
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)


def get_config(config_file='config.json'):
    """
    Reads and parses the config file.
    """
    logger = Logger.logger
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            logger.info('Config found:\n')

            # Check config syntax briefly.
            for key in ['users', 'secret_key']:
                if not key in config:
                    logger.error('Config.json is missing "{}" attribute. Please add it.'.format(key))
                    sys.exit(-1)

            pprint(config)
            print('\n')
            return config
    else:
        with open(config_file, 'w') as file:
            config = {
                "users": [
                    {
                        "username": "admin",
                        "password": "pass123"
                    }
                ],
                "secret_key": "yp&3>d7H(T~_K6jhKDE9LHJJ",
            }
            json.dump(config, file, indent=4)
            return config

        logger.error('No config found. Default values will be set.')
        sys.exit(-1)
