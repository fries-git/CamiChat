def warn(input_str):
    print(f"\033[33m[!] {input_str}\033[0m")
    #yellow

def error(input_str):
    print(f"\033[31m[?] {input_str}\033[0m")
    #red

def success(input_str):
    print(f"\033[32m[$] {input_str}\033[0m")
    #green

def info(input_str):
    print(f"\033[34m[>] {input_str}\033[0m")
    #blue

def register(input_str):
    print(f"\033[35m[+] {input_str}\033[0m")
    #magenta