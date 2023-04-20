# Draw the bandwidth graph
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

data = pd.read_csv('./bandwidth.csv')  # read the csv file

new_data = pd.DataFrame({'len': data['frame.len'], 'time': data['frame.time_epoch']})  # select length and time
new_data['time'] = pd.to_datetime(new_data['time'], unit='s')  # convert timestamp to time
new_data = new_data.set_index('time')
new_data = new_data.resample('10T').sum()  # every 10 minutes

sb.lineplot(x=np.arange(0, 27)*10, y=new_data['len']).set(xlabel='Minutes', ylabel='Frame Length')
plt.show()
