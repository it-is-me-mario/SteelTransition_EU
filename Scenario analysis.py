#%% Import dependencies
import mario
import pandas as pd
import numpy as np
from Support import update_mix_u, CCUS, H2inj_mix, inj_change

#%% importing baseline final
world = mario.parse_from_txt("Database/Baseline model/coefficients", mode='coefficients', table='SUT')
aggr_activities = pd.read_excel("Aggregations/3. Plots.xlsx",sheet_name="Activity",index_col=[0])
aggr_activities = aggr_activities.to_dict()

#%% scenarios

# list years, scenarios and sensitivities to perform on each scenario
taxonomy = {
    "2022":{
        "Baseline": ['Average','100% green H2','100% pink H2']
        },
    "2030":{
        "GS-Delayed": [
            'Average','CCUS min',"CCUS max","CHL-inj min","CHL-inj max",
            "H2-inj min","H2 100%SR","H2 100%ELZ","EE 2022"],
        "GS-H2": ['Average','CCUS min',"CCUS max","CHL-inj min","CHL-inj max","H2-inj min","H2 100%SR","H2 100%ELZ","EE 2022"],
        "GS-Mix": ['Average','CCUS min',"CCUS max","CHL-inj min","CHL-inj max","H2-inj min","H2 100%SR","H2 100%ELZ","EE 2022"],
        "REPowerEU": ['Average','CCUS min',"CCUS max","CHL-inj min","CHL-inj max","H2-inj min","H2 100%SR","H2 100%ELZ","EE 2022"]
        },
    "2050":{
        "GS-Scrap": ['Average','CCUS min',"CCUS max","CHL-inj min","CHL-inj max","H2-inj min","H2 100%SR","H2 100%ELZ","EE 2022","EE clean"],
        "GS-Tech": ['Average','CCUS min',"CCUS max","CHL-inj min","CHL-inj max","H2-inj min","H2 100%SR","H2 100%ELZ","EE 2022","EE clean"],
        "IEA STEPS": ["Average","EE 2022","EE clean"]
        }
    }

# informations on electricity mixes to implement in selected scenarios: 'All' means in all scenarios and sensitivities referred to that year unless specified by another dict key
ee_mixes = {
    "2030": {'All':pd.DataFrame({"Electricity from fossil fuels":[0.11],"Electricity from nuclear":[0.2],"Electricity from renewables":[0.69]}).T,},
    "2050": {
        'All':pd.DataFrame({"Electricity from fossil fuels":[0.07],"Electricity from nuclear":[0.12],"Electricity from renewables":[0.81]}).T,
        'EE clean':pd.DataFrame({"Electricity from fossil fuels":[0],"Electricity from nuclear":[0.15],"Electricity from renewables":[0.85]}).T,
        }}


# f_act = pd.DataFrame()
# f_com = pd.DataFrame()
# p_steel = pd.DataFrame()

gwp = {'CO2':1,'CH4':29.8,'N2O':273}
steelmaking_acts = world.search('Activity','steel')
steel_coms = world.search('Commodity','basic iron')

