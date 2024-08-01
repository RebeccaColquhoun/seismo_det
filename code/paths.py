import os
import inspect

base_path = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())),
    "..")

data_path = os.path.join(base_path, "data")
figure_path = os.path.join(base_path, "figures")

data_subfolders = ["example"]
