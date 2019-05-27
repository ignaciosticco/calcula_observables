'''
This script process the configuration and pressure values of each pedestrian and
puts the values into a grid representing the room  
'''
import pylab
import numpy as np
import math

######################### PARAMETER #########################
begin_corridor = 0.0
end_corridor =  27.0
wall_up = 24.0  
wall_down = 0.0
lenght_x = end_corridor-begin_corridor
lenght_y = wall_up-wall_down
#############################################################   



######################## Functions ######################## 

def extract_config(data,n):
     '''
     n is the number of pedestrians in the room
     this function extracts the configuration when the room has n pedestrians
     only one timestep is extracted
     '''
     str_n='{}\n'.format(n)
     f=open(data, 'r')
     lines=f.readlines()
     index=[]
     x=[]
     y=[]
     vx=[]
     vy=[]
     diameter=[]
     i=0
     flag=True
     while i<len(lines) and flag:
          line = lines[i].rstrip('\n')
          if(line=='ITEM: NUMBER OF ATOMS'):
               number_pedestrians=lines[i+1]
               if(number_pedestrians==str_n):
                    number_pedestrians=int(number_pedestrians)
                    first_line_table=i+7
                    for j in range(first_line_table, first_line_table+number_pedestrians):
                         row=lines[j].split(' ')
                         index+=[int(row[0])]
                         x+=[float(row[1])]
                         y+=[float(row[2])]
                         vx+=[float(row[3])]
                         vy+=[float(row[4])]
                         diameter+=[float(row[5])]
                    flag=False
          i+=1
     f.close()
     if i==len(lines):
     	print("\nERROR: Number of pedestrians not found. Try a different number of pedestrians\n")
     	exit()
     return index,x,y,vx,vy,diameter


def extract_observable(data,n):
     '''
     n is the number of pedestrians in the room
     this function extracts the observables (pressure, work of friction) when the room has n pedestrians
     only one timestep is extracted
     '''
     str_n='{}'.format(n)
     f=open(data, 'r')
     lines=f.readlines()
     index=[]
     pressure=[]
     friction_work=[]
     i=0
     flag=True
     while i<len(lines) and flag:
          line = lines[i].rstrip('\n')  
          if(line=='Cantidad de peatones = {} '.format(str_n)):
               number_pedestrians= int(str_n)
               first_line_table=i+2
               for j in range(first_line_table, first_line_table+number_pedestrians):
                    row=lines[j].split(' ')
                    index+=[int(row[0])]
                    friction_work+=[float(row[1])]
                    pressure+=[float(row[2])]
               flag=False
          i+=1
     f.close()
     return index,friction_work,pressure


def normaliza_por_n(grid_presion,grid_N):
     '''
     Esta funcion divide el valor de cada celda por la cantidad de peatones de cada celda. 
     '''	
     for i in range(0,len(grid_presion)):
          for j in range(0,len(grid_presion[0])):
               if grid_N[i,j] != 0:
                    grid_presion[i,j]= float(grid_presion[i,j])/float(grid_N[i,j])
               else:
                    grid_presion[i,j]=0.0
     return grid_presion



########################  MAIN  ########################
def main():
     '''
     Create matrices with X Y and average pressure per person per 1 square meter
     '''

     ################## IMPORTATION ################## 

     data_config = input("Enter configurations file name:\n")
     data_observables = input("Enter file with observables:\n") 
     numer_of_pedestrians = input("Enter number of pedestrians:\n")
     output_file_name = input("Enter output file name:\n")

     index2,x,y,vx,vy,diameter=extract_config(data_config,numer_of_pedestrians)
     index1,friction_work,presion = extract_observable(data_observables,numer_of_pedestrians)
     ################################################# 

     grid_x = np.linspace(begin_corridor,end_corridor,end_corridor-begin_corridor)
     grid_y = np.linspace(wall_down,wall_up,wall_up-wall_down)

     grid_presion = np.zeros((len(grid_y),len(grid_x)))
     grid_N = np.zeros((len(grid_y),len(grid_x)))

     for i in range(0,len(presion)):
          col=int((x[i]-begin_corridor)/(lenght_x)*(len(grid_x)))
          fil = int((y[i]-wall_down)/(lenght_y)*(len(grid_y)))
          grid_presion[fil][col] += presion[i]
          grid_N[fil][col] += 1

     grid_presion = normaliza_por_n(grid_presion,grid_N)
     np.savetxt('{}'.format(output_file_name), grid_presion,fmt='%3.3f') 


if __name__=='__main__':
     main()
