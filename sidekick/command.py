
class CommandType(type):

    commands = {}

    def __new__(meta, class_name, bases, new_attrs):
        cls = type.__new__(meta, class_name, bases, new_attrs)

        if class_name != 'Command':
            command = new_attrs.get("name", class_name.lower())
            if command in meta.commands:
                raise RuntimeError("Command '%s' was already defined")
            meta.commands[command] = cls

        return cls


class Command(object):

    def do(self):
        raise NotImplementedError

