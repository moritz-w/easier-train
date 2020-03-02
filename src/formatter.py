import abc
import json


class Formatter(abc.ABC):


    @abc.abstractmethod
    def formatToStr (self, dct) -> str:
        pass


    @abc.abstractmethod
    def formatToFile (self, dct, filename):
        pass


    @property
    @abc.abstractmethod
    def name (self):
        pass



class JSONFormatter(Formatter):


    def formatToStr(self, dct) -> str:
        return json.dumps(dct, indent=4)


    def formatToFile(self, dct, filename):
        outstr = self.formatToStr(dct)
        if not outstr:
            raise ValueError("Something went wrong while encoding!")

        success = True
        try:
            with open(f"{filename}.json", 'w') as f:
                f.write(outstr)
        except IOError as e:
            print (e)
            success = False

        return success


    @property
    def name(self):
        return self.__name__


