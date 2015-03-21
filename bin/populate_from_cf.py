#!/usr/bin/env python3
import consul
from boto import cloudformation
import sys

def main(stack, env, host="ops1-consul-1892812477.us-east-1.elb.amazonaws.com"):
	conn = cloudformation.connect_to_region('us-east-1')
	cons = consul.Consul(host, 80)
	for o in conn.describe_stacks(env+"-"+stack)[0].outputs:
		print(o.key.lower(), o.value.lower())
		cons.kv.put(stack+"/"+o.key.lower(), o.value.lower())

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])

