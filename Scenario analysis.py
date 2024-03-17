#%% Import dependencies

import mario
import pandas as pd
import numpy as np


paths = {
    'Database': 'Database',
    'Aggregations': 'Aggregations',
    'Scenarios': {
        "Baseline":"Scenarios/Baseline",
        "2030":"Scenarios/2030",
        "2050":"Scenarios/2050",
        },
    'Results': {
        'Footprints':'Results/Footprints',
        }
    }

#%% importing baseline final
world = mario.parse_from_txt(paths['Database']+"/1. Baseline final/coefficients", mode='coefficients', table='SUT')
aggr_activities = pd.read_excel(paths['Aggregations']+"/3. Plots.xlsx",sheet_name="Activity",index_col=[0])
aggr_activities = aggr_activities.to_dict()

#%% shock hydrogen mix baseline
world.shock_calc(paths['Scenarios']["Baseline"]+"/100% green hydrogen.xlsx",z=True,scenario='Baseline - 100% green H2')
world.shock_calc(paths['Scenarios']["Baseline"]+"/100% pink hydrogen.xlsx",z=True,scenario='Baseline - 100% pink H2')

#%% main scenarios
scenarios = {
    "2030":["GS-Delayed","GS-H2","GS-Mix","REPowerEU"],
    "2050":["GS-Scrap","GS-Tech","IEA STEPS"],    
    }

clusters = {'Region':{'No EU': world.get_index('Region')}}
clusters['Region']['No EU'].remove('EU')

for year,gs in scenarios.items():
    for scenario in gs:
        world.shock_calc(
            paths['Scenarios'][year]+f"/{scenario}.xlsx",
            z=True,
            scenario=f'{year} - {scenario} - Average', 
            **clusters
            )

#%% sensitivities...


#%% calculations
f_ghg = {}

gwp = {'CO2':1,'CH4':29.8,'N2O':273}
steelmaking_acts = world.search('Activity','steel')


for scenario in world.scenarios:
    f_ghg[scenario] = pd.DataFrame()
    for k in world.get_index('Satellite account'):
        print(f"{scenario} -  {k}")
        e = world.get_data(['e'],scenarios=[scenario])[scenario][0]    
        w = world.get_data(['w'],scenarios=[scenario])[scenario][0]    
        
        f = pd.DataFrame(np.diagflat(e.loc[k,:].values) @ w.values,index=e.columns,columns=e.columns).loc[(slice(None),"Activity",slice(None)),:]*gwp[k]
        f_ghg[scenario] = pd.concat([f_ghg[scenario],f],axis=0)
        
    new_ind = pd.DataFrame(list(f_ghg[scenario].index.get_level_values(-1)),columns=['Old'])
    new_ind['New'] = new_ind['Old'].map(aggr_activities['Aggregation']) 
    new_ind = pd.MultiIndex.from_arrays([f_ghg[scenario].index.get_level_values(0),f_ghg[scenario].index.get_level_values(1),new_ind['New']])
    
    f_ghg[scenario].index = new_ind
    f_ghg[scenario] = f_ghg[scenario].groupby(level=[0,1,2],axis=0).sum()

#%%
for scenario,data in f_ghg.items():
    data = data.loc[:,(slice(None),slice(None),steelmaking_acts)]
    data = data.stack()
    data = data.stack()
    data = data.stack().to_frame()
    data = data.droplevel(1,axis=0)
    data = data.droplevel(3,axis=0)   
    data.index.names=['From','Activity','Route','To']
    data.columns = ['Value']
    data.reset_index(inplace=True)
    data['Scenario'] = scenario
    
    f_ghg[scenario] = data

f_final = pd.DataFrame()
for scenario,data in f_ghg.items():
    f_final = pd.concat([f_final,data])

f_final['Unit'] = 'ton CO2eq/ton steel'

f_final.to_csv(paths['Results']['Footprints']+"/GHG_SteelRoutes_by_scen,reg,act.csv", index=False)
    

    



