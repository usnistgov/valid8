import pytest
import yaml

from rbv import engine, actions, filters

rules_list1 = [
    {
        "rulename": "predictions_file",
        "filters": {"path": "predictions.csv"},
        "actions": {"exists": True},
    }
]

rules_list2 = [
    {
        "rulename": "arbitraryrulename",
        "filters": {"path_list": ["Makefile", "setup.py", "rbv/cli.py"]},
        "actions": {"exists": True},
    }
]


@pytest.mark.parametrize("rules_list", [rules_list1, rules_list2])
def test_parse_yml(tmp_path, rules_list):
    # make fake file with rules_list
    file_contents = yaml.dump(rules_list)
    tmp_file = tmp_path / "tmp.yml"
    tmp_file.write_text(file_contents)
    # call parse_yml
    new_rules_list = engine.parse_yml(tmp_file.as_posix())
    # check ==
    assert new_rules_list == rules_list


@pytest.mark.parametrize("rules_list", [rules_list1, rules_list2])
def test_extracted_rules(rules_list):
    extracted_rules = engine.extract_rules(rules_list)
    assert len(rules_list) == len(extracted_rules)
    for rule_name, rule_content in extracted_rules.items():
        assert "filters" in rule_content.keys()
        assert "actions" in rule_content.keys()
        assert len(rule_content["filters"]) != 0
        matching_rule = [rule for rule in rules_list if rule["rulename"] == rule_name]
        assert len(matching_rule) == 1
        matching_rule = matching_rule[0]
        assert len(matching_rule["filters"]) == len(rule_content["filters"])
        assert len(matching_rule["actions"]) == len(rule_content["actions"])

        def sub_checks(subname, expected_fields):
            for element in rule_content[subname]:
                assert type(element) == dict
                for efield in expected_fields:
                    assert efield in element.keys()
                assert callable(element["func"])
                assert type(element["args"]) != dict
                assert type(element["kwargs"]) == dict

        sub_checks("filters", expected_fields=["name", "func", "args", "kwargs"])
        sub_checks("actions", expected_fields=["name", "func", "args", "kwargs"])


extracted_rules1 = {
    "predictions_file": {
        "filters": [
            {
                "name": "path",
                "func": filters.path,
                "args": "predictions.csv",
                "kwargs": {},
            }
        ],
        "actions": [
            {"name": "exists", "func": actions.exists, "args": True, "kwargs": {}}
        ],
    }
}
extracted_rules2 = {
    "arbitraryrulename": {
        "filters": [
            {
                "name": "path_list",
                "func": filters.path_list,
                "args": ["Makefile", "setup.py", "rbv/cli.py"],
                "kwargs": {},
            }
        ],
        "actions": [
            {"name": "exists", "func": actions.exists, "args": True, "kwargs": {}}
        ],
    }
}


@pytest.mark.parametrize(
    "rules_list, extracted_rules",
    [(rules_list1, extracted_rules1), (rules_list2, extracted_rules2)],
)
def test_extracted_rules_with_expected_output(rules_list, extracted_rules):
    assert engine.extract_rules(rules_list) == extracted_rules


@pytest.mark.parametrize(
    "type_str, name, expected",
    [("filters", "path", filters.path), ("actions", "exists", actions.exists)],
)
def test_map_to_func(type_str, name, expected):
    assert engine.retrieve_associated_function(type_str, name) == expected


@pytest.mark.parametrize("type_str", ["filters", "actions"])
def test_map_to_func_auto(type_str):
    type_module = eval(type_str)
    func_name_list = [a for a in dir(type_module) if callable(getattr(type_module, a))]
    func_map = {k: getattr(type_module, k) for k in func_name_list}

    for name, func in func_map.items():
        assert engine.retrieve_associated_function(type_str, name) == func


@pytest.mark.parametrize(
    "rules, expected",
    [
        ({"a": {"output": True}, "b": {"output": True}, "c": {"output": True}}, True),
        ({}, True),
        (
            {"a": {"output": False}, "b": {"output": False}, "c": {"output": False}},
            False,
        ),
        ({"a": {"output": True}, "b": {"output": True}, "c": {"output": False}}, False),
        pytest.param({}, False, marks=[pytest.mark.xfail]),
    ],
)
def test_rules_output(rules, expected):
    output = engine.rules_output(rules)
    assert output == expected
    assert output == (False not in [rule["output"] for rule in rules.values()])


# TODO test_act_on_rule
# actual vs expected with small example (path+exists)

# TODO test_act_on_rules
# same as above with multiple rules

# TODO test_end_to_end
# use the rules_listi for end to end actual v expected comparison
