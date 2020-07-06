import os.path
import re
from datetime import datetime
from datetime import timedelta
import os.path
import subprocess

filename = "/var/log/pveproxy/access.log"

i = 0
REGEXP_FORMAT=".*(extjs\/version\?_dc).*"

with open(filename, 'r') as f:
    for x in f:
        i += 1
        re_dto = re.search(REGEXP_FORMAT, x)
        if re_dto:
            dt_log = re_dto.group(0)
            dt_now = datetime.now()
            date_str = dt_log.split()[3].split('[')[1]
            if datetime.strptime('{}'.format(date_str), '%d/%m/%Y:%H:%M:%S') + timedelta(minutes=1) >= dt_now:
                ip_log = dt_log.split()[0]
                ip_log = re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip_log)
                user_log = dt_log.split()[2]
                process = subprocess.Popen(['/bin/bash', '/opt/ssh-login-alert-telegram/alert.sh', ip_log.group(0), user_log], stdout=subprocess.PIPE)
