# py-cliscript

## Usage

### single function
This is all you need to create a cli script that calls a single function with args/options:
```python
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
```
This can be called with and produces the output:
```bash
$ python examples/sysargs-single-function-example.py argument -b -c carg
arg: argument, b: "True", c: carg
```
the argument is passed as arg, -b sets the bool option to true and -c sets the c param to the passed string afterwards

### multi function
This is all you need to create a cli script that calls a range of functions depending on the first argument with args/options:
```python
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
```
This can be called with and produces the output:
```bash
$ python examples/sysargs-multi-function-example.py takeArg asd
arg: asd

$ python examples/sysargs-multi-function-example.py print
example
```
This in contrast to the single function calling supports the built in `CliScriptHelpCommand`, it builds a help message depending on the `helpMessages` of the different commands. In this example it would look like:
```bash
$ python examples/sysargs-multi-function-example.py -h
List of Commands:
print   -       print my str
takeArg <arg 1>...<arg 1>       -       arg example
```

### interactive script (main loop)
This is all you need to create a cli script that creates a mainloop with all the functionality of the multi function script
```python
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
```
It is mostly the same to the `CliScriptCommandLine`, it just wraps it into a loop that exits on run of a `CliScriptExitCommand`

## Docs

### exceptions
- `CliScriptOptionMissesValueException`
- `CliScriptInvalidArgumentsException`

### classes
- `CliScriptOption`
  - `name` - name of the option (kwarg) for the function
  - `optionKey` - list of identifiers for this option example: `['-l', '--long-name']`
  - `takesValue` - bool value determining if the next arg is the value of this option
  - `helpMessage`

- `CliScriptCommand`
  - `commandName` - name of the command, on what string this command should be called
  - `callback` - function to call
  - `allowedArgs` - number of allowed args, default = -1 meaning infinite
  - `allowedOptions` - list of `CliScriptOption`
  - `helpMessage`

- `CliScriptExitCommand` - only usable/useful in `CliScriptMainLoop`
  - `commandName` - name of the command
  - `message` - message to print before exiting

- `CliScriptHelpCommand` - prints help info gathered by the helpMessages

- `CliScriptCallingFunction` - used to call a single function with different args
  - `callback` - function to call
  - `allowedArgs` - see above
  - `allowedOptions` - see above

- `CliScriptCommandLine`
  - `definition` - list of `CliScriptCommand`

- `CliScriptMainLoop`
  - `definition` - see above
  - `inputSymbol` - string to show at the start of the input prompt
