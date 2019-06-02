/*
Input: Lammps configuration dump with: id x y vx vy diameter
Output: For each timestep, N, Wfg and pressure (helbing social force) for each pedestrian
*/
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <vector>
#include <string>
#include <math.h>
using namespace std;

#define INTEGRATION_STEP 0.0001
#define MASS 			 70.0
#define A 				 2000.0
#define B 				 0.08
#define MOT 			 140.0
#define KAPPA 			 240000.0

void escribir(int cantAtoms,double time,vector<int> &vector_id, vector<double> &observable_1, vector<double> &observable_2);
void calcula_presion(vector<double> &vector_x,vector<double> &vector_y,int cantAtoms,vector<double> &vector_presion,vector<double> &vector_diameter);
void calcula_work_desired_force(vector<double> &vector_x, vector<double> &vector_y,vector<double> &vector_pre_x, vector<double> &vector_pre_y,vector<double> &vector_vx,vector<double> &vector_vy,vector<double> &vector_pre_vx,vector<double> &vector_pre_vy,int cantAtoms,vector<double> &vector_w_desired,vector<int> &vector_id,vector<int> &vector_pre_id);
int esta_en(int id,vector<int> &vector_pre_id,int cantAtoms);
void calcula_work_granular_force(vector<double> &vector_x, vector<double> &vector_y,vector<double> &vector_pre_x, vector<double> &vector_pre_y,vector<double> &vector_vx,vector<double> &vector_vy,vector<double> &vector_pre_vx,vector<double> &vector_pre_vy, int cantAtoms,vector<double> &vector_w_granular,vector<int> &vector_id,vector<int> &vector_pre_id,vector<double> &vector_diameter);
void calcula_granular_force(vector<double> &vector_fg,vector<double> &vector_x, vector<double> &vector_y, vector<double> &vector_vx,vector<double> &vector_vy, int cantAtoms,vector<double> &vector_diameter,double id);

// Posiciones xy de los targets (hacia donde van los individuos). 
double x_door; 	  // posicion x de la puerta
double y_opening1;  // posicion y del target de abajo	
double y_opening2; // posicion y del target de arriba
double y_wall_down; // posicion de la pared inferior en y
double y_wall_up; // posicion de la pared superior en y
double vd = 1.0;
int cantAtoms_inicial;		

