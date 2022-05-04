import abc
from dataclasses import dataclass
import os
from typing import Dict
from json_reader import ConfigJsonReader, DataConnectorParam
from json_reader import SupportedConnectorType

class UnsupportedDataConnector(RuntimeError):
    """Error raised when the connector type isn't supported"""
    pass

class DataConnector(metaclass=abc.ABCMeta):
    """connector interface with abstracted out methods which any connector can use for extensibility purpose of connector module"""
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'init') and 
                callable(subclass.init) and 
                hasattr(subclass, 'data') and 
                callable(subclass.data) or 
                NotImplemented)
    @abc.abstractmethod
    def init(self):
        """initialize the data connector with necessary connector configs"""
        raise NotImplementedError
    @abc.abstractmethod
    def data(self):
        """fetch the data from source using data connector props"""
        raise NotImplementedError

class ConnectorConfigError(RuntimeError):
    """Raised when the connector config is not proper"""
    pass

@dataclass
class FileDataConnector(DataConnector):
    """File based data connector. Will be instantiated when reader connector type set to file"""
    dcparam: DataConnectorParam
    def init(self):
        print("initializing the file data connector")
        config = self.dcparam.config
        print("printing the present config", config)
        self.validate_configs(self.dcparam.config)
        pass
    def data(self) -> str:
        with open(self.dcparam.config.get("path"), 'r', encoding='utf-8') as input:
            return input.read()

    def validate_configs(self, config: Dict) :
        if "path" in config:
            os.path.isfile(config.get("path"))
        else:
            raise ConnectorConfigError("config should have 'path' property set`")
        

class JDBCDataConnector(DataConnector):
    """Currently not supported. Will be available for future scope"""
    dcparam: DataConnectorParam
    def init(self):
        print("initializing the file data connector")
        config = self.dcparam.config
        print("printing the present config", config) 
        pass
    def data(self):
        """write your logic for jdbc connector"""
        pass

@dataclass
class SourceConnectorFactory:
    dcparam: DataConnectorParam
    
    def getDataConnector(self) -> DataConnector :
        contype = self.dcparam.type
        if contype is SupportedConnectorType.FILE:
            fileconnector = FileDataConnector(self.dcparam)
            # initialize the connector first then return the object
            fileconnector.init()
            return fileconnector
        else:
            raise UnsupportedDataConnector("{} Connector is not supported currently".format(contype))

def main():
    config_json_reader = ConfigJsonReader()
    config_json = config_json_reader.read("../tests/config.json")
    dc: DataConnector = FileDataConnector(config_json.reader.connector)   
    dc.init()  
    print(dc.data())  

if __name__=="__main__":
    main()         



