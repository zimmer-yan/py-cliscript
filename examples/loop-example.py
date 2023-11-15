import _import_parent
import CliScript


def printExampleNoArgs():
    print('example')


def printExampleArgs(arg1, arg2, b=False, c=''):
    print(f'arg1: {arg1}, args2: {arg2}, b: "{b}", c: {c}')


def printExampleAllTheArgs(*args):
    print('example of all the args')
    print(args)


if __name__ == '__main__':
    mainLoop = CliScript.CliScriptMainLoop([
        CliScript.CliScriptExitCommand('exit', 'bye bye'),
        CliScript.CliScriptExitCommand('q', 'bye bye 2'),

        CliScript.CliScriptHelpCommand('-h'),

        CliScript.CliScriptCommand(
            'noargs', printExampleNoArgs, 0, helpMessage='print my str'),
        CliScript.CliScriptCommand(
            'someargs', printExampleArgs, 2, [
                CliScript.CliScriptOption(
                    'b', ['-b'], helpMessage='b option'),
                CliScript.CliScriptOption(
                    'c', ['-c'], True, helpMessage='c option'),
            ], helpMessage='takes some args and kwargs'),
        CliScript.CliScriptCommand(
            'allargs', printExampleAllTheArgs, helpMessage='print and accept all args'),
    ])
    mainLoop.run()
