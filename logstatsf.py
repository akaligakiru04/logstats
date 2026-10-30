import re
import sys

p = re.compile(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\sport')
def ip_time_extractor(line):
    if not isinstance(line,str):
        raise TypeError(f"Invalid input type in:  {line} , expects String")
    matched = re.search(p,line)
    if matched is not None:
        return {'time':line.split(" ")[0],'ip':matched.group(1)}

def file_parser(path):
    with open(path) as f:
        ip_list = []
        for line in f:
            if ip_time_extractor(line) is not None:
                ip_list.append(ip_time_extractor(line))
        return ip_list

if __name__ == "__main__" :
    path = sys.argv[1]
    try:
        ip_list = file_parser(path)
    except FileNotFoundError:
        sys.exit(f"logstats : file not found <{path}>")
    print(ip_list)
    for dic in ip_list:
        print(f"Date and Time : {dic['time']}, IP Addresss : {dic['ip']}")