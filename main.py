# from typing import Optional
#
# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name: int):
#     # Optional[int]:
#     # Use a breakpoint in the code line below to debug your script.
#     print(f"Hi, {name}")  # Press Ctrl+F8 to toggle the breakpoint.


#     return None
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == "__main__":
#     # asdf
#     x: int = print_hi(3)
#     print_hi("PyCharm")
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/


import unittest

loader = unittest.TestLoader()


def get():
    # raise Exception("oops")
    start_dir = r"C:\Users\Nathan - Personal\PycharmProjects\p8export\test2"
    return start_dir


suite = loader.discover(get())


runner = unittest.TextTestRunner()
runner.run(suite)
