import _import_parent
import CliScript
import sys


def printExample():
    print('example')


def takeArg(arg):
    print(f'arg: {arg}')


if __name__ == '__main__':
    functionDict = CliScript.CliScriptCommandLine([
        CliScript.CliScriptHelpCommand('-h'),

        CliScript.CliScriptCommand(
            'print', printExample, 0, helpMessage='print my str'),
        CliScript.CliScriptCommand(
            'takeArg', takeArg, 1, helpMessage='arg example'),
    ])
    try:
        functionDict.handle(sys.argv[1:])
    except CliScript.CliScriptInvalidArgumentsException | CliScript.CliScriptOptionMissesValueException as e:
        print(e)
