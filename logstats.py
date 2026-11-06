import re
import sys
from dataclasses import dataclass

p = re.compile(r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\sport')
def ip_time_extractor(line):
    if not isinstance(line,str):
        raise TypeError(f"Invalid input type in:  {line} , expects String")
    matched = re.search(p,line)
    if matched is not None:
        return Record(line.split(" ")[0], matched.group(1))
@dataclass
class Record:
     time : str
     ip : str

def file_parser(path):
    with open(path) as f:
        for line in f:
            rec = ip_time_extractor(line)
            if rec is not None:
                 yield rec
        
def stats(path):
    lines = 0
    records = file_parser(path)
    records_list = list(records)
    lines_with_ip = len(records_list)
    with open(path) as f:
        lines = sum(1 for line in f)

    unique_ips = len(list({record.ip for record in records_list}))
    ip_count = {}
    for record in records_list:
        if ip_count.get(record.ip, 0):
             ip_count[record.ip] += 1
        else:
             ip_count[record.ip] = 1
    sorted_ips = sorted(ip_count.items(), key = lambda x : (-x[1],x[0]) ,reverse= False)
    top_ips = sorted_ips[:5]
    return(lines, lines_with_ip, unique_ips, top_ips)


if __name__ == "__main__" :
    path = sys.argv[1]
    try:
        lines, lines_with_ip, unique_ips, top_ips = stats(path)
        print("lines: " ,lines)
        print("lines_with_ip: " ,lines_with_ip)
        print("unique_ips: " ,unique_ips)
        print("top_ips: " ,top_ips)
    except FileNotFoundError:
            sys.exit(f"logstats : file not found <{path}>")
    except IsADirectoryError:
            sys.exit(f"<{path}> is a directory, expects a file")