'''
XOR plotter - Back Grid Only Version
'''
import os
import sys
path_parent = os.path.dirname(os.getcwd())
sys.path.insert(0,path_parent)
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import json
from pylab import rcParams

def create_back_grid(ax, xlim, ylim, zlim, grid_density=5, color='white', alpha=0.3, linewidth=0.8):
    """Create grid lines on exactly 3 faces: back face, right face, and bottom face"""
    x_vals = np.linspace(xlim[0], xlim[1], grid_density)
    y_vals = np.linspace(ylim[0], ylim[1], grid_density)
    z_vals = np.linspace(zlim[0], zlim[1], grid_density)
    
    lines = []
    
    # Back face (y = ylim[1])
    for x in x_vals:
        line = [(x, ylim[1], zlim[0]), (x, ylim[1], zlim[1])]
        lines.append(line)
    for z in z_vals:
        line = [(xlim[0], ylim[1], z), (xlim[1], ylim[1], z)]
        lines.append(line)
    
    # Right face (x = xlim[1])
    for y in y_vals:
        line = [(xlim[1], y, zlim[0]), (xlim[1], y, zlim[1])]
        lines.append(line)
    for z in z_vals:
        line = [(xlim[1], ylim[0], z), (xlim[1], ylim[1], z)]
        lines.append(line)
    
    # Bottom face (z = zlim[0])
    for x in x_vals:
        line = [(x, ylim[0], zlim[0]), (x, ylim[1], zlim[0])]
        lines.append(line)
    for y in y_vals:
        line = [(xlim[0], y, zlim[0]), (xlim[1], y, zlim[0])]
        lines.append(line)
    
    line_collection = Line3DCollection(lines, colors=color, alpha=alpha, linewidth=linewidth)
    ax.add_collection3d(line_collection)