int main(int argc, char const *argv[]){

	string archivoDatos;
	double x,y,vx,vy,id,time,diameter;
	cout<<"Enter configuration file: "<<endl;	
	cin>>archivoDatos;
	
	y_wall_up=24.0;
	y_wall_down=0.0;
	x_door=27.0;
	cantAtoms_inicial=1300;
 
	y_opening1 = 10.8; //y_wall_down;
	y_opening2 = 13.2; //y_wall_up;

	//archivoDatos = "configuraciones.txt";

	string line;
	int cantAtoms, n_time,i;
	int iter=0;

	vector<int> vector_pre_id(cantAtoms_inicial, 0);	
	vector<double> vector_pre_x(cantAtoms_inicial, 0.0);
	vector<double> vector_pre_y(cantAtoms_inicial, 0.0);
	vector<double> vector_w_desired(cantAtoms_inicial, 0.0);
	vector<double> vector_w_granular(cantAtoms_inicial,0.0);
	vector<double> vector_pre_vx(cantAtoms_inicial, 0.0);
	vector<double> vector_pre_vy(cantAtoms_inicial, 0.0);

	ifstream fileIn(archivoDatos.c_str());
	while(fileIn.good()){
		getline(fileIn,line,'P');
		getline(fileIn,line,'I');
		n_time=atoi(line.c_str());
		time = n_time*INTEGRATION_STEP;
		getline(fileIn,line,'S');
		getline(fileIn,line,'I');
		cantAtoms=atoi(line.c_str());
		getline(fileIn,line,'y');
		getline(fileIn,line,'r');// ultima letra en tabla configuraciones es r (de diameter)
		getline(fileIn,line,' ');

		vector<int> vector_id;
		vector<double> vector_x;
		vector<double> vector_y;
		vector<double> vector_vx;
		vector<double> vector_vy;
		vector<double> vector_diameter;
		vector<double> vector_presion(cantAtoms, 0.0);


		i = 0;
		while(i<cantAtoms){		
			getline(fileIn,line,' ');
			id=atoi(line.c_str());
			getline(fileIn,line,' ');
			x=atof(line.c_str());
			getline(fileIn,line,' ');
			y=atof(line.c_str());
			getline(fileIn,line,' ');
			vx=atof(line.c_str());
			getline(fileIn,line,' ');
			vy=atof(line.c_str());
			getline(fileIn,line,' ');
			diameter=atof(line.c_str());
			vector_id.push_back(id);
			vector_x.push_back(x);
			vector_y.push_back(y);			
			vector_vx.push_back(vx);
			vector_vy.push_back(vy);	
			vector_diameter.push_back(diameter);		
			i++;
			
		}

		calcula_presion(vector_x, vector_y,cantAtoms,vector_presion,vector_diameter);
		
		//// Calculo de trabajos ////////
		if (iter>0){
			calcula_work_granular_force(vector_x, vector_y,vector_pre_x, vector_pre_y,vector_vx,vector_vy,vector_pre_vx,vector_pre_vy,cantAtoms,vector_w_granular,vector_id,vector_pre_id,vector_diameter);
		}	
		
		for (int i = 0; i < cantAtoms; ++i){
			vector_pre_id[i] = vector_id[i];
			vector_pre_x[i] = vector_x[i];
			vector_pre_y[i] = vector_y[i];
			vector_pre_vx[i] = vector_vx[i];
			vector_pre_vy[i] = vector_vy[i];
		}

		///////////////////////////////

		iter++;
		escribir(cantAtoms,time,vector_id,vector_w_granular,vector_presion);
	}


}


void calcula_work_granular_force(vector<double> &vector_x, vector<double> &vector_y,vector<double> &vector_pre_x, vector<double> &vector_pre_y,vector<double> &vector_vx,vector<double> &vector_vy,vector<double> &vector_pre_vx,vector<double> &vector_pre_vy, int cantAtoms,vector<double> &vector_w_granular,vector<int> &vector_id,vector<int> &vector_pre_id,vector<double> &vector_diameter){

	int    id, i_pre;
	double delx,dely,dfdx,dfdy;

	for (int i = 0; i < cantAtoms; ++i){
		id = vector_id[i];
		i_pre = esta_en(id,vector_pre_id,cantAtoms);  //Chekea si el atomo esta en el paso anterior		

		if (i_pre>-1){
			vector<double> vector_fg(2, 0.0); 	// vector fg de la particula i (2 componentes)
			vector<double> vector_pre_fg(2, 0.0);
			calcula_granular_force(vector_fg,vector_x, vector_y, vector_vx,vector_vy,cantAtoms,vector_diameter,i);
			calcula_granular_force(vector_pre_fg,vector_pre_x, vector_pre_y, vector_pre_vx,vector_pre_vy,cantAtoms,vector_diameter,i_pre);
			delx = vector_x[i] - vector_pre_x[i_pre];
			dely = vector_y[i] - vector_pre_y[i_pre];

			dfdx = vector_fg[0] + vector_pre_fg[0];
			dfdy = vector_fg[1] + vector_pre_fg[1];		
		}
		vector_w_granular[i] = 0.5*(delx*dfdx+dely*dfdy);
	}
}

