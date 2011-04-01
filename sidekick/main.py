import sys
from sidekick.command import ProjectCommand, Command, CommandType

class Init(Command):
    name = "init"

class Up(ProjectCommand):
    name = "up"

class Down(ProjectCommand):
    name = "down"

def main():
    if len(sys.argv) < 2:
        print "Usage: %s <%s> [OPTIONS]" % (sys.argv[0], '|'.join(CommandType.commands.keys()))
        sys.exit(1)

    command = sys.argv[1]
    if not command in CommandType.commands:
        print "Unknown subcommand; %s" % cmd
        sys.exit(1)

    CommandType.commands[command]().do(sys.argv[2:])

