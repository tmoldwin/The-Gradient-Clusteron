'''
G clusteeron toy model run
'''
from G_Clusteron_TOY_git import G_Clusteron_TOY
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.linalg import block_diag
import DataOrganizer as do
norm = plt.Normalize()
import matplotlib.animation as animation
from matplotlib.markers import MarkerStyle
import matplotlib.cm as cm

num_of_pix = 100
clstr_sz = None
epoch_to_plot = 3
wlr = 0
batch_size = 1
learning_protocol = 'L'
y = np.array([0])

label = 'pos'#'pos','neg'
experiment = 'mv_gaussian'#'uniform','mv_gaussian'
radius_size = 'small'#'large','small'
num_of_panels = 2

'learning rate factor'
factor = 10
speed_factor = 0.05
global num_of_init_frames
num_of_init_frames = 0
num_of_final_frames = 0

if experiment == 'uniform':
    g_f = 3#gaussian factor
    dataset = np.matrix(np.random.rand(num_of_pix)-0.5)
    shapes = np.repeat('o',num_of_pix)
    if label == 'pos':
        if radius_size == 'small':
            location_lr = 0.000075
            epochs = 1600
            radius = 0.01
        elif radius_size == 'large':
            location_lr = 0.001
            epochs = 1000
            radius = 2.5
    elif label == 'neg':
        epochs = 800
        radius = 0.01
        location_lr = 0.001
        dataset = np.sort(dataset)
    colors = np.array(dataset)[0]+0.5
elif experiment == 'mv_gaussian':
    ec='k'#edgecolor
    fc=[0,0,0,0]
    n_clusters = 4
    clstr_sz = 5
    N = clstr_sz * n_clusters
    num_of_examples = 1000
    y = np.ones(num_of_examples)
    means = np.zeros(N)#means of gaussian
    variance = 1
    dg = 0.7*variance*np.ones((clstr_sz,clstr_sz)) #off diagonals - should be 0.95
    dg_lst = [dg]*int(N/clstr_sz) #repeating off diagonal blocks
    cov = block_diag(*dg_lst)
    cov[np.where(cov==0)]=-0.2*variance
    np.fill_diagonal(cov,variance) #creates the actual diagonal (variances)
    shapes = np.repeat(['s','^','D','8','p','X'],clstr_sz)
    dataset = np.array(np.random.multivariate_normal(means, cov, num_of_examples))
    test_set = np.array(np.random.multivariate_normal(means, cov, num_of_examples))
    dataset = np.matrix(dataset)
    test_set = np.matrix(test_set)
    colors = plt.cm.RdYlBu(norm(np.squeeze(np.array(dataset[0]))))
    speed_factor = 0.5
    if label == 'pos':
        epochs = 200
        location_lr = 0.005
        radius = 0.5
    elif label == 'neg':
        epochs = 400
        batch_size = 1
        location_lr = 0.1
        radius = 5

blr = 500*location_lr

clusteron = G_Clusteron_TOY(dataset,y,radius,label,experiment,clstr_sz)
clusteron.train(epochs,learning_protocol,batch_size,location_lr,blr)

def animate(i):
    xlim = (clusteron.location_mat.min()-0.2, clusteron.location_mat.max()+0.2)
    x_vec = np.arange(xlim[0]-5, xlim[1]+5)
    epoch_num = i-num_of_init_frames
    if i<num_of_init_frames:
        epoch_num = 0
    elif i>epochs+num_of_init_frames-1:
        epoch_num = epochs-1
    locations_i = clusteron.location_mat[epoch_num]
    activations_i = clusteron.activations_mat[epoch_num]
    avg_act_i = np.mean(clusteron.activations_mat,1)[epoch_num]
    ax.set_title('Epoch ' + str(epoch_num))
    scat.set_offsets(np.c_[locations_i, activations_i])
    if experiment == 'mv_gaussian':
        colors_i = plt.cm.RdYlBu(norm(np.squeeze(np.array(dataset[epoch_num]))))
        '''to change the marker colors on every epoch'''
        scat.set_color(colors_i)
        new_marker_1 = MarkerStyle('s')#'s','^','D','8','p','X'
        new_marker_2 = MarkerStyle('^')
        new_marker_3 = MarkerStyle('p')
        new_marker_4 = MarkerStyle('8')
        scat.set_paths((new_marker_1.get_path(),new_marker_1.get_path(),new_marker_1.get_path(),new_marker_1.get_path(),new_marker_1.get_path(),
                        new_marker_2.get_path(),new_marker_2.get_path(),new_marker_2.get_path(),new_marker_2.get_path(),new_marker_2.get_path(),
                        new_marker_3.get_path(),new_marker_3.get_path(),new_marker_3.get_path(),new_marker_3.get_path(),new_marker_3.get_path(),
                        new_marker_4.get_path(),new_marker_4.get_path(),new_marker_4.get_path(),new_marker_4.get_path(),new_marker_4.get_path(),))
        scat.set_ec('k')
    hline.set_data(x_vec, avg_act_i*np.ones(len(x_vec)))
    
