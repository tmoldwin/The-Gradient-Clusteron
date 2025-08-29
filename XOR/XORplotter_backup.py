'''
XOR plotter for data in json files - Multiple Aesthetic Styles Version
Shows both initial and final weights using different aesthetic styles for axes and grid lines
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
import matplotlib.patches as patches
from matplotlib import cm
import pprint 
import json
from pylab import rcParams
from datetime import datetime

fig_folder = path_parent 
fignum = 6

def create_face_grids(ax, xlim, ylim, zlim, grid_density=5, color='gray', alpha=0.3, linewidth=0.8):
    """Create grid lines on the front and back faces of the cube boundary"""
    x_vals = np.linspace(xlim[0], xlim[1], grid_density)
    z_vals = np.linspace(zlim[0], zlim[1], grid_density)
    
    lines = []
    
    # Front face (y = ylim[0])
    for x in x_vals:
        line = [(x, ylim[0], zlim[0]), (x, ylim[0], zlim[1])]
        lines.append(line)
    for z in z_vals:
        line = [(xlim[0], ylim[0], z), (xlim[1], ylim[0], z)]
        lines.append(line)
    
    # Back face (y = ylim[1])
    for x in x_vals:
        line = [(x, ylim[1], zlim[0]), (x, ylim[1], zlim[1])]
        lines.append(line)
    for z in z_vals:
        line = [(xlim[0], ylim[1], z), (xlim[1], ylim[1], z)]
        lines.append(line)
    
    # Add the grid lines to the plot
    line_collection = Line3DCollection(lines, colors=color, alpha=alpha, linewidth=linewidth)
    ax.add_collection3d(line_collection)

def create_combined_scatter_plots(json_files,epochs=10000,fig_size = (7.5,6.)):
    
    # Define different aesthetic styles
    all_styles = {
        'minimal': {
            'name': 'Minimal',
            'axis_linewidth': 0.5,
            'axis_alpha': 0.3,
            'grid_alpha': 0.05,
            'grid_linewidth': 0.3,
            'cube_alpha': 0.05,
            'cube_edge_alpha': 0.2,
            'cube_edge_linewidth': 0.3,
            'pane_alpha': 0.1,
            'palette': 'pastel',
            'full_grid': False
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
            'pane_alpha': 0.8,
            'palette': 'vibrant',
            'full_grid': False
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
            'pane_alpha': 0.6,
            'palette': 'professional',
            'full_grid': False
        },
        'full_grid_neon': {
            'name': 'FullGridNeon',
            'axis_linewidth': 0.8,
            'axis_alpha': 0.6,
            'grid_alpha': 0.0,  # Turn off default grid
            'grid_linewidth': 0.6,
            'cube_alpha': 0.05,
            'cube_edge_alpha': 1.0,
            'cube_edge_linewidth': 2.5,
            'pane_alpha': 0.1,
            'palette': 'electric',
            'full_grid': True,
            'full_grid_alpha': 0.4,
            'full_grid_linewidth': 0.6,
            'full_grid_density': 6
        },
        'full_grid_bold': {
            'name': 'FullGridBold',
            'axis_linewidth': 3,
            'axis_alpha': 1.0,
            'grid_alpha': 0.0,  # Turn off default grid
            'grid_linewidth': 1.5,
            'cube_alpha': 0.2,
            'cube_edge_alpha': 0.9,
            'cube_edge_linewidth': 2,
            'pane_alpha': 0.3,
            'palette': 'bold',
            'full_grid': True,
            'full_grid_alpha': 0.6,
            'full_grid_linewidth': 1.0,
            'full_grid_density': 5
        },
        'full_grid_subtle': {
            'name': 'FullGridSubtle',
            'axis_linewidth': 1.0,
            'axis_alpha': 0.5,
            'grid_alpha': 0.0,  # Turn off default grid
            'grid_linewidth': 0.5,
            'cube_alpha': 0.08,
            'cube_edge_alpha': 0.3,
            'cube_edge_linewidth': 1,
            'pane_alpha': 0.2,
            'palette': 'muted',
            'full_grid': True,
            'full_grid_alpha': 0.2,
            'full_grid_linewidth': 0.4,
            'full_grid_density': 7
        },
        'wireframe_dense': {
            'name': 'WireframeDense',
            'axis_linewidth': 0.5,
            'axis_alpha': 0.4,
            'grid_alpha': 0.0,  # Turn off default grid
            'grid_linewidth': 0.4,
            'cube_alpha': 0.02,
            'cube_edge_alpha': 0.8,
            'cube_edge_linewidth': 1.8,
            'pane_alpha': 0.05,
            'palette': 'professional',
            'full_grid': True,
            'full_grid_alpha': 0.3,
            'full_grid_linewidth': 0.3,
            'full_grid_density': 8
        }
    }
    
    # List of styles to actually run (you can modify this list)
    styles_to_run = [
        'minimal',
        'bold', 
        'clean',
        'full_grid_neon',
        'full_grid_bold',
        'full_grid_subtle',
        'wireframe_dense'
    ]
    
    # Filter styles to only run the selected ones
    styles = {k: all_styles[k] for k in styles_to_run if k in all_styles}
    
    # Define color palettes based on style
    palettes = {
        'pastel': {
            'color_schemes': [
                {'conv': '#8B4B8A', 'non_conv': '#5B7C99', 'non_conv_exp': '#6B8B3D'},
                {'conv': '#A0522D', 'non_conv': '#CD853F', 'non_conv_exp': '#708090'},
                {'conv': '#B22222', 'non_conv': '#4682B4', 'non_conv_exp': '#2F4F4F'},
                {'conv': '#DAA520', 'non_conv': '#9932CC', 'non_conv_exp': '#191970'},
                {'conv': '#228B22', 'non_conv': '#FF6347', 'non_conv_exp': '#696969'},
                {'conv': '#B8860B', 'non_conv': '#008B8B', 'non_conv_exp': '#800000'}
            ],
            'panel_backgrounds': ['#F8F8FF', '#F5F5DC', '#F0F8FF', '#FFFAF0', '#FFF8DC', '#F5F5F5'],
            'cube_colors': ['#FAFAFA', '#FEFEFE', '#FDFDFD', '#FCFCFC', '#FBFBFB', '#F9F9F9']
        },
        'vibrant': {
            'color_schemes': [
                {'conv': '#FF1493', 'non_conv': '#00CED1', 'non_conv_exp': '#32CD32'},
                {'conv': '#FF4500', 'non_conv': '#8A2BE2', 'non_conv_exp': '#FFD700'},
                {'conv': '#DC143C', 'non_conv': '#4169E1', 'non_conv_exp': '#228B22'},
                {'conv': '#FF6347', 'non_conv': '#9370DB', 'non_conv_exp': '#FF8C00'},
                {'conv': '#00FF7F', 'non_conv': '#FF1493', 'non_conv_exp': '#4682B4'},
                {'conv': '#FFD700', 'non_conv': '#DC143C', 'non_conv_exp': '#8B008B'}
            ],
            'panel_backgrounds': ['#8B0000', '#000080', '#006400', '#8B4513', '#4B0082', '#B8860B'],
            'cube_colors': ['#A52A2A', '#191970', '#228B22', '#D2691E', '#663399', '#DAA520']
        },
        'professional': {
            'color_schemes': [
                {'conv': '#2E86AB', 'non_conv': '#A23B72', 'non_conv_exp': '#F18F01'},
                {'conv': '#6A994E', 'non_conv': '#BC4749', 'non_conv_exp': '#F2E8CF'},
                {'conv': '#264653', 'non_conv': '#E76F51', 'non_conv_exp': '#F4A261'},
                {'conv': '#7209B7', 'non_conv': '#F72585', 'non_conv_exp': '#4361EE'},
                {'conv': '#F72585', 'non_conv': '#4CC9F0', 'non_conv_exp': '#7209B7'},
                {'conv': '#FF6B35', 'non_conv': '#004E89', 'non_conv_exp': '#1A936F'}
            ],
            'panel_backgrounds': ['#FAFAFA', '#F5F5F5', '#FFFFFF', '#F8F9FA', '#FDFDFD', '#F7F7F7'],
            'cube_colors': ['#E8E8E8', '#EEEEEE', '#F0F0F0', '#EDEDED', '#EBEBEB', '#E9E9E9']
        },
        'dreamy': {
            'color_schemes': [
                {'conv': '#E6B3FF', 'non_conv': '#B3E6FF', 'non_conv_exp': '#FFE6B3'},
                {'conv': '#FFB3E6', 'non_conv': '#B3FFE6', 'non_conv_exp': '#E6FFB3'},
                {'conv': '#D1B3FF', 'non_conv': '#FFD1B3', 'non_conv_exp': '#B3FFD1'},
                {'conv': '#B3D1FF', 'non_conv': '#FFB3D1', 'non_conv_exp': '#D1FFB3'},
                {'conv': '#FFCCB3', 'non_conv': '#B3CCFF', 'non_conv_exp': '#CCFFB3'},
                {'conv': '#E6CCFF', 'non_conv': '#CCFFE6', 'non_conv_exp': '#FFCCE6'}
            ],
            'panel_backgrounds': ['#F0E6FF', '#E6F0FF', '#FFF0E6', '#E6FFF0', '#FFE6F0', '#F0FFE6'],
            'cube_colors': ['#F8F0FF', '#F0F8FF', '#FFF8F0', '#F0FFF8', '#FFF0F8', '#F8FFF0']
        },
        'neon': {
            'color_schemes': [
                {'conv': '#00FFFF', 'non_conv': '#FF00FF', 'non_conv_exp': '#FFFF00'},
                {'conv': '#00FF00', 'non_conv': '#FF0080', 'non_conv_exp': '#8000FF'},
                {'conv': '#FF4000', 'non_conv': '#00FF80', 'non_conv_exp': '#4080FF'},
                {'conv': '#FFFF00', 'non_conv': '#FF0040', 'non_conv_exp': '#40FF00'},
                {'conv': '#FF8000', 'non_conv': '#0080FF', 'non_conv_exp': '#FF0080'},
                {'conv': '#80FF00', 'non_conv': '#8000FF', 'non_conv_exp': '#FF8000'}
            ],
            'panel_backgrounds': ['#1A0D1A', '#0D1A1A', '#1A1A0D', '#0D1A0D', '#1A0D0D', '#0D0D1A'],
            'cube_colors': ['#2A1A2A', '#1A2A2A', '#2A2A1A', '#1A2A1A', '#2A1A1A', '#1A1A2A']
        },
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
    
    # Loop through each style
    for style_name, style_params in styles.items():
        print(f"Generating {style_params['name']} style...")
    
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

            # Select palette based on style
            current_palette = palettes[style_params['palette']]
            color_schemes = current_palette['color_schemes']
            panel_backgrounds = current_palette['panel_backgrounds']
            cube_colors = current_palette['cube_colors']
            
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
            
            # Add face grids if specified
            if style_params.get('full_grid', False):
                create_face_grids(ax_init, (-1, 1), (-1, 1), (0, 1), 
                                grid_density=style_params.get('full_grid_density', 5),
                                color='white', 
                                alpha=style_params.get('full_grid_alpha', 0.3),
                                linewidth=style_params.get('full_grid_linewidth', 0.6))
            
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
            
            # Add face grids if specified
            if style_params.get('full_grid', False):
                create_face_grids(ax_final, (-1, 1), (-1, 1), (0, 1), 
                                grid_density=style_params.get('full_grid_density', 5),
                                color='white', 
                                alpha=style_params.get('full_grid_alpha', 0.3),
                                linewidth=style_params.get('full_grid_linewidth', 0.6))
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

        # Save the figure
        figure_filename = f'figures_output/XOR_{style_name}.png'
    try:
        plt.savefig(figure_filename, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Saved figure: {figure_filename}")
    except Exception as e:
        print(f"Error saving figure: {e}")
    
    # Save parameters used for this visualization
    parameters = {
            'style': style_name,
            'style_params': style_params,
        'json_files': json_files,
        'epochs': epochs,
            'fig_size': fig_size
        }
        
        parameters_filename = f'parameters_output/XOR_{style_name}_parameters.json'
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