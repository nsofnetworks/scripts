#!/usr/bin/python3

"""
This script generates DNS record per device/client (aka device alias).
The DNS record is created from the device name and optionally concatenated
 with a domain name

In order to use this script, you must pass the following environment vars:
1. API_KEY_ID: Your API Key ID
2. API_KEY_SECRET: Your API Key secret

You may pass a domain name: --domain-name {my_domain_name}

The script requires only python v3.6

Usage example:
API_KEY_ID=key-** API_KEY_SECRET=** python3 generate_fqdn.py --domain-name x.x
"""
import functools
import os
import re
import requests
import sys
import time

API_ENDPOINT = os.getenv("API_ENDPOINT", "https://api.metanetworks.com")
API_KEY_ID = os.environ["API_KEY_ID"]
API_KEY_SECRET = os.environ["API_KEY_SECRET"]


def memoize_ttl(ttl):
    def _memoize(func):
        cache = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            value, age = cache.get('token', (None, None))
            if age is None or age + ttl < now:
                value = func(*args, **kwargs)
                cache['token'] = value, now
            return value
        return wrapper
    return _memoize


@memoize_ttl(270)
def get_access_token():
    url = "%s/v1/oauth/token" % API_ENDPOINT
    request_data = {"grant_type": "client_credentials",
                    "client_id": API_KEY_ID,
                    "client_secret": API_KEY_SECRET}
    response = requests.post(url=url, json=request_data)
    response.raise_for_status()
    return response.json()['access_token']


def get_devices():
    access_token = get_access_token()
    url = "%s/v1/network_elements" % API_ENDPOINT
    headers = {'Authorization': 'Bearer %s' % access_token}
    params = {"type": "Device", "expand": True}
    response = requests.get(url=url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def modify_aliases(method, ne_id, alias):
    access_token = get_access_token()
    url = "%s/v1/network_elements/%s/aliases/%s" % (API_ENDPOINT, ne_id, alias)
    headers = {'Authorization': 'Bearer %s' % access_token}
    response = requests.request(method, url=url, headers=headers)
    if not response.ok:
        print(response.json()['detail'])


def is_hostname(instance):
    if len(instance) < 1 or len(instance) > 255 or instance[-1] == ".":
        return False
    labels = instance.split(".")
    # the TLD must be not all-numeric
    if re.match(r"[0-9]+$", labels[-1]):
        return False
    allowed = re.compile(r"(?!-)[A-Z\d\-\_]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(label) for label in labels)


def _get_alias(device_name, domain_name):
    return "%s.%s" % (domain_name, device_name) if domain_name else device_name


def _get_device_name(dev):
    device_info = dev.get("device_info") or {}
    return device_info.get("device_name")


def generate_fqdns(domain_name=None, deprovisioning=False):
    for dev in get_devices():
        device_name = _get_device_name(dev)
        if not device_name:
            print("%s doesn't have a device name, skipping" % dev['id'])
            continue
        alias = _get_alias(device_name, domain_name)
        if not is_hostname(alias):
            print("%s isn't a valid hostname, skipping" % alias)
            continue
        if alias not in dev['aliases'] and not deprovisioning:
            print("Setting alias %s for %s" % (alias, dev['id']))
            modify_aliases("put", dev['id'], alias)
        elif alias in dev['aliases'] and deprovisioning:
            print("Removing alias %s from %s" % (alias, dev['id']))
            modify_aliases("delete", dev['id'], alias)


if __name__ == '__main__':
    deprovision = '--deprovision' in sys.argv
    domain_name = None
    if '--domain-name' in sys.argv:
        try:
            domain_name = sys.argv[sys.argv.index('--domain-name') + 1]
        except IndexError:
            print("Please enter your domain name after --domain-name")
            sys.exit()
    generate_fqdns(domain_name=domain_name, deprovisioning=deprovision)
