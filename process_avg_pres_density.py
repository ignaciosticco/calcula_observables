'''
This script process the configuration and pressure values of each pedestrian and
outputs the number of pedestrians in the room, the avg pressure, max pressure,
avg density and max density. The pressure is not normalized by the surface.   
'''
import pylab
import numpy as np
import math
import pandas as pd

######################### PARAMETER #########################
begin_corridor = 0.0
end_corridor =  27.0
wall_up = 24.0  
wall_down = 0.0
lenght_x = end_corridor-begin_corridor
lenght_y = wall_up-wall_down
#############################################################   



######################## Functions ######################## 


def calculate_density(data):
     '''
     this function extracts the configuration for each timestep
     and calculates de mean density and max density for each timestep
     '''
     #str_n='{}\n'.format(n)
     f=open(data, 'r')
     lines=f.readlines()
     i=0
     mean_density = []
     max_density = []
     while i<len(lines):
          line = lines[i].rstrip('\n')
          if(line=='ITEM: NUMBER OF ATOMS'):
               index=[]
               x=[]
               y=[]
               n=int(lines[i+1])
               first_line_table=i+7
               for j in range(first_line_table, first_line_table+n):
                    row=lines[j].split(' ')
                    index+=[int(row[0])]
                    x+=[float(row[1])]
                    y+=[float(row[2])]
               density_matrix = create_density_matrx(x,y)
               density_matrix[density_matrix == 0] = np.nan
               mean_density += [np.nanmean(density_matrix)]
               max_density += [int(np.nanmax(density_matrix))]
          i+=1
     f.close()
     return mean_density,max_density


def calculate_pressure(data):
     '''
     this function extracts the observables (pressure)
     for every timestep returns a table with time, number pedestrians
     avg pressure, max pressure
     '''
     f=open(data, 'r')
     lines=f.readlines()
     number_pedestrians = []
     time = []
     avg_pressure = []
     max_pressure = []
     i=0
     while i<len(lines):
          index=[]
          pressure=[]
          friction_work=[]
          line = lines[i].rstrip('\n')
          first_str = line.split(" ")[0] # first word of the line 
          if(first_str=="Cantidad"):
               n= int(line.split(" ")[4]) # n = number of pedestrians 
               if n>0:
                    t = lines[i+1].split(' ')[2] 
                    first_line_table=i+2
                    for j in range(first_line_table, first_line_table+n):
                         row=lines[j].split(' ')
                         index+=[int(row[0])]
                         friction_work+=[float(row[1])]
                         pressure+=[float(row[2])]
                    number_pedestrians += [n]
                    time += [t]
                    avg_pressure += [np.mean(pressure)]
                    max_pressure += [np.max(pressure)]
          i+=1
     f.close()
     return time,number_pedestrians,avg_pressure,max_pressure

def create_density_matrx(x,y):
     grid_x = np.linspace(begin_corridor,end_corridor,end_corridor-begin_corridor)
     grid_y = np.linspace(wall_down,wall_up,wall_up-wall_down)
     density_matrix = np.zeros((len(grid_y),len(grid_x)))

     for i in range(0,len(x)):
          col=int((x[i]-begin_corridor)/(lenght_x)*(len(grid_x)))
          fil = int((y[i]-wall_down)/(lenght_y)*(len(grid_y)))
          density_matrix[fil][col] += 1
     return density_matrix



########################  MAIN  ########################
def main():
     '''
     Create matrices with X Y and average pressure per person per 1 square meter
     '''

     ################## IMPORTATION ################## 

     data_config = input("Enter configurations file name:\n")
     data_observables = input("Enter file with observables:\n") 
     output_file_name = input("Enter output file name:\n")
     mean_density,max_density = calculate_density(data_config)
     time,number_pedestrians,avg_pressure,max_pressure = calculate_pressure(data_observables)

     ################################################# 
     d = {'time': time,
          'number_pedestrians':number_pedestrians,
          'avg_pressure':np.round(avg_pressure,2),
          'max_pressure': np.round(max_pressure,2),
          'max_density': np.round(max_density,2),
          'mean_density': np.round(mean_density,2),
          }
     df = pd.DataFrame(data=d)
     df.to_csv("{}".format(output_file_name), sep='\t',index = False
    ,columns=["time","number_pedestrians","avg_pressure","max_pressure","max_density","mean_density"])

if __name__=='__main__':
     main()
