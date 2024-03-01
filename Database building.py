# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 10:40:36 2023

@author: loren
"""

import mario
import pandas as pd
import os
import numpy as np
from mario import slicer

user = "DG"
sN = slice(None)

paths = 'Paths.xlsx'

#%% Importing Exiobase with VA

exio_hybrid_path = pd.read_excel(paths, index_col=[0]).loc['EXIOBASE Hybrid SUT',user]
exio_hybrid_base = mario.parse_from_txt(exio_hybrid_path+"\\flows",table='SUT',mode='flows')
                     
#%% Aggregating regions and electricity

#exio_hybrid_base.get_aggregation_excel('Aggregation regions and electricity.xlsx')
exio_hybrid_base.aggregate('Aggregations\Aggregation regions and electricity_filled.xlsx', ignore_nan=True)

export_path = "\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Aggregations\\Regions and electricity"
exio_hybrid_base.to_txt(export_path)


#%% CREATION OF TWO SEPARATED SECTORS FOR IRON AND BLAST FURNACE GAS/OXYGEN STEEL FURNACE GAS
#%% Importing aggregated database

import_path = "\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Aggregations\\Regions and electricity"
exio_hybrid_base = mario.parse_from_txt(import_path+"\\flows",table='SUT',mode='flows')

#%% Splitting Manufacture of basic iron into two sectors: "Manufacture of basic iron" and "Blast furnace gas production"

#exio_hybrid_base.get_add_sectors_excel(path='Split manufacture of basic iron sector.xlsx', new_sectors=['Blast furnace gas production'], regions=['EU27', 'China', 'USA', 'India', 'Russia', 'RoW'], item='Activity',)
exio_hybrid_base.add_sectors('Add_sectors\Split manufacture of basic iron sector_filled.xlsx', new_sectors=['Blast furnace gas production'], regions=['EU27', 'China', 'USA', 'India', 'Russia', 'RoW'], item='Activity',)

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Splitted manufacture of basic iron" 
exio_hybrid_base.to_txt(export_path, coefficients=True, flows=False)
                                                                                                                        
#%% Making coefficients of "Blast furnace gas production" equal to those of "Manufacture of basic iron"

import_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Splitted manufacture of basic iron\\coefficients" 
exio_hybrid_base = mario.parse_from_txt(path=import_path, table='SUT', mode='coefficients') 

z_new = exio_hybrid_base.get_data(matrices=['z'], scenarios=['baseline'])['baseline'][0]
e_new = exio_hybrid_base.get_data(matrices=['e'], scenarios=['baseline'])['baseline'][0]
v_new = exio_hybrid_base.get_data(matrices=['v'], scenarios=['baseline'])['baseline'][0]

regions_to_update = ['EU27', 'China', 'India', 'USA', 'Russia', 'RoW']

for region in regions_to_update:
    z_new.loc(axis=1)[region, 'Activity', 'Blast furnace gas production'] = z_new.loc(axis=1)[region, 'Activity', 'Manufacture of basic iron and steel and of ferro-alloys and first products thereof']
    e_new.loc(axis=1)[region, 'Activity', 'Blast furnace gas production'] = e_new.loc(axis=1)[region, 'Activity', 'Manufacture of basic iron and steel and of ferro-alloys and first products thereof'] 
    v_new.loc(axis=1)[region, 'Activity', 'Blast furnace gas production'] = v_new.loc(axis=1)[region, 'Activity', 'Manufacture of basic iron and steel and of ferro-alloys and first products thereof'] 

exio_hybrid_base.update_scenarios(scenario='baseline',z=z_new, e=e_new, v=v_new)
exio_hybrid_base.reset_to_coefficients('baseline')

#%% Implementing changes on emissions of "Blast furnace gas production" and "Manufacture of basic iron"

exio_hybrid_base.clone_scenario(scenario='baseline', name='new emissions',)

regions_to_update = ['EU27', 'China', 'India', 'USA', 'Russia', 'RoW']

for region in regions_to_update:
    
    # null emissions for "Blast furnace gas production" and doubled for "Manufacture of basic iron"
    e_rows = slicer(matrix='e',axis= 0,Item=['CO2'])
    e_cols_bf = slicer(matrix='e',axis= 1,Region=[region],Item=['Blast furnace gas production'])
    e_cols_m = slicer(matrix='e',axis= 1,Region=[region],Item=['Manufacture of basic iron and steel and of ferro-alloys and first products thereof'])
    e_new = exio_hybrid_base.matrices['baseline']['e']
    e_new.loc[e_rows,e_cols_bf]=0 
    e_new.loc[e_rows,e_cols_m]*=2
    
    # removing production of "Blast furnace gas" and "Oxygen steel furnace gas" from "Manufacture of basic iron"
    z_rows_m = slicer(matrix='z',axis= 0,Region=[region],Item=['Manufacture of basic iron and steel and of ferro-alloys and first products thereof'])
    z_cols_m = slicer(matrix='z',axis= 1,Region=[region],Item=['Blast Furnace Gas', 'Oxygen Steel Furnace Gas'])
    z_new = exio_hybrid_base.matrices['baseline']['z']
    z_new.loc[z_rows_m,z_cols_m]=0
    
    
    # adding production of "Blast furnace gas" and "Oxygen steel furnace gas" to "Blast furnace gas production"
    z_rows_bf = slicer(matrix='z',axis= 0,Region=['China'],Item=['Blast furnace gas production'])
    z_cols_bf = slicer(matrix='z',axis= 1,Region=['China'],Item=['Blast Furnace Gas', 'Oxygen Steel Furnace Gas'])
    z_new = exio_hybrid_base.matrices['baseline']['z']
    z_new.loc[z_rows_bf,z_cols_bf]=1 
    
    z_rows_bf = slicer(matrix='z',axis= 0,Region=['EU27'],Item=['Blast furnace gas production'])
    z_cols_bf = slicer(matrix='z',axis= 1,Region=['EU27'],Item=['Blast Furnace Gas', 'Oxygen Steel Furnace Gas'])
    z_new = exio_hybrid_base.matrices['baseline']['z']
    z_new.loc[z_rows_bf,z_cols_bf]=1
    
    z_rows_bf = slicer(matrix='z',axis= 0,Region=['RoW'],Item=['Blast furnace gas production'])
    z_cols_bf = slicer(matrix='z',axis= 1,Region=['RoW'],Item=['Blast Furnace Gas', 'Oxygen Steel Furnace Gas'])
    z_new = exio_hybrid_base.matrices['baseline']['z']
    z_new.loc[z_rows_bf,z_cols_bf]=1
    
    z_rows_bf = slicer(matrix='z',axis= 0,Region=['India'],Item=['Blast furnace gas production'])
    z_cols_bf = slicer(matrix='z',axis= 1,Region=['India'],Item=['Blast Furnace Gas'])
    z_new = exio_hybrid_base.matrices['baseline']['z']
    z_new.loc[z_rows_bf,z_cols_bf]=1
    
    z_rows_bf = slicer(matrix='z',axis= 0,Region=['Russia'],Item=['Blast furnace gas production'])
    z_cols_bf = slicer(matrix='z',axis= 1,Region=['Russia'],Item=['Blast Furnace Gas'])
    z_new = exio_hybrid_base.matrices['baseline']['z']
    z_new.loc[z_rows_bf,z_cols_bf]=1
    
    z_rows_bf = slicer(matrix='z',axis= 0,Region=['USA'],Item=['Blast furnace gas production'])
    z_cols_bf = slicer(matrix='z',axis= 1,Region=['USA'],Item=['Blast Furnace Gas'])
    z_new = exio_hybrid_base.matrices['baseline']['z']
    z_new.loc[z_rows_bf,z_cols_bf]=1
    
    
exio_hybrid_base.update_scenarios(scenario='new emissions', e=e_new, z=z_new)
exio_hybrid_base.reset_to_coefficients(scenario='new emissions')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\New iron and blast furnace gas sectors" 
exio_hybrid_base.to_txt(export_path, scenario='new emissions',coefficients=True,flows=False)


#%% ADDITION OF NEW SECTORS FOR STEAM REFORMER/ELECTROLYSER PRODUCTION
#%% Importing aggregated database with two sectors for iron and blast furnace gas

import_path = "\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\New iron and blast furnace gas sectors"
exio_hybrid_base = mario.parse_from_txt(import_path+"\\coefficients",table='SUT',mode='coefficients')

#%% Adding activities "Manufacturing of steam reformer/electrolyser" 

#exio_hybrid_base.get_add_sectors_excel(path='Add manufacturing activities.xlsx', new_sectors=['Manufacturing of steam reformer','Manufacturing of electrolyser'], regions=['EU27'], item='Activity',)
exio_hybrid_base.add_sectors('Add_sectors\Add manufacturing activities_filled.xlsx', new_sectors=['Manufacturing of steam reformer', 'Manufacturing of electrolyser'], regions=['EU27'], item='Activity',)

#%% Adding commodities "Steam reformer/Electrolyser"

#exio_hybrid_base.get_add_sectors_excel(path='Add technologies.xlsx', new_sectors=['Steam reformer', 'Electrolyser'], regions=['EU27'], item='Commodity',)
exio_hybrid_base.add_sectors('Add_sectors\Add technologies_filled.xlsx', new_sectors=['Steam reformer', 'Electrolyser'], regions=['EU27'], item='Commodity',)

export_path = "\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\New manufacturing sectors"
exio_hybrid_base.to_txt(export_path,coefficients=True,flows=False)


#%% ADDITION OF NEW SECTORS FOR HYDROGEN PRODUCTION
#%% Importing aggregated database with new manufacturing activities

import_path = "\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\New manufacturing sectors"
exio_hybrid_base = mario.parse_from_txt(import_path+"\\coefficients",table='SUT',mode='coefficients')

#%% Adding activities "Hydrogen production with steam reforming/electrolysis" 

#exio_hybrid_base.get_add_sectors_excel(path='Add H2 production activities.xlsx', new_sectors=['Hydrogen production with steam reforming','Hydrogen production with electrolysis'], regions=['EU27'], item='Activity',)
exio_hybrid_base.add_sectors('Add_sectors\Add H2 production activities_filled.xlsx', new_sectors=['Hydrogen production with steam reforming', 'Hydrogen production with electrolysis'], regions=['EU27'], item='Activity',)

#%% Adding commodities "Steam reforming/Electrolysis hydrogen"

#exio_hybrid_base.get_add_sectors_excel(path='Add hydrogen.xlsx', new_sectors=['Steam reforming hydrogen','Electrolysis hydrogen'], regions=['EU27'], item='Commodity',)
exio_hybrid_base.add_sectors('Add_sectors\Add hydrogen_filled.xlsx', new_sectors=['Steam reforming hydrogen','Electrolysis hydrogen'], regions=['EU27'], item='Commodity',)

export_path = "\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Hydrogen sector"
exio_hybrid_base.to_txt(export_path,coefficients=True,flows=False)

#%% Calculating H2 footprint 

f_H2 = exio_hybrid_base.f.loc[['CO2', 'CH4', 'N2O'],('EU27',sN,['Steam reforming hydrogen','Electrolysis hydrogen'])] 


#%% ADDITION OF NEW STEEL PRODUCTION SECTORS
#%% Importing database with hydrogen sector 

import_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Hydrogen sector\\coefficients" 
exio_hybrid_base = mario.parse_from_txt(path=import_path, table='SUT', mode='coefficients') 

#%% Adding steel production activities: "Steel production with H2 inj to BF", "Steel production through NG-DR", "Steel production through 100%H2-DR", "Steel production with charcoal inj to BF", "Steel production with charcoal inj to BF + CCUS", "Steel production with BF-BOF + CCUS"

#exio_hybrid_base.get_add_sectors_excel(path='Add steel production activities.xlsx', new_sectors=['Steel production with H2 inj to BF','Steel production through NG-DR','Steel production through 100%H2-DR','Steel production with charcoal inj to BF','Steel production with charcoal inj to BF + CCUS', 'Steel production with BF-BOF + CCUS'], regions=['EU27'], item='Activity',)
exio_hybrid_base.add_sectors('Add_sectors\Add steel production activities_filled.xlsx', new_sectors=['Steel production with H2 inj to BF','Steel production through NG-DR','Steel production through 100%H2-DR','Steel production with charcoal inj to BF','Steel production with charcoal inj to BF + CCUS', 'Steel production with BF-BOF + CCUS'], regions=['EU27'], item='Activity',)

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Steel sector" 
exio_hybrid_base.to_txt(export_path,coefficients=True,flows=False)

#%% Making coefficients of new steel production sectors equal to those of "Manufacture of basic iron"

import_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Steel sector\\coefficients" 
exio_hybrid_base = mario.parse_from_txt(path=import_path, table='SUT', mode='coefficients') 

z_new = exio_hybrid_base.get_data(matrices=['z'], scenarios=['baseline'])['baseline'][0]
e_new = exio_hybrid_base.get_data(matrices=['e'], scenarios=['baseline'])['baseline'][0]
v_new = exio_hybrid_base.get_data(matrices=['v'], scenarios=['baseline'])['baseline'][0]

columns_to_update = ['Steel production with H2 inj to BF','Steel production through NG-DR','Steel production through 100%H2-DR','Steel production with charcoal inj to BF','Steel production with charcoal inj to BF + CCUS', 'Steel production with BF-BOF + CCUS']

for column in columns_to_update:
    z_new.loc(axis=1)['EU27', 'Activity', column] = z_new.loc(axis=1)['EU27', 'Activity', 'Manufacture of basic iron and steel and of ferro-alloys and first products thereof']
    e_new.loc(axis=1)['EU27', 'Activity', column] = e_new.loc(axis=1)['EU27', 'Activity', 'Manufacture of basic iron and steel and of ferro-alloys and first products thereof'] 
    v_new.loc(axis=1)['EU27', 'Activity', column] = v_new.loc(axis=1)['EU27', 'Activity', 'Manufacture of basic iron and steel and of ferro-alloys and first products thereof']

exio_hybrid_base.update_scenarios(scenario='baseline',z=z_new, e=e_new, v=v_new)
exio_hybrid_base.reset_to_coefficients(scenario='baseline')

#%% Implementing shocks for characterization of new steel production sectors 

#exio_hybrid_base.get_shock_excel(r'Shocks\Baseline\New steel sectors.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\Baseline\New steel sectors.xlsx',z=True,e=True,scenario='New steel sectors definition')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\New steel sectors definition" 
exio_hybrid_base.to_txt(export_path, scenario='New steel sectors definition', coefficients=True, flows=False)

#%% Importing "New steel sectors definition" scenario as baseline and calculating CO2 footprint

import_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\New steel sectors definition\\coefficients" 
exio_hybrid_base = mario.parse_from_txt(path=import_path, table='SUT', mode='coefficients') 

column_steel_act = exio_hybrid_base.search('Activity','Steel')
column_steel_com = exio_hybrid_base.search('Commodity','Basic iron')

e_CO2 = exio_hybrid_base.e.loc[('CO2'),:]

f_steel = np.diag(e_CO2) @ exio_hybrid_base.w
f_steel.index=f_steel.columns
f_steel_act = f_steel.loc[:,('EU27', 'Activity', column_steel_act)].sum()


































