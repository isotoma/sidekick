import sys

from sidekick.commands import CommandType


def main():
    if len(sys.argv) < 2:
        print "Usage: %s <%s> [OPTIONS]" % (sys.argv[0], '|'.join(CommandType.commands.keys()))
        sys.exit(1)

    command = sys.argv[1]
    if not command in CommandType.commands:
        print "Unknown subcommand; %s" % command
        sys.exit(1)

    CommandType.commands[command](sys.argv[2:]).do()
    print "done."
