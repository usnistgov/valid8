import argparse

from . import engine, exceptions


def main():
    """
    Main package function, reads CLI args and launches program.
    """
    args = define_cli()
    cmd_run_validation(args)


def define_cli():
    """
    Defines accepted CLI syntax and the actions to take for command and args.
    Returns:
        argparse args

    """
    parser = argparse.ArgumentParser(
        description="Validate directory structure according to user-defined yaml rules"
    )
    subparsers = parser.add_subparsers(
        help="Available subcommands. Call -h to see usage"
    )

    base_args = [
        # Main positional argument
        [["ymlrules"], dict(help="the rules defined in yaml")],
        # Verbosity flag (no effect for now)
        [
            ["-v", "--verbose"],
            dict(help="Toggle verbose log output", action="store_true"),
        ],
    ]

    def add_protocol_subparser(name, kwargs, func, arguments):
        subp = subparsers.add_parser(name, **kwargs)
        for a, b in arguments:
            subp.add_argument(*a, **b)

        subp.set_defaults(func=func)
        return subp

    add_protocol_subparser(
        "validate",
        dict(help="Check the rules against the directory structure"),
        func=cmd_run_validation,
        arguments=base_args,
    )

    add_protocol_subparser(
        "lint",
        dict(help="Check the rules against the directory structure"),
        func=cmd_run_lint,
        arguments=base_args,
    )

    args = parser.parse_args()
    return args


def cmd_run_validation(args):
    """
    CLI command: runs the validation, e.g. the main command for this package

    Args:
        args: argparse args

    Raises:
        SystemExit(error_code)
        with error_code=1 if the directory structure does not follow the rules

    """
    rules_structure = engine.process_configured_rules(args.ymlrules)

    engine.print_summary(rules_structure)

    # exiting with 0 or 1 depending on the combined rules output
    combined_output = engine.rules_output(rules_structure)
    raise SystemExit(0 if combined_output else 1)


def cmd_run_lint(args):
    """
    [Alpha] CLI command to run yaml configuration file validation (i.e. linting)
    Does not apply the rules (filters OR actions).
    When invalid, prints errors to stdout.

    Args:
        args: argparse args

    Returns:
        bool: False if any exception was raised when parsing and extracting the yml rules

    """
    import yaml

    try:
        rules_structure = engine.parse_yml(args.ymlrules)
        engine.extract_rules(rules_structure)
        # TODO make this into a real linting cmd
    except yaml.YAMLError as exc:
        print("Yaml error in configuration file:", exc)
    except exceptions.UnknownRule as unk:
        print("Rule not recognized: ", unk)
    else:
        print("The configuration file looks good")
        return True

    return False


if __name__ == "__main__":
    main()
