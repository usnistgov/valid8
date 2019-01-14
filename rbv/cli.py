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
    rules_d = engine.process_configured_rules(args.ymlmarkup)

    for rule_name, rule_content in rules_d.items():
        print("Rule: ", rule_name)
        print("  Context:")
        for context in rule_content["context"]:
            print("    ", context)
        for action in rule_content["actions"]:
            print("  Action: ", action["name"], action["output"])
        print("Rule output: ", rule_content["output"])

    combined_output = engine.rules_output(rules_d)
    print("--\nCombined rules output: ", combined_output)

    # exiting with 0 or 1 depending on the combined rules output
    raise SystemExit(0 if combined_output else 1)


def main():
    args = cli_input()
    cli_action(args)


if __name__ == "__main__":
    main()
