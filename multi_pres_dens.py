'''
Takes multiple files: config and observables. Loops over the files in order to
calculate the pressure and density for each desired velocity.
Calls another python script to do the calculation of density and pressure. 
Outputs a table of avg density and pressure for each pair of inputs (config and observ)
'''
import process_avg_pres_density as modulo
import sys

def main():

	for vd in range(4,5):
		config_file = "config_vd{}_kix10_kwx10".format(vd)
		observables_file = "observables_vd{}_kix10_kwx10.txt".format(vd)
		output_file = "avg_pres_dens_vd{}_kix10_kwx10".format(vd)

		modulo.main(config_file, observables_file, output_file) 

if __name__=='__main__':
     main()
