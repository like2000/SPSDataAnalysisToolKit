import glob, h5py, sys, tables
sys.path.append('/home/kli/workspace/')
sys.path.append('/eos/user/k/kli/workspace/')
sys.path.append('/afs/cern.ch/user/k/kli/public')

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

# import pjlsa
# lsa = pjlsa.LSAClient()

import pytimber
ldb = pytimber.LoggingDB()
# from headtail.modules import bqht


sns.set(context='notebook', style='darkgrid', palette='deep',
        font='serif', font_scale=1, color_codes=False,
        rc={'axes.edgecolor': '0.4',
            'axes.linewidth': 2,
            'font.family': 'sans-serif',
            'font.sans-serif': 'helvetica',
            'lines.markeredgewidth': 0.1,
            'savefig.transparent': False,
#             'text.usetex': True,
#             'text.latex.preamble': (
#                 r'\usepackage{helvet}',),
        })

