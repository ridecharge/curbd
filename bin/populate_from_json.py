#!/usr/bin/env python3
import json
import sys
import consul


def main(type, app, host="ops1-consul-1892812477.us-east-1.elb.amazonaws.com"):
    cons = consul.Consul(host, 80)
    with open("../curbd/" + type + "/" + app + ".json") as f:
	    for k, v in json.load(f).items():
	        print(k, v)
	        cons.kv.put(type+"/"+app+"/"+k.lower(), v.lower())

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
