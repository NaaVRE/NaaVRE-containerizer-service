
import argparse
import json
import os

def _load_json_args(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def _parse_value(value, field_name, target_type, elem_type=None):
    if target_type is list:
        if isinstance(value, list):
            return value
        elif isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                # the value may be "['list_str', 'space in elem', '3']"
                if value.startswith('[') and value.endswith(']'):
                    value = value[1:-1].strip()  # remove the brackets and trim whitespace
                    if value:
                        return [elem.strip().strip("'").strip('"') for elem in value.split(',')]
                    else:
                        return []
                else:
                    arg_parser.error(field_name + " is not a valid list")

    if target_type is str:
        return value

    if target_type is int:
        return int(value)

    if target_type is float:
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            return float(value)
    arg_parser.error(field_name + " has unsupported target type")

def get_arg_value(name,args,raw_args):
    for arg in raw_args:
        if arg['name'] == name:
            return arg['value']
    arg_parser.error("Argument '" + name + "' not found in JSON args")

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--args_json', action='store', type=str, required=True, dest='args_json')

args = arg_parser.parse_args()

expected_arg_names = set()
expected_arg_names.add('var_float')
expected_arg_names.add('var_int')
expected_arg_names.add('var_list_int')
expected_arg_names.add('var_list_str')
expected_arg_names.add('var_string')
expected_arg_names.add('var_string_with_comment')
expected_arg_names.add('param_float')
expected_arg_names.add('param_int')
expected_arg_names.add('param_list_int')
expected_arg_names.add('param_list_str')
expected_arg_names.add('param_string')
expected_arg_names.add('param_string_with_comment')
expected_arg_names.add('conf_float')
expected_arg_names.add('conf_int')
expected_arg_names.add('conf_list_int')
expected_arg_names.add('conf_list_str')
expected_arg_names.add('conf_string')
expected_arg_names.add('conf_string_with_comment')
expected_arg_names.add('id')

raw_args = _load_json_args(args.args_json)
for arg in raw_args:
    if 'name' not in arg:
        arg_parser.error("Argument with no name found in JSON args")
    if arg['name'] not in expected_arg_names:
        arg_parser.error("Unexpected argument '" + arg['name'] + "' found in JSON args")
    if not arg['name'].startswith('conf'):
            if 'value' not in arg or arg['value'] is None:
                arg_parser.error("Argument '" + arg['name'] + "' has no value in JSON args")
    if arg['name'].startswith('conf'):
            if 'assignation' not in arg or arg['assignation'] is None:
                arg_parser.error("Argument '" + arg['name'] + "' has no assignation in JSON args")

arg_name = 'var_float'
arg_value = get_arg_value(arg_name,args,raw_args)
arg_type = float
var_float = _parse_value(arg_value, arg_name, arg_type)
arg_name = 'var_int'
arg_value = get_arg_value(arg_name,args,raw_args)
arg_type = int
var_int = _parse_value(arg_value, arg_name, arg_type)
arg_name = 'var_list_int'
arg_value = get_arg_value(arg_name,args,raw_args)
arg_type = list
var_list_int = _parse_value(arg_value, arg_name, arg_type)
arg_name = 'var_list_str'
arg_value = get_arg_value(arg_name,args,raw_args)
arg_type = list
var_list_str = _parse_value(arg_value, arg_name, arg_type)
arg_name = 'var_string'
arg_value = get_arg_value(arg_name,args,raw_args)
arg_type = str
var_string = _parse_value(arg_value, arg_name, arg_type)
arg_name = 'var_string_with_comment'
arg_value = get_arg_value(arg_name,args,raw_args)
arg_type = str
var_string_with_comment = _parse_value(arg_value, arg_name, arg_type)
arg_name = 'param_float'
arg_value = get_arg_value(arg_name,args,raw_args)
arg_type = float
param_float = _parse_value(arg_value, arg_name, arg_type)
arg_name = 'param_int'
arg_value = get_arg_value(arg_name,args,raw_args)
arg_type = int
param_int = _parse_value(arg_value, arg_name, arg_type)
arg_name = 'param_list_int'
arg_value = get_arg_value(arg_name,args,raw_args)
arg_type = list
param_list_int = _parse_value(arg_value, arg_name, arg_type)
arg_name = 'param_list_str'
arg_value = get_arg_value(arg_name,args,raw_args)
arg_type = list
param_list_str = _parse_value(arg_value, arg_name, arg_type)
arg_name = 'param_string'
arg_value = get_arg_value(arg_name,args,raw_args)
arg_type = str
param_string = _parse_value(arg_value, arg_name, arg_type)
arg_name = 'param_string_with_comment'
arg_value = get_arg_value(arg_name,args,raw_args)
arg_type = str
param_string_with_comment = _parse_value(arg_value, arg_name, arg_type)

conf_float = 1.1
conf_int = 1
conf_list_int = [1, 2, 3]
conf_list_str = ['list_str', 'space in elem', '3']
conf_string = 'param_string value'
conf_string_with_comment = 'param_string value'


arg_value = get_arg_value('id',args,raw_args)
id = _parse_value(arg_value, 'id', str)

print('conf_string: ' + str(conf_string) + ' type: ' + str(type(conf_string)))
print('conf_string_with_comment: ' + str(conf_string_with_comment) + ' type: ' + str(type(conf_string_with_comment)))
print('conf_int: ' + str(conf_int) + ' type: ' + str(type(conf_int)))
print('conf_float: ' + str(conf_float) + ' type: ' + str(type(conf_float)))
print('conf_list_int: ' + str(conf_list_int) + ' type: ' + str(type(conf_list_int)))
print('conf_list_str: ' + str(conf_list_str) + ' type: ' + str(type(conf_list_str)))

print('param_string: ' + str(param_string) + ' type: ' + str(type(param_string)))
print('param_string_with_comment: ' + str(param_string_with_comment) + ' type: ' + str(type(param_string_with_comment)))
print('param_int: ' + str(param_int) + ' type: ' + str(type(param_int)))
print('param_float: ' + str(param_float) + ' type: ' + str(type(param_float)))
print('param_list_int: ' + str(param_list_int) + ' type: ' + str(type(param_list_int)))
print('param_list_str: ' + str(param_list_str) + ' type: ' + str(type(param_list_str)))

print('var_string: ' + str(var_string) + ' type: ' + str(type(var_string)))
print('var_string_with_comment: ' + str(var_string_with_comment) + ' type: ' + str(type(var_string_with_comment)))
print('var_int: ' + str(var_int) + ' type: ' + str(type(var_int)))
print('var_float: ' + str(var_float) + ' type: ' + str(type(var_float)))
print('var_list_int: ' + str(var_list_int) + ' type: ' + str(type(var_list_int)))
print('var_list_str: ' + str(var_list_str) + ' type: ' + str(type(var_list_str)))

check = conf_string
if not isinstance(check, str):
    print('conf_string is not a string. It is a ' + str(type(check)))
    exit(1)
check = conf_string_with_comment
if not isinstance(check, str):
    print('conf_string_with_comment is not a string. It is a ' + str(type(check)))
    exit(1)
check = conf_int
if not isinstance(check, int):
    print('conf_int is not an int. It is a ' + str(type(check)))
    exit(1)
check = conf_float
if not isinstance(check, float):
    print('conf_float is not a float. It is a ' + str(type(check)))
    exit(1)
check = conf_list_int
if not isinstance(check, list):
    print('conf_list_int is not a list. It is a ' + str(type(check)))
    exit(1)
for i in conf_list_int:
    if not isinstance(i, int):
        print('conf_list_int contains a non-int value: ' + str(i))
        exit(1)
check = conf_list_str
if not isinstance(check, list):
    print('conf_list_str is not a list. It is a ' + str(type(check)))
    exit(1)
for i in conf_list_str:
    if not isinstance(i, str):
        print('conf_list_str contains a non-str value: ' + str(i))
        exit(1)

check = param_string
if not isinstance(check, str):
    print('param_string is not a string. It is a ' + str(type(check)))
    exit(1)
check = param_string_with_comment
if not isinstance(check, str):
    print('param_string_with_comment is not a string. It is a ' + str(type(check)))
    exit(1)
check = param_int
if not isinstance(check, int):
    print('param_int is not an int. It is a ' + str(type(check)))
    exit(1)
check = param_float
if not isinstance(check, float):
    print('param_float is not a float. It is a ' + str(type(check)))
    exit(1)
check = param_list_int
if not isinstance(check, list):
    print('param_list_int is not a list. It is a ' + str(type(check)))
    exit(1)
for i in param_list_int:
    if not isinstance(i, int):
        print('param_list_int contains a non-int value: ' + str(i))
        exit(1)
check = param_list_str
if not isinstance(check, list):
    print('param_list_str is not a list. It is a ' + str(type(check)))
    exit(1)
for i in param_list_str:
    if not isinstance(i, str):
        print('param_list_str contains a non-str value: ' + str(i))
        exit(1)


check = var_string
if not isinstance(check, str):
    print('var_string is not a string. It is a ' + str(type(check)))
    exit(1)
check = var_string_with_comment
if not isinstance(check, str):
    print('var_string_with_comment is not a string. It is a ' + str(type(check)))
    exit(1)
check = var_int
if not isinstance(check, int):
    print('var_int is not an int. It is a ' + str(type(check)))
    exit(1)
check = var_float
if not isinstance(check, float):
    print('var_float is not a float. It is a ' + str(type(check)))
    exit(1)
check = var_list_int
if not isinstance(check, list):
    print('var_list_int is not a list. It is a ' + str(type(check)))
    exit(1)
for i in var_list_int:
    if not isinstance(i, int):
        print('var_list_int contains a non-int value: ' + str(i))
        exit(1)
check = var_list_str
if not isinstance(check, list):
    print('var_list_str is not a list. It is a ' + str(type(check)))
    exit(1)
for i in var_list_str:
    if not isinstance(i, str):
        print('var_list_str contains a non-str value: ' + str(i))
        exit(1)
print('All vars are of the correct type')

done = 'True'

file_done = open("/tmp/done_" + id + ".json", "w")
file_done.write(json.dumps(done))
file_done.close()
