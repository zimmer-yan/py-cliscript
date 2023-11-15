import _import_parent
import CliScript
import sys


def printExample(arg, b=False, c=''):
    print(f'arg: {arg}, b: "{b}", c: {c}')


if __name__ == '__main__':
    func = CliScript.CliScriptCallingFunction(printExample, 1,  [
        CliScript.CliScriptOption('b', ['-b']),
        CliScript.CliScriptOption('c', ['-c'], True),
    ])
    try:
        func.call(sys.argv[1:])
    except (CliScript.CliScriptInvalidArgumentsException, CliScript.CliScriptOptionMissesValueException) as e:
        print(e)