for year,scenarios in taxonomy.items():
    for scenario,sensitivities in scenarios.items():    
        for sensitivity in sensitivities:
            scemario_name = f"{scenario} - {year} - {sensitivity}"

            f_act = pd.DataFrame()
            f_com = pd.DataFrame()
            
            print(scemario_name,end=" ")
            
            if year == "2022":
                # in case of baseline, just clone it as is
                if scenario == 'Baseline':
                    if sensitivity == 'Average':    
                        world.clone_scenario('baseline', 'Shock')
                    else:
                        world.shock_calc(f"Scenarios/Sensitivities/{sensitivity}.xlsx",z=True,scenario='Shock',force_rewrite=True,)
            
            else:
                # for all other scenarios, first start by implementing the main changes related to the steel production market shares (from excel templates)
                world.shock_calc(f"Scenarios/{year}/{scenario}.xlsx",z=True,scenario='Shock',force_rewrite=True,)
                
                # in case sensitivity is not on electricity mix, also apply changes on electricity mixes in 2030 or 2050 according to EU targets on all scenarios
                if sensitivity not in ['EE 2022','EE clean']:
                    update_mix_u(world,ee_mixes[year]['All'],'Shock',region='EU')
                    
                    # sensitivities on CCUS rate
                    if sensitivity=='CCUS min':
                        routes = ['Steel production BF-BOF + CCUS','Steel production with charcoal inj to BF + CCUS']
                        for route in routes:
                            CCUS(world,route,2,'EU','Shock')
                    if sensitivity=='CCUS max':
                        routes = ['Steel production BF-BOF + CCUS','Steel production with charcoal inj to BF + CCUS']
                        for route in routes:
                            CCUS(world,route,0.5,'EU','Shock')
                    
                    # sensitivities on H2 mix into H2-inj route
                    if sensitivity=='H2 100%SR':
                        route = 'Steel production with H2 inj to BF'
                        H2inj_mix(world,'Electrolysis hydrogen','Steam reforming hydrogen',route,'EU','Shock')
                    if sensitivity=='H2 100%ELZ':
                        route = 'Steel production with H2 inj to BF'
                        H2inj_mix(world,'Steam reforming hydrogen','Electrolysis hydrogen',route,'EU','Shock')
                    
                    # sensitivities on amount of charcoal injected in CHL-inj routes
                    if sensitivity=='CHL-inj min':
                        inj_change(world,['Charcoal','Coke Oven Coke'],[0.158701532912534,0.000500323773400313],['Steel production with charcoal inj to BF','Steel production with charcoal inj to BF + CCUS'],'EU','Shock')
                    if sensitivity=='CHL-inj max':
                        inj_change(world,commodities=['Charcoal','Coke Oven Coke'],values=[0.0780476637192975,0.0811541929666366],routes=['Steel production with charcoal inj to BF','Steel production with charcoal inj to BF + CCUS'],region='EU',scenario='Shock',)

                    # sensitivities on amount of hydrogen injected in H2-inj route
                    if sensitivity=='H2-inj min':
                        inj_change(world,['Coke Oven Coke','Steam reforming hydrogen','Electrolysis hydrogen'],[0.15467074757863,0.302073940486925,1.2082957619477],['Steel production with H2 inj to BF'],'EU','Shock',)
                
                # if sensitivity is on ellectricity mix: if EE clean, then implement expected electricity mix in EE clean, if not, keep baseline mix (don't do anything more)
                elif sensitivity=='EE clean':
                    update_mix_u(world,ee_mixes[year][sensitivity],'Shock',region='EU')
              
            # calculate & export prices 
            p = world.get_data(['p'],scenarios=['Shock'])['Shock'][0].loc[(slice(None),slice(None),steel_coms), :]*1e6
            p = p.droplevel(1,axis=0)
            p = p.droplevel(1,axis=0)
            p.columns = ['Value']
            p['Scenario'] = scenario
            p['Year'] = year
            p['Sensitivity'] = sensitivity
            p['Unit'] = "EUR/ton steel"
            p.reset_index(inplace=True)
            
            # export p by scemario
            p.to_csv(f"Results/Prices/{scemario_name}.csv", index=False)            
            
            # calculate & export footprints by origin
            e = world.get_data(['e'],scenarios=['Shock'])['Shock'][0]    
            w = world.get_data(['w'],scenarios=['Shock'])['Shock'][0]    
            
            for k,g in gwp.items():
                f = pd.DataFrame(
                    np.diagflat(e.loc[k,:].values) @ w.values,
                    index=e.columns,
                    columns=e.columns
                    ).loc[(slice(None),"Activity",slice(None)),:]*g
                f = f.stack([0,1,2])
                f = f.to_frame()
                
                f = f.droplevel(1)
                f.columns = ['Value']
                f.index.names = ['From','Activity','To','Level','Item']
                f['Scenario'] = scenario
                f['Year'] = year 
                f['Sensitivity'] = sensitivity   
                f['Unit'] = 'tonCO2eq/ton steel'
                f.reset_index(inplace=True)

                f['Activity'] = f['Activity'].map(aggr_activities['Aggregation'])
                f_act_k = f.query("Item==@steelmaking_acts")
                f_act_k['Gas'] = k

                f_com_k = f.query("Item==@steel_coms")
                f_com_k['Gas'] = k
                
                f_act = pd.concat([f_act,f_act_k],axis=0)
                f_com = pd.concat([f_com,f_com_k],axis=0)
                
            cols = list(f_act.columns)
            cols.remove('Gas')
            cols.remove('Value')
            
            f_act.set_index(cols,inplace=True)
            f_com.set_index(cols,inplace=True)
            f_act = f_act.groupby(level=cols,axis=0).sum()
            f_com = f_com.groupby(level=cols).sum()

            f_act.reset_index(inplace=True)
            f_com.reset_index(inplace=True)

            f_act.to_csv(f"Results/GHG_Footprints_act/{scemario_name}.csv", index=False)
            f_com.to_csv(f"Results/GHG_Footprints_com/{scemario_name}.csv", index=False)
                
                
# %%
