from typing import Union


class CliScriptOptionMissesValueException(Exception):
    pass


class CliScriptInvalidArgumentsException(Exception):
    pass


class CliScriptOption:
    def __init__(self, name: str, optionKeys: list, takesValue: bool = False, helpMessage: str = '') -> None:
        self.name: str = name
        self.optionKeys: list = optionKeys
        self.takesValue: bool = takesValue
        self.helpMessage: str = helpMessage


class _CliScriptCommandBase:
    def __init__(self, commandName: str) -> None:
        self.name = commandName


class CliScriptCommand(_CliScriptCommandBase):
    def __init__(self, commandName: str, callback, allowedArgs: int = -1, allowedOptions: list = [], helpMessage: str = '') -> None:
        super().__init__(commandName)
        self.callback = callback
        self.allowedArgs: int = allowedArgs
        self.allowedKwargs: dict = self._buildAllowedKwargs(allowedOptions)
        self.helpMessage: str = helpMessage

    def _buildAllowedKwargs(self, allowedOptions: list) -> dict:
        allowedKwargs = {}
        option: CliScriptOption
        for option in allowedOptions:
            for key in option.optionKeys:
                allowedKwargs[key] = option
        return allowedKwargs

    def getOption(self, argumentName: str) -> Union[CliScriptOption, None]:
        if not argumentName in self.allowedKwargs.keys():
            return None
        return self.allowedKwargs[argumentName]

    def convertToArgsKwargs(self, arguments: list):
        args = []
        kwargs = {}
        iterator = iter(arguments)
        while argument := next(iterator, None):

            option = self.getOption(argument)
            if option is None:
                args.append(argument)
                continue

            if option.takesValue:
                value = next(iterator, None)
                if value is None:
                    raise CliScriptOptionMissesValueException(
                        f'Option {argument} excepts value but reached EOF')
                kwargs[option.name] = value
            else:
                kwargs[option.name] = True

        if self.allowedArgs != -1 and not len(args) == self.allowedArgs:
            raise CliScriptInvalidArgumentsException(
                f'Number of arguments mismatch, should be "{self.allowedArgs}" is "{len(args)}"')

        return args, kwargs


class CliScriptExitCommand(CliScriptCommand):
    def __init__(self, commandName: str, message: str = '') -> None:
        self.message = message
        super().__init__(commandName, self._bye, 0, [], 'exit')

    def _bye(self):
        if self.message:
            print(self.message)


class CliScriptHelpCommand(_CliScriptCommandBase):
    pass


class CliScriptCallingFunction:
    def __init__(self, callback, allowedArgs: int = -1, allowedOptions: list = []) -> None:
        self.cmd = CliScriptCommand(
            '', callback, allowedArgs, allowedOptions)

    def call(self, arguments: list[str]) -> any:
        args, kwargs = self.cmd.convertToArgsKwargs(arguments)
        return self.cmd.callback(*args, **kwargs)


class CliScriptCommandLine:
    def __init__(self, definition: list) -> None:
        self.functions = self._buildFunctionsDict(definition)

    def _buildFunctionsDict(self, definition: list) -> dict:
        functions = {}
        command: CliScriptCommand
        for command in definition:
            functions[command.name] = command
        return functions

    def handle(self, arguments: list[str]) -> bool:
        if not arguments:
            print(f'No command found')
            return True
        if not arguments[0] in self.functions.keys():
            print(f'Unknown command: "{arguments[0]}"')
            return True

        command: _CliScriptCommandBase = self.functions[arguments[0]]
        if isinstance(command, CliScriptHelpCommand):
            self._outputHelp()
        elif isinstance(command, CliScriptCommand):
            return self._processCommand(command, arguments[1:])
        return True

    def _processCommand(self, command: CliScriptCommand, arguments: list[str]) -> bool:
        try:
            args, kwargs = command.convertToArgsKwargs(arguments)
        except (CliScriptInvalidArgumentsException, CliScriptOptionMissesValueException) as e:
            print(e)
            return True
        command.callback(*args, **kwargs)

        if isinstance(command, CliScriptExitCommand):
            return False
        return True

    def _outputHelp(self):
        output: list = ['List of Commands:']
        name: str
        command: _CliScriptCommandBase
        for name, command in self.functions.items():
            if not isinstance(command, CliScriptCommand):
                continue

            argsStr = ''
            if command.allowedArgs == -1:
                argsStr = ' [<arg 1>...<arg n>]'
            elif command.allowedArgs != 0:
                argsStr = f' <arg 1>...<arg {command.allowedArgs}>'

            output.append(f'{name}{argsStr}\t-\t{command.helpMessage}')
            optionName: str
            option: CliScriptOption
            for optionName, option in command.allowedKwargs.items():
                valueStr = ''
                if option.takesValue:
                    valueStr = ' <value>'
                output.append(
                    f'\t{optionName}{valueStr}\t-\t{option.helpMessage}')

        print('\n'.join(output))


class CliScriptMainLoop:
    def __init__(self, definition: list, inputSymbol='>') -> None:
        self.exit = False
        self.inputSymbol: str = inputSymbol
        self.cli: CliScriptCommandLine = CliScriptCommandLine(definition)

    def run(self):
        while not self.exit:
            try:
                self._processInput()
            except KeyboardInterrupt:
                pass

    def _processInput(self) -> None:
        userInput = input(f"{self.inputSymbol} ")
        arguments = userInput.split(' ')

        self.exit = not self.cli.handle(arguments)