void calcula_granular_force(vector<double> &vector_fg,vector<double> &vector_x, vector<double> &vector_y, vector<double> &vector_vx,vector<double> &vector_vy, int cantAtoms,vector<double> &vector_diameter,double id){

	double xi,yi,xj,yj,vxi,vyi,vxj,vyj,delx,dely,delvx,delvy,sum_rads,r,gpair,granular_factor,rsq;

	xi = vector_x[id];
	yi = vector_y[id];
	vxi = vector_vx[id];
	vyi = vector_vy[id];	
	int j = 0;
	while(j<cantAtoms){
		xj = vector_x[j];
		yj = vector_y[j];
		vxj = vector_vx[j];
		vyj = vector_vy[j];		
		delx = xi-xj;
		dely = yi-yj;
		delvx = vxi - vxj;
		delvy = vyi - vyj;		
		sum_rads = (vector_diameter[id]+vector_diameter[j])/2.0;
		rsq = delx*delx+dely*dely;

		if (rsq<(sum_rads*sum_rads) && rsq>0.0 ){
			r = sqrt(rsq);	
			gpair = sum_rads - r;
			granular_factor = KAPPA*gpair*(dely*delvx-delx*delvy)/rsq; 
	      	vector_fg[0] +=- granular_factor*dely; 
	      	vector_fg[1] += granular_factor*delx;
		}
		j++;
	}
	//// Calculo del rozamiento con las paredes (paredes horizontales-pasillo-) ///
	if (yi > y_wall_up-vector_diameter[id]/2.0){
	    vector_fg[0] +=- KAPPA*vxi*(vector_diameter[id]/2.0-(y_wall_up-yi));
	    vector_fg[1] += 0.0;		
	}
	if (yi < y_wall_down+vector_diameter[id]/2.0){
	   	vector_fg[0] +=- KAPPA*vxi*(vector_diameter[id]/2.0-(yi-y_wall_down)); 
	   	vector_fg[1] += 0.0;		
	}
}


void escribir(int cantAtoms,double time,vector<int> &vector_id ,vector<double> &observable_1,vector<double> &observable_2){
	
	FILE *fp;
	fp=fopen("output_observables.txt","a");
	fprintf(fp,"Cantidad de peatones = %i \n",cantAtoms);
	fprintf(fp,"tiempo = %lg \n",time);
	for (int i = 0; i < cantAtoms; ++i){
		fprintf(fp,"%i %.2f %.2f \n",vector_id[i],observable_1[i],observable_2[i]);
	}
	fclose(fp);
}


int esta_en(int id,vector<int> &vector_pre_id,int cantAtoms){
	/*
	Esta funcion encuentra el indice del vector_id previo tal que su id coincide
	con el id del de la particula a la que se le quiere calcular el trabajo. 
	*/

	int i=0;
	int i_pre = -1;
	while(i<cantAtoms && (id !=vector_pre_id[i])){
		i++; 	
	}
	if(i<cantAtoms){
		i_pre = i; 
	}
	else if (i==cantAtoms && id ==vector_pre_id[i]){
		i_pre=i;
	} 
	else{
		i_pre = -1;
	}
	return i_pre;
}


void calcula_presion(vector<double> &vector_x,vector<double> &vector_y,int cantAtoms,vector<double> &vector_presion,vector<double> &vector_diameter){
	/*
	Calcula la presion de compresion de cada individuo. El output es un vector
	de presiones (cada elemento corresponde a un individuo). 
	*/
	double xi,xj,yi,yj,dist2,fs,r,sum_rads,delx,dely;
	int    j;
	for (int i = 0; i < cantAtoms; ++i){
		xi = vector_x[i];
		yi = vector_y[i];
		j = i+1;
		while(j<cantAtoms){
			xj = vector_x[j];
			yj = vector_y[j];
			delx = xi-xj;
			dely = yi-yj;	
			sum_rads = (vector_diameter[i]+vector_diameter[j])/2.0;
			dist2 = delx*delx+dely*dely;
			if (dist2<sum_rads*sum_rads){
				r = sqrt(dist2);	
				fs = A*exp((sum_rads-r)/B) - A;
				vector_presion[i] += fs; 
				vector_presion[j] += fs; 
			}
			j++;
		}
	}
}