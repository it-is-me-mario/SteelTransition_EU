# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 16:09:08 2024

@author: debor
"""

import mario
import os
import pandas as pd
import plotly.graph_objects as go
from Plots_CO2 import df_footprint, df_env_transactions 

sN = slice(None)

#%% Importing database with new steel sectors 

import_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\New steel sectors definition" 
exio_hybrid_base = mario.parse_from_txt(import_path+"\\coefficients",table='SUT',mode='coefficients')


#%% Implementating "char inj max/min" sensitivity on all scenarios 

# Mixed implementation
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Mixed implementation - char inj max.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Mixed implementation - char inj max.xlsx',z=True,scenario='Mixed implementation - char inj max')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Mixed implementation - char inj max" 
exio_hybrid_base.to_txt(export_path, scenario='Mixed implementation - char inj max', coefficients=True, flows=False)

#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Mixed implementation - char inj min.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Mixed implementation - char inj min.xlsx',z=True,scenario='Mixed implementation - char inj min')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Mixed implementation - char inj min" 
exio_hybrid_base.to_txt(export_path, scenario='Mixed implementation - char inj min', coefficients=True, flows=False)


# Delayed implementation
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Delayed implementation - char inj max.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Delayed implementation - char inj max.xlsx',z=True,scenario='Delayed implementation - char inj max')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Delayed implementation - char inj max" 
exio_hybrid_base.to_txt(export_path, scenario='Delayed implementation - char inj max', coefficients=True, flows=False)

#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Delayed implementation - char inj min.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Delayed implementation - char inj min.xlsx',z=True,scenario='Delayed implementation - char inj min')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Delayed implementation - char inj min" 
exio_hybrid_base.to_txt(export_path, scenario='Delayed implementation - char inj min', coefficients=True, flows=False)


# Increased H2 availability
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Increased H2 availability - char inj max.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Increased H2 availability - char inj max.xlsx',z=True,scenario='Increased H2 availability - char inj max')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Increased H2 availability - char inj max" 
exio_hybrid_base.to_txt(export_path, scenario='Increased H2 availability - char inj max', coefficients=True, flows=False)

#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Increased H2 availability - char inj min.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Increased H2 availability - char inj min.xlsx',z=True,scenario='Increased H2 availability - char inj min')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Increased H2 availability - char inj min" 
exio_hybrid_base.to_txt(export_path, scenario='Increased H2 availability - char inj min', coefficients=True, flows=False)


# REPowerEU
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\REPowerEU - char inj max.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\REPowerEU - char inj max.xlsx',z=True,scenario='REPowerEU - char inj max')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\REPowerEU - char inj max" 
exio_hybrid_base.to_txt(export_path, scenario='REPowerEU - char inj max', coefficients=True, flows=False)

#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\REPowerEU - char inj min.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\REPowerEU - char inj min.xlsx',z=True,scenario='REPowerEU - char inj min')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\REPowerEU - char inj min" 
exio_hybrid_base.to_txt(export_path, scenario='REPowerEU - char inj min', coefficients=True, flows=False)


# Without other technologies 
#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios_sensitivity\Without other technologies - char inj max.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios_sensitivity\Without other technologies - char inj max.xlsx',z=True,scenario='Without other technologies - char inj max')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios_sensitivity\\Without other technologies - char inj max" 
exio_hybrid_base.to_txt(export_path, scenario='Without other technologies - char inj max', coefficients=True, flows=False)

#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios_sensitivity\Without other technologies - char inj min.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios_sensitivity\Without other technologies - char inj min.xlsx',z=True,scenario='Without other technologies - char inj min')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios_sensitivity\\Without other technologies - char inj min" 
exio_hybrid_base.to_txt(export_path, scenario='Without other technologies - char inj min', coefficients=True, flows=False)


# More scrap + Without other technologies (also known as Increased scrap availability)
#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios_sensitivity\More scrap + Without other technologies - char inj max.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios_sensitivity\More scrap + Without other technologies - char inj max.xlsx',z=True,scenario='More scrap + Without other technologies - char inj max')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios_sensitivity\\More scrap + Without other technologies - char inj max" 
exio_hybrid_base.to_txt(export_path, scenario='More scrap + Without other technologies - char inj max', coefficients=True, flows=False)

#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios_sensitivity\More scrap + Without other technologies - char inj min.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios_sensitivity\More scrap + Without other technologies - char inj min.xlsx',z=True,scenario='More scrap + Without other technologies - char inj min')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios_sensitivity\\More scrap + Without other technologies - char inj min" 
exio_hybrid_base.to_txt(export_path, scenario='More scrap + Without other technologies - char inj min', coefficients=True, flows=False)


#%% Implementing "H2 inj min" sensitivity on all scenarios 

# Mixed implementation
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Mixed implementation - H2 inj min.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Mixed implementation - H2 inj min.xlsx',z=True,scenario='Mixed implementation - H2 inj min')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Mixed implementation - H2 inj min" 
exio_hybrid_base.to_txt(export_path, scenario='Mixed implementation - H2 inj min', coefficients=True, flows=False)


# Delayed implementation
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Delayed implementation - H2 inj min.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Delayed implementation - H2 inj min.xlsx',z=True,scenario='Delayed implementation - H2 inj min')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Delayed implementation - H2 inj min" 
exio_hybrid_base.to_txt(export_path, scenario='Delayed implementation - H2 inj min', coefficients=True, flows=False)


# Increased H2 availability
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Increased H2 availability - H2 inj min.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Increased H2 availability - H2 inj min.xlsx',z=True,scenario='Increased H2 availability - H2 inj min')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Increased H2 availability - H2 inj min" 
exio_hybrid_base.to_txt(export_path, scenario='Increased H2 availability - H2 inj min', coefficients=True, flows=False)


# REPowerEU
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\REPowerEU - H2 inj min.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\REPowerEU - H2 inj min.xlsx',z=True,scenario='REPowerEU - H2 inj min')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\REPowerEU - H2 inj min" 
exio_hybrid_base.to_txt(export_path, scenario='REPowerEU - H2 inj min', coefficients=True, flows=False)


# Without other technologies 
#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios_sensitivity\Without other technologies - H2 inj min.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios_sensitivity\Without other technologies - H2 inj min.xlsx',z=True,scenario='Without other technologies - H2 inj min')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios_sensitivity\\Without other technologies - H2 inj min" 
exio_hybrid_base.to_txt(export_path, scenario='Without other technologies - H2 inj min', coefficients=True, flows=False)


# More scrap + Without other technologies (also known as Increased scrap availability)
#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios_sensitivity\More scrap + Without other technologies - H2 inj min.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios_sensitivity\More scrap + Without other technologies - H2 inj min.xlsx',z=True,scenario='More scrap + Without other technologies - H2 inj min')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios_sensitivity\\More scrap + Without other technologies - H2 inj min" 
exio_hybrid_base.to_txt(export_path, scenario='More scrap + Without other technologies - H2 inj min', coefficients=True, flows=False)


#%% Implementing "100% SR/ELE H2 inj" sensitivity on all scenarios 

# Mixed implementation
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Mixed implementation - 100% SR H2 inj.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Mixed implementation - 100% SR H2 inj.xlsx',z=True,scenario='Mixed implementation - 100% SR H2 inj')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Mixed implementation - 100% SR H2 inj" 
exio_hybrid_base.to_txt(export_path, scenario='Mixed implementation - 100% SR H2 inj', coefficients=True, flows=False)

#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Mixed implementation - 100% ELE H2 inj.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Mixed implementation - 100% ELE H2 inj.xlsx',z=True,scenario='Mixed implementation - 100% ELE H2 inj')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Mixed implementation - 100% ELE H2 inj" 
exio_hybrid_base.to_txt(export_path, scenario='Mixed implementation - 100% ELE H2 inj', coefficients=True, flows=False)


# Delayed implementation
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Delayed implementation - 100% SR H2 inj.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Delayed implementation - 100% SR H2 inj.xlsx',z=True,scenario='Delayed implementation - 100% SR H2 inj')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Delayed implementation - 100% SR H2 inj" 
exio_hybrid_base.to_txt(export_path, scenario='Delayed implementation - 100% SR H2 inj', coefficients=True, flows=False)

#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Delayed implementation - 100% ELE H2 inj.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Delayed implementation - 100% ELE H2 inj.xlsx',z=True,scenario='Delayed implementation - 100% ELE H2 inj')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Delayed implementation - 100% ELE H2 inj" 
exio_hybrid_base.to_txt(export_path, scenario='Delayed implementation - 100% ELE H2 inj', coefficients=True, flows=False)


# Increased H2 availability
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Increased H2 availability - 100% SR H2 inj.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Increased H2 availability - 100% SR H2 inj.xlsx',z=True,scenario='Increased H2 availability - 100% SR H2 inj')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Increased H2 availability - 100% SR H2 inj" 
exio_hybrid_base.to_txt(export_path, scenario='Increased H2 availability - 100% SR H2 inj', coefficients=True, flows=False)

#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Increased H2 availability - 100% ELE H2 inj.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Increased H2 availability - 100% ELE H2 inj.xlsx',z=True,scenario='Increased H2 availability - 100% ELE H2 inj')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Increased H2 availability - 100% ELE H2 inj" 
exio_hybrid_base.to_txt(export_path, scenario='Increased H2 availability - 100% ELE H2 inj', coefficients=True, flows=False)


# REPowerEU
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\REPowerEU - 100% SR H2 inj.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\REPowerEU - 100% SR H2 inj.xlsx',z=True,scenario='REPowerEU - 100% SR H2 inj')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\REPowerEU - 100% SR H2 inj" 
exio_hybrid_base.to_txt(export_path, scenario='REPowerEU - 100% SR H2 inj', coefficients=True, flows=False)

#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\REPowerEU - 100% ELE H2 inj.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\REPowerEU - 100% ELE H2 inj.xlsx',z=True,scenario='REPowerEU - 100% ELE H2 inj')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\REPowerEU - 100% ELE H2 inj" 
exio_hybrid_base.to_txt(export_path, scenario='REPowerEU - 100% ELE H2 inj', coefficients=True, flows=False)


# Without other technologies 
#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios_sensitivity\Without other technologies - 100% SR H2 inj.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios_sensitivity\Without other technologies - 100% SR H2 inj.xlsx',z=True,scenario='Without other technologies - 100% SR H2 inj')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios_sensitivity\\Without other technologies - 100% SR H2 inj" 
exio_hybrid_base.to_txt(export_path, scenario='Without other technologies - 100% SR H2 inj', coefficients=True, flows=False)

#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios_sensitivity\Without other technologies - 100% ELE H2 inj.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios_sensitivity\Without other technologies - 100% ELE H2 inj.xlsx',z=True,scenario='Without other technologies - 100% ELE H2 inj')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios_sensitivity\\Without other technologies - 100% ELE H2 inj" 
exio_hybrid_base.to_txt(export_path, scenario='Without other technologies - 100% ELE H2 inj', coefficients=True, flows=False)


# More scrap + Without other technologies (also known as Increased scrap availability)
#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios_sensitivity\More scrap + Without other technologies - 100% SR H2 inj.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios_sensitivity\More scrap + Without other technologies - 100% SR H2 inj.xlsx',z=True,scenario='More scrap + Without other technologies - 100% SR H2 inj')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios_sensitivity\\More scrap + Without other technologies - 100% SR H2 inj" 
exio_hybrid_base.to_txt(export_path, scenario='More scrap + Without other technologies - 100% SR H2 inj', coefficients=True, flows=False)

#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios_sensitivity\More scrap + Without other technologies - 100% ELE H2 inj.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios_sensitivity\More scrap + Without other technologies - 100% ELE H2 inj.xlsx',z=True,scenario='More scrap + Without other technologies - 100% ELE H2 inj')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios_sensitivity\\More scrap + Without other technologies - 100% ELE H2 inj" 
exio_hybrid_base.to_txt(export_path, scenario='More scrap + Without other technologies - 100% ELE H2 inj', coefficients=True, flows=False)


#%% Implementing "less RES" sensitivity on all scenarios 

# Mixed implementation
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Mixed implementation - less RES.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Mixed implementation - less RES.xlsx',z=True,scenario='Mixed implementation - less RES')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Mixed implementation - less RES" 
exio_hybrid_base.to_txt(export_path, scenario='Mixed implementation - less RES', coefficients=True, flows=False)


# Delayed implementation
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Delayed implementation - less RES.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Delayed implementation - less RES.xlsx',z=True,scenario='Delayed implementation - less RES')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Delayed implementation - less RES" 
exio_hybrid_base.to_txt(export_path, scenario='Delayed implementation - less RES', coefficients=True, flows=False)


# Increased H2 availability
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Increased H2 availability - less RES.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Increased H2 availability - less RES.xlsx',z=True,scenario='Increased H2 availability - less RES')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Increased H2 availability - less RES" 
exio_hybrid_base.to_txt(export_path, scenario='Increased H2 availability - less RES', coefficients=True, flows=False)


# REPowerEU
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\REPowerEU - less RES.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\REPowerEU - less RES.xlsx',z=True,scenario='REPowerEU - less RES')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\REPowerEU - less RES" 
exio_hybrid_base.to_txt(export_path, scenario='REPowerEU - less RES', coefficients=True, flows=False)


# Without other technologies 
#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios_sensitivity\Without other technologies - less RES.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios_sensitivity\Without other technologies - less RES.xlsx',z=True,scenario='Without other technologies - less RES')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios_sensitivity\\Without other technologies - less RES" 
exio_hybrid_base.to_txt(export_path, scenario='Without other technologies - less RES', coefficients=True, flows=False)


# More scrap + Without other technologies (also known as Increased scrap availability)
#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios_sensitivity\More scrap + Without other technologies - less RES.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios_sensitivity\More scrap + Without other technologies - less RES.xlsx',z=True,scenario='More scrap + Without other technologies - less RES')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios_sensitivity\\More scrap + Without other technologies - less RES" 
exio_hybrid_base.to_txt(export_path, scenario='More scrap + Without other technologies - less RES', coefficients=True, flows=False)


#%% Implementing "CCUS max/min" sensitivity on all scenarios 

# Mixed implementation
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Mixed implementation - CCUS max.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Mixed implementation - CCUS max.xlsx',e=True,z=True,scenario='Mixed implementation - CCUS max')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Mixed implementation - CCUS max" 
exio_hybrid_base.to_txt(export_path, scenario='Mixed implementation - CCUS max', coefficients=True, flows=False)

#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Mixed implementation - CCUS min.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Mixed implementation - CCUS min.xlsx',e=True,z=True,scenario='Mixed implementation - CCUS min')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Mixed implementation - CCUS min" 
exio_hybrid_base.to_txt(export_path, scenario='Mixed implementation - CCUS min', coefficients=True, flows=False)


# Delayed implementation
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Delayed implementation - CCUS max.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Delayed implementation - CCUS max.xlsx',e=True,z=True,scenario='Delayed implementation - CCUS max')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Delayed implementation - CCUS max" 
exio_hybrid_base.to_txt(export_path, scenario='Delayed implementation - CCUS max', coefficients=True, flows=False)

#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Delayed implementation - CCUS min.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Delayed implementation - CCUS min.xlsx',e=True,z=True,scenario='Delayed implementation - CCUS min')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Delayed implementation - CCUS min" 
exio_hybrid_base.to_txt(export_path, scenario='Delayed implementation - CCUS min', coefficients=True, flows=False)


# Increased H2 availability
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Increased H2 availability - CCUS max.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Increased H2 availability - CCUS max.xlsx',e=True,z=True,scenario='Increased H2 availability - CCUS max')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Increased H2 availability - CCUS max" 
exio_hybrid_base.to_txt(export_path, scenario='Increased H2 availability - CCUS max', coefficients=True, flows=False)

#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\Increased H2 availability - CCUS min.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\Increased H2 availability - CCUS min.xlsx',e=True,z=True,scenario='Increased H2 availability - CCUS min')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\Increased H2 availability - CCUS min" 
exio_hybrid_base.to_txt(export_path, scenario='Increased H2 availability - CCUS min', coefficients=True, flows=False)


# REPowerEU
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\REPowerEU - CCUS max.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\REPowerEU - CCUS max.xlsx',e=True,z=True,scenario='REPowerEU - CCUS max')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\REPowerEU - CCUS max" 
exio_hybrid_base.to_txt(export_path, scenario='REPowerEU - CCUS max', coefficients=True, flows=False)

#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios_sensitivity\REPowerEU - CCUS min.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios_sensitivity\REPowerEU - CCUS min.xlsx',e=True,z=True,scenario='REPowerEU - CCUS min')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios_sensitivity\\REPowerEU - CCUS min" 
exio_hybrid_base.to_txt(export_path, scenario='REPowerEU - CCUS min', coefficients=True, flows=False)


# Without other technologies 
#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios_sensitivity\Without other technologies - CCUS max.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios_sensitivity\Without other technologies - CCUS max.xlsx',e=True,z=True,scenario='Without other technologies - CCUS max')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios_sensitivity\\Without other technologies - CCUS max" 
exio_hybrid_base.to_txt(export_path, scenario='Without other technologies - CCUS max', coefficients=True, flows=False)

#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios_sensitivity\Without other technologies - CCUS min.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios_sensitivity\Without other technologies - CCUS min.xlsx',e=True,z=True,scenario='Without other technologies - CCUS min')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios_sensitivity\\Without other technologies - CCUS min" 
exio_hybrid_base.to_txt(export_path, scenario='Without other technologies - CCUS min', coefficients=True, flows=False)


# More scrap + Without other technologies (also known as Increased scrap availability)
#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios_sensitivity\More scrap + Without other technologies - CCUS max.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios_sensitivity\More scrap + Without other technologies - CCUS max.xlsx',e=True,z=True,scenario='More scrap + Without other technologies - CCUS max')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios_sensitivity\\More scrap + Without other technologies - CCUS max" 
exio_hybrid_base.to_txt(export_path, scenario='More scrap + Without other technologies - CCUS max', coefficients=True, flows=False)

#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios_sensitivity\More scrap + Without other technologies - CCUS min.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios_sensitivity\More scrap + Without other technologies - CCUS min.xlsx',e=True,z=True,scenario='More scrap + Without other technologies - CCUS min')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios_sensitivity\\More scrap + Without other technologies - CCUS min" 
exio_hybrid_base.to_txt(export_path, scenario='More scrap + Without other technologies - CCUS min', coefficients=True, flows=False)


#%% Implementing "clean el" sensitivity on 2050 scenarios 

# Without other technologies 
#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios_sensitivity\Without other technologies - clean el.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios_sensitivity\Without other technologies - clean el.xlsx',z=True,scenario='Without other technologies - clean el')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios_sensitivity\\Without other technologies - clean el" 
exio_hybrid_base.to_txt(export_path, scenario='Without other technologies - clean el', coefficients=True, flows=False)


# More scrap + Without other technologies (also known as Increased scrap availability)
#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios_sensitivity\More scrap + Without other technologies - clean el.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios_sensitivity\More scrap + Without other technologies - clean el.xlsx',z=True,scenario='More scrap + Without other technologies - clean el')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios_sensitivity\\More scrap + Without other technologies - clean el" 
exio_hybrid_base.to_txt(export_path, scenario='More scrap + Without other technologies - clean el', coefficients=True, flows=False)


#%% BAR CHARTS

# Information on scenarios  

sensitivity_scenarios = exio_hybrid_base.scenarios 
sensitivity_scenarios.remove("baseline")
                    
sensitivity_scenarios_info = {'Mixed implementation - char inj max': {'year': 2030, 'sensitivity': 'char inj max', 'name': 'Mixed implementation'},'Delayed implementation - char inj max': {'year': 2030, 'sensitivity': 'char inj max','name': 'Delayed implementation'},'Increased H2 availability - char inj max': {'year': 2030, 'sensitivity': 'char inj max','name': 'Increased H2 availability'},'REPowerEU - char inj max': {'year': 2030, 'sensitivity': 'char inj max','name': 'REPowerEU'},'Without other technologies - char inj max': {'year': 2050, 'sensitivity': 'char inj max','name': 'Without other technologies'},'More scrap + Without other technologies - char inj max': {'year': 2050, 'sensitivity': 'char inj max','name': 'More scrap + Without other technologies'},
                              'Mixed implementation - char inj min': {'year': 2030, 'sensitivity': 'char inj min', 'name': 'Mixed implementation'},'Delayed implementation - char inj min': {'year': 2030, 'sensitivity': 'char inj min', 'name': 'Delayed implementation'},'Increased H2 availability - char inj min': {'year': 2030, 'sensitivity': 'char inj min', 'name': 'Increased H2 availability'},'REPowerEU - char inj min': {'year': 2030, 'sensitivity': 'char inj min', 'name': 'REPowerEU'},'Without other technologies - char inj min': {'year': 2050, 'sensitivity': 'char inj min', 'name': 'Without other technologies'},'More scrap + Without other technologies - char inj min': {'year': 2050, 'sensitivity': 'char inj min', 'name': 'More scrap + Without other technologies'},
                              'Mixed implementation - H2 inj min': {'year': 2030, 'sensitivity': 'H2 inj min', 'name': 'Mixed implementation'},'Delayed implementation - H2 inj min': {'year': 2030, 'sensitivity': 'H2 inj min', 'name': 'Delayed implementation'},'Increased H2 availability - H2 inj min': {'year': 2030, 'sensitivity': 'H2 inj min', 'name': 'Increased H2 availability'},'REPowerEU - H2 inj min': {'year': 2030, 'sensitivity': 'H2 inj min', 'name': 'REPowerEU'},'Without other technologies - H2 inj min': {'year': 2050, 'sensitivity': 'H2 inj min', 'name': 'Without other technologies'},'More scrap + Without other technologies - H2 inj min': {'year': 2050, 'sensitivity': 'H2 inj min', 'name': 'More scrap + Without other technologies'},
                              'Mixed implementation - 100% SR H2 inj': {'year': 2030, 'sensitivity': '100% SR H2 inj', 'name': 'Mixed implementation'},'Delayed implementation - 100% SR H2 inj': {'year': 2030, 'sensitivity': '100% SR H2 inj', 'name': 'Delayed implementation'},'Increased H2 availability - 100% SR H2 inj': {'year': 2030, 'sensitivity': '100% SR H2 inj', 'name': 'Increased H2 availability'},'REPowerEU - 100% SR H2 inj': {'year': 2030, 'sensitivity': '100% SR H2 inj', 'name': 'REPowerEU'},'Without other technologies - 100% SR H2 inj': {'year': 2050, 'sensitivity': '100% SR H2 inj', 'name': 'Without other technologies'},'More scrap + Without other technologies - 100% SR H2 inj': {'year': 2050, 'sensitivity': '100% SR H2 inj', 'name': 'More scrap + Without other technologies'},           
                              'Mixed implementation - 100% ELE H2 inj': {'year': 2030, 'sensitivity': '100% ELE H2 inj', 'name': 'Mixed implementation'},'Delayed implementation - 100% ELE H2 inj': {'year': 2030, 'sensitivity': '100% ELE H2 inj', 'name': 'Delayed implementation'},'Increased H2 availability - 100% ELE H2 inj': {'year': 2030, 'sensitivity': '100% ELE H2 inj', 'name': 'Increased H2 availability'},'REPowerEU - 100% ELE H2 inj': {'year': 2030, 'sensitivity': '100% ELE H2 inj', 'name': 'REPowerEU'},'Without other technologies - 100% ELE H2 inj': {'year': 2050, 'sensitivity': '100% ELE H2 inj', 'name': 'Without other technologies'},'More scrap + Without other technologies - 100% ELE H2 inj': {'year': 2050, 'sensitivity': '100% ELE H2 inj', 'name': 'More scrap + Without other technologies'}, 
                              'Mixed implementation - CCUS max': {'year': 2030, 'sensitivity': 'CCUS max', 'name': 'Mixed implementation'},'Delayed implementation - CCUS max': {'year': 2030, 'sensitivity': 'CCUS max', 'name': 'Delayed implementation'},'Increased H2 availability - CCUS max': {'year': 2030, 'sensitivity': 'CCUS max', 'name': 'Increased H2 availability'},'REPowerEU - CCUS max': {'year': 2030, 'sensitivity': 'CCUS max', 'name': 'REPowerEU'},'Without other technologies - CCUS max': {'year': 2050, 'sensitivity': 'CCUS max', 'name': 'Without other technologies'},'More scrap + Without other technologies - CCUS max': {'year': 2050, 'sensitivity': 'CCUS max', 'name': 'More scrap + Without other technologies'}, 
                              'Mixed implementation - CCUS min': {'year': 2030, 'sensitivity': 'CCUS min', 'name': 'Mixed implementation'},'Delayed implementation - CCUS min': {'year': 2030, 'sensitivity': 'CCUS min', 'name': 'Delayed implementation'},'Increased H2 availability - CCUS min': {'year': 2030, 'sensitivity': 'CCUS min', 'name': 'Increased H2 availability'},'REPowerEU - CCUS min': {'year': 2030, 'sensitivity': 'CCUS min', 'name': 'REPowerEU'},'Without other technologies - CCUS min': {'year': 2050, 'sensitivity': 'CCUS min', 'name': 'Without other technologies'},'More scrap + Without other technologies - CCUS min': {'year': 2050, 'sensitivity': 'CCUS min', 'name': 'More scrap + Without other technologies'}, 
                              'Mixed implementation - less RES': {'year': 2030, 'sensitivity': 'less RES', 'name': 'Mixed implementation'},'Delayed implementation - less RES': {'year': 2030, 'sensitivity': 'less RES','name': 'Delayed implementation'},'Increased H2 availability - less RES': {'year': 2030, 'sensitivity': 'less RES','name': 'Increased H2 availability'},'REPowerEU - less RES': {'year': 2030, 'sensitivity': 'less RES','name': 'REPowerEU'},'Without other technologies - less RES': {'year': 2050, 'sensitivity': 'less RES','name': 'Without other technologies'},'More scrap + Without other technologies - less RES': {'year': 2050, 'sensitivity': 'less RES','name': 'More scrap + Without other technologies'},
                              'Without other technologies - clean el': {'year': 2050, 'sensitivity': 'clean el', 'name': 'Without other technologies'},'More scrap + Without other technologies - clean el': {'year': 2050, 'sensitivity': 'clean el', 'name': 'More scrap + Without other technologies'}, 
                              }
                              
scenario_names = {"Mixed implementation": "GS30-Mix",
                  "Delayed implementation": "GS30-Delayed",
                  "Increased H2 availability": "GS30-H<sub>2</sub>",
                  "REPowerEU": "REPowerEU",
                  "Without other technologies": "GS50-Tech",
                  "More scrap + Without other technologies": "GS50-Scrap",
                  "IEA STEPS": "IEA STEPS",
                 }

#%% Bar charts for sensitivity analysis: f

# Creating a dataframe for footprint for every sensitivity 
f_sensitivity = {}

row_steel_com = exio_hybrid_base.search('Commodity','Basic iron and steel')

for scenario in sensitivity_scenarios:
      
        f_steel_act = exio_hybrid_base.get_data(['f'],scenarios=[scenario])[scenario][0].loc[('CO2'),('EU27',sN,row_steel_com)]
                
        f_sensitivity[sensitivity_scenarios_info[scenario]['year'],
                      sensitivity_scenarios_info[scenario]['name'],
                      sensitivity_scenarios_info[scenario]['sensitivity']] = f_steel_act
        

df_f_sensitivity = pd.DataFrame(f_sensitivity)
df_f_sensitivity.columns.names = ['Year', 'Scenario', 'Sensitivity']

df_f_stack = df_f_sensitivity.stack('Year')
df_f_stack = df_f_stack.stack('Scenario')

df_f_sensitivity = df_f_stack.reset_index()
df_f_sensitivity = df_f_sensitivity.drop(['Item', 'Level'], axis=1)


# Combining df_f_sensitivity with df_footprint to have "no sensitivity" values 
df_combined = pd.merge(df_f_sensitivity, df_footprint[['Scenario', 'Values']], on=['Scenario'])
df_combined = df_combined.rename(columns={'Values':'no sensitivity'})

df_combined["Short_Scenario"] = df_combined["Scenario"].apply(lambda x: scenario_names.get(x, x))


# Plot
fig = go.Figure(data=[
    go.Bar(name='no sensitivity', x=[df_combined["Year"], df_combined["Short_Scenario"]], y=df_combined["no sensitivity"], marker_color="#1b263b"),
    go.Scatter(
        name='footprint in baseline (2022)',
        x=[None],
        y=[None],
        mode='lines',
        line=dict(color='black', dash='dot'),
        showlegend=True,
        ),
    go.Scatter(
        name=' ',
        x=[None],
        y=[None],
        mode='lines',
        marker=dict(color='rgba(255, 255, 255, 0)'), 
        showlegend=True,
        ),    
    go.Bar(name='', x=[None], y=[None], marker_color='rgba(255, 255, 255, 0)', showlegend=False),
    go.Bar(name='char inj max', x=[df_combined["Year"], df_combined["Short_Scenario"]], y=df_combined["char inj max"], marker_color="#fb8500"),
    go.Bar(name='char inj min', x=[df_combined["Year"], df_combined["Short_Scenario"]], y=df_combined["char inj min"], marker_color="#ffb703"),
    go.Bar(name='H<sub>2</sub> inj min', x=[df_combined["Year"], df_combined["Short_Scenario"]], y=df_combined["H2 inj min"], marker_color="#fae588"),
    go.Bar(name='100% ELE H<sub>2</sub> inj', x=[df_combined["Year"], df_combined["Short_Scenario"]], y=df_combined["100% ELE H2 inj"], marker_color="#c6c013"),
    go.Bar(name='100% SR H<sub>2</sub> inj', x=[df_combined["Year"], df_combined["Short_Scenario"]], y=df_combined["100% SR H2 inj"], marker_color="#d3d3d3" ),
    go.Bar(name='CCUS max', x=[df_combined["Year"], df_combined["Short_Scenario"]], y=df_combined["CCUS max"], marker_color="#219ebc"),
    go.Bar(name='CCUS min', x=[df_combined["Year"], df_combined["Short_Scenario"]], y=df_combined["CCUS min"], marker_color="#83c5be"),
    go.Bar(name='less RES', x=[df_combined["Year"], df_combined["Short_Scenario"]], y=df_combined["less RES"], marker_color="#b08968"),
    go.Bar(name='clean el', x=[df_combined["Year"], df_combined["Short_Scenario"]], y=df_combined["clean el"], marker_color="#99d98c"),
    ])
     
y_baseline = df_footprint[df_footprint["Scenario"] == "baseline"]["Values"].item()

fig.add_hline(y=y_baseline, line_width=2, line_dash="dash", line_color="black")


fig.update_layout(
    title=dict(
        text="CO<sub>2</sub> footprint by scenario with sensitivity analysis",
        x=0.455,
        ),
    yaxis_title='ton<sub>CO<sub>2</sub></sub>/ton<sub>steel</sub>',
    xaxis_tickangle=0,
    yaxis=dict(
        range=[0,1.3]),
    barmode='group',
    template="plotly_white",
    font_family="Helvetica",
    font_size=13, 
    )


fig.show(renderer="browser")
fig.write_html('Plots\Sensitivity.html')

#%% Bar charts for sensitivity analysis: E

# Creating a dataframe for E for every sensitivity 
E_sensitivity = {}

steel_act = exio_hybrid_base.search('Activity','Steel')

for scenario in sensitivity_scenarios:
      
        E = exio_hybrid_base.get_data(['E'],scenarios=[scenario])[scenario][0].loc['CO2',('EU27',sN,steel_act)]
             
        E_sensitivity[sensitivity_scenarios_info[scenario]['year'],
                      sensitivity_scenarios_info[scenario]['name'],
                      sensitivity_scenarios_info[scenario]['sensitivity']] = E
        

df_E_sensitivity = pd.DataFrame(E_sensitivity).sum()
df_E_sensitivity = df_E_sensitivity.rename_axis(index=['Year', 'Scenario', 'Sensitivity']).reset_index()
df_E_sensitivity.reset_index(inplace=True)
df_E_sensitivity.drop(columns=['index'], inplace=True)
df_E_sensitivity = df_E_sensitivity.rename(columns={0: 'Values'})

df_E_sensitivity = df_E_sensitivity.pivot_table(index=['Year', 'Scenario'], columns='Sensitivity', values='Values', aggfunc='sum')
df_E_sensitivity.reset_index(inplace=True)


# Combining df_E_sensitivity with df_env_transactions to have "no sensitivity" values 
df_combined_E = pd.merge(df_E_sensitivity, df_env_transactions[['Scenario', 'Values']], on=['Scenario'])
df_combined_E = df_combined_E.rename(columns={'Values':'no sensitivity'})

df_combined_E["Short_Scenario"] = df_combined_E["Scenario"].apply(lambda x: scenario_names.get(x, x))


# Plot
fig = go.Figure(data=[
    go.Bar(name='no sensitivity', x=[df_combined_E["Year"], df_combined_E["Short_Scenario"]], y=df_combined_E["no sensitivity"], marker_color="#1b263b"),
    go.Scatter(
        name='footprint in baseline (2022)',
        x=[None],
        y=[None],
        mode='lines',
        line=dict(color='black', dash='dot'),
        showlegend=True,
        ),
    go.Scatter(
        name=' ',
        x=[None],
        y=[None],
        mode='lines',
        marker=dict(color='rgba(255, 255, 255, 0)'), 
        showlegend=True,
        ),    
    go.Bar(name='', x=[None], y=[None], marker_color='rgba(255, 255, 255, 0)', showlegend=False),
    go.Bar(name='char inj max', x=[df_combined_E["Year"], df_combined_E["Short_Scenario"]], y=df_combined_E["char inj max"], marker_color="#fb8500"),
    go.Bar(name='char inj min', x=[df_combined_E["Year"], df_combined_E["Short_Scenario"]], y=df_combined_E["char inj min"], marker_color="#ffb703"),
    go.Bar(name='H<sub>2</sub> inj min', x=[df_combined_E["Year"], df_combined_E["Short_Scenario"]], y=df_combined_E["H2 inj min"], marker_color="#fae588"),
    go.Bar(name='100% ELE H<sub>2</sub> inj', x=[df_combined_E["Year"], df_combined_E["Short_Scenario"]], y=df_combined_E["100% ELE H2 inj"], marker_color="#c6c013"),
    go.Bar(name='100% SR H<sub>2</sub> inj', x=[df_combined_E["Year"], df_combined_E["Short_Scenario"]], y=df_combined_E["100% SR H2 inj"], marker_color="#d3d3d3" ),
    go.Bar(name='CCUS max', x=[df_combined_E["Year"], df_combined_E["Short_Scenario"]], y=df_combined_E["CCUS max"], marker_color="#219ebc"),
    go.Bar(name='CCUS min', x=[df_combined_E["Year"], df_combined_E["Short_Scenario"]], y=df_combined_E["CCUS min"], marker_color="#83c5be"),
    go.Bar(name='less RES', x=[df_combined_E["Year"], df_combined_E["Short_Scenario"]], y=df_combined_E["less RES"], marker_color="#b08968"),
    go.Bar(name='clean el', x=[df_combined_E["Year"], df_combined_E["Short_Scenario"]], y=df_combined_E["clean el"], marker_color="#99d98c"),
    ])
     
y_baseline = df_env_transactions[df_env_transactions["Scenario"] == "baseline"]["Values"].item()

fig.add_hline(y=y_baseline, line_width=2, line_dash="dash", line_color="black")


fig.update_layout(
    title=dict(
        text="CO<sub>2</sub> emissions by scenario with sensitivity analysis",
        x=0.455,
        ),
    yaxis_title='ton<sub>CO<sub>2</sub></sub>',
    xaxis_tickangle=0,
    yaxis=dict(
        range=[0,300000000]),
    barmode='group',
    template="plotly_white",
    font_family="Helvetica",
    font_size=13, 
    )


fig.show(renderer="browser")
fig.write_html('Plots\Sensitivity E.html')
  
    
    


