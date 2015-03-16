from fabric.colors import green as _green, yellow as _yellow, red as _red, blue as _blue, cyan as _cyan, \
    magenta as _magenta


class Notification(object):
    """
    Notification class for terminal output.
    Requires message.
    """

    def __init__(self, message=""):
        self.message = message

    def success(self):
        print(_green(self.message + "!"))

    def info(self):
        print(_cyan(self.message))

    def warning(self):
        print(_yellow(self.message))

    def error(self):
        print(_red(self.message))
