# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def text_to_hex(text):
    return ''.join([hex(ord(c))[2:] for c in text])

def text_to_hex_2(text):
    return ''.join([f'{ord(c):04x}' for c in text])

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(text_to_hex('ramona'))
    print(text_to_hex('Ramona'))
    print()
    print(text_to_hex_2('ramona'))
    print(text_to_hex_2('Ramona'))
    print(text_to_hex_2('Hello World'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