def create_plots():
    json_files = ['W_test_161','just_location1','both']
    
    # Define the grid styles to regenerate
    styles = {
        'full_grid_neon': {
            'name': 'FullGridNeon',
            'palette': 'electric',
            'grid_density': 6,
            'grid_alpha': 0.4,
            'grid_linewidth': 0.6
        },
        'full_grid_bold': {
            'name': 'FullGridBold', 
            'palette': 'bold',
            'grid_density': 5,
            'grid_alpha': 0.6,
            'grid_linewidth': 1.0
        },
        'full_grid_subtle': {
            'name': 'FullGridSubtle',
            'palette': 'muted',
            'grid_density': 7,
            'grid_alpha': 0.2,
            'grid_linewidth': 0.4
        }
    }
    
    # Color palettes
    palettes = {
        'electric': {
            'color_schemes': [
                {'conv': '#00FFFF', 'non_conv': '#FF00FF', 'non_conv_exp': '#FFFF00'},
                {'conv': '#FF0080', 'non_conv': '#80FF00', 'non_conv_exp': '#0080FF'},
                {'conv': '#8000FF', 'non_conv': '#FF8000', 'non_conv_exp': '#00FF80'},
                {'conv': '#FF4080', 'non_conv': '#40FF80', 'non_conv_exp': '#8040FF'},
                {'conv': '#80FF40', 'non_conv': '#FF4080', 'non_conv_exp': '#4080FF'},
                {'conv': '#FF8040', 'non_conv': '#40FF40', 'non_conv_exp': '#8080FF'}
            ],
            'panel_backgrounds': ['#000000', '#0A0A0A', '#050505', '#080808', '#030303', '#0C0C0C'],
            'cube_colors': ['#1A1A1A', '#151515', '#121212', '#181818', '#0F0F0F', '#1C1C1C']
        },
        'bold': {
            'color_schemes': [
                {'conv': '#FF0000', 'non_conv': '#0000FF', 'non_conv_exp': '#00FF00'},
                {'conv': '#FF8000', 'non_conv': '#8000FF', 'non_conv_exp': '#00FF80'},
                {'conv': '#FF0080', 'non_conv': '#0080FF', 'non_conv_exp': '#80FF00'},
                {'conv': '#FF4000', 'non_conv': '#4000FF', 'non_conv_exp': '#00FF40'},
                {'conv': '#FF6000', 'non_conv': '#6000FF', 'non_conv_exp': '#00FF60'},
                {'conv': '#FF2000', 'non_conv': '#2000FF', 'non_conv_exp': '#00FF20'}
            ],
            'panel_backgrounds': ['#800000', '#000080', '#008000', '#804000', '#800080', '#408000'],
            'cube_colors': ['#A00000', '#0000A0', '#00A000', '#A05000', '#A000A0', '#50A000']
        },
        'muted': {
            'color_schemes': [
                {'conv': '#8B7355', 'non_conv': '#556B8B', 'non_conv_exp': '#738B55'},
                {'conv': '#8B5A73', 'non_conv': '#5A8B73', 'non_conv_exp': '#8B735A'},
                {'conv': '#8B6B55', 'non_conv': '#558B6B', 'non_conv_exp': '#6B8B55'},
                {'conv': '#8B5555', 'non_conv': '#558B8B', 'non_conv_exp': '#8B8B55'},
                {'conv': '#8B7D55', 'non_conv': '#558B7D', 'non_conv_exp': '#7D8B55'},
                {'conv': '#8B5573', 'non_conv': '#738B55', 'non_conv_exp': '#558B73'}
            ],
            'panel_backgrounds': ['#F5F5DC', '#E6E6FA', '#F0FFF0', '#FFF8DC', '#FFE4E1', '#F0F8FF'],
            'cube_colors': ['#FAEBD7', '#F8F8FF', '#F5FFFA', '#FFFACD', '#FFEBCD', '#F0FFFF']
        }
    }
    
    for style_name, style_params in styles.items():
        print(f"Generating {style_params['name']} with back grid only...")
        
        rcParams['figure.figsize'] = (7.5, 6.0)
        fig = plt.figure(f'XOR - {style_params["name"]}', facecolor='white')
        fig.patch.set_facecolor('white')
        
        palette = palettes[style_params['palette']]
        color_schemes = palette['color_schemes']
        panel_backgrounds = palette['panel_backgrounds']
        cube_colors = palette['cube_colors']
        
        viewing_angles_init = [(14, -141), (24, -134), (11, -143)]
        viewing_angles_final = [(17, -147), (19, -143), (11, -143)]
        
        for i in range(len(json_files)):
            file_name = f'XORData/{json_files[i]}.json'
            with open(file_name, "r") as read_file:
                results = json.load(read_file)
            
            # Process data
            list_of_convergences = [0 if result['convergence'] == -1 else 1 for result in results]
            list_of_expectations = [result['expected to converge'] for result in results]
            conv_indices = np.where(list_of_convergences)
            non_conv_indices_unexp = np.where([1 if list_of_convergences[ind] == 0 and list_of_expectations[ind] == 1 else 0 for ind in range(len(list_of_convergences))])[0]
            non_conv_but_expctd_indices = np.where([1 if list_of_convergences[ind] == 0 and list_of_expectations[ind] == 0 else 0 for ind in range(len(list_of_convergences))])[0]
            
            w1_init = np.array([result['initial weights'][0] for result in results])
            w1_final = np.array([result['final weights'][0] for result in results])
            w2_init = np.array([result['initial weights'][1] for result in results])
            w2_final = np.array([result['final weights'][1] for result in results])
            f_init = np.array([result['initial f'] for result in results])
            f_final = np.array([result['final f'] for result in results])
            
            # INITIAL WEIGHTS - TOP ROW
            ax_init = fig.add_subplot(2, 3, i+1, projection='3d')
            
            color_scheme = color_schemes[i]
            panel_bg = panel_backgrounds[i]
            cube_bg = cube_colors[i]
            
            # Plot points
            if len(conv_indices) > 0:
                mask = (w1_init[conv_indices] >= -1) & (w1_init[conv_indices] <= 1) & \
                       (w2_init[conv_indices] >= -1) & (w2_init[conv_indices] <= 1) & \
                       (f_init[conv_indices] >= 0) & (f_init[conv_indices] <= 1)
                ax_init.scatter(w1_init[conv_indices][mask], w2_init[conv_indices][mask],
                           f_init[conv_indices][mask], c=color_scheme['conv'], marker='o', s=10, alpha=1)
            
            if len(non_conv_indices_unexp) > 0:
                mask = (w1_init[non_conv_indices_unexp] >= -1) & (w1_init[non_conv_indices_unexp] <= 1) & \
                       (w2_init[non_conv_indices_unexp] >= -1) & (w2_init[non_conv_indices_unexp] <= 1) & \
                       (f_init[non_conv_indices_unexp] >= 0) & (f_init[non_conv_indices_unexp] <= 1)
                ax_init.scatter(w1_init[non_conv_indices_unexp][mask], w2_init[non_conv_indices_unexp][mask],
                           f_init[non_conv_indices_unexp][mask], edgecolor=color_scheme['non_conv_exp'],
                           facecolor=(0,0,0,0), marker='v', s=40)
            
            if len(non_conv_but_expctd_indices) > 0:
                mask = (w1_init[non_conv_but_expctd_indices] >= -1) & (w1_init[non_conv_but_expctd_indices] <= 1) & \
                       (w2_init[non_conv_but_expctd_indices] >= -1) & (w2_init[non_conv_but_expctd_indices] <= 1) & \
                       (f_init[non_conv_but_expctd_indices] >= 0) & (f_init[non_conv_but_expctd_indices] <= 1)
                ax_init.scatter(w1_init[non_conv_but_expctd_indices][mask], w2_init[non_conv_but_expctd_indices][mask],
                           f_init[non_conv_but_expctd_indices][mask], edgecolor=color_scheme['non_conv'],
                           facecolor=(0,0,0,0), marker='o', s=10)
            
            # Style the plot
            ax_init.set_zlim(0,1)
            ax_init.set_xlim(-1,1)
            ax_init.set_ylim(-1,1)
            ax_init.set_xticks([])
            ax_init.set_yticks([])
            ax_init.set_zticks([])
            ax_init.set_xlabel('')
            ax_init.set_ylabel('')
            ax_init.set_zlabel('')
            ax_init.set_title('')
            ax_init.grid(False)
            ax_init.set_facecolor(panel_bg)
            ax_init.xaxis.pane.fill = True
            ax_init.yaxis.pane.fill = True
            ax_init.zaxis.pane.fill = True
            ax_init.xaxis.pane.set_facecolor(cube_bg)
            ax_init.yaxis.pane.set_facecolor(cube_bg)
            ax_init.zaxis.pane.set_facecolor(cube_bg)
            ax_init.xaxis.pane.set_alpha(0.3)
            ax_init.yaxis.pane.set_alpha(0.3)
            ax_init.zaxis.pane.set_alpha(0.3)
            
            # Add back grid only
            create_back_grid(ax_init, (-1, 1), (-1, 1), (0, 1),
                           grid_density=style_params['grid_density'],
                           color='white',
                           alpha=style_params['grid_alpha'],
                           linewidth=style_params['grid_linewidth'])
            
            ax_init.view_init(elev=viewing_angles_init[i][0], azim=viewing_angles_init[i][1])
            
            # FINAL WEIGHTS - BOTTOM ROW
            ax_final = fig.add_subplot(2, 3, i+4, projection='3d')
            
            final_color_scheme = color_schemes[i + 3]
            final_panel_bg = panel_backgrounds[i + 3]
            final_cube_bg = cube_colors[i + 3]
            
            # Plot final points
            if len(conv_indices) > 0:
                mask = (w1_final[conv_indices] >= -1) & (w1_final[conv_indices] <= 1) & \
                       (w2_final[conv_indices] >= -1) & (w2_final[conv_indices] <= 1) & \
                       (f_final[conv_indices] >= 0) & (f_final[conv_indices] <= 1)
                ax_final.scatter(w1_final[conv_indices][mask], w2_final[conv_indices][mask],
                           f_final[conv_indices][mask], c=final_color_scheme['conv'], marker='o', s=10, alpha=1)
            
            if len(non_conv_indices_unexp) > 0:
                mask = (w1_final[non_conv_indices_unexp] >= -1) & (w1_final[non_conv_indices_unexp] <= 1) & \
                       (w2_final[non_conv_indices_unexp] >= -1) & (w2_final[non_conv_indices_unexp] <= 1) & \
                       (f_final[non_conv_indices_unexp] >= 0) & (f_final[non_conv_indices_unexp] <= 1)
                ax_final.scatter(w1_final[non_conv_indices_unexp][mask], w2_final[non_conv_indices_unexp][mask],
                           f_final[non_conv_indices_unexp][mask], edgecolor=final_color_scheme['non_conv_exp'],
                           facecolor=(0,0,0,0), marker='v', s=40)
            
            if len(non_conv_but_expctd_indices) > 0:
                mask = (w1_final[non_conv_but_expctd_indices] >= -1) & (w1_final[non_conv_but_expctd_indices] <= 1) & \
                       (w2_final[non_conv_but_expctd_indices] >= -1) & (w2_final[non_conv_but_expctd_indices] <= 1) & \
                       (f_final[non_conv_but_expctd_indices] >= 0) & (f_final[non_conv_but_expctd_indices] <= 1)
                ax_final.scatter(w1_final[non_conv_but_expctd_indices][mask], w2_final[non_conv_but_expctd_indices][mask],
                           f_final[non_conv_but_expctd_indices][mask], edgecolor=final_color_scheme['non_conv'],
                           facecolor=(0,0,0,0), marker='o', s=10)
            
            # Style final plot
            ax_final.set_zlim(0,1)
            ax_final.set_xlim(-1,1)
            ax_final.set_ylim(-1,1)
            ax_final.set_xticks([])
            ax_final.set_yticks([])
            ax_final.set_zticks([])
            ax_final.set_xlabel('')
            ax_final.set_ylabel('')
            ax_final.set_zlabel('')
            ax_final.set_title('')
            ax_final.grid(False)
            ax_final.set_facecolor(final_panel_bg)
            ax_final.xaxis.pane.fill = True
            ax_final.yaxis.pane.fill = True
            ax_final.zaxis.pane.fill = True
            ax_final.xaxis.pane.set_facecolor(final_cube_bg)
            ax_final.yaxis.pane.set_facecolor(final_cube_bg)
            ax_final.zaxis.pane.set_facecolor(final_cube_bg)
            ax_final.xaxis.pane.set_alpha(0.3)
            ax_final.yaxis.pane.set_alpha(0.3)
            ax_final.zaxis.pane.set_alpha(0.3)
            
            # Add back grid only
            create_back_grid(ax_final, (-1, 1), (-1, 1), (0, 1),
                           grid_density=style_params['grid_density'],
                           color='white',
                           alpha=style_params['grid_alpha'],
                           linewidth=style_params['grid_linewidth'])
            
            ax_final.view_init(elev=viewing_angles_final[i][0], azim=viewing_angles_final[i][1])
        
        plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0, wspace=0.0, hspace=-0.3)
        
        # Save figure
        figure_filename = f'figures_output/XOR_{style_name}.png'
        plt.savefig(figure_filename, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Saved: {figure_filename}")
        plt.close(fig)

if __name__ == "__main__":
    create_plots()
