from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
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

##n = 0.01
##f_12 = 1
##
##x_neg = np.arange(-10,-n,n) 
##x_pos = np.arange(n,10,n)
##x_range = np.concatenate((x_neg,x_pos))
##
##x_sqr = np.float16(np.square(x_range))
##x = x_range
##y = (x_sqr/x)*(-2)*f_12
##y1 = (x_sqr/x)*(1/((-2)*f_12))
##y_neg = y[:len(y)//2]
##y1_neg = y1[:len(y1)//2]
##fig, ax = plt.subplots()
##line = (y,x_range)
##ax.plot(x_range,y)
##ax.plot(x_range,y1)
##
##ax.grid()
##ax.set_xlim(-10,10)
##ax.set_ylim(-10,10)
##
##plt.fill_between(x_neg,y_neg,color = 'b',alpha=0.3)
##plt.fill_between(x_neg,y1_neg,10,color = 'orange',alpha=0.3)
##plt.fill_between(-x_neg,-y_neg,color = 'b',alpha=0.3)
##plt.fill_between(-x_neg,-y1_neg,-10,color = 'orange',alpha=0.3)
##
##fig.show()
##


import plotly.express as px
import numpy

# data_x = []
# data_y = []
# data_z = []
# inc = 0.1
# for z in numpy.arange(0, 1, inc/2):
#     for x in numpy.arange(-1, 1, inc):
#         for y in numpy.arange(-1, 1, inc):
#             if x**2 < -2*x*y*z and y**2 < -2*x*y*z:
#                 data_x.append(x)
#                 data_y.append(y)
#                 data_z.append(z)
# 
# ##            if y**2 < -2*x*y*z:
# ##                data_x.append(x)
# ##                data_y.append(y)
# ##                data_z.append(z)
# 
# 
fig = plt.figure()
ax = fig.gca(projection='3d')
# ax.scatter(data_x, data_y, data_z,marker = 'o',s = 1 ,alpha = 0.1)
pts = np.random.rand(3,100)
ax.scatter((pts[0]*2)-1, (pts[1]*2)-1, pts[2],marker = 'o', facecolors = 'none', s = 20 ,alpha = 1)
# ax.set_zlim(-0.1,1)
# eps = 10**-5
# ax.set_xticks(np.arange(-1,1+eps,0.5))
# ax.set_yticks(np.arange(-1,1+eps,0.5))
# ax.set_zticks(np.arange(0,1+eps,0.25))
fig.show()
# zs = np.arange(0,1,0.01)
# for z in zs:
#     line1x = [-1,1]
#     line1y = line1x/-2*z
#     line2y = [-1,1]
#     line2x = line2y/-2*z
#     for z in zs:
#         xs = 
#         ys = 
#     ys[0], ys[-1] = 0, 0
#     verts.append(list(zip(xs, ys)))
#     ax.add_collection3d(pl.fill_between(line1x[0], line1x[1], 1.05*z, color='r', alpha=0.3), zs=1, zdir='z')
# 
#     #     ax.plot3D(line1x, line1y, z, color = 'gray')
# #     ax.plot3D(line2x, line2y, z, color = 'gray')
# 

# print(pts)
# ax.set_zlim([0,1])
# ax.set_xlabel('W_1')
# ax.set_ylabel('W_2')
# ax.set_zlabel('f(l1,l2)')
# 
# fig.show()






