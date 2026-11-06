
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
expected_arg_names.add('done')
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

arg_name = 'done'
arg_value = get_arg_value(arg_name,args,raw_args)
arg_type = str
done = _parse_value(arg_value, arg_name, arg_type)
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

print(done)

check_string = 'param_string value'
check_string_with_comment = 'param_string value'  # comment
check_int = 1
check_float = 1.1
check_list_int = [1, 2, 3]
check_list_str = ["list_str", "space in elem", "3"]

assert conf_string == check_string
assert conf_string_with_comment == check_string_with_comment
assert conf_int == check_int
assert conf_float == check_float
assert conf_list_int == check_list_int
assert conf_list_str == check_list_str


assert param_string == check_string
assert param_string_with_comment == check_string_with_comment
assert param_int == check_int
assert param_float == check_float
assert param_list_int == check_list_int
assert param_list_str == check_list_str

print("All variables are the same.")

