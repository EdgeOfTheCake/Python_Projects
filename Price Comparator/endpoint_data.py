import json
import os


class EndpointData:
    def __init__(self):
        self.endpoint_data = {}
        self.currency_rates = {}

    def read_data(self, datas_file_path):
        for file in datas_file_path:
            try:
                if os.path.exists(file):
                    f = open(file, 'r')
                    if "endpoint_data" in file:
                        self.endpoint_data = json.loads(f.read())
                    else:
                        self.currency_rates = json.loads(f.read())
                else:
                    print("Reading data Failed: Requested data file does not exist")
                    raise FileNotFoundError(f"Config file not found: {file}")
            except ValueError:
                print("Reading data Failed: JSON syntax not recognized")
                raise ValueError(f"Config file has wrong format: {file}")
    