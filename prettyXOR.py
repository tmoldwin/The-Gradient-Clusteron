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
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
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
            'has_grid': False,
            'dark_mode': True
        },
        'electric_grid': {
            'name': 'ElectricGrid',
            'palette': 'electric',
            'has_grid': True,
            'grid_density': 6,
            'grid_alpha': 0.5,
            'grid_linewidth': 0.7,
            'dark_mode': True
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
    styles_to_run = ['electric']
    
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
        dark_mode = style_params.get('dark_mode', False)
        print(f"Generating {style_params['name']} with back grid only..." + (" [dark mode]" if dark_mode else ""))
        
        rcParams['figure.figsize'] = (12.5, 10.0)
        fig_bg = '#000000' if dark_mode else 'white'
        fig = plt.figure(f'XOR - {style_params["name"]}', facecolor=fig_bg)
        fig.patch.set_facecolor(fig_bg)
        # GridSpec: top/bottom rows (dendrites) less tall; first/last columns (dendrites) even thinner
        gs = GridSpec(4, 5, figure=fig, height_ratios=[0.45, 1.2, 1.2, 0.45], width_ratios=[0.35, 1.2, 1.2, 1.2, 0.35], hspace=0, wspace=0)
        
        palette = palettes[style_params['palette']]
        color_schemes = palette['color_schemes']
        panel_backgrounds = palette['panel_backgrounds']
        cube_colors = palette['cube_colors']
        
        viewing_angles_init = [(14, -141), (24, -134), (11, -143)]
        viewing_angles_final = [(17, -147), (19, -143), (11, -143)]
        
        # Generate random synapse positions for all dendrite examples
        np.random.seed(42)  # For reproducible randomization
        dendrite_configs = []
        
        # Define subtle color palette with very light gray variations
        subtle_colors = [
            '#FEFEFE',  # Almost white
            '#FDFDFD',  # Almost white
            '#FCFCFC',  # Almost white
            '#FBFBFB',  # Almost white
            '#FAFAFA',  # Almost white
            '#F9F9F9',  # Almost white
            '#F8F8F8',  # Very light gray
            '#F7F7F7',  # Very light gray
            '#F6F6F6',  # Very light gray
            '#F5F5F5',  # White smoke
            '#F4F4F4',  # Very light gray
            '#F3F3F3'   # Very light gray
        ]
        
        def calculate_panel_color(syn1_pos, syn2_pos, syn1_color, syn2_color, panel_name=""):
            """
            Calculate panel background color based on synapse distance and color similarity.
            Light mode: white for far/different, subtle gray for close/same.
            Dark mode: always black (no grays).
            """
            if dark_mode:
                # Dendrite panels in dark mode should be pure black only
                print(f"Panel {panel_name}: BLACK (dark_mode forced)")
                return '#000000'

            distance = abs(syn1_pos - syn2_pos)
            same_color = syn1_color == syn2_color
            if distance < 2.0 and same_color:
                gray_variations = ['#E0E0E0', '#D8D8D8', '#D0D0D0', '#C8C8C8']
                gray_index = hash(panel_name) % len(gray_variations)
                gray_color = gray_variations[gray_index]
                print(f"Panel {panel_name}: GRAY {gray_color} (distance={distance:.2f}, same_color={same_color})")
                return gray_color
            else:
                print(f"Panel {panel_name}: WHITE (distance={distance:.2f}, same_color={same_color})")
                return 'white'
        
        def get_synapse_color_with_intensity(base_color, intensity_factor=1.0):
            """
            Get synapse color with intensity variation.
            intensity_factor: 0.5-1.5 for lighter to darker variations
            """
            if base_color == 'red':
                # Red variations from light to dark
                red_intensities = ['#FFB6C1', '#FF69B4', '#FF1493', '#DC143C', '#B22222']
                idx = min(int(intensity_factor * 4), 4)
                return red_intensities[idx]
            elif base_color == 'blue':
                # Blue variations from light to dark
                blue_intensities = ['#ADD8E6', '#87CEEB', '#4169E1', '#0000CD', '#000080']
                idx = min(int(intensity_factor * 4), 4)
                return blue_intensities[idx]
            else:
                return base_color
        
        # Define specific configurations for gray panels at r1c1, r1c3, r2c5, r3c1, r4c3, r4c5
        # Map to actual dendrite positions: [1,2,3,4,5, 6,10, 11,15, 16,17,18,19,20]
        # Position mapping: r1c1=1, r1c3=3, r2c5=10, r3c1=11, r4c3=18, r4c5=20
        specific_configs = [
            # Position 1 (r1c1): GRAY
            {'pos1': 3.0, 'pos2': 4.5, 'syn1_color': 'red', 'syn2_color': 'red'},
            # Position 2 (r1c2): WHITE
            {'pos1': 2.0, 'pos2': 6.0, 'syn1_color': 'red', 'syn2_color': 'blue'},
            # Position 3 (r1c3): GRAY
            {'pos1': 3.2, 'pos2': 4.8, 'syn1_color': 'blue', 'syn2_color': 'blue'},
            # Position 4 (r1c4): WHITE
            {'pos1': 3.5, 'pos2': 6.5, 'syn1_color': 'red', 'syn2_color': 'blue'},
            # Position 5 (r1c5): WHITE
            {'pos1': 4.0, 'pos2': 6.0, 'syn1_color': 'blue', 'syn2_color': 'red'},
            # Position 6 (r2c1): WHITE
            {'pos1': 2.8, 'pos2': 6.2, 'syn1_color': 'red', 'syn2_color': 'blue'},
            # Position 10 (r2c5): GRAY (keep original)
            {'pos1': 3.1, 'pos2': 4.9, 'syn1_color': 'red', 'syn2_color': 'red'},
            # Position 11 (r3c1): GRAY (keep original)
            {'pos1': 3.2, 'pos2': 4.8, 'syn1_color': 'blue', 'syn2_color': 'blue'},
            # Position 15 (r3c5): WHITE
            {'pos1': 3.5, 'pos2': 6.5, 'syn1_color': 'red', 'syn2_color': 'blue'},
            # Position 16 (r4c1): WHITE
            {'pos1': 2.9, 'pos2': 6.1, 'syn1_color': 'red', 'syn2_color': 'blue'},
            # Position 17 (r4c2): WHITE
            {'pos1': 3.4, 'pos2': 6.2, 'syn1_color': 'red', 'syn2_color': 'blue'},
            # Position 18 (r4c3): GRAY
            {'pos1': 2.6, 'pos2': 4.4, 'syn1_color': 'blue', 'syn2_color': 'blue'},
            # Position 19 (r4c4): WHITE
            {'pos1': 3.7, 'pos2': 6.3, 'syn1_color': 'blue', 'syn2_color': 'red'},
            # Position 20 (r4c5): GRAY
            {'pos1': 3.3, 'pos2': 4.7, 'syn1_color': 'blue', 'syn2_color': 'blue'},
        ]
        
        for i in range(20):  # 20 dendrite examples total
            if i < len(specific_configs):
                config = specific_configs[i]
                pos1 = config['pos1']
                pos2 = config['pos2']
                syn1_color = config['syn1_color']
                syn2_color = config['syn2_color']
            else:
                # Fallback to random for any additional positions
                pos1 = np.random.uniform(2.5, 7.5)
                pos2 = np.random.uniform(2.5, 7.5)
                while abs(pos1 - pos2) < 1.0:
                    pos2 = np.random.uniform(2.5, 7.5)
                syn1_color = np.random.choice(['red', 'blue'])
                syn2_color = np.random.choice(['red', 'blue'])
            
            # Generate intensity factors for color variation
            syn1_intensity = np.random.uniform(0.5, 1.5)
            syn2_intensity = np.random.uniform(0.5, 1.5)
            
            dendrite_configs.append({
                'syn1_color': syn1_color, 
                'syn2_color': syn2_color, 
                'pos1': pos1, 
                'pos2': pos2,
                'syn1_intensity': syn1_intensity,
                'syn2_intensity': syn2_intensity
            })
        
        # PANEL LAYOUT MAPPING:
        # Top row (positions 1-5): All dendrites
        # Middle rows: Dendrites on sides + 3D plots in center
        #   Row 2: dendrite(6), 3D(7,8,9), dendrite(10)  
        #   Row 3: dendrite(11), 3D(12,13,14), dendrite(15)
        # Bottom row (positions 16-20): All dendrites
        
        # ALL DENDRITE PANELS: positions 1-5, 6, 10, 11, 15, 16-20
        print("=== ALL DENDRITE PANELS ===")
        dendrite_positions = [1,2,3,4,5, 6,10, 11,15, 16,17,18,19,20]
        # Mapping from dendrite_positions to specific_configs indices
        config_mapping = [0,1,2,3,4, 5,6, 7,8, 9,10,11,12,13]
        
        # Dendrite border color (white on dark panels in dark_mode, else from palette)
        dendrite_border_color = '#FFFFFF' if dark_mode else palette.get('grid_color', '#888888')
        for i, panel_num in enumerate(dendrite_positions):
            row, col = (panel_num - 1) // 5, (panel_num - 1) % 5
            ax_dendrite = fig.add_subplot(gs[row, col])
            ax_dendrite.set_xlim(0, 10)
            ax_dendrite.set_ylim(0, 10)
            # Turn axes on but hide ticks/labels; borders are drawn at figure-level
            ax_dendrite.set_xticks([])
            ax_dendrite.set_yticks([])
            for spine_name in ['top', 'right', 'bottom', 'left']:
                ax_dendrite.spines[spine_name].set_visible(False)
                ax_dendrite.spines[spine_name].set_linewidth(0.0)
                ax_dendrite.spines[spine_name].set_alpha(0.0)
            
            config = dendrite_configs[config_mapping[i]]
            print(f"Config {config_mapping[i]}: pos1={config['pos1']:.2f}, pos2={config['pos2']:.2f}, syn1={config['syn1_color']}, syn2={config['syn2_color']}")
            
            # Calculate panel color based on synapse distance and colors
            panel_color = calculate_panel_color(config['pos1'], config['pos2'], 
                                              config['syn1_color'], config['syn2_color'], f"Panel-{panel_num}")
            ax_dendrite.set_facecolor(panel_color)
            dendrite_color = 'w-' if dark_mode else 'k-'
            branch_color = 'w-' if dark_mode else 'k-'
            vertical = (col == 0 or col == 4)  # first/last column: orient dendrite vertically
            
            syn1_color_with_intensity = get_synapse_color_with_intensity(
                config['syn1_color'], config['syn1_intensity'])
            syn2_color_with_intensity = get_synapse_color_with_intensity(
                config['syn2_color'], config['syn2_intensity'])
            
            if vertical:
                # Main dendrite vertical (x=5, y from 2 to 8); synapses branch left/right
                ax_dendrite.plot([5, 5], [2, 8], dendrite_color, linewidth=2)
                ax_dendrite.plot([5, 3], [config['pos1'], config['pos1']], branch_color, linewidth=1.5)
                ax_dendrite.plot(3, config['pos1'], 'o', color=syn1_color_with_intensity, markersize=8)
                ax_dendrite.plot([5, 7], [config['pos2'], config['pos2']], branch_color, linewidth=1.5)
                ax_dendrite.plot(7, config['pos2'], 'o', color=syn2_color_with_intensity, markersize=8)
            else:
                # Main dendrite horizontal (y=5); synapses branch up/down
                ax_dendrite.plot([2, 8], [5, 5], dendrite_color, linewidth=2)
                ax_dendrite.plot([config['pos1'], config['pos1']], [5, 3], branch_color, linewidth=1.5)
                ax_dendrite.plot(config['pos1'], 3, 'o', color=syn1_color_with_intensity, markersize=8)
                ax_dendrite.plot([config['pos2'], config['pos2']], [5, 7], branch_color, linewidth=1.5)
                ax_dendrite.plot(config['pos2'], 7, 'o', color=syn2_color_with_intensity, markersize=8)

        # CENTER 3D PLOTS: positions 7,8,9,12,13,14 (middle of rows 2&3)
        print("=== CENTER 3D PLOTS ===")
        plot_positions = [7,8,9,12,13,14]
        
        for i, panel_num in enumerate(plot_positions):
            file_name = f'XOR/XORData/{json_files[i % len(json_files)]}.json'
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
            
            # Create 3D plot
            row, col = (panel_num - 1) // 5, (panel_num - 1) % 5
            ax_init = fig.add_subplot(gs[row, col], projection='3d')
            
            color_scheme = color_schemes[i % len(color_schemes)]
            panel_bg = panel_backgrounds[i % len(panel_backgrounds)]
            cube_bg = cube_colors[i % len(cube_colors)]
            
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
            # Remove outer frame/spines for 3D panels (avoid double borders)
            try:
                ax_init.patch.set_facecolor(panel_bg)
                ax_init.patch.set_alpha(1.0)
                ax_init.patch.set_edgecolor((0, 0, 0, 0))
                ax_init.patch.set_linewidth(0.0)
            except Exception:
                pass
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
            
            ax_init.view_init(elev=viewing_angles_init[i % len(viewing_angles_init)][0], azim=viewing_angles_init[i % len(viewing_angles_init)][1])
            
        
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)

        # Draw borders/separators once at the figure level (prevents "double spines")
        def _fig_line(x0, y0, x1, y1, lw=1.0):
            fig.add_artist(Line2D([x0, x1], [y0, y1],
                                  transform=fig.transFigure,
                                  color=dendrite_border_color,
                                  linewidth=lw,
                                  solid_capstyle='butt',
                                  antialiased=True))

        row_boxes = [gs[r, 0].get_position(fig) for r in range(4)]
        col_boxes = [gs[0, c].get_position(fig) for c in range(5)]

        left = col_boxes[0].x0
        right = col_boxes[4].x1
        top = row_boxes[0].y1
        bottom = row_boxes[3].y0

        # Outer border
        _fig_line(left, top, right, top)
        _fig_line(left, bottom, right, bottom)
        _fig_line(left, bottom, left, top)
        _fig_line(right, bottom, right, top)

        # Horizontal separators: between top dendrite row and middle, and between middle and bottom dendrite row
        y_01 = row_boxes[0].y0
        y_23 = row_boxes[2].y0
        _fig_line(left, y_01, right, y_01)
        _fig_line(left, y_23, right, y_23)

        # Column boundaries (x at right edge of col c)
        x_01 = col_boxes[0].x1
        x_12 = col_boxes[1].x1
        x_23 = col_boxes[2].x1
        x_34 = col_boxes[3].x1

        # Top row: separators between all dendrite panels
        y0_top, y1_top = row_boxes[0].y0, row_boxes[0].y1
        for x in (x_01, x_12, x_23, x_34):
            _fig_line(x, y0_top, x, y1_top)

        # Bottom row: separators between all dendrite panels
        y0_bot, y1_bot = row_boxes[3].y0, row_boxes[3].y1
        for x in (x_01, x_12, x_23, x_34):
            _fig_line(x, y0_bot, x, y1_bot)

        # Middle rows: ONLY the inner spines for column dendrites
        # - first column right boundary (col0|col1)
        # - last column left boundary (col3|col4)
        y0_mid = row_boxes[2].y0
        y1_mid = row_boxes[1].y1
        _fig_line(x_01, y0_mid, x_01, y1_mid)
        _fig_line(x_34, y0_mid, x_34, y1_mid)
        
        # Print final panel summary
        print("\n=== FINAL PANEL SUMMARY ===")
        print("Top Row: 1 gray, 4 white")
        print("Left Column: 1 gray, 1 white") 
        print("Right Column: 1 gray, 1 white")
        print("Bottom Row: 1 gray, 4 white")
        print("Total: 4 gray panels, 10 white panels")
        
        # Save figure
        figure_filename = f'XOR/figures_output/XOR_{style_name}.png'
        plt.savefig(figure_filename, dpi=300, bbox_inches='tight', pad_inches=0, facecolor=fig_bg)
        print(f"Saved: {figure_filename}")
        
        # Save as PDF
        pdf_filename = f'XOR/figures_output/XOR_{style_name}.pdf'
        plt.savefig(pdf_filename, bbox_inches='tight', pad_inches=0, facecolor=fig_bg)
        print(f"Saved: {pdf_filename}")
        
        plt.close(fig)

if __name__ == "__main__":
    create_plots()
