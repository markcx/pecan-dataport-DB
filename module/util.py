import os
import inspect
import sys

def get_module_directory():
    # Taken from http://stackoverflow.com/a/6098238/732596
    path_to_this_file = os.path.dirname(inspect.getfile(inspect.currentframe()))
    if not os.path.isdir(path_to_this_file):
        encoding = sys.getfilesystemencoding()
        path_to_this_file = os.path.dirname(str(__file__, encoding))
    if not os.path.isdir(path_to_this_file):
        os.path.abspath(inspect.getsourcefile(lambda _: None))
    if not os.path.isdir(path_to_this_file):
        path_to_this_file = os.getcwd()
    assert os.path.isdir(path_to_this_file), path_to_this_file + ' is not a directory'
    return path_to_this_file
