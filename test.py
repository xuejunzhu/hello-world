
#%%

import matplotlib.pyplot as plt
import numpy as np
import os
os.getcwd()
os.chdir("C:/Temp")

my_x = np.linspace(-1,1) 
my_y = np.sin(my_x) 

plt.plot(my_x,my_y) 
title = "Plot"
filename = "plot.jpg" 

plt.title(title) 
plt.savefig(filename)  
plt.show()

# step 2

# step 3

# step 4

# step 5















