import argparse

from . import engine


def cli_input():
    parser = argparse.ArgumentParser(
        description="Validate file structure according to rules"
    )
    parser.add_argument("ymlmarkup", help="the rules in yaml")

    args = parser.parse_args()
    return args


def cli_action(args):
    parsed_rules = engine.parse_yml(args.ymlmarkup)
    rules_d = engine.extract_rules(parsed_rules)
    engine.act_on_rules(rules_d)

    for rule_name, rule_content in rules_d.items():
        print("Rule: ", rule_name)
        print("  Contexts:")
        for context in rule_content["context"]:
            print("    ", context.filepath)
        for action in rule_content["actions"]:
            print("  Action: ", action["name"], action["output"])


def main():
    args = cli_input()
    cli_action(args)


if __name__ == "__main__":
    main()