def plot_activations(epochs,activations_mat,location_mat,experiment,colors,
                     epoch_to_plot,training_examples=None,
                     num_of_panels=3):
    fig, axes = plt.subplots(1,num_of_panels,sharex=False,sharey=True,figsize=(4,3))

    ylim = (np.min(activations_mat)-0.5,
            np.max(activations_mat)+0.5)
    xlim = (location_mat.min()-1, location_mat.max()+1)
    if num_of_panels == 3:
        epochs_to_plot = [0,epoch_to_plot,epochs-1]
        panel_titles = ['Before learning','During learning', 'After learning']
    elif num_of_panels == 2:
        epochs_to_plot = [0,epochs-1]
        panel_titles = ['Before learning', 'After learning']
    if experiment == 'uniform': 
        #the gaussian
        c_o_d = (np.max(clusteron.location_mat[-1])+np.min(clusteron.location_mat[-1]))/2 #center of distribution
        x = np.linspace(c_o_d-g_f,c_o_d+g_f,1000)
        gaussian = np.exp((-(x-c_o_d)**2)/radius)

    for i in range(num_of_panels):
        epoch = epochs_to_plot[i]
        axes[i].set_title(panel_titles[i])
        axes[i].set_xticks([])
        axes[i].axhline(np.mean(activations_mat,1)[epoch],ls='-.',alpha=1)
        axes[i].spines['right'].set_visible(False)#removes top border
        axes[i].spines['top'].set_visible(False)
        if experiment == 'uniform':
            axes[i].set_ylim(ylim)
            axes[i].set_xlim(xlim)
            axes[i].scatter(location_mat[epoch],activations_mat[epoch],c = colors,
                            edgecolor = 'k',linewidths=0.4,cmap=plt.cm.RdYlBu_r,
                            s = 40)
            if i == 0:
                axes[i].plot(x,gaussian-1)
            plt.ylim(ylim)
        elif experiment == 'mv_gaussian':
            ylim_min = np.min((np.min(clusteron.activations_mat[0]),np.min(clusteron.activations_mat[-1])))
            ylim_max = np.max((np.max(clusteron.activations_mat[0]),np.max(clusteron.activations_mat[-1])))
            ylim = ((ylim_min-1,ylim_max+1))
            axes[i].set_ylim(ylim)
            colors = plt.cm.RdYlBu(norm(np.squeeze(np.array(dataset[training_examples[epoch]]))))

            for xp, yp, m, clr in zip(location_mat[epoch], activations_mat[epoch],
                             shapes,colors):
                axes[i].scatter([xp],[yp], marker=m,#c=clr,#cmap=plt.cm.RdYlBu_r,
                            s=60,edgecolor=ec,facecolors=clr)
            plt.ylim(ylim)
    plt.show()

plot_activations(epochs,clusteron.activations_mat,clusteron.location_mat,
                 experiment,colors,epoch_to_plot,
                 clusteron.training_examples_used,num_of_panels)
    
    
def plot_animation(activations_mat,location_mat,colors,
                   experiment,radius_size):
    global fig,ax,scat,hline,V
    fig, ax = plt.subplots(figsize=(10, 10))
    xlim = (location_mat.min()-0.2, location_mat.max()+0.2)
    ylim = (np.min(activations_mat)-4,np.max(activations_mat)+10)
    ax.set(xlim=xlim,ylim=ylim)
    ax.set_xlabel('Location')
    ax.set_ylabel('Activation')
    if experiment == 'uniform':
        scat = ax.scatter(location_mat[0], np.zeros(len(location_mat[0])),
              c = colors,edgecolors = 'k',s = 65,cmap=plt.cm.RdYlBu_r)
    elif experiment == 'mv_gaussian':
        scat = ax.scatter(location_mat[0], np.zeros(len(location_mat[0])),c=colors
                      ,marker='8',edgecolor='k',s=60)
    line_0 = np.mean(activations_mat,1)[0]
    x_vec = np.arange(xlim[0], xlim[1])
    hline, = ax.plot(x_vec, line_0 * np.ones(len(x_vec)),linestyle='--',
                     alpha=0.9,markersize=100.0)
    anim = FuncAnimation(fig, animate, frames=epochs+num_of_init_frames+num_of_final_frames,
                         interval=speed_factor*100,
                         repeat=False)
    plt.show()
    return 

plot_animation(clusteron.activations_mat,clusteron.location_mat,
               colors,experiment,radius_size)
