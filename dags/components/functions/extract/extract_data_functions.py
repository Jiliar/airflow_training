import logging
import requests

from components.functions.i_extract import IExtractData

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    fmt='%(asctime)s [%(levelname)s] %(name)s - %(filename)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

class ExtractFunctions(IExtractData):
    def __init__(self, api_url: str, api_key: str, output_path_bash: str, output_path_python: str):
        self.api_url = api_url
        self.api_key = api_key
        self.output_path_bash = output_path_bash
        self.output_path_python = output_path_python
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                fmt='%(asctime)s [%(levelname)s] %(name)s - %(filename)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def get_api_bash_command(self) -> str:
        try:
            command = f'curl -o {self.output_path_bash} {self.api_url}?key={self.api_key}'
            self.logger.info("Generated Bash command: %s", command)
            return command  # Asegúrate de que siempre devuelva un string
        except Exception as e:
            self.logger.error("Error generating bash command: %s", str(e))
            raise

    def get_api_python(self) -> None:
        headers = {'X-API-Key': self.api_key}
        try:
            self.logger.info("Requesting data from API (Python)...")
            response = requests.get(self.api_url, headers=headers)
            if response.status_code == 200:
                with open(self.output_path_python, 'w') as f:
                    f.write(response.content.decode('utf-8'))
                self.logger.info("Data fetched and written to %s", self.output_path_python)
                self.logger.debug("Data content preview: %s", response.content.decode('utf-8')[:100])
            else:
                raise Exception(f"API request failed with status code: {response.status_code}")
        except Exception as e:
            self.logger.exception("Error fetching data from API: %s", e)
            raise