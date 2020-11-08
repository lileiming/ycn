#import vthread
#import requests
import urllib.request
from pprint import pprint
from bs4 import BeautifulSoup
from config import QUERY_URL, DOMAINS_FILE

DEBUG = False


def lookup_ip(url):
    print('quering', url)
    try:
        response = urllib.request.urlopen(url, timeout=10)
    except:
        print('urlopen failed, try reopenning...')
        try:
            response = urllib.request.urlopen(url, timeout=10)
        except:
            print('urlreopen failed.')
            return None
    try:
        html = response.read().decode('utf-8')
    except:
        print('response read failed, try rereading...')
        try:
            html = response.read().decode('utf-8')
        except:
            print('response reread failed.')
            return None

    bs = BeautifulSoup(html, 'html.parser')
    ips = bs.ul.strings
    return list(ips)


def lookup_host(url, domain):
    ips = lookup_ip(url)
    host = None
    if ips is not None:
        # host = ['{} {}'.format(ip, domain) for ip in ips]
        host = [[ip, domain] for ip in ips]
    if DEBUG:
        pprint(host)
    return host


def lookup_hosts(domains):
    conv_domains = lambda x: QUERY_URL.format(
        prefix='.'.join(x.split('.')[-2:]), suffix='' if x.count('.') == 1 else x
    )
    _domains = list(set(domains))
    _domains.sort(key=domains.index)
    urls = list(map(conv_domains, _domains))
    if DEBUG:
        pprint(urls)
    urls_domains = list(zip(urls, domains))
    hosts = []
    [hosts.extend(y) for y in list(map(lambda x: lookup_host(*x), urls_domains))]
    return hosts


def make_hosts_file_content(hosts):
    try:
        content = '\n'.join(['\t'.join(host) for host in hosts])
    except:
        return None
    return content


def pull_hosts_str(domains):
    hosts = lookup_hosts(domains)
    return make_hosts_file_content(hosts)


def get_domains():
    with open(DOMAINS_FILE) as f:
        content = f.read().splitlines()
    return content


def get_hosts():
    domains = get_domains()
    hosts = pull_hosts_str(domains)
    return hosts


def main():
    hosts = get_hosts()
    print('# Github')
    print(hosts)


if __name__ == '__main__':
    main()