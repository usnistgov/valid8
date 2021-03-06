# Contents subject to LICENSE.txt at project root

import argparse

from . import engine, exceptions


def main():
    """
    Main package function, reads CLI args and launches program.
    """
    parser = define_parser()
    args = parser.parse_args()
    if hasattr(args, "func") and args.func is not None:
        args.func(args)
    else:
        parser.print_help()


def define_parser():
    """
    Defines accepted CLI syntax and the actions to take for command and args.

    Returns:
        argparse parser

    """
    parser = argparse.ArgumentParser(
        description="Validate directory structure according to user-defined yaml rules"
    )
    subparsers = parser.add_subparsers(
        help="Available subcommands. Call -h to see usage", dest="apply"
    )
    subparsers.required = True

    base_args = [
        # Main positional argument
        [["rules_in_yaml"], dict(help="the rules defined in yaml")],
        # Verbosity flag (no effect for now)
        [
            ["-v", "--verbose"],
            dict(help="Toggle verbose log output", action="store_true"),
        ],
    ]
    apply_args = base_args + [
        [
            ["-d", "--directory"],
            dict(help="The directory to run the checks on", default="."),
        ]
    ]

    def add_protocol_subparser(name, kwargs, func, arguments):
        subp = subparsers.add_parser(name, **kwargs)
        for a, b in arguments:
            subp.add_argument(*a, **b)

        subp.set_defaults(func=func)
        return subp

    add_protocol_subparser(
        "apply",
        dict(help="Check the rules against the directory structure"),
        func=cmd_run_validation,
        arguments=apply_args,
    )

    add_protocol_subparser(
        "lint",
        dict(help="Lint the yaml configuration file"),
        func=cmd_run_lint,
        arguments=base_args,
    )

    return parser


def cmd_run_validation(args):
    """
    CLI command: runs the validation, e.g. the main command for this package

    Args:
        args: argparse args

    Raises:
        SystemExit(error_code) \
        with error_code=1 if the directory structure does not follow the rules

    """
    rules_structure = engine.process_configured_rules(
        args.rules_in_yaml, args.directory
    )

    engine.print_summary(rules_structure)

    # exiting with 0 or 1 depending on the combined rules output
    combined_output = engine.rules_output(rules_structure)
    raise SystemExit(0 if combined_output else 1)


def cmd_run_lint(args):
    """
    CLI command to run yaml configuration file validation (i.e. linting)
    Does not apply the rules (filters OR actions).
    When invalid, prints errors to stdout.

    DOES NOT detect wrong arguments in filters or actions
    because those are only used when applying the rule.

    Things it will detect:
        * no rules list
        * missing rule name, filters section or actions section
        * non-existing filter or action (e.g. when typing `exist` instead of `exists`)

    Things it will not detect:
        * Filter or action arguments of the wrong type (e.g. `count` expects integers)
        * Filter or action arguments of the wrong YAML type \
        (e.g. `count` expects direct arguments, `path_list` expects a YAML list)

    Args:
        args: argparse args

    Returns:
        bool: False if any exception was raised when parsing and extracting the yml rules

    """
    import yaml

    try:
        rules_structure = engine.parse_yml(args.rules_in_yaml)
        engine.extract_rules(rules_structure)
    except yaml.YAMLError as exc:
        print("Yaml error in configuration file:", exc)
    except exceptions.UnknownRule as unk:
        print("Rule not recognized: ", unk)
    except exceptions.ValidationSyntaxError as ws:
        print("Syntax is incorrect", ws)
    else:
        print("The configuration file looks good")
        return True

    raise SystemExit(2)


if __name__ == "__main__":
    main()
