from collections import defaultdict
import os

import yaml

from .exceptions import ValidationSyntaxError, UnknownRule

# retrieve_associated_function depends on this line
from . import actions, filters  # noqa: F401


def process_configured_rules(filepath, directory):
    """
    Processes the user-defined rules.
    Interprets the user-defined rules, maps then to functions,
    executes the filters and actions.

    Args:
        filepath: yml file with the configured rules. (str or pathlib.Path)
        directory: the directory to run checks on

    Returns:
         dict: rules structure with the interpreted rules and their output

    """
    parsed_rules = parse_yml(filepath)
    rules_structure = extract_rules(parsed_rules)
    act_on_rules(rules_structure, directory=directory)
    return rules_structure


def parse_yml(filepath):
    """
    Extracts a rule list from the user-defined rules configuration file

    Args:
        filepath: yml file with the configured rules. str or pathlib.Path

    Returns:
        list: of rules with their arguments

    """
    with open(filepath) as ymlf:
        rules_list = yaml.load(ymlf)
    return rules_list


def extract_rules(parsed_rules):
    """
    Transforms the parsed rules into a complete data structure called
    `rules_structure`.

    Args:
        parsed_rules (list): the rules parsed from the user-defined configuration file.

    Returns:
        dict: rules_structure,
            a nested structure containing every information required to
            apply filters and actions to the directory structure, including the
            mapping to the functions to use.
            Dictionary of rules. A rule is iteslf a dictionary with the following keys:
            (filters, actions), both of which are lists of dictionaries.

    """

    rules_structure = defaultdict(dict)

    rules_subtypes = ["filters", "actions"]
    for rule in parsed_rules:

        try:
            rule_content = rule["rulename"]
        except (KeyError, TypeError) as e:
            raise ValidationSyntaxError(e) from e

        for subtype in rules_subtypes:
            rules_structure[rule_content][subtype] = extract_rules_subtype(
                subtype, rule
            )
            rules_structure[rule_content][subtype] = extract_rules_subtype(
                subtype, rule
            )

    return rules_structure


def extract_rules_subtype(rules_subtype, rule_dict):
    extracted_functions = list()

    try:
        type_dict = rule_dict[rules_subtype]
    except KeyError as e:
        raise ValidationSyntaxError(e) from e

    for func_name, func_contents in type_dict.items():
        func_dict = dict()
        func_dict["name"] = func_name
        func_dict["func"] = retrieve_associated_function(rules_subtype, func_name)

        # Setting args and kwargs for later unpacking
        if type(func_contents) is dict:
            func_dict["args"] = []
            func_dict["kwargs"] = func_contents
        else:
            func_dict["args"] = func_contents
            func_dict["kwargs"] = {}

        extracted_functions.append(func_dict)
    return extracted_functions


def retrieve_associated_function(rule_subtype, name):
    """
    Retrieves the associated function from the user-defined name.

    Args:
        rule_subtype (str): 'filters' or 'actions'
        name (str): the name of the filter or action

    Returns:
        <function>: the function associated to that name.

    """
    all_available_variables = globals()
    try:
        rule_subtype_module = all_available_variables[rule_subtype]
        associated_function = getattr(rule_subtype_module, name)
    except (KeyError, AttributeError) as e:
        raise UnknownRule(rule_subtype, name) from e
    return associated_function


def act_on_rules(rules_structure, directory):
    """
    Call the associated code for each rule.
    The output of each rule action is reported in the dict of that rule in
    `rules_structure`.

    Args:
        rules_structure(dict): the structure representing rules.

    """
    cdir = os.getcwd()
    try:
        os.chdir(directory)
        print(f"we are in {directory}")

        for rule_name, rule_contents in rules_structure.items():
            act_on_rule(rule_contents)

    finally:
        os.chdir(cdir)


def act_on_rule(rule):
    """
    Call the associated code for a single rule.
    The output of the rules action is reported in the `rule` dict under
    keys 'output' and 'errors'

    Args:
        rule (dict): the structure representing the rule,
            found as a value of `rules_structure`

    """
    context = list()
    # get context from filters
    for filter in rule["filters"]:
        filter["func"](filter["args"], context=context, **filter["kwargs"])

    rule["context"] = context

    for action in rule["actions"]:
        action_output = action["func"](
            action["args"], context=context, **action["kwargs"]
        )
        action["output"], action["errors"] = action_output

    # determining whole rule output
    rule["output"] = all([action["output"] for action in rule["actions"]])


def print_summary(rules_structure):
    """
    Prints a summary of the completed validation to stdout.

    Args:
        rules_structure(dict): the structure representing rules.
    """
    for rule_name, rule_content in rules_structure.items():
        print("Rule: ", rule_name)
        print("  Context:")
        for context in rule_content["context"]:
            print("    ", context)
        for action in rule_content["actions"]:
            print("  Action: ", action["name"], action["output"])
        print("Rule output: ", rule_content["output"])

    combined_output = rules_output(rules_structure)
    print("--\nCombined rules output: ", combined_output)


def rules_output(rules_structure):
    """
    Determines the total rules output after the filters and actions after `act_on_rules`

    Args:
        rules_structure (dict): dict representing the extracted and interpreted rules

    Returns:
        bool: True if the rules were followed in the directory structure.

    """
    rules_output = all([rule["output"] for rule in rules_structure.values()])
    return rules_output
