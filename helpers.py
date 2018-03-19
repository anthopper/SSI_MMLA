import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Set up skeleton_df
def col_names():
    # returns a 560-dimension vector that can be used for the names optional input when calling pd.read_csv to make the Kinect dataframe
    # names/values from https://github.com/hcmlab/ssi/blob/master/plugins/microsoftkinect/include/MicrosoftKinect.h
    JOINTS = [
            'HIP_CENTER',
            'SPINE',
            'SHOULDER_CENTER',
            'HEAD',
            'SHOULDER_LEFT',
            'ELBOW_LEFT',
            'WRIST_LEFT',
            'HAND_LEFT',
            'SHOULDER_RIGHT',
            'ELBOW_RIGHT',
            'WRIST_RIGHT',
            'HAND_RIGHT',
            'HIP_LEFT',
            'KNEE_LEFT',
            'ANKLE_LEFT',
            'FOOT_LEFT',
            'HIP_RIGHT',
            'KNEE_RIGHT',
            'ANKLE_RIGHT',
            'FOOT_RIGHT'
            ]

    JOINT_VALS = [
            'POS_X',
            'POS_Y',
            'POS_Z',
            'POS_CONF',

            'ROT_W',
            'ROT_X',
            'ROT_Y',
            'ROT_Z',
            'ROT_CONF',

            'RELROT_W',
            'RELROT_X',
            'RELROT_Y',
            'RELROT_Z',
            'RELROT_CONF'
            ]

    col_names = []
    for j in JOINTS:
        for jv in JOINT_VALS:
            col_names.append(j+'_'+jv+'_P1')

    for j in JOINTS:
        for jv in JOINT_VALS:
            col_names.append(j+'_'+jv+'_P2')
    return col_names

# Set up dataframe of XYZ position columns
def create_xyz_df(df):
    # df should have the Kinect data collected with SSI and column names 
    # returns a dataframe of just the X_POS, Y_POS, and Z_POS values for each tracked joint 
    xyz_cols = []
    for c in df.columns.values:
        if ('POS_X' in c) or ('POS_Y' in c) or ('POS_Z' in c):
            xyz_cols.append(c)
    return df[xyz_cols]

# Plotting a point cloud for a specific row of Kinect data
def xyz_triples(r):
    # r is a 120-dimension vector 
    # (i.e. a row in kinect_xyz_df, 
    # which just has X_POS, Y_POS, and Z_POS values for each tracked joint)
    
    # getting XYZ triples from r
    points = []
    for i in range(0, 120, 3):
        points.append([r[i], r[i+1], r[i+2]])                 
    return pd.DataFrame(points, columns=['X_POS', 'Y_POS', 'Z_POS'])

def plot_xyz_triples(r_points_df, title=''):
    # r_points_df is the output of xyz_triples(r) function
    # returns nothing but plots a specific skeletal configuration for you in the jupyter notebook!

    # plotting
    fig = plt.figure(1)
    ax = Axes3D(fig)
    ax.scatter(r_points_df['X_POS'], r_points_df['Y_POS'], r_points_df['Z_POS'])
    ax.set_xlabel('X_POS')
    ax.set_ylabel('Y_POS')
    ax.set_zlabel('Z_POS')
    ax.set_title(title)
    plt.show()
    return