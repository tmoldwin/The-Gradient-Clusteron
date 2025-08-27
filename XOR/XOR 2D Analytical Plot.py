from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from pylab import rcParams
import os

##
##fig = plt.figure()
##ax = fig.gca(projection='3d')
##
### Make data.
##X = np.arange(-5, 5, 0.25)
##Y = np.arange(-5, 5, 0.25)
##X, Y = np.meshgrid(X, Y)
##R = np.sqrt(X**2 + Y**2)
##Z = np.sin(R)
##
### Plot the surface.
##surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
##                       linewidth=0, antialiased=False)
##
### Customize the z axis.
##ax.set_zlim(-1.01, 1.01)
##ax.zaxis.set_major_locator(LinearLocator(10))
##ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
##
### Add a color bar which maps values to colors.
##fig.colorbar(surf, shrink=0.5, aspect=5)
##
##plt.show()
path_parent = os.path.dirname(os.getcwd())
fig_folder = path_parent + '/PaperFigures_5_31_2020'
fignum = 5

n = 0.01

x_neg = np.arange(-10,-n,n) 
x_pos = np.arange(n,10,n)
x_range = np.concatenate((x_neg,x_pos))

x_sqr = np.float16(np.square(x_range))
x = x_range
rcParams['figure.figsize'] = 5, 5

f_values = [1]
num_of_plots = len(f_values)
fig, ax = plt.subplots(1,num_of_plots)

for i in range(num_of_plots):
    f_12 = f_values[i]
    
    y = (x_sqr/x)*(-2)*f_12
    y1 = (x_sqr/x)*(1/((-2)*f_12))
    y_neg = y[:len(y)//2]
    y1_neg = y1[:len(y1)//2]
    
    
    line = (y,x_range)
    ax.plot(x_range,y)
    ax.plot(x_range,y1)

    #ax.grid()
    ax.set_xlim(-5,5)
    ax.set_ylim(-5,5)
    ax.set_xlabel(r'$\ w_1$')
    ax.set_ylabel(r'$\ w_2$')

    ax.fill_between(x_neg,y_neg,color = 'b',alpha=0.3,label='_nolegend_')
    ax.fill_between(x_neg,y1_neg,10,color = 'orange',alpha=0.3,label='_nolegend_')
    ax.fill_between(-x_neg,-y_neg,color = 'b',alpha=0.3,label='_nolegend_')
    ax.fill_between(-x_neg,-y1_neg,-10,color = 'orange',alpha=0.3,label='_nolegend_')
    ax.set_title(r'$\ f(l_1-l_2) = %g$' %f_12)

plt.tight_layout()
fig.show()
#plt.savefig(fig_folder + '/Figure' + str(fignum) + '/f_analytical'  + '.png')#, bbox_inches = 'tight')







