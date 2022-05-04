from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import json
from typing import List
from dataclass_wizard import JSONWizard

class SupportedConnectorType(Enum):
    FILE = "file"
    #JDBC = "jdbc"
class SupportedTransformation(Enum):
    TO_UPPER = "TO_UPPER"
    UNIQUE_WORD_COUNT = "UNIQUE_WORD_COUNT"

@dataclass
class DataConnectorParam:
    type: SupportedConnectorType
    config: dict

@dataclass
class TransformType:
    type: SupportedTransformation

@dataclass
class Reader:
    connector: DataConnectorParam

# @dataclass
# class Transform:
#     : List[str]    

@dataclass
class Writer:
    connector: DataConnectorParam

# The object which will hold the information related to configuration provided in json format
@dataclass
class ConfigJson(JSONWizard):
    reader: Reader
    transform: List[TransformType]
    writer: Writer


# ConfigJsonReader class used for reading the config json and return the dataclass object
class ConfigJsonReader:
    def read(self, filepath: str) -> ConfigJson: 
        # print("inside read method")
        with open(filepath, 'r', encoding='utf-8') as input:  
            return ConfigJson.from_json(input.read())

                        
# Defining main function
# def main():
#     print("inside main class,..")
#     confJson = ConfigJsonReader().read("../tests/config.json")
#     print(repr(confJson))
  
  
# Using the special variable 
# __name__
# if __name__=="__main__":
    # string = r"""
    # {
    # "reader": {
    #     "connector": {
    #         "type": "file",
    #         "config": {
    #             "path": "/file/location/withfilename/"
    #         }
    #     }
    # },
    # "transform": [
    #     {
    #         "type": "TO_UPPER"
    #     },
    #     {
    #         "type": "UNIQUE_WORD_COUNT"
    #     }
    # ],
    # "writer": {
    #     "connector": {
    #         "type": "file",
    #         "config": {
    #             "path": "/file/location/withfilename"
    #         }
    #     }
    # }
    # }
    # """

    # print(type(string))
    # r=ConfigJson.from_json(string)
    # print(repr(r))
    
    # with open("../tests/config.json", 'r', encoding='utf-8') as input:
    #         #txtjson = json.load(input)
    #         #ConfigJson(**json.loads(txtjson))
    #         #from_dict(ConfigJson, inputjson)
    #         #dumper = json.dumps(txtjson, indent=4)
    #         #print(dumper)
    #         #print(txtjson)
    #         textjson = input.read()
    #         print(type(textjson))
    #         values = ConfigJson.from_json(textjson)
    #         print(repr(values))
    # main()                        