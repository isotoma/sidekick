import sys, optparse

def cmd_up(args):
    pass

def cmd_down(args):
    pass


commands = {
    "up": cmd_up,
    "down": cmd_down,
    }


def main():
    if len(sys.argv) < 2:
        print "Usage: %s <%s> [OPTIONS]" % (sys.argv[0], '|'.join(commands.keys())
        sys.exit(1)

    command = sys.argv[1]
    if not command in commands:
        print "Unknown subcommand; %s" % cmd
        sys.exit(1)

    commands[command](sys.argv[2:])

