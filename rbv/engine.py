from . import filters, actions  # getattr depends on this line
import yaml
from collections import defaultdict

some_text_file = ""
# to-yaml


def parse_yml(filepath):
    with open(filepath) as ymlf:
        h = yaml.load(ymlf)
    return h


def map_to_func(type, name):
    return getattr(globals()[type], name)


# input dict (from parsing file)
# output dict of dict
def extract_rules(rules_list):

    extracted = defaultdict(dict)

    def parse_subdict(rtype, rule_dict):
        extracted_functions = list()
        type_dict = rule_dict[rtype]
        for func_name, func_contents in type_dict.items():
            func_dict = dict()
            func_dict["name"] = func_name
            func_dict["func"] = map_to_func(rtype, func_name)

            # Setting args and kwargs for later unpacking
            if type(func_contents) is dict:
                func_dict["kwargs"] = func_contents
                func_dict["args"] = []
            elif type(func_contents) is list:
                func_dict["args"] = func_contents
                func_dict["kwargs"] = {}
            else:
                func_dict["args"] = [func_contents]
                func_dict["kwargs"] = {}

            extracted_functions.append(func_dict)
        return extracted_functions

    for rule in rules_list:
        extracted[rule["rulename"]]["filters"] = parse_subdict("filters", rule)
        extracted[rule["rulename"]]["actions"] = parse_subdict("actions", rule)

    return extracted


from .context import Context

# dict of dict rules
# keeps track of action returns
# output: dict of action returns
def act_on_rules(rules):
    output = list()

    for rule_name, rule_contents in rules.items():
        rule_output = act_on_rule(rule_contents)
        output.append(rule_output)


def act_on_rule(rule):
    contexts = list()
    # get context from filters
    for filter in rule['filters']:
        filter['func'](filter['args'], contexts=contexts, **filter['kwargs'])

    rule['context'] = contexts

    for action in rule['actions']:
        action_output = action['func'](action['args'], contexts=contexts, **action['kwargs'])
        action['output'], action['exceptions'], action['detail'] = action_output


if __name__ == '__main__':

    filename = 'examples/single_rule_single_action.yml'
    execution_dir = '.'  # cannot change this for now

    yml_contents = parse_yml(filename)
    rules_d = extract_rules(yml_contents)
    act_on_rules(rules_d)

    for rule_name, rule_content in rules_d.items():
        print("Rule: ", rule_name)
        print("  Contexts:")
        for context in rule_content['context']:
            print("    ", context.filepath)
        for action in rule_content['actions']:
            print("  Action: ", action['name'], action['output'])
    pass
