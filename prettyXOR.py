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
    
    # Define all color palettes with WITH GRID and WITHOUT GRID versions
    all_styles = {
        # PASTEL palette - with and without grid
        'pastel': {
            'name': 'Pastel',
            'palette': 'pastel',
            'has_grid': False
        },
        'pastel_grid': {
            'name': 'PastelGrid',
            'palette': 'pastel',
            'has_grid': True,
            'grid_density': 5,
            'grid_alpha': 0.4,
            'grid_linewidth': 0.8
        },
        
        # VIBRANT palette - with and without grid
        'vibrant': {
            'name': 'Vibrant',
            'palette': 'vibrant',
            'has_grid': False
        },
        'vibrant_grid': {
            'name': 'VibrantGrid',
            'palette': 'vibrant',
            'has_grid': True,
            'grid_density': 5,
            'grid_alpha': 0.6,
            'grid_linewidth': 1.2
        },
        
        # PROFESSIONAL palette - with and without grid
        'professional': {
            'name': 'Professional',
            'palette': 'professional',
            'has_grid': False
        },
        'professional_grid': {
            'name': 'ProfessionalGrid',
            'palette': 'professional',
            'has_grid': True,
            'grid_density': 6,
            'grid_alpha': 0.5,
            'grid_linewidth': 0.9
        },
        
        # ELECTRIC palette - with and without grid
        'electric': {
            'name': 'Electric',
            'palette': 'electric',
            'has_grid': False
        },
        'electric_grid': {
            'name': 'ElectricGrid',
            'palette': 'electric',
            'has_grid': True,
            'grid_density': 6,
            'grid_alpha': 0.5,
            'grid_linewidth': 0.7
        },
        
        # WARHOL palette - with and without grid
        'warhol': {
            'name': 'Warhol',
            'palette': 'warhol',
            'has_grid': False
        },
        'warhol_grid': {
            'name': 'WarholGrid',
            'palette': 'warhol',
            'has_grid': True,
            'grid_density': 5,
            'grid_alpha': 0.4,
            'grid_linewidth': 0.8
        },
        
        # BOLD palette - with and without grid
        'bold': {
            'name': 'Bold',
            'palette': 'bold',
            'has_grid': False
        },
        'bold_grid': {
            'name': 'BoldGrid',
            'palette': 'bold',
            'has_grid': True,
            'grid_density': 5,
            'grid_alpha': 0.7,
            'grid_linewidth': 1.3
        },
        
        # MUTED palette - with and without grid
        'muted': {
            'name': 'Muted',
            'palette': 'muted',
            'has_grid': False
        },
        'muted_grid': {
            'name': 'MutedGrid',
            'palette': 'muted',
            'has_grid': True,
            'grid_density': 6,
            'grid_alpha': 0.4,
            'grid_linewidth': 0.8
        }
    }
    
    # List of styles to run (all palettes with and without grids)
    styles_to_run = [
        'pastel', 'pastel_grid'
        # 'vibrant', 'vibrant_grid', 
        # 'professional', 'professional_grid',
        # 'electric', 'electric_grid',
        # 'warhol', 'warhol_grid',
        # 'bold', 'bold_grid',
        # 'muted', 'muted_grid'
    ]
    
    # Filter styles to only run the selected ones
    styles = {k: all_styles[k] for k in styles_to_run if k in all_styles}
    
    # All color palettes
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
            'panel_backgrounds': ['#F8F8FF', '#F5F5DC', '#F0F8FF', '#FFFAF0', '#FFF8DC', '#F5F5F5'],  # Very light panels
            'cube_colors': ['#E0E0E0', '#D8D8D8', '#E5E5E5', '#DDDDDD', '#E2E2E2', '#DADADA'],      # Medium gray cubes
            'grid_color': '#333333'  # Dark grid for light backgrounds
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
            'panel_backgrounds': ['#2D0000', '#000040', '#001A00', '#2D1A00', '#1A0040', '#404000'],  # Much darker panels
            'cube_colors': ['#CC6666', '#6666CC', '#66CC66', '#CC9966', '#9966CC', '#CCCC66'],      # Much brighter cubes
            'grid_color': '#FFFFFF'  # White grid for dark backgrounds
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
            'panel_backgrounds': ['#F0F0F0', '#E8E8E8', '#F5F5F5', '#EEEEEE', '#F2F2F2', '#EBEBEB'],  # Light gray panels
            'cube_colors': ['#CCCCCC', '#C0C0C0', '#D3D3D3', '#C8C8C8', '#D0D0D0', '#C5C5C5'],      # Darker gray cubes
            'grid_color': '#666666'  # Medium gray grid for light backgrounds
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
            'cube_colors': ['#1A1A1A', '#151515', '#121212', '#181818', '#0F0F0F', '#1C1C1C'],
            'grid_color': '#FFFFFF'  # White grid for black backgrounds
        },
        'warhol': {
            'color_schemes': [
                {'conv': '#8B4513', 'non_conv': '#4169E1', 'non_conv_exp': '#32CD32'},  # Brown, blue, lime - top left panel
                {'conv': '#8A2BE2', 'non_conv': '#FF8C00', 'non_conv_exp': '#FFD700'},  # Purple, orange, gold - top center panel
                {'conv': '#FF1493', 'non_conv': '#32CD32', 'non_conv_exp': '#000000'},  # Hot pink, lime, black - top right panel
                {'conv': '#DAA520', 'non_conv': '#8A2BE2', 'non_conv_exp': '#FF69B4'},  # Gold, purple, pink - bottom left panel
                {'conv': '#DC143C', 'non_conv': '#32CD32', 'non_conv_exp': '#FF1493'},  # Crimson, lime, hot pink - bottom center panel
                {'conv': '#B8860B', 'non_conv': '#8B0000', 'non_conv_exp': '#4169E1'}   # Dark gold, dark red, blue - bottom right panel
            ],
            'panel_backgrounds': ['#FF7F7F', '#9BB3E0', '#90EE90', '#F5F5DC', '#FFB6C1', '#D3D3D3'],  # Exact original Warhol colors
            'cube_colors': ['#E6E6E6', '#F0F0F0', '#E8E8E8', '#F8F8F8', '#EFEFEF', '#EBEBEB'],      # Light gray cubes for contrast
            'grid_color': '#666666'  # Medium gray grid that works on all backgrounds
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
            'panel_backgrounds': ['#1A0000', '#000020', '#001A00', '#1A0F00', '#1A001A', '#0F1A00'],  # Much darker panels
            'cube_colors': ['#FF6666', '#6666FF', '#66FF66', '#FF9966', '#FF66FF', '#99FF66'],      # Much brighter cubes
            'grid_color': '#CCCCCC'  # Light gray grid for dark colored backgrounds
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
            'cube_colors': ['#FAEBD7', '#F8F8FF', '#F5FFFA', '#FFFACD', '#FFEBCD', '#F0FFFF'],
            'grid_color': '#444444'  # Dark gray grid for light muted backgrounds
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
            file_name = f'XOR/XORData/{json_files[i]}.json'
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
            
            # Add back grid only if specified
            if style_params.get('has_grid', False):
                create_back_grid(ax_init, (-1, 1), (-1, 1), (0, 1),
                               grid_density=style_params['grid_density'],
                               color=palette['grid_color'],
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
            
            # Add back grid only if specified
            if style_params.get('has_grid', False):
                create_back_grid(ax_final, (-1, 1), (-1, 1), (0, 1),
                               grid_density=style_params['grid_density'],
                               color=palette['grid_color'],
                               alpha=style_params['grid_alpha'],
                               linewidth=style_params['grid_linewidth'])
            
            ax_final.view_init(elev=viewing_angles_final[i][0], azim=viewing_angles_final[i][1])
        
        plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0, wspace=0.0, hspace=-0.3)
        
        # Save figure
        figure_filename = f'XOR/figures_output/XOR_{style_name}.png'
        plt.savefig(figure_filename, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Saved: {figure_filename}")
        plt.close(fig)

if __name__ == "__main__":
    create_plots()
