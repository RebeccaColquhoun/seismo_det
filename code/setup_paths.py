import os
import inspect

# set data and figure path relative to directory containing code.
# can manually change these paths here
base_path = os.path.join(os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe()))),
    "..")
data_path = os.path.join(os.path.dirname(base_path), '../data/')
data_path = os.path.join(os.path.dirname(base_path), '../../data/')
figure_path = os.path.join(os.path.dirname(base_path), '../figures/')

# create data and figure directories if they don't exist
if not os.path.exists(data_path):
    os.mkdir(data_path)
if not os.path.exists(figure_path):
    os.mkdir(figure_path)

# default subfolders of data is all subfolders of data_path except results_database
data_subfolders = [name for name in os.listdir(data_path) if (os.path.isdir(os.path.join(data_path, name)) and name != 'results_database')]
data_subfolders = ['2019_global_m3', '2005_2018_global_m5', '2018_2021_global_m5']
# for processing, can use multiple threads, set number of threads here
num_threads = 4
