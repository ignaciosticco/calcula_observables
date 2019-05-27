'''
This script plots the pressure map of a room with pedestrians. 

Source: https://scipy.github.io/old-wiki/pages/Cookbook/Matplotlib/LaTeX_Examples.html
'''
import pylab
import numpy as np
import matplotlib.pyplot as plt
import math

# a dos columnas: 3+3/8 (ancho, in)
# a una columna : 6.5   (ancho  in)

golden_mean = (math.sqrt(5)-1.0)/2.0        # Aesthetic ratio
fig_width = 3+3/8 			    			# width  in inches
fig_height = fig_width*golden_mean          # height in inches
fig_size =  [fig_width,fig_height]

params = {'backend': 'ps',
          'axes.titlesize': 8,
          'axes.labelsize': 9,
          'axes.linewidth': 0.5, 
          'axes.grid': True,
          'axes.labelweight': 'normal',  
          'font.family': 'serif',
          'font.size': 8.0,
          'font.weight': 'normal',
          'text.color': 'black',
          'xtick.labelsize': 8,
          'ytick.labelsize': 8,
          'text.usetex': True,
          'legend.fontsize': 8,
          'figure.dpi': 300,
          'figure.figsize': fig_size,
          'savefig.dpi': 600,
         }

pylab.rcParams.update(params)

def main():
	######################### PARAMETERS #########################
	'''
	This parameters are for a room like the Club Kiss.
	Change the values whenever simulate a different layout
	'''
	begin_corridor = 0.0
	end_corridor =  27.0
	wall_up = 24.0  
	wall_down = 0.0
	lenght_x = end_corridor-begin_corridor
	lenght_y = wall_up-wall_down
	#############################################################   

	input_file_name = input("Enter input file name:\n")
	output_file_name = input("Enter output file name:\n")

	grid_presion = np.genfromtxt("{}".format(input_file_name),delimiter=' ',dtype=float)

	grid_x = np.linspace(begin_corridor,end_corridor,end_corridor-begin_corridor)
	grid_y = np.linspace(wall_down,wall_up,wall_up-wall_down)

	levels=np.linspace(0,np.max(grid_presion),70,endpoint=True)
	levbar=np.linspace(0,np.max(grid_presion),7,endpoint=True)
	plt.contourf(grid_x,grid_y,grid_presion, levels, cmap=plt.cm.jet,zorder=1)
	plt.colorbar(ticks=levbar)
	#cb = plt.colorbar()
	#cb.ax.set_yticklabels(cb.ax.get_yticklabels(), fontsize=12)
	plt.grid(False)
	plt.xlabel('$x$-location~(m)',fontsize=10)
	plt.ylabel('$y$-location~(m)',fontsize=10)
	plt.yticks(np.linspace(0,wall_up,4), fontsize=10)
	plt.xticks(fontsize=10)
	plt.xlim(20,27)
	pylab.savefig('{}.png'.format(output_file_name), bbox_inches='tight')

if __name__=='__main__':
	main()