import subprocess
from os import environ
from pathlib import Path

from ..exceptions import BaseValidationError


class ScriptError(BaseValidationError):
    def __init__(self, command, code, stderr=None):
        self.command = command
        self.code = code
        self.stderr = stderr
        super().__init__(
            f"Command '{command}' returned code {code}", command, code, stderr
        )


def scripts(commands, context):
    if isinstance(commands, str):
        commands = [commands]

    outputs = list()
    errors = list()
    for filepath in context:
        s_ouptut, s_errors = single_script(commands, filepath)
        outputs.append(s_ouptut)
        errors.extend(s_errors)

    return all(outputs), errors


def single_script(commands, context_filepath):
    variables = context_variables(context_filepath)

    interpreted_commands = [command.format(**variables) for command in commands]

    for command in interpreted_commands:
        try:
            subprocess.run([environ["SHELL"], "-c", command], check=True)
        except subprocess.CalledProcessError as e:
            return False, [ScriptError(command, e.returncode)]

    return True, []


def context_variables(context_filepath):
    """
    Context file path subsitutions for :func:`scripts`.
    All variables are surrounded by single quotes to avoid problems with
    non escaped characters (e.g. a unescaped space can mess up an `ls` command)

    Args:
        context_filepath: the context the substitution variables refer to

    Returns:
        dict: of all the substitution keys and their values
    """
    context_path = Path(context_filepath)
    variables = {
        "DIR_NAME": context_path.parent.name,
        "DIR_PATH": context_path.parent,
        "FILENAME_NOEXT": context_path.stem,
        "FILENAME": context_path.name,
        "FILEPATH": context_path,
    }
    variables_with_quotes = {k: f"'{v}'" for k, v in variables.items()}
    return variables_with_quotes
