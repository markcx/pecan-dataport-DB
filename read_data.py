import pandas as pd


dataname = 'data/eg_angle_15min.h5'
with pd.HDFStore(dataname) as hdf:
    # This prints a list of all group names:
    print(hdf.keys())

df=pd.read_hdf(dataname, key='/building1/elec/meter1')
print(df)