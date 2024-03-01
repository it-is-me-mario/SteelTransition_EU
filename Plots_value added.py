# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 12:55:30 2024

@author: debor
"""

import mario
import os
import pandas as pd
import plotly.graph_objects as go
from Plots_CO2 import df_footprint, df_env_transactions

sN = slice(None)

#%% Importing database with baseline scenario (2022)

import_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\New steel sectors definition\\coefficients" 
exio_hybrid_base = mario.parse_from_txt(path=import_path, table='SUT', mode='coefficients') 

#%% Importing 2030 and 2050 scenarios 
  
# Mixed implementation
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios\Mixed implementation.xlsx',z=True,scenario='Mixed implementation')
 
# Delayed implementation
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios\Delayed implementation.xlsx',z=True,scenario='Delayed implementation')

# Increased H2 availability
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios\Increased H2 availability.xlsx',z=True,scenario='Increased H2 availability')

# REPowerEU
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios\REPowerEU.xlsx',z=True,scenario='REPowerEU')

# Without other technologies
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios\Without other technologies.xlsx',z=True,scenario='Without other technologies')

# More scrap + Without other technologies
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios\More scrap + Without other technologies.xlsx',z=True,scenario='More scrap + Without other technologies')

# IEA STEPS
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios\IEA STEPS.xlsx',z=True,scenario='IEA STEPS')

#%% Updating "Consumption of fixed capital" value for new steel technologies in all scenarios

steel_act = exio_hybrid_base.search('Activity','Steel')

scenarios = exio_hybrid_base.scenarios 
scenarios_info = {
    'baseline': {'year': 2022}, 'Mixed implementation': {'year': 2030},
    'Delayed implementation': {'year': 2030}, 'Increased H2 availability': {'year': 2030},
    'REPowerEU': {'year': 2030}, 'Without other technologies': {'year': 2050},
    'More scrap + Without other technologies': {'year': 2050}, 'IEA STEPS': {'year': 2050}
    }

v_scenario = {}

for scenario in scenarios: 
    
    v = exio_hybrid_base.get_data(['v'],scenarios=[scenario])[scenario][0]
        
    v.loc['Operating surplus: Consumption of fixed capital', ('EU27', 'Activity', 'Steel production through 100%H2-DR')] *= 0.125
    v.loc['Operating surplus: Consumption of fixed capital', ('EU27', 'Activity', 'Steel production through NG-DR')] *= 0.125
    v.loc['Operating surplus: Consumption of fixed capital', ('EU27', 'Activity','Steel production with BF-BOF + CCUS')] *= 1.25
    v.loc['Operating surplus: Consumption of fixed capital', ('EU27', 'Activity','Steel production with H2 inj to BF')] *= 0.15
    v.loc['Operating surplus: Consumption of fixed capital', ('EU27', 'Activity','Steel production with charcoal inj to BF')] *= 1.004
    v.loc['Operating surplus: Consumption of fixed capital', ('EU27', 'Activity','Steel production with charcoal inj to BF + CCUS')] *= 1.254
      
    exio_hybrid_base.update_scenarios(scenario=scenario,v=v)
    exio_hybrid_base.reset_to_coefficients(scenario=scenario)
    
    v_scenario[scenario] = v
    
#%% Calculatig price of steel in different scenarios 

steel_com = exio_hybrid_base.search('Commodity','Basic iron')

p_scenario = {}

for scenario in scenarios: 
    
    p = exio_hybrid_base.get_data(['p'],scenarios=[scenario])[scenario][0].loc[('EU27', sN, steel_com), :]
    
    p_scenario[scenario,
               scenarios_info[scenario]['year']] = p
    
df_p = pd.concat(p_scenario)
df_p.reset_index(inplace=True)

df_p = df_p.rename(columns={'level_0': 'Scenario', 'level_1': 'Year', 'price index': 'Values'})
df_p = df_p.drop(['Region', 'Level'], axis=1)

df_p['Values'] = df_p['Values'].mul(10**6)

#%% Calculating delta_p/delta_f for every scenario with respect to baseline 

delta_fp = {}
delta_f_scenario = {}
delta_p_scenario = {}

baseline_f = df_footprint.loc[df_footprint['Scenario'] == 'baseline', 'Values'].iloc[0]
baseline_p = df_p.loc[df_p['Scenario'] == 'baseline', 'Values'].iloc[0]

scenarios.remove('baseline')

for scenario in scenarios: 
       
    scenario_f = df_footprint.loc[df_footprint['Scenario'] == scenario, 'Values'].iloc[0]
    scenario_p = df_p.loc[df_p['Scenario'] == scenario, 'Values'].iloc[0]
    
    delta_f = abs(scenario_f - baseline_f)
    delta_p = abs(scenario_p - baseline_p)
    
    delta_f_scenario[scenario] = delta_f 
    delta_p_scenario[scenario] = delta_p
    
    delta_fp[scenario] = (delta_p / delta_f) 
    
df_fp = pd.DataFrame.from_dict(delta_fp, orient='index', columns=['delta_fp'])
df_fp.reset_index(inplace=True)

df_fp = df_fp.rename(columns={'index': 'Scenario'})

scenario_names = {
    "Mixed implementation": "GS30-Mix",
    "Delayed implementation": "GS30-Delayed",
    "Increased H2 availability": "GS30-H<sub>2</sub>",
    "REPowerEU": "REPowerEU",
    "Without other technologies": "GS50-Tech",
    "More scrap + Without other technologies": "GS50-Scrap"}

df_fp["Short_Scenario"] = df_fp["Scenario"].apply(lambda x: scenario_names.get(x, x))
df_fp = pd.merge(df_fp, df_p[['Scenario', 'Year']], on='Scenario', how='left')

scenario_color = {'Mixed implementation': '#F79256',
                  'Delayed implementation': '#FBD1A2',
                  'Increased H2 availability': '#7DCFB6',
                  'REPowerEU': 'black',
                  'IEA STEPS': 'black',
                  'Without other technologies': '#00B2CA',
                  'More scrap + Without other technologies': '#1D4E89',
                   }

scenario_marker = {'Mixed implementation': 'circle',
                   'Delayed implementation': 'circle',
                   'Increased H2 availability': 'circle',
                   'REPowerEU': 'x-dot',
                   'IEA STEPS': 'diamond',
                   'Without other technologies': 'circle',
                   'More scrap + Without other technologies': 'circle',
                   }

scenario_names = {
    "Mixed implementation": "GS30-Mix",
    "Delayed implementation": "GS30-Delayed",
    "Increased H2 availability": "GS30-H<sub>2</sub>",
    "REPowerEU": "REPowerEU",
    "Without other technologies": "GS50-Tech",
    "More scrap + Without other technologies": "GS50-Scrap",}


df_fp["Color"] = df_fp["Scenario"].apply(lambda x: scenario_color.get(x, x))
df_fp["Marker"] = df_fp["Scenario"].apply(lambda x: scenario_marker.get(x, x))
df_fp["Short_Scenario"] = df_fp["Scenario"].apply(lambda x: scenario_names.get(x, x))

df_env_transactions['Values'] = df_env_transactions['Values'] / 10**6
df_fp = pd.merge(df_fp, df_env_transactions[['Scenario', 'Values']], on='Scenario', how='left')
df_fp = df_fp.rename(columns={'Values': 'E'})

#%% Plotting E-df/dp 

from plotly.subplots import make_subplots

fig = make_subplots(
    rows=1,
    cols=2,
    column_widths=[4/8, 4/8], 
    shared_yaxes=True,
    subplot_titles=['2030',"2050"],
    x_title= 'Total CO<sub>2</sub> emissions of steel production [Mton]',
    )

for i in df_fp.index:
    if df_fp.loc[i,'Year'] == 2030:
        col = 1
    else:
        col = 2
    fig.add_trace(go.Scatter(
        x=[df_fp.loc[i,'E']],
        y=[df_fp.loc[i,'delta_fp']],
        name=df_fp.loc[i,'Short_Scenario'],
        mode='markers',
        marker=dict(
            size=10,
            color=df_fp.loc[i,'Color'],
            symbol=df_fp.loc[i,'Marker'],
            )
        ),row=1,col=col)

fig.update_layout(
    template='seaborn',
    font=dict(family='Helvetica',size=13),
    yaxis_title='Cost of avoided CO<sub>2</sub> [€/ton<sub>CO<sub>2</sub></sub>]', 
    legend_traceorder='grouped',
    legend_title='Scenario'
    )
fig.show(renderer="browser")
fig.write_html('Plots\Cost avoided CO2.html')

#%% Plotting E-V

V_scenario = {}

for scenario in scenarios: 
    V = exio_hybrid_base.get_data(['V'],scenarios=[scenario])[scenario][0].loc[('Operating surplus: Consumption of fixed capital', ('EU27', sN, steel_act))].sum()
    
    V_scenario[scenario] = V
    
df_V = pd.DataFrame.from_dict(V_scenario, orient='index', columns=['V'])
df_V.reset_index(inplace=True)

df_V = df_V.rename(columns={'index': 'Scenario'})

df_V = pd.merge(df_V, df_env_transactions[['Scenario', 'Values']], on='Scenario', how='left')
df_V = df_V.rename(columns={'Values': 'E'})

df_V["Color"] = df_V["Scenario"].apply(lambda x: scenario_color.get(x, x))
df_V["Marker"] = df_V["Scenario"].apply(lambda x: scenario_marker.get(x, x))
df_V["Short_Scenario"] = df_V["Scenario"].apply(lambda x: scenario_names.get(x, x))
df_V = pd.merge(df_V, df_p[['Scenario', 'Year']], on='Scenario', how='left')


from plotly.subplots import make_subplots

fig = make_subplots(
    rows=1,
    cols=2,
    column_widths=[4/7, 3/7], 
    shared_yaxes=True,
    subplot_titles=['2030',"2050"],
    x_title= 'Total CO<sub>2</sub> emissions of steel production [Mton]',
    )

for i in df_V.index:
    if df_V.loc[i,'Year'] == 2030:
        col = 1
    else:
        col = 2
    fig.add_trace(go.Scatter(
        x=[df_V.loc[i,'E']],
        y=[df_V.loc[i,'V']],
        name=df_V.loc[i,'Short_Scenario'],
        mode='markers',
        marker=dict(
            size=10,
            color=df_V.loc[i,'Color'],
            symbol=df_V.loc[i,'Marker'],
            )
        ),row=1,col=col)

fig.update_layout(
    template='seaborn',
    font=dict(family='Helvetica',size=12),
    yaxis_title='Value added [M€]', 
    legend_traceorder='grouped',
    legend_title='Scenario'
    )
fig.show(renderer="browser")
fig.write_html('Plots\Value added vs CO2.html')

#%% Plotting df-fp

df_delta_f = pd.DataFrame.from_dict(delta_f_scenario, orient='index', columns=['delta_f'])
df_delta_f.reset_index(inplace=True)

df_delta_p = pd.DataFrame.from_dict(delta_p_scenario, orient='index', columns=['delta_p'])
df_delta_p.reset_index(inplace=True)

merged_df = pd.merge(df_delta_f, df_delta_p, on='index')
merged_df = merged_df.rename(columns={'index': 'Scenario'})
merged_df["Color"] = merged_df["Scenario"].apply(lambda x: scenario_color.get(x, x))
merged_df["Marker"] = merged_df["Scenario"].apply(lambda x: scenario_marker.get(x, x))
merged_df["Short_Scenario"] = merged_df["Scenario"].apply(lambda x: scenario_names.get(x, x))
merged_df = pd.merge(merged_df, df_p[['Scenario', 'Year']], on='Scenario', how='left')


from plotly.subplots import make_subplots

fig = make_subplots(
    rows=1,
    cols=2,
    column_widths=[4/8, 4/8], 
    shared_yaxes=True,
    subplot_titles=['2030',"2050"],
    x_title= 'Reduction of European steel CO<sub>2</sub> footprint [ton<sub>CO<sub>2</sub></sub>/ton<sub>steel</sub>]',
    )

for i in merged_df.index:
    if merged_df.loc[i,'Year'] == 2030:
        col = 1
    else:
        col = 2
    fig.add_trace(go.Scatter(
        x=[merged_df.loc[i,'delta_f']],
        y=[merged_df.loc[i,'delta_p']],
        name=merged_df.loc[i,'Short_Scenario'],
        mode='markers',
        marker=dict(
            size=10,
            color=merged_df.loc[i,'Color'],
            symbol=merged_df.loc[i,'Marker'],
            )
        ),row=1,col=col)

fig.update_layout(
    template='seaborn',
    font=dict(family='Helvetica',size=13),
    yaxis_title='Increase of European steel price [€/ton<sub>steel</sub>]', 
    legend_traceorder='grouped',
    legend_title='Scenario',
    #xaxis = dict(range=[0,0.71])
    )
fig.show(renderer="browser")
fig.write_html('Plots\df vs dp.html')



