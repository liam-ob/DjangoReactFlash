# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class MyObject():
    def __init__(self, number, name):
        self.number = number
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    my_list = [MyObject(1, 'one'), MyObject(2, 'two'), MyObject(3, 'three')]
    new_my_list = []
    for item in my_list:
        new_my_list.extend([item] * item.number)
    print(new_my_list)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
