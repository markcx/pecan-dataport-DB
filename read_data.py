import pandas as pd

with pd.HDFStore('data/26_eg_realpower_1hr.h5') as hdf:
    # This prints a list of all group names:
    print(hdf.keys())

df=pd.read_hdf('data/26_eg_realpower_1hr.h5', key='/building1/elec/meter1')
print(df)