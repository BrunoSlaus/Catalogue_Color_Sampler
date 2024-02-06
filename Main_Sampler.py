# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Created on Sun Jul 16 2017

DESCRIPTION: Merger code.

Code Author: Bruno Slaus
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import numpy as np
import astropy
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM (H0 = 70, Om0 = 0.3)
from astropy.constants import M_sun
##############################################################################################
#   User defined parameters:                                                                 #
##############################################################################################
Catalogue_Name_AGN  = 'AGN_Catalogue.fits'
Catalogue_Name_Full = 'Full_Catalogue.fits'

#Redshift bins file
Zbins_Name = 'Redshift_Subsets.txt'

#Column Naames
Nuvr_Column     = "Color"
Rlum_Column     = "Luminosity_Real"
Redshift_Column = "Redshift_Real" 

N_Color_Bins = 10
##############################################################################################
print('**************************************************')
print('Starting code') 
print('**************************************************\n')

Data_AGN  = fits.open('Input/' + Catalogue_Name_AGN)[1].data    #Opening the data with astropy
Data_Full = fits.open('Input/' + Catalogue_Name_Full)[1].data    #Opening the data with astropy
Zbins = np.loadtxt('Input/' + Zbins_Name)


Output_Length = 0
Full_Subset_Output = np.array([])
for zbin in Zbins:
    print(zbin)
    
    AGN_Z_Subset = Data_AGN[Data_AGN[Redshift_Column] >  zbin[0]]
    AGN_Z_Subset = AGN_Z_Subset[AGN_Z_Subset[Redshift_Column] < zbin[1]]

    Full_Z_Subset = Data_Full[Data_Full[Redshift_Column] >  zbin[0]]
    Full_Z_Subset = Full_Z_Subset[Full_Z_Subset[Redshift_Column] < zbin[1]]

    #print('Z-subsets len', len(AGN_Z_Subset), len(Full_Z_Subset))

    AGN_Color_Min = np.amin(AGN_Z_Subset[Nuvr_Column])
    AGN_Color_Max = np.amax(AGN_Z_Subset[Nuvr_Column])
    print('AGN colours range: ', AGN_Color_Min, AGN_Color_Max)
    color_width   =  (AGN_Color_Max - AGN_Color_Min) / N_Color_Bins 



    for c in range(N_Color_Bins):
    
        color_low_edge  = AGN_Color_Min + c*color_width
        color_high_edge = AGN_Color_Min + (c+1)*color_width
        
        if c == (N_Color_Bins-1):
            color_high_edge = AGN_Color_Max
                
            AGN_Subset = AGN_Z_Subset[AGN_Z_Subset[Nuvr_Column] >=  color_low_edge]
            AGN_Subset = AGN_Subset[AGN_Subset[Nuvr_Column] <= color_high_edge]

            Full_Subset = Full_Z_Subset[Full_Z_Subset[Nuvr_Column] >=  color_low_edge]
            Full_Subset = Full_Subset[Full_Subset[Nuvr_Column] <= color_high_edge]       

        else:                
            AGN_Subset = AGN_Z_Subset[AGN_Z_Subset[Nuvr_Column] >=  color_low_edge]
            AGN_Subset = AGN_Subset[AGN_Subset[Nuvr_Column] < color_high_edge]

            Full_Subset = Full_Z_Subset[Full_Z_Subset[Nuvr_Column] >=  color_low_edge]
            Full_Subset = Full_Subset[Full_Subset[Nuvr_Column] < color_high_edge]   
            
            
            
        AGN_Source_N = len(AGN_Subset)
        Full_Subset = np.random.choice(Full_Subset,AGN_Source_N,replace=False)
        #print(Full_Subset)
        #print(np.array(Full_Subset))  
        #print(AGN_Source_N, len(Full_Subset))      

        #print(color_low_edge, color_high_edge, AGN_Color_Max, AGN_Source_N , len(Full_Subset))
        #print(Full_Subset)

        
        try:
            Full_Subset_Output = np.append([Full_Subset_Output], [Full_Subset])
        except:
            Full_Subset_Output = Full_Subset
            #print('First loop iteration')

        Output_Length = Output_Length + len(Full_Subset)





c1 = fits.Column(name = 'ID_Real',            array = Full_Subset_Output['ID_Real'], format='f8')    #Adding a column
c2 = fits.Column(name = 'Redshift_Real',      array = Full_Subset_Output['Redshift_Real'], format='f8')    #Adding a column
c3 = fits.Column(name = 'Stellar_Mass',       array = Full_Subset_Output['Stellar_Mass'], format='f8')    #Adding a column
c4 = fits.Column(name = 'Flux_Real',          array = Full_Subset_Output['Flux_Real'], format='f8')    #Adding a column
c5 = fits.Column(name = 'Luminosity_Real',    array = Full_Subset_Output['Luminosity_Real'], format='f8')    #Adding a column
c6 = fits.Column(name = 'Alpha_Real',         array = Full_Subset_Output['Alpha_Real'], format='f8')    #Adding a column
c7 = fits.Column(name = 'Color',              array = Full_Subset_Output['Color'], format='f8')    #Adding a column
Output_Fits = fits.BinTableHDU.from_columns([c1, c2, c3, c4, c5, c6, c7])         #Creatng a fits file 
Output_Fits.writeto('Output/' + 'Sampled_Catalogue.fits', overwrite = 'True')


#print(Output_Length)
#Plotting histograms as check

histo_counter = 0
for zbin in Zbins:


    AGN_Z_Subset = Data_AGN[Data_AGN[Redshift_Column] >  zbin[0]]
    AGN_Z_Subset = AGN_Z_Subset[AGN_Z_Subset[Redshift_Column] < zbin[1]]
 
    AGN_Color_Min = np.amin(AGN_Z_Subset[Nuvr_Column])
    AGN_Color_Max = np.amax(AGN_Z_Subset[Nuvr_Column]) 
    
    Output_Fits_Subset = Full_Subset_Output[Full_Subset_Output[Redshift_Column] >  zbin[0]]
    Output_Fits_Subset = Output_Fits_Subset[Output_Fits_Subset[Redshift_Column] < zbin[1]]    

    print('Histogram summed numbers: ', len(AGN_Z_Subset), len(Output_Fits_Subset))

    plt.hist(AGN_Z_Subset[Nuvr_Column], label = 'AGN catalogu', bins=N_Color_Bins, range=(AGN_Color_Min, AGN_Color_Max), alpha = 0.5)
    plt.hist(Output_Fits_Subset[Nuvr_Column], label = 'Full Sampled catalogu', range=(AGN_Color_Min, AGN_Color_Max), histtype = 'step')
    plt.savefig('Output/Histogram_' + str(histo_counter) + '.png')
    plt.legend()
    plt.close()
    histo_counter = histo_counter + 1






##############################################################################################
### Modification history:
### 1)




