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
            for key in ['interval', 'deployments', 'namespace', 'node_label_selector']:
                if not key in config:
                    logger.error('Config.json is missing "{}" attribute. Please add it.'.format(key))
                    sys.exit(-1)

            valid_interval = isinstance(config['interval'], int) and config['interval'] > 0
            valid_deployments = isinstance(config['deployments'], list) and not bool([])
            valid_namespace = isinstance(config['namespace'], str) and not bool(config['namespace'])
            valid_node_label_selector = isinstance(config['node_label_selector'], str) and not bool(
                config['node_label_selector'])

            if not valid_interval and valid_deployments and valid_namespace and valid_node_label_selector:
                logger.error('Config.json is not valid. Please check it.')
                sys.exit(-1)

            pprint(config)
            print('\n')
            return config
    else:
        with open(config_file, 'w') as file:
            config = {
                'deployments': [],
                'interval': 0,
                'namespace': '',
                'node_label_selector': '',
            }
            json.dump(config, file, indent=4)

        logger.error('No config found. Please provide one by editing the generated config.json.')
        sys.exit(-1)
