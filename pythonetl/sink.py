import abc
from dataclasses import dataclass
import os
from typing import Dict
import uuid
from json_reader import DataConnectorParam, ConfigJsonReader
from json_reader import SupportedConnectorType
from source import UnsupportedDataConnector

class SinkDataConnector(metaclass=abc.ABCMeta):
    """connector interface with abstracted out methods which any connector can use for extensibility purpose of connector module"""
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'init') and 
                callable(subclass.init) and 
                hasattr(subclass, 'write') and 
                callable(subclass.data) or 
                NotImplemented)
    @abc.abstractmethod
    def init(self):
        """initialize the data connector with necessary connector configs"""
        raise NotImplementedError
    @abc.abstractmethod
    def write(self, data: str, transformtype: str = "DEFAULT"):
        """write the data into source using data connector props"""
        raise NotImplementedError

class SinkConnectorConfigError(RuntimeError):
    """Raised when the connector config is not proper"""
    pass


@dataclass
class SinkFileDataConnector(SinkDataConnector):
    """File based data connector. Will be instantiated when writer connector type set to file"""
    dcparam: DataConnectorParam
    def init(self):
        print("initializing the sink file data connector")
        config = self.dcparam.config
        print("printing the present config", config)
        self.validate_configs(self.dcparam.config)
        pass
    def write(self, data: str, transformtype: str = "DEFAULT"):
        filename = transformtype + uuid.uuid4().hex + ".txt"
        filepath = self.dcparam.config.get("path") + "/" + filename
        print("writing data into this path: {}".format(filepath))
        with open(filepath, 'w+', encoding='utf-8') as out:
            out.write(data)
   
    def validate_configs(self, config: Dict) :
        if "path" in config:
            if os.path.isdir(config.get("path")) != True:
                raise SinkConnectorConfigError("Writer directory path doesn't exist. Please provide correct directory path")
        else:
            raise SinkConnectorConfigError("config should have 'path' property set")

@dataclass
class SinkDataConnectorFactory:
    dcparam: DataConnectorParam
    
    def getDataConnector(self) -> SinkDataConnector :
        contype = self.dcparam.type
        if contype is SupportedConnectorType.FILE:
            fileconnector = SinkFileDataConnector(self.dcparam)
            # initialize the connector first then return the object
            fileconnector.init()
            return fileconnector
        else:
            raise UnsupportedDataConnector("{} Sink connector is not supported currently".format(contype))

def main():
    config_json_reader = ConfigJsonReader()
    config_json = config_json_reader.read("../tests/config.json")
    dc: SinkDataConnector = SinkFileDataConnector(config_json.writer.connector)   
    dc.init()  
    print(dc.write("hello world"))

if __name__=="__main__":
    main()  
