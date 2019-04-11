# -*- coding: utf-8 -*-
import urllib2

import os.path
import requests

LINE_TOKEN = ''
IP_TXT_FILENAME = 'ip.txt'


def get_global_ip():
    ip = urllib2.urlopen('http://ipcheck.ieserver.net').read().decode('utf-8').strip()
    return ip


def send_line(msg, token):
    api = 'https://notify-api.line.me/api/notify'

    post_data = {'message': msg}
    headers = {'Authorization': 'Bearer ' + token}
    verify = '/etc/ssl/certs/ca-bundle.crt'
    res = requests.post(api, data=post_data,
                        headers=headers, verify=verify)
    return res.text


if __name__ == "__main__":

    current_ip = get_global_ip()
    output_log = ''

    if os.path.exists(IP_TXT_FILENAME):
        ip_file = open(IP_TXT_FILENAME, 'r+')
        past_ip = ip_file.read().strip()
        if past_ip == current_ip:
            output_log = 'global ip is not changed.'
        else:
            # seek(), truncate() -> to overwrite ip.txt
            # http://d.hatena.ne.jp/kakurasan/20090309/p1
            ip_file.seek(0)
            ip_file.write(current_ip)
            ip_file.truncate()
            result = send_line(msg='Global IP is changed! Current IP is ' + current_ip, token=LINE_TOKEN)
            output_log = 'global ip is changed (' + past_ip + ' -> ' + current_ip + '), line api result is ' + result
    else:
        ip_file = open(IP_TXT_FILENAME, 'w')
        ip_file.write(current_ip)
        result = send_line(msg='Current Global IP is ' + current_ip, token=LINE_TOKEN)
        output_log = 'global ip is ' + current_ip + ', line api result is ' + result

    ip_file.close()
    print(output_log)
