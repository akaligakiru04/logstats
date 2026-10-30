from pathlib import Path

import logstatsf

no_ip_line_1 = "2026-10-23T11:00:37.098457+02:00 Farah groupadd[452]: new group: name=farah, GID=1000"
no_ip_line_2 = "2026-10-23T11:00:57.216209+02:00 Farah usermod[482]: add 'farah' to group 'adm'"
no_ip_line_3 = "2026-10-23T11:00:57.461552+02:00 Farah systemd-logind[188]: Session c1 logged out. Waiting for processes to exit."
fake_ip_line = "2026-10-23T11:02:20.868129+02:00 Farah sudo: farah : TTY=/dev/pts/0 ; PWD=/mnt/c/WINDOWS/system32 ; USER=root ; COMMAND=/usr/bin/ls /lib/modules/6.18.54.1-microsoft-standard-WSL2"
no_ip_line_4 = "2026-10-23T11:17:01.389496+02:00 Farah CRON[1175]: pam_unix(cron:session): session opened for user root(uid=0) by root(uid=0)"
no_ip_line_5 = "2026-10-23T11:02:20.865470+02:00 Farah sudo: pam_unix(sudo:session): session opened for user root(uid=0) by (uid=1000)"

ip_line_1 = "2026-10-23T05:12:06.098457+02:00 Farah sshd[12744]: Failed none for invalid user 0 from 192.0.2.4 port 49445 ssh2"
ip_line_2 = "2026-10-23T05:11:25.098457+02:00 Farah sshd[12740]: Failed password for invalid user 0101 from 198.51.100.99 port 47796 ssh2"
ip_line_3 = "2026-10-23T06:26:08.098457+02:00 Farah sshd[15088]: Did not receive identification string from 198.51.100.56 port 53286"
ip_line_4 = "2026-10-23T05:11:28.098457+02:00 Farah sshd[12739]: Failed password for invalid user 0101 from 203.0.113.15 port 34990 ssh2"
two_digit_port_line = "2026-10-23T05:11:28.098457+02:00 Farah sshd[12740]: Connection closed by 203.0.113.5 port 22 [preauth]"

empty_line = ""

path1 = Path(__file__).parent / "sample_auth.log"
path2 = Path(__file__).parent / "empty.log"


def test_sample_file_returns_all_ips():
    assert logstatsf.file_parser(path1) == [{'time':'2026-10-23T05:12:06.098457+02:00','ip':'192.0.2.4'}, {'time':'2026-10-23T05:11:25.098457+02:00','ip':'198.51.100.99'},{'time':'2026-10-23T06:26:08.098457+02:00','ip':'198.51.100.56'},{ 'time':'2026-10-23T05:11:28.098457+02:00','ip':'203.0.113.15'},{'time':'2026-10-23T05:11:28.098457+02:00','ip':'203.0.113.5'}]

def test_empty_file_returns_empty_list():
    assert logstatsf.file_parser(path2) == []
    
def test_no_ip_returns_None():
    assert logstatsf.ip_time_extractor(no_ip_line_4) is None

def test_sudo_version_returns_None():
    assert logstatsf.ip_time_extractor(fake_ip_line) is None

def test_sshd_failed_password_returns_time_and_ip():
    assert logstatsf.ip_time_extractor(ip_line_1) == { "time":'2026-10-23T05:12:06.098457+02:00', "ip":"192.0.2.4" }

def test_2_digit_port_returns_ip_and_time():
    assert logstatsf.ip_time_extractor(two_digit_port_line) == { "time":'2026-10-23T05:11:28.098457+02:00', "ip":"203.0.113.5" }

def test_empty_line_returns_None():
    assert logstatsf.ip_time_extractor(empty_line) is None
