"""runner module to be used for running this utility"""
from json_reader import ConfigJsonReader
from sink import SinkDataConnectorFactory
from source import SourceConnectorFactory
from transform import TransformationFactory


def main(config_json_path):
    config_json_reader = ConfigJsonReader()
    print(config_json_path)
    confJsonObj = config_json_reader.read(config_json_path)
    sourcedc = SourceConnectorFactory(confJsonObj.reader.connector).getDataConnector()
    sinkdc = SinkDataConnectorFactory(confJsonObj.writer.connector).getDataConnector()
    alltransformations = TransformationFactory(confJsonObj.transform).getTransformations()
    print(alltransformations)
    for transformation in alltransformations:
        inputdata = sourcedc.data()
        transformeddata = transformation.execute(inputdata)
        sinkdc.write(transformeddata, transformation.type)
    #print(repr(confJsonObj))

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Takes config json as input and runs this utility')
    parser.add_argument('--config_json', metavar='path', required=True,
                        help='the path to config json file')
    args = parser.parse_args()
    main(config_json_path = args.config_json)