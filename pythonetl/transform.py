import abc
from dataclasses import dataclass
from typing import List
from unittest import case

from json_reader import SupportedTransformation, TransformType

class UnSupportedTransformationError(RuntimeError):
    pass

@dataclass
class Transformation(metaclass=abc.ABCMeta):
    """Transformation interface which can be used by many """
    type: str
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'validate') and 
                callable(subclass.init) and 
                hasattr(subclass, 'execute') and 
                callable(subclass.data) or 
                NotImplemented)
    @abc.abstractmethod
    def validate(self):
        """validates the transformation props used. Can be used for future scope"""
        raise NotImplementedError
    @abc.abstractmethod
    def execute(self, data: str):
        """running the transformation logic on input data"""
        raise NotImplementedError

@dataclass
class ToUpperTransformation(Transformation):
    type: str
    """transformation for convering each character of the text file into upper case"""
    def validate(self):
        pass
    def execute(self, data: str):
        return data.upper() 

@dataclass
class UniqueWordCount(Transformation):
    """transformation for calculating case insensitive unque word count present in a text"""
    def validate(self):
        pass 
    def execute(self, data: str):
        case_insensitive_data = data.lower()
        # print(case_insensitive_data)
        from collections import Counter
        wordcount = Counter(case_insensitive_data.split())
        #return count
        # return the formatted result to be pushed into sunk
        return '\n'.join(["{}\t{}".format(*item) for item in wordcount.items()]) 

@dataclass
class TransformationFactory:
    tfparam: List[TransformType]
    def getTransformations(self) -> List[Transformation]:
        tlist = []
        for transformtype in self.tfparam:
            if transformtype.type is SupportedTransformation.TO_UPPER:
                tlist.append(ToUpperTransformation(SupportedTransformation.TO_UPPER.name))
            elif transformtype.type is SupportedTransformation.UNIQUE_WORD_COUNT:
                tlist.append(UniqueWordCount(SupportedTransformation.UNIQUE_WORD_COUNT.name))
            else:
                UnSupportedTransformationError("{} isn't supported currently".format(transformtype))
        return tlist
def main():
    with open("../tests/input.txt", 'r', encoding='utf-8') as input:
        lines = input.read()
        # print(lines)
        wordcount = UniqueWordCount().execute(lines)
        print(wordcount)

if __name__=="__main__":
    main()