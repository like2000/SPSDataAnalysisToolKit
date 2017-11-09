import os
import glob
import h5py
import numpy as np
import pandas as pd

from sddsdata import sddsdata


path_to_fbct = '/user/slops/data/SPS_DATA/OP_DATA/SPS_FBCT/'
output_path = '/afs/cern.ch/user/k/kli/afswork/Data/OP_DATA/SPS/'


def pull_to_hdf5(device='fbct', day=pd.datetime.today().strftime("%Y_%m_%d")):

    global path_to_fbct, output_path

    if device is 'fbct':
        device_no = '31450'
        path_to_fbct += "{:s}/SPS.BCTFR.{:s}@Acquisition/".format(day, device_no)
        output_path += device.upper() + "/{:s}/SPS.BCTFR.{:s}@Acquisition/".format(day, device_no)

        files = glob.glob(path_to_fbct + "*.sdds")
        filenames = map(lambda s: s.split('/')[-1], files)
    else:
        raise ValueError("Unknown device {:s}".format(device))

    # Create output directories if not already present
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    # Store in file all sdds which have already been converted
    if not os.path.exists(output_path + 'converted_fbct.txt'):
        with open(output_path + 'converted_fbct.txt', 'w') as fh:
            fh.write("*** Converted fbct files created at {:s}".format(str(pd.datetime.now())))
    else:
        with open(output_path + 'converted_fbct.txt', 'r') as fh:
            converted_list = fh.read().splitlines()
        del converted_list[0]

    # List of files still to be converted
    unconverted_files = [fn for i, fn in enumerate(files) if filenames[i] not in converted_list]
    
    for fl in unconverted_files[:]:
        try:
            data = sddsdata(fl, endian='little', full=True)
        except IOError as err:
            print("Failed to open file {:s}!".format(fl.split('/')[-1]))
            print(err.message)
            raise err

        ddict = data.data[0]
        fname = data.filename.split("/")[-1].replace("sdds", "h5")

        with h5py.File(output_path + fname, "w") as h5file:
            for t, v in ddict.items():
                try:
                    h5file.create_dataset(t, data=v, compression='gzip', compression_opts=9)
                except TypeError as err:
                    # print(err.message)
                    h5file.create_dataset(t, data=v)

        # Register converted files in converted file list
        with open(output_path + 'converted_fbct.txt', 'a') as fh:
            fh.write(fname.replace("h5", "sdds") + "\n")

        print("\n--> Converted file {:s} to hdf5 in folder {:s}".format(fname, output_path))
