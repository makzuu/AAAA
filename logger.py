import sys

def error(msg, line):
    sys.exit(f"Error! at {line}: {msg}")

def warning(msg, line):
    print(f"Warning. at {line}: {msg}")
