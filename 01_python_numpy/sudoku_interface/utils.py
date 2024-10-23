
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def update_position(inp, pos):
    if inp in {"W", "w", b"W", b"w"}: pos[0] -= 1
    elif inp in {"A", "a", b"A", b"a"}: pos[1] -= 1
    elif inp in {"S", "s", b"S", b"s"}: pos[0] += 1
    elif inp in {"D", "d", b"D", b"d"}: pos[1] += 1
    else: return False
    pos[0] = max(pos[0], 0)
    pos[1] = max(pos[1], 0)
    pos[0] = min(pos[0], 8)
    pos[1] = min(pos[1], 8)
    return True
