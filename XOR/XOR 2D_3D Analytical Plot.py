#analytival 2D/3D solution plotter
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from pylab import rcParams
import os

path_parent = os.path.dirname(os.getcwd())
fig_folder = path_parent

###2D Figure
##n = 0.01
##
##x_neg = np.arange(-10,-n,n) 
##x_pos = np.arange(n,10,n)
##x_range = np.concatenate((x_neg,x_pos))
##
##x_sqr = np.float16(np.square(x_range))
##x = x_range
##rcParams['figure.figsize'] = 5, 2
##
##f_values = [0.4,0.6,1]
##num_of_plots = len(f_values)
##fig, ax = plt.subplots(1,num_of_plots)
##
##for i in range(num_of_plots):
##    f_12 = f_values[i]
##    
##    y = (x_sqr/x)*(-2)*f_12
##    y1 = (x_sqr/x)*(1/((-2)*f_12))
##    y_neg = y[:len(y)//2]
##    y1_neg = y1[:len(y1)//2]
##    
##    
##    line = (y,x_range)
##    ax[i].plot(x_range,y,'b')
##    ax[i].plot(x_range,y1,'y')
##
##    #ax.grid()
##    ax[i].set_xlim(-1,1)
##    ax[i].set_ylim(-1,1)
##    ax[i].set_xlabel(r'$\ w_1$')
##
##    ax[i].fill_between(x_neg,y_neg,color = 'b',alpha=0.3,label='_nolegend_')
##    ax[i].fill_between(x_neg,y1_neg,10,color = 'yellow',alpha=0.3,label='_nolegend_')
##    ax[i].fill_between(-x_neg,-y_neg,color = 'b',alpha=0.3,label='_nolegend_')
##    ax[i].fill_between(-x_neg,-y1_neg,-10,color = 'yellow',alpha=0.3,label='_nolegend_')
##    ax[i].set_title(r'$\ F_{12} = %g$' %f_12)
##    
##fig.text(0.04,0.55, r'$\ w_2$', va='center', rotation='vertical')
##plt.tight_layout()
##fig.show()
##plt.savefig(fig_folder + '/Figure' + str(fignum) + '/f_analytical_2D'  + '.png')#, bbox_inches = 'tight')


import plotly.express as px
import numpy

#3D
data_x = []
data_y = []
data_z = []
inc = 0.025
for z in numpy.arange(0, 1, inc/2):
    for x in numpy.arange(-1, 1, inc):
        for y in numpy.arange(-1, 1, inc):
            if x**2 < -2*x*y*z and y**2 < -2*x*y*z:
                data_x.append(x)
                data_y.append(y)
                data_z.append(z)

##            if y**2 < -2*x*y*z:
##                data_x.append(x)
##                data_y.append(y)
##                data_z.append(z)

rcParams['figure.figsize'] = 3.5,3
fig = plt.figure()
num = 1
for i in range(num):
    ax = fig.add_subplot(1, num, i+1, projection='3d')
    ax = fig.gca(projection='3d')  #lightseagreen
    ax.scatter(data_x, data_y, data_z,c = 'mediumspringgreen',marker = 'o',s = 10 ,
               alpha = 0.4)
    ax.set_zlim([0,1])
    ax.set_xticks([-1,0,1])
    ax.set_yticks([-1,0,1])
    ax.set_zticks(np.linspace(0,1,5))
    ax.set_xlabel(r'$W_1$')
    ax.set_ylabel(r'$W_2$')
##    azimuths = [-60,-45]
##    elevations = [23,17]
    azimuths = [25]
    elevations = [38]   
    ax.view_init(elev=elevations[i], azim=azimuths[i])
#fig.text(0.06, 0.5, r'$\ f(l_1-l_2)$', va='center', rotation='vertical')
fig.text(0.06, 0.5, r'$\ F_{12}$', va='center', rotation='vertical')
plt.subplots_adjust(right = 1,top = 1)#,wspace = 0.1,hspace = 0.0)
#plt.savefig(fig_folder + '/Figure' + str(fignum) + '/f_analytical_3D'  + '.png')#, bbox_inches = 'tight')
plt.savefig(fig_folder+'/f_analytical_3D_single'  + '.png')#, bbox_inches = 'tight')

fig.show()





