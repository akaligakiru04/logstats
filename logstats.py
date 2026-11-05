import re
import sys
from dataclasses import dataclass

p = re.compile(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\sport')
def ip_time_extractor(line):
    if not isinstance(line,str):
        raise TypeError(f"Invalid input type in:  {line} , expects String")
    matched = re.search(p,line)
    if matched is not None:
        # return {'time':line.split(" ")[0],'ip':matched.group(1)}
        return Record(line.split(" ")[0], matched.group(1))
@dataclass
class Record:
     time : str
     ip : str

def file_parser(path):
    with open(path) as f:
        for line in f:
            dic = ip_time_extractor(line)
            if dic is not None:
                 yield dic
        
def stats(path):
     file_parser(path)



if __name__ == "__main__" :
    
    print(list(file_parser("tests/sample_auth.log")))
    path = sys.argv[1]
    ip_list = file_parser(path)
    try:
        for dic in ip_list:
            print(f"Date and Time : {dic['time']}, IP Addresss : {dic['ip']}")
    except FileNotFoundError:
            sys.exit(f"logstats : file not found <{path}>")
    except IsADirectoryError:
            sys.exit(f"<{path}> is a directory, expects a file")