import os

import yaml

class Config:
    valid_keys = [
        'AMQP_HOST',
        'AMQP_PORT',
        'AMQP_USERNAME',
        'AMQP_PASSWORD',
        'AMQP_EXCHANGE',
        'AMQP_EXCHANGE_TYPE',
        'AMQP_QUEUE_NAME',
        'AMQP_ROUTING_KEY',
        'DOWNLOAD_LOCATION',
    ]

    config = {}

    def __init__(self):

        for key in self.valid_keys:
            self.config[key] = os.environ.get(key)

        if None in self.config.values():
            config_yaml = None
            with open('config.yml', 'r') as stream:
                try:
                    config_yaml = yaml.load(stream)
                except yaml.YAMLError as exc:
                    print(exc)

            if config_yaml == None:
                raise('Failed to parse config.yml')

            no_values = []
            for key in [key for key in self.config if self.config[key] == None]:

                if config_yaml[key] == None:
                    no_values.append(key)
                    continue

                self.config[key] = config_yaml[key]

            if no_values:
                raise('Failed to load keys from config: {}'.format(', '.join(no_values)))
