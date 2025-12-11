
import argparse
import json
import os
arg_parser = argparse.ArgumentParser()


arg_parser.add_argument('--id', action='store', type=str, required=True, dest='id')



args = arg_parser.parse_args()
print(args)

id = args.id




list1 = ["0001", "0010", "0011"]

file_list1 = open("/tmp/list1_" + id + ".json", "w")
file_list1.write(json.dumps(list1))
file_list1.close()