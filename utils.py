from sqlalchemy import create_engine
import yaml

CONFIG_FILE = 'config.yaml'

def get_config():
    with open(CONFIG_FILE, 'r') as file:
        config = yaml.safe_load(file)
    cfg=config['PG']
    return cfg

def get_engine():
    cfg = get_config()

    url = "{driver}://{user}:{password}@{host}/{database}".format(**cfg)
    print('URL', url)

    engine = create_engine(url)
    return engine