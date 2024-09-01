import yaml

from utils.Log import Log



class ConfigLoader():
    def __init__(self, base_url) -> None:
        self.base_url = base_url

    def read_yaml(self, file_name):
        file_path = f"{self.base_url}/{file_name}"
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)

        logger = Log()
        logger.debug(f"loaded {file_name} finished...")
        return data
    
