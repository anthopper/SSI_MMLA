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
    return df.loc[:,:][xyz_cols].copy()

# Plotting a point cloud for a specific row of Kinect data
def xyz_triples(r):
    # r is a row in kinect_xyz_df, 
    # which just has X_POS, Y_POS, and Z_POS values for each tracked joint)
    
    # getting XYZ triples from r
    points = []
    for i in range(0, r.shape[0], 3):
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

def draw_line(ax, a, b):    
    x = np.linspace(a[0], b[0], 100)
    y = np.linspace(a[1], b[1], 100)
    z = np.linspace(a[2], b[2], 100)
    ax.plot(x, y, z)

def drop_lower_parts(df):
    UPPER_PARTS = ['SHOULDER', 'HEAD', 'ELBOW', 'WRIST', 'HAND'] 
    UPPER_PARTS_COLS = []
    for c in df.columns.values.tolist():
        for part in UPPER_PARTS:
            if ('POS' in c) and (part in c) and ('CONF' not in c):
                UPPER_PARTS_COLS.append(c)
    return df.loc[:,:][UPPER_PARTS_COLS].copy()

JOINT_PAIRS = [
                ['WRIST_LEFT', 'HAND_LEFT'],
                ['WRIST_LEFT', 'ELBOW_LEFT'],
                ['ELBOW_LEFT', 'SHOULDER_LEFT'],
                ['SHOULDER_LEFT', 'SHOULDER_CENTER'],
                ['SHOULDER_CENTER', 'SHOULDER_RIGHT'],
                ['ELBOW_RIGHT', 'SHOULDER_RIGHT'],
                ['WRIST_RIGHT', 'ELBOW_RIGHT'],
                ['WRIST_RIGHT', 'HAND_RIGHT'],
                ['SHOULDER_CENTER', 'HEAD'],
              ]

def plot_skeleton(ax, row):
    # expecting row to be from a dataframe with UPPER_PARTS_COLS values
    
    for person in ['P1', 'P2']:
        for jp in JOINT_PAIRS:
            draw_line(ax, [row[jp[0]+'_POS_X_'+person], row[jp[0]+'_POS_Z_'+person], row[jp[0]+'_POS_Y_'+person]], 
                          [row[jp[1]+'_POS_X_'+person], row[jp[1]+'_POS_Z_'+person], row[jp[1]+'_POS_Y_'+person]])
                
    return 

def readable_timestamp(df, timestamp_col_name='Timestamp'):
    # converting Timestamp in milliseconds (for analysis) 
    # to a MM:SS format (for readability and revisiting transcripts afterwards)

    timestamp = df.loc[:, 'Timestamp'].copy()
    timestamp_min = np.floor(timestamp/1000/60)
    timestamp_sec = (timestamp - timestamp_min*1000*60)/1000
    readable_timestamp = []

    for i in range(len(timestamp)):
        m = "%02d" % timestamp_min[i]
        s = "%02d" % timestamp_sec[i]
        readable_timestamp.append(m + ":" + s)

    df.loc[:, 'Readable Timestamp'] = readable_timestamp
    return df.loc[:, :].copy()