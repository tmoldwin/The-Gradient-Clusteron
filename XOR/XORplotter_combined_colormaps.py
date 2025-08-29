'''
XOR plotter for data in json files - Multiple Aesthetic Styles Version
Shows both initial and final weights using different aesthetic styles for axes and grid lines
'''
import os
import sys
path_parent = os.path.dirname(os.getcwd())
sys.path.insert(0,path_parent)
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
from datetime import datetime

fig_folder = path_parent 
fignum = 6

def create_combined_scatter_plots(json_files,epochs=10000,fig_size = (7.5,6.)):
    
    # Define different aesthetic styles
    styles = {
        'minimal': {
            'name': 'Minimal',
            'axis_linewidth': 0.5,
            'axis_alpha': 0.3,
            'grid_alpha': 0.05,
            'grid_linewidth': 0.3,
            'cube_alpha': 0.05,
            'cube_edge_alpha': 0.2,
            'cube_edge_linewidth': 0.3,
            'pane_alpha': 0.1
        },
        'bold': {
            'name': 'Bold',
            'axis_linewidth': 6,
            'axis_alpha': 1.0,
            'grid_alpha': 0.6,
            'grid_linewidth': 1.5,
            'cube_alpha': 0.3,
            'cube_edge_alpha': 0.8,
            'cube_edge_linewidth': 2,
            'pane_alpha': 0.8
        },
        'clean': {
            'name': 'Clean',
            'axis_linewidth': 1.5,
            'axis_alpha': 0.8,
            'grid_alpha': 0.3,
            'grid_linewidth': 0.8,
            'cube_alpha': 0.15,
            'cube_edge_alpha': 0.6,
            'cube_edge_linewidth': 1,
            'pane_alpha': 0.6
        },
        'ethereal': {
            'name': 'Ethereal',
            'axis_linewidth': 1,
            'axis_alpha': 0.4,
            'grid_alpha': 0.15,
            'grid_linewidth': 0.5,
            'cube_alpha': 0.08,
            'cube_edge_alpha': 0.3,
            'cube_edge_linewidth': 0.8,
            'pane_alpha': 0.2
        }
    }
    
    # Loop through each style
    for style_name, style_params in styles.items():
        # Generate timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        rcParams['figure.figsize'] = fig_size
        fig = plt.figure(f'Combined XOR Visualization - {style_params["name"]}', facecolor='white')
        fig.patch.set_facecolor('white')

        for i in range(len(json_files)):
            file_name = 'XORData/'+json_files[i]+'.json'
            with open(file_name, "r") as read_file:
                results = json.load(read_file)

            num_of_tests = len(results)

            #getting mean of convergence
            conv_count = 0
            neg_conv_count = 0
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

            # Six completely different tri-color schemes
            color_schemes = [
                {'conv': 'darkred', 'non_conv': 'darkblue', 'non_conv_exp': 'darkgreen'},
                {'conv': 'darkviolet', 'non_conv': 'darkorange', 'non_conv_exp': 'saddlebrown'},
                {'conv': 'deeppink', 'non_conv': 'darkcyan', 'non_conv_exp': 'black'},
                {'conv': 'gold', 'non_conv': 'darkmagenta', 'non_conv_exp': 'navy'},
                {'conv': 'limegreen', 'non_conv': 'orangered', 'non_conv_exp': 'dimgray'},
                {'conv': 'darkgoldenrod', 'non_conv': 'teal', 'non_conv_exp': 'maroon'}
            ]
            
            # Different panel background colors for each plot
            panel_backgrounds = [
                'lightcoral', 'lightsteelblue', 'lightgreen', 
                'lightyellow', 'lightpink', 'lightgray'
            ]
            
            # Different cube interior colors
            cube_colors = [
                'mistyrose', 'aliceblue', 'honeydew', 
                'ivory', 'lavenderblush', 'azure'
            ]
            
            # Viewing angles
            viewing_angles_init = [(14, -141), (24, -134), (11, -143)]
            viewing_angles_final = [(17, -147), (19, -143), (11, -143)]
            
            # INITIAL WEIGHTS - TOP ROW
            ax_init = fig.add_subplot(2, 3, i+1, projection='3d')
            
            init_plot_index = i
            init_color_scheme = color_schemes[init_plot_index]
            init_panel_bg = panel_backgrounds[init_plot_index]
            init_cube_bg = cube_colors[init_plot_index]
            init_angle = viewing_angles_init[i]
            
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
            
            # Remove numbers and labels for aesthetic focus
            ax_init.set_xticks([])
            ax_init.set_yticks([])
            ax_init.set_zticks([])
            ax_init.set_xlabel('')
            ax_init.set_ylabel('')
            ax_init.set_zlabel('')
            ax_init.set_title('')
            
            # Style axes based on current style parameters
            ax_init.xaxis.line.set_color((0.2, 0.2, 0.2, style_params['axis_alpha']))
            ax_init.yaxis.line.set_color((0.2, 0.2, 0.2, style_params['axis_alpha']))
            ax_init.zaxis.line.set_color((0.2, 0.2, 0.2, style_params['axis_alpha']))
            ax_init.xaxis.line.set_linewidth(style_params['axis_linewidth'])
            ax_init.yaxis.line.set_linewidth(style_params['axis_linewidth'])
            ax_init.zaxis.line.set_linewidth(style_params['axis_linewidth'])
            
            # Add grid based on style
            ax_init.grid(True, alpha=style_params['grid_alpha'], linewidth=style_params['grid_linewidth'])
            ax_init.set_facecolor(init_panel_bg)
            
            # Style panes
            ax_init.xaxis.pane.fill = True
            ax_init.yaxis.pane.fill = True
            ax_init.zaxis.pane.fill = True
            ax_init.xaxis.pane.set_facecolor(init_cube_bg)
            ax_init.yaxis.pane.set_facecolor(init_cube_bg)
            ax_init.zaxis.pane.set_facecolor(init_cube_bg)
            ax_init.xaxis.pane.set_edgecolor('gray')
            ax_init.yaxis.pane.set_edgecolor('gray')
            ax_init.zaxis.pane.set_edgecolor('gray')
            ax_init.xaxis.pane.set_alpha(style_params['pane_alpha'])
            ax_init.yaxis.pane.set_alpha(style_params['pane_alpha'])
            ax_init.zaxis.pane.set_alpha(style_params['pane_alpha'])
            
            # Add cube outline
            vertices = np.array([
                [-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0],
                [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
            ])
            
            faces = [
                [vertices[0], vertices[1], vertices[2], vertices[3]],  # bottom
                [vertices[4], vertices[5], vertices[6], vertices[7]],  # top
                [vertices[0], vertices[1], vertices[5], vertices[4]],  # front
                [vertices[2], vertices[3], vertices[7], vertices[6]],  # back
                [vertices[1], vertices[2], vertices[6], vertices[5]],  # right
                [vertices[0], vertices[3], vertices[7], vertices[4]]   # left
            ]
            
            poly3d = Poly3DCollection(faces, alpha=style_params['cube_alpha'], 
                                     facecolor=init_cube_bg, edgecolor='gray', 
                                     linewidth=style_params['cube_edge_linewidth'])
            ax_init.add_collection3d(poly3d)
            
            ax_init.view_init(elev=init_angle[0], azim=init_angle[1])

            # FINAL WEIGHTS - BOTTOM ROW
            ax_final = fig.add_subplot(2, 3, i+4, projection='3d')
            
            final_plot_index = i + 3
            final_color_scheme = color_schemes[final_plot_index]
            final_panel_bg = panel_backgrounds[final_plot_index]
            final_cube_bg = cube_colors[final_plot_index]
            final_angle = viewing_angles_final[i]
            
            conv_colors_final = final_color_scheme['conv']
            non_conv_colors_final = final_color_scheme['non_conv']
            non_conv_but_expctd_colors_final = final_color_scheme['non_conv_exp']
            
            # Same scatter plot logic for final weights
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
            
            # Same styling for final plots
            ax_final.set_xticks([])
            ax_final.set_yticks([])
            ax_final.set_zticks([])
            ax_final.set_xlabel('')
            ax_final.set_ylabel('')
            ax_final.set_zlabel('')
            ax_final.set_title('')
            
            ax_final.xaxis.line.set_color((0.2, 0.2, 0.2, style_params['axis_alpha']))
            ax_final.yaxis.line.set_color((0.2, 0.2, 0.2, style_params['axis_alpha']))
            ax_final.zaxis.line.set_color((0.2, 0.2, 0.2, style_params['axis_alpha']))
            ax_final.xaxis.line.set_linewidth(style_params['axis_linewidth'])
            ax_final.yaxis.line.set_linewidth(style_params['axis_linewidth'])
            ax_final.zaxis.line.set_linewidth(style_params['axis_linewidth'])
            
            ax_final.grid(True, alpha=style_params['grid_alpha'], linewidth=style_params['grid_linewidth'])
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
            ax_final.xaxis.pane.set_alpha(style_params['pane_alpha'])
            ax_final.yaxis.pane.set_alpha(style_params['pane_alpha'])
            ax_final.zaxis.pane.set_alpha(style_params['pane_alpha'])
            
            poly3d_final = Poly3DCollection(faces, alpha=style_params['cube_alpha'], 
                                           facecolor=final_cube_bg, edgecolor='gray', 
                                           linewidth=style_params['cube_edge_linewidth'])
            ax_final.add_collection3d(poly3d_final)
            
            ax_final.view_init(elev=final_angle[0], azim=final_angle[1])
        
        plt.subplots_adjust(left = 0.0, right = 1.0, top = 1.0, bottom = 0.0, wspace = 0.0, hspace = -0.3)

        # Save the timestamped figure
        figure_filename = f'figures_output/XOR_{style_name}_{timestamp}.png'
        try:
            plt.savefig(figure_filename, dpi=300, bbox_inches='tight', facecolor='white')
            print(f"Saved figure: {figure_filename}")
        except Exception as e:
            print(f"Error saving figure: {e}")
        
        # Save parameters used for this visualization
        parameters = {
            'timestamp': timestamp,
            'style': style_name,
            'style_params': style_params,
            'json_files': json_files,
            'epochs': epochs,
            'fig_size': fig_size
        }
        
        parameters_filename = f'parameters_output/XOR_{style_name}_parameters_{timestamp}.json'
        try:
            with open(parameters_filename, 'w') as param_file:
                json.dump(parameters, param_file, indent=2)
            print(f"Saved parameters: {parameters_filename}")
        except Exception as e:
            print(f"Error saving parameters: {e}")
        
        # Close the figure to avoid blocking and free memory
        plt.close(fig)
    
    return 

files = ['W_test_161','just_location1','both']
create_combined_scatter_plots(files, fig_size = (7.5,6.))