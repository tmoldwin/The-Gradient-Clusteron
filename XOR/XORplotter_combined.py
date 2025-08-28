'''
XOR plotter for data in json files - Combined version
Shows both initial and final weights in a single figure with two rows
'''
import os
import sys
path_parent = os.path.dirname(os.getcwd())
# os.chdir(path_parent)
sys.path.insert(0,path_parent)
#print(path_parent)
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import matplotlib.patches as patches
from matplotlib import cm
import pprint 
import json
from pylab import rcParams


fig_folder = path_parent 
fignum = 6

def create_combined_scatter_plots(json_files,epochs=10000,fig_size = (7.5,6.)):
    rcParams['figure.figsize'] = fig_size
    fig = plt.figure('Combined XOR Visualization', facecolor='white')
    fig.patch.set_facecolor('white')

    for i in range(len(json_files)):
        file_name = 'XORData/'+json_files[i]+'.json'
        with open(file_name, "r") as read_file:#extract data from file
            results = json.load(read_file)

        num_of_tests = len(results)

        #getting mean of convergence
        conv_count = 0
        neg_conv_count = 0#number of times no convergence
        for result in results:
            if result['convergence'] == -1:
                neg_conv_count += 1
            else:
                conv_count += result['convergence']

        initfs = [result['initial f'] for result in results]
        convergences = [epochs if result['convergence'] == -1 else result['convergence'] for result in results]
        w1_init = np.array([result['initial weights'][0] for result in results])
        w1_final = np.array([result['final weights'][0] for result in results])
        w2_init = np.array([result['initial weights'][1] for result in results])
        w2_final = np.array([result['final weights'][1] for result in results])
        f_init = np.array([result['initial f'] for result in results])
        f_final = np.array([result['final f'] for result in results])

        if file_name[file_name.find('/')+1:file_name.find('.')] == json_files[0]:
            title = 'Weight and Location Rule'
        elif file_name[file_name.find('/')+1:file_name.find('.')] == json_files[2]:
            title = 'Weight Rule'
        elif file_name[file_name.find('/')+1:file_name.find('.')] == json_files[1]:
            title = 'Location Rule'
        else:
            title = 'title'
           
        eps = 1
        
        colors = np.array([epochs if (result['convergence'] == -1) else result['convergence'] for result in results]) + eps
        list_of_convergences = [0 if result['convergence'] == -1 else 1 for result in results]
        list_of_expectations = [result['expected to converge'] for result in results]
        conv_indices = np.where(list_of_convergences)
        non_conv_indices_unexp = np.where([1 if list_of_convergences[ind] == 0 and list_of_expectations[ind] == 1 else 0 for ind in range(len(list_of_convergences))])[0]
        non_conv_but_expctd_indices = np.where([1 if list_of_convergences[ind] == 0 and list_of_expectations[ind] == 0 else 0 for ind in range(len(list_of_convergences))])[0]

        norm = matplotlib.colors.LogNorm(vmin=colors.min(),vmax=colors.max())
        cmap = plt.get_cmap("viridis_r")

        # Six completely different tri-color schemes - one for each plot
        color_schemes = [
            # Plot 1 (top left) - Red, Blue, Green
            {'conv': 'red', 'non_conv': 'blue', 'non_conv_exp': 'green'},
            # Plot 2 (top middle) - Purple, Orange, Brown
            {'conv': 'purple', 'non_conv': 'orange', 'non_conv_exp': 'brown'},
            # Plot 3 (top right) - Pink, Cyan, Black
            {'conv': 'pink', 'non_conv': 'cyan', 'non_conv_exp': 'black'},
            # Plot 4 (bottom left) - Yellow, Magenta, Navy
            {'conv': 'yellow', 'non_conv': 'magenta', 'non_conv_exp': 'navy'},
            # Plot 5 (bottom middle) - Lime, Coral, Gray
            {'conv': 'lime', 'non_conv': 'coral', 'non_conv_exp': 'gray'},
            # Plot 6 (bottom right) - Gold, Teal, Maroon
            {'conv': 'gold', 'non_conv': 'teal', 'non_conv_exp': 'maroon'}
        ]
        
        # Different panel background colors for each plot
        panel_backgrounds = [
            'lightcoral',    # Plot 1 (top left)
            'lightsteelblue', # Plot 2 (top middle)
            'lightgreen',    # Plot 3 (top right)
            'lightyellow',   # Plot 4 (bottom left)
            'lightpink',     # Plot 5 (bottom middle)
            'lightcyan'      # Plot 6 (bottom right)
        ]
        
        # Different cube interior colors for each plot
        cube_colors = [
            'mistyrose',     # Plot 1 (top left)
            'aliceblue',     # Plot 2 (top middle)
            'honeydew',      # Plot 3 (top right)
            'ivory',         # Plot 4 (bottom left)
            'lavenderblush', # Plot 5 (bottom middle)
            'azure'          # Plot 6 (bottom right)
        ]
        
        # INITIAL WEIGHTS - TOP ROW
        ax_init = fig.add_subplot(2, 3, i+1, projection='3d')
        
        # Select color scheme and backgrounds for INITIAL weights (top row)
        init_plot_index = i  # 0,1,2 for top row
        init_color_scheme = color_schemes[init_plot_index]
        init_panel_bg = panel_backgrounds[init_plot_index]
        init_cube_bg = cube_colors[init_plot_index]
        
        conv_colors = init_color_scheme['conv']
        non_conv_colors = init_color_scheme['non_conv']
        non_conv_but_expctd_colors = init_color_scheme['non_conv_exp']

        # Filter points to be within the box boundaries
        if len(conv_indices) > 0:
            mask = (w1_init[conv_indices] >= -1) & (w1_init[conv_indices] <= 1) & \
                   (w2_init[conv_indices] >= -1) & (w2_init[conv_indices] <= 1) & \
                   (f_init[conv_indices] >= 0) & (f_init[conv_indices] <= 1)
            ax_init.scatter(w1_init[conv_indices][mask], w2_init[conv_indices][mask],
                       f_init[conv_indices][mask], c = conv_colors, marker = 'o',
                       s = 10, alpha = 1)
        if len(non_conv_indices_unexp) > 0:
            mask = (w1_init[non_conv_indices_unexp] >= -1) & (w1_init[non_conv_indices_unexp] <= 1) & \
                   (w2_init[non_conv_indices_unexp] >= -1) & (w2_init[non_conv_indices_unexp] <= 1) & \
                   (f_init[non_conv_indices_unexp] >= 0) & (f_init[non_conv_indices_unexp] <= 1)
            ax_init.scatter(w1_init[non_conv_indices_unexp][mask], w2_init[non_conv_indices_unexp][mask],
                       f_init[non_conv_indices_unexp][mask], edgecolor = non_conv_but_expctd_colors,
                       facecolor=(0,0,0,0), marker ='v',s = 40)
        if len(non_conv_but_expctd_indices) > 0:   
            mask = (w1_init[non_conv_but_expctd_indices] >= -1) & (w1_init[non_conv_but_expctd_indices] <= 1) & \
                   (w2_init[non_conv_but_expctd_indices] >= -1) & (w2_init[non_conv_but_expctd_indices] <= 1) & \
                   (f_init[non_conv_but_expctd_indices] >= 0) & (f_init[non_conv_but_expctd_indices] <= 1)
            ax_init.scatter(w1_init[non_conv_but_expctd_indices][mask], w2_init[non_conv_but_expctd_indices][mask],
                       f_init[non_conv_but_expctd_indices][mask],edgecolor = non_conv_colors,
                       facecolor=(0,0,0,0), marker ='o',s = 10)
        
        ax_init.set_zlim(0,1)
        ax_init.set_xlim(-1,1)
        ax_init.set_ylim(-1,1)
        # Remove all axes, labels, and titles
        ax_init.set_xticks([])
        ax_init.set_yticks([])
        ax_init.set_zticks([])
        ax_init.set_xlabel('')
        ax_init.set_ylabel('')
        ax_init.set_zlabel('')
        ax_init.set_title('')
        # Remove axis lines
        ax_init.xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        ax_init.yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        ax_init.zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        # Set background to panel-specific color and remove all grid elements
        ax_init.grid(False)
        ax_init.set_facecolor(init_panel_bg)
        ax_init.xaxis.pane.fill = True
        ax_init.yaxis.pane.fill = True
        ax_init.zaxis.pane.fill = True
        ax_init.xaxis.pane.set_facecolor(init_cube_bg)
        ax_init.yaxis.pane.set_facecolor(init_cube_bg)
        ax_init.zaxis.pane.set_facecolor(init_cube_bg)
        ax_init.xaxis.pane.set_edgecolor('gray')
        ax_init.yaxis.pane.set_edgecolor('gray')
        ax_init.zaxis.pane.set_edgecolor('gray')
        ax_init.xaxis.pane.set_alpha(0.3)
        ax_init.yaxis.pane.set_alpha(0.3)
        ax_init.zaxis.pane.set_alpha(0.3)
        
        # Add transparent 3D block around the plot
        x = np.array([-1, -1, -1, -1, 1, 1, 1, 1])
        y = np.array([-1, -1, 1, 1, -1, -1, 1, 1])
        z = np.array([0, 1, 0, 1, 0, 1, 0, 1])
        
        # Create wireframe box
        
        # Define the 8 vertices of the cube
        vertices = np.array([
            [-1, -1, 0],  # 0
            [1, -1, 0],   # 1
            [1, 1, 0],    # 2
            [-1, 1, 0],   # 3
            [-1, -1, 1],  # 4
            [1, -1, 1],   # 5
            [1, 1, 1],    # 6
            [-1, 1, 1]    # 7
        ])
        
        # Define the 6 faces of the cube
        faces = [
            [vertices[0], vertices[1], vertices[2], vertices[3]],  # bottom
            [vertices[4], vertices[5], vertices[6], vertices[7]],  # top
            [vertices[0], vertices[1], vertices[5], vertices[4]],  # front
            [vertices[2], vertices[3], vertices[7], vertices[6]],  # back
            [vertices[1], vertices[2], vertices[6], vertices[5]],  # right
            [vertices[0], vertices[3], vertices[7], vertices[4]]   # left
        ]
        
        # All plots use cube-colored polyhedron
        poly3d = Poly3DCollection(faces, alpha=0.2, facecolor=init_cube_bg, edgecolor='gray', linewidth=0.8)
        ax_init.add_collection3d(poly3d)
        
        # Set all plots to the same normal viewing angle
        ax_init.view_init(elev=20, azim=-135)

        # FINAL WEIGHTS - BOTTOM ROW
        ax_final = fig.add_subplot(2, 3, i+4, projection='3d')
        
        # Select color scheme and backgrounds for FINAL weights (bottom row)
        final_plot_index = i + 3  # 3,4,5 for bottom row
        final_color_scheme = color_schemes[final_plot_index]
        final_panel_bg = panel_backgrounds[final_plot_index]
        final_cube_bg = cube_colors[final_plot_index]
        
        # Update colors for final weights plots
        conv_colors_final = final_color_scheme['conv']
        non_conv_colors_final = final_color_scheme['non_conv']
        non_conv_but_expctd_colors_final = final_color_scheme['non_conv_exp']
        
        # Filter points to be within the box boundaries
        if len(conv_indices) > 0:
            mask = (w1_final[conv_indices] >= -1) & (w1_final[conv_indices] <= 1) & \
                   (w2_final[conv_indices] >= -1) & (w2_final[conv_indices] <= 1) & \
                   (f_final[conv_indices] >= 0) & (f_final[conv_indices] <= 1)
            ax_final.scatter(w1_final[conv_indices][mask], w2_final[conv_indices][mask],
                       f_final[conv_indices][mask], c = conv_colors_final, marker = 'o',
                       s = 10, alpha = 1)
        if len(non_conv_indices_unexp) > 0:
            mask = (w1_final[non_conv_indices_unexp] >= -1) & (w1_final[non_conv_indices_unexp] <= 1) & \
                   (w2_final[non_conv_indices_unexp] >= -1) & (w2_final[non_conv_indices_unexp] <= 1) & \
                   (f_final[non_conv_indices_unexp] >= 0) & (f_final[non_conv_indices_unexp] <= 1)
            ax_final.scatter(w1_final[non_conv_indices_unexp][mask], w2_final[non_conv_indices_unexp][mask],
                       f_final[non_conv_indices_unexp][mask], edgecolor = non_conv_but_expctd_colors_final,
                       facecolor=(0,0,0,0), marker ='v',s = 40)
        if len(non_conv_but_expctd_indices) > 0:   
            mask = (w1_final[non_conv_but_expctd_indices] >= -1) & (w1_final[non_conv_but_expctd_indices] <= 1) & \
                   (w2_final[non_conv_but_expctd_indices] >= -1) & (w2_final[non_conv_but_expctd_indices] <= 1) & \
                   (f_final[non_conv_but_expctd_indices] >= 0) & (f_final[non_conv_but_expctd_indices] <= 1)
            ax_final.scatter(w1_final[non_conv_but_expctd_indices][mask], w2_final[non_conv_but_expctd_indices][mask],
                       f_final[non_conv_but_expctd_indices][mask],edgecolor = non_conv_colors_final,
                       facecolor=(0,0,0,0), marker ='o',s = 10)
        

        ax_final.set_zlim(0,1)
        ax_final.set_xlim(-1,1)
        ax_final.set_ylim(-1,1)
        # Remove all axes, labels, and titles
        ax_final.set_xticks([])
        ax_final.set_yticks([])
        ax_final.set_zticks([])
        ax_final.set_xlabel('')
        ax_final.set_ylabel('')
        ax_final.set_zlabel('')
        ax_final.set_title('')
        # Remove axis lines
        ax_final.xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        ax_final.yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        ax_final.zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        # Set background to panel-specific color and remove all grid elements
        ax_final.grid(False)
        ax_final.set_facecolor(final_panel_bg)
        ax_final.xaxis.pane.fill = True
        ax_final.yaxis.pane.fill = True
        ax_final.zaxis.pane.fill = True
        ax_final.xaxis.pane.set_facecolor(final_cube_bg)
        ax_final.yaxis.pane.set_facecolor(final_cube_bg)
        ax_final.zaxis.pane.set_facecolor(final_cube_bg)
        ax_final.xaxis.pane.set_edgecolor('gray')
        ax_final.yaxis.pane.set_edgecolor('gray')
        ax_final.zaxis.pane.set_edgecolor('gray')
        ax_final.xaxis.pane.set_alpha(0.3)
        ax_final.yaxis.pane.set_alpha(0.3)
        ax_final.zaxis.pane.set_alpha(0.3)
        
        # Add transparent 3D block around the plot
        x = np.array([-1, -1, -1, -1, 1, 1, 1, 1])
        y = np.array([-1, -1, 1, 1, -1, -1, 1, 1])
        z = np.array([0, 1, 0, 1, 0, 1, 0, 1])
        
        # Create wireframe box
        
        # Define the 8 vertices of the cube
        vertices = np.array([
            [-1, -1, 0],  # 0
            [1, -1, 0],   # 1
            [1, 1, 0],    # 2
            [-1, 1, 0],   # 3
            [-1, -1, 1],  # 4
            [1, -1, 1],   # 5
            [1, 1, 1],    # 6
            [-1, 1, 1]    # 7
        ])
        
        # Define the 6 faces of the cube
        faces = [
            [vertices[0], vertices[1], vertices[2], vertices[3]],  # bottom
            [vertices[4], vertices[5], vertices[6], vertices[7]],  # top
            [vertices[0], vertices[1], vertices[5], vertices[4]],  # front
            [vertices[2], vertices[3], vertices[7], vertices[6]],  # back
            [vertices[1], vertices[2], vertices[6], vertices[5]],  # right
            [vertices[0], vertices[3], vertices[7], vertices[4]]   # left
        ]
        
        # All plots use cube-colored polyhedron
        poly3d = Poly3DCollection(faces, alpha=0.2, facecolor=final_cube_bg, edgecolor='gray', linewidth=0.8)
        ax_final.add_collection3d(poly3d)
        
        # Set all plots to the same normal viewing angle
        ax_final.view_init(elev=20, azim=-135)
    
    plt.subplots_adjust(left = 0.0, right = 1.0, top = 1.0, bottom = 0.0, wspace = 0.0, hspace = -0.1)

    # Save the figure
    plt.savefig('figures/XOR_combined_visualization.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    return 


files = ['W_test_161','just_location1','both']
#files = ['just_locationonly_expected_convs','just_locationonly_expected_convs','just_locationonly_expected_convs']
#files = ['both','just_location_2','just_weights']

create_combined_scatter_plots(files, fig_size = (7.5,6.))