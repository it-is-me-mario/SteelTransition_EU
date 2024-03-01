# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 15:51:28 2024

@author: debor
"""

import mario
import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go

sN = slice(None)

#%% Importing database with new steel sectors 

import_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\New steel sectors definition" 
exio_hybrid_base = mario.parse_from_txt(import_path+"\\coefficients",table='SUT',mode='coefficients')

#%% Adding "100% H2-DR" and "H2 inj to BF" with 100% green hydrogen and 100% pink hydrogen

# 100% green hydrogen
#exio_hybrid_base.get_shock_excel(r'Shocks\Baseline\100% green hydrogen.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\Baseline\100% green hydrogen.xlsx',z=True,scenario='100% green hydrogen')

# 100% pink hydrogen
#exio_hybrid_base.get_shock_excel(r'Shocks\Baseline\100% pink hydrogen.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\Baseline\100% pink hydrogen.xlsx',z=True,scenario='100% pink hydrogen')


#%% Footprint for each technology + "100% H2-DR" and "H2 inj" with 100% green/pink hydrogen

# Calculating footprint for each technology with aggregation on activities  
aggregation_file_path = "\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Aggregations\\Aggregation activities_graph.xlsx"
aggregation_df = pd.read_excel(aggregation_file_path)

activity_mapping = dict(zip(aggregation_df['Unnamed: 0'], aggregation_df['Aggregation']))

scenarios = {'baseline','100% green hydrogen', '100% pink hydrogen'}
column_steel_act = exio_hybrid_base.search('Activity','Steel')


foot_tech_H2 = {}

for scenario in scenarios:
    
        e_CO2_H2 = exio_hybrid_base.get_data(['e'],scenarios=[scenario])[scenario][0].loc[('CO2'), :]             
        
        w_H2 = exio_hybrid_base.get_data(['w'],scenarios=[scenario])[scenario][0]
        
        f_steel_H2 = np.diag(e_CO2_H2) @ w_H2
        f_steel_H2.index=f_steel_H2.columns
        f_steel_act_H2 = f_steel_H2.loc[:,('EU27', 'Activity', column_steel_act)]
        
        f_steel_act_agg_H2 = f_steel_act_H2.groupby(activity_mapping, level='Item').sum()     
                       
        foot_tech_H2[scenario] = f_steel_act_agg_H2
                      
       
df_foot_tech_H2 = pd.concat(foot_tech_H2, axis=1)
df_foot_tech_H2.columns.names = ['Scenario', 'Region', 'Level', 'None']

df_f_stack = df_foot_tech_H2.stack('Scenario')
df_f_stack = df_f_stack.stack('Region')
df_f_stack = df_f_stack.stack('Level')
df_f_stack = df_f_stack.stack('None')

df_foot_tech_H2 = df_f_stack.reset_index()
df_foot_tech_H2 = df_foot_tech_H2.rename(columns={'Item': 'Activity', 'None': 'Item', 0:'Values'})
df_foot_tech_H2.drop(columns=['Level', 'Region'], inplace=True)

# Removing technologies without H2 from 100% green/pink hydrogen scenarios 
df_foot_tech_H2 = df_foot_tech_H2[
    ((df_foot_tech_H2["Item"].isin(["Steel production with H2 inj to BF", "Steel production through 100%H2-DR"])) &
    (df_foot_tech_H2["Scenario"].isin(["100% green hydrogen", "100% pink hydrogen"]))) |
    (df_foot_tech_H2["Scenario"] == "baseline")
]

# Changing the name of H2 technologies for 100% green/pink hydrogen scenarios 
df_foot_tech_H2.loc[(df_foot_tech_H2["Scenario"] == "100% green hydrogen") &
                    (df_foot_tech_H2["Item"] == "Steel production through 100%H2-DR"),
                    "Item"] = "Steel production through 100%H2-DR-GH"

df_foot_tech_H2.loc[(df_foot_tech_H2["Scenario"] == "100% green hydrogen") &
                    (df_foot_tech_H2["Item"] == "Steel production with H2 inj to BF"),
                    "Item"] = "Steel production with H2 inj to BF-GH"

df_foot_tech_H2.loc[(df_foot_tech_H2["Scenario"] == "100% pink hydrogen") &
                    (df_foot_tech_H2["Item"] == "Steel production through 100%H2-DR"),
                    "Item"] = "Steel production through 100%H2-DR-PH"

df_foot_tech_H2.loc[(df_foot_tech_H2["Scenario"] == "100% pink hydrogen") &
                    (df_foot_tech_H2["Item"] == "Steel production with H2 inj to BF"),
                    "Item"] = "Steel production with H2 inj to BF-PH"

# Plot
from plotly.subplots import make_subplots

activities = df_foot_tech_H2["Activity"].unique()[::-1]

tech_names = {
    "Manufacture of basic iron and steel and of ferro-alloys and first products thereof": "BF-BOF",
    "Re-processing of secondary steel into new steel": "EAF",
    "Steel production through 100%H2-DR": "100%<br>H<sub>2</sub>-DR",
    "Steel production through NG-DR": "NG-DR<br>",
    "Steel production with BF-BOF + CCUS": "BF-BOF<br>+ CCUS",
    "Steel production with H2 inj to BF": "H<sub>2</sub> inj<br>",
    "Steel production with charcoal inj to BF": "Charcoal<br>inj<br>",
    "Steel production with charcoal inj to BF + CCUS": "Charcoal<br>inj+ CCUS",
    "Steel production through 100%H2-DR-GH": "100% H<sub>2</sub>-DR<br>-GH",
    "Steel production through 100%H2-DR-PH": "100% H<sub>2</sub>-DR<br>-PH",
    "Steel production with H2 inj to BF-GH": "H<sub>2</sub> inj<br>-GH",
    "Steel production with H2 inj to BF-PH": "H<sub>2</sub> inj<br>-PH",    
    }

activity_colors = {
    "Agriculture": "#f94144",
    "Electricity production and transmission": "#fb8500",
    "Hydrogen production": "#ffb703",
    "Manufacturing and processing activities": "#fae588",  
    "Mining and extraction activities; metals production": "#d3d3d3",
    "Re-processing of secondary steel into new steel": "#83c5be",
    "Services and transport activities": "#99d98c",
    "Steel production": "#219ebc", 
    "Waste treatment and recycling activities": "#1b4332"
    }


fig= go.Figure()
fig = make_subplots(
    rows=1,
    cols=3,
    column_widths=[8/14, 3/14, 3/14], 
    shared_yaxes=True,
    subplot_titles=['(a)',"(b)","(c)"],
    )

desired_order = ['Manufacture of basic iron and steel and of ferro-alloys and first products thereof', 'Steel production with BF-BOF + CCUS',  
                 'Steel production with charcoal inj to BF', 'Steel production with charcoal inj to BF + CCUS', 'Steel production with H2 inj to BF',
                 'Steel production through NG-DR', 'Steel production through 100%H2-DR',
                 'Re-processing of secondary steel into new steel'
 ]

# Create a sorting key based on the desired order
sorting_key = {item: index for index, item in enumerate(desired_order)}

def get_sorting_key(item):
    return sorting_key.get(item, float('inf'))

for activity in activities:
   
    # Filtering data for footprint by technology in baseline scenario 
    baseline_df = df_foot_tech_H2.query(f"Activity == '{activity}' and Scenario == 'baseline'").copy()
    baseline_df.loc[:, "Short_Tech"] = baseline_df["Item"].apply(lambda x: tech_names.get(x, x))
        
    baseline_df['sorting_key'] = baseline_df['Item'].apply(get_sorting_key)
    baseline_df = baseline_df.sort_values(by='sorting_key').drop(columns='sorting_key')
    
    color = activity_colors.get(activity)
    
    # First subplot (baseline)
    fig.add_trace(
        go.Bar(
            x=baseline_df["Short_Tech"],
            y=baseline_df["Values"],
            name=f"{activity}",
            marker_color=color,
            legendgroup=f"{activity}",
        ),
        row=1, col=1
    )
    
    # Filtering data for footprint "100% H2-DR" in all scenarios 
    H2DR_df = df_foot_tech_H2.query(f"Activity == '{activity}' and Item in ['Steel production through 100%H2-DR', 'Steel production through 100%H2-DR-GH', 'Steel production through 100%H2-DR-PH']").copy()[::-1]
    H2DR_df.loc[:, "Short_Tech"] = H2DR_df["Item"].apply(lambda x: tech_names.get(x, x))
             
    # Second subplot (100% H2-DR)
    fig.add_trace(
        go.Bar(
            x=H2DR_df["Short_Tech"],
            y=H2DR_df["Values"],
            name=f"{activity}",
            marker_color=color,
            showlegend = False,
            legendgroup=f"{activity}",
        ),
        row=1, col=2
    )    

    
    # Filtering data for footprint "H2 inj" in all scenarios 
    H2inj_df = df_foot_tech_H2.query(f"Activity == '{activity}' and Item in ['Steel production with H2 inj to BF', 'Steel production with H2 inj to BF-GH', 'Steel production with H2 inj to BF-PH']").copy()[::-1]
    H2inj_df.loc[:, "Short_Tech"] = H2inj_df["Item"].apply(lambda x: tech_names.get(x, x))
             
    # Third subplot (H2 inj)
    fig.add_trace(
        go.Bar(
            x=H2inj_df["Short_Tech"],
            y=H2inj_df["Values"],
            name=f"{activity}",
            marker_color=color,
            showlegend = False,
            legendgroup=f"{activity}",
        ),
        row=1, col=3
    )   
   
        
fig.update_layout(title=dict(
                  text="CO<sub>2</sub> footprint of European steel for each technology",
                  x=0.27, 
                  ),
                  barmode='stack',
                  legend_traceorder='reversed',
                  legend_title='Activity',
                  xaxis_tickangle=0,                  
                  template="plotly_white",
                  font_family="Helvetica",
                  font_size=12, 
                  legend=dict(
                  orientation="h",  
                  y=-0.3, 
                  xanchor="left",
                  yanchor="top",
                  )                                 
                 )

custom_tick_labels = ["H<sub>2</sub> mix<br>Baseline", "Pink H<sub>2</sub>", "Green H<sub>2</sub>"]

fig.update_xaxes(title_text="All technologies | Baseline", ticktext=custom_tick_labels, row=1, col=1)                      
fig.update_xaxes(title_text="100% H<sub>2</sub>-DR", tickvals=list(range(len(custom_tick_labels))), ticktext=custom_tick_labels, row=1, col=2)
fig.update_xaxes(title_text="H<sub>2</sub> inj", tickvals=list(range(len(custom_tick_labels))), ticktext=custom_tick_labels, row=1, col=3)

fig.update_yaxes(title_text="ton<sub>CO<sub>2</sub></sub>/ton<sub>steel</sub>",
                  range=[0, 2.05],
                  row=1, col=1)


fig.show(renderer="browser")  
fig.write_html('Plots\Footprint by technology + H2.html')    

#%% 2030 SCENARIOS

# Mixed implementation
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios\Mixed implementation.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios\Mixed implementation.xlsx',z=True,scenario='Mixed implementation')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios\\Mixed implementation" 
exio_hybrid_base.to_txt(export_path, scenario='Mixed implementation', coefficients=True, flows=False)


# Delayed implementation
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios\Delayed implementation.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios\Delayed implementation.xlsx',z=True,scenario='Delayed implementation')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios\\Delayed implementation" 
exio_hybrid_base.to_txt(export_path, scenario='Delayed implementation', coefficients=True, flows=False)


# Increased H2 availability
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios\Increased H2 availability.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios\Increased H2 availability.xlsx',z=True,scenario='Increased H2 availability')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios\\Increased H2 availability" 
exio_hybrid_base.to_txt(export_path, scenario='Increased H2 availability', coefficients=True, flows=False)


# REPowerEU
#exio_hybrid_base.get_shock_excel(r'Shocks\2030 scenarios\REPowerEU.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2030 scenarios\REPowerEU.xlsx',z=True,scenario='REPowerEU')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2030 scenarios\\REPowerEU" 
exio_hybrid_base.to_txt(export_path, scenario='REPowerEU', coefficients=True, flows=False)


#%% 2050 SCENARIOS

# Without other technologies
#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios\Without other technologies.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios\Without other technologies.xlsx',z=True,scenario='Without other technologies')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios\\Without other technologies" 
exio_hybrid_base.to_txt(export_path, scenario='Without other technologies', coefficients=True, flows=False)


# More scrap + Without other technologies (also known as Increased scrap availability)
#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios\More scrap + Without other technologies.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios\More scrap + Without other technologies.xlsx',z=True,scenario='More scrap + Without other technologies')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios\\More scrap + Without other technologies" 
exio_hybrid_base.to_txt(export_path, scenario='More scrap + Without other technologies', coefficients=True, flows=False)


# IEA STEPS
#exio_hybrid_base.get_shock_excel(r'Shocks\2050 scenarios\IEA STEPS.xlsx')
exio_hybrid_base.shock_calc(r'Shocks\2050 scenarios\IEA STEPS.xlsx',z=True,scenario='IEA STEPS')

export_path = r"\\".join(os.getcwd().split("\\")[:-1])+"\\IAM-COMPACT\\Output\\Results\\2050 scenarios\\IEA STEPS" 
exio_hybrid_base.to_txt(export_path, scenario='IEA STEPS', coefficients=True, flows=False)


#%% PLOTS

# Definition of scenarios, markers and colors for plots
import plotly.graph_objects as go

scenarios = exio_hybrid_base.scenarios
scenarios.remove('100% green hydrogen')
scenarios.remove('100% pink hydrogen')
             
scenario_info = {
    'baseline': {'year': 2022, 'sensitivity': 'No sensitivity'},
    'Mixed implementation': {'year': 2030, 'sensitivity': 'No sensitivity'},
    'Delayed implementation': {'year': 2030, 'sensitivity': 'No sensitivity'},
    'Increased H2 availability': {'year': 2030, 'sensitivity': 'No sensitivity'},
    'REPowerEU': {'year': 2030, 'sensitivity': 'No sensitivity'},
    'Without other technologies': {'year': 2050, 'sensitivity': 'No sensitivity'},
    'More scrap + Without other technologies': {'year': 2050, 'sensitivity': 'No sensitivity'},
    'IEA STEPS': {'year': 2050, 'sensitivity': 'No sensitivity'},}
    
scenario_names = {
    "Mixed implementation": "GS30-Mix",
    "Delayed implementation": "GS30-Delayed",
    "Increased H2 availability": "GS30-H<sub>2</sub>",
    "REPowerEU": "REPowerEU",
    "Without other technologies": "GS50-Tech",
    "More scrap + Without other technologies": "GS50-Scrap",}
    
scenario_marker = {'Mixed implementation': 'circle',
                   'Delayed implementation': 'circle',
                   'Increased H2 availability': 'circle',
                   'REPowerEU': 'x-dot',
                   'IEA STEPS': 'diamond',
                   'Without other technologies': 'circle',
                   'More scrap + Without other technologies': 'circle',
                   }

scenario_color = {'Mixed implementation': '#F79256',
                  'Delayed implementation': '#FBD1A2',
                  'Increased H2 availability': '#7DCFB6',
                  'REPowerEU': 'black',
                  'IEA STEPS': 'black',
                  'Without other technologies': '#00B2CA',
                  'More scrap + Without other technologies': '#1D4E89',
                   }

#%% Plotting E by scenario from 2022 to 2050

# Dataframe for E
env_transactions = {}

steel_act = exio_hybrid_base.search('Activity','Steel')

for scenario in scenarios :
       
    E = exio_hybrid_base.get_data(['E'],scenarios=[scenario])[scenario][0].loc['CO2',('EU27',sN,steel_act)]
    
    E_df = pd.DataFrame(E)
    
    E = E_df.squeeze(axis=1)
                    
    env_transactions[scenario_info[scenario]['year'],
              scenario_info[scenario]['sensitivity'],
              scenario] = E
    
        
df_env_transactions = pd.DataFrame(env_transactions).sum()
df_env_transactions = df_env_transactions.rename_axis(index=['Year', 'Sensitivity', 'Scenario']).reset_index()

df_env_transactions = df_env_transactions.rename(columns={0: 'Values'})
df_env_transactions["Short_Scenario"] = df_env_transactions["Scenario"].apply(lambda x: scenario_names.get(x, x))


# Identifying points to be displayed on the graph 
baseline_2022_env = df_env_transactions[(df_env_transactions['Scenario'] == 'baseline')]
mix_2030_env = df_env_transactions[(df_env_transactions['Scenario'] == 'Mixed implementation')]
delayed_2030_env = df_env_transactions[(df_env_transactions['Scenario'] == 'Delayed implementation')]
REP_2030_env = df_env_transactions[(df_env_transactions['Scenario'] == 'REPowerEU')]
more_2050_env = df_env_transactions[(df_env_transactions['Scenario'] == 'More scrap + Without other technologies')]
tech_2050_env = df_env_transactions[(df_env_transactions['Scenario'] == 'Without other technologies')]
IEA_STEPS_2050_env = df_env_transactions[(df_env_transactions['Scenario'] == 'IEA STEPS')]


# Plots
fig = go.Figure()

# E plot
fig.add_traces([
    go.Scatter(x=[baseline_2022_env["Year"].iloc[0], mix_2030_env["Year"].iloc[0]],
                         y=[baseline_2022_env["Values"].iloc[0], mix_2030_env["Values"].iloc[0]],
                         mode='lines',
                         line=dict(color='grey', width=0.5),
                         showlegend=False),
    go.Scatter(x=[baseline_2022_env["Year"].iloc[0], mix_2030_env["Year"].iloc[0]],
                         y=[baseline_2022_env["Values"].iloc[0], delayed_2030_env["Values"].iloc[0]],
                         fill='tonexty',
                         fillcolor = 'rgba(128,128,128,0.2)',
                         mode='none',
                         showlegend=False),
    go.Scatter(x=[baseline_2022_env["Year"].iloc[0], delayed_2030_env["Year"].iloc[0]],
                         y=[baseline_2022_env["Values"].iloc[0], delayed_2030_env["Values"].iloc[0]],
                         mode='lines',
                         line=dict(color='grey', width=0.5),
                         showlegend=False),
    go.Scatter(x=[mix_2030_env["Year"].iloc[0], more_2050_env["Year"].iloc[0]],
                         y=[mix_2030_env["Values"].iloc[0], more_2050_env["Values"].iloc[0]],
                         mode='lines',
                         line=dict(color='grey', width=0.5),
                         showlegend=False),
    go.Scatter(x=[delayed_2030_env["Year"].iloc[0], more_2050_env["Year"].iloc[0]],
                         y=[delayed_2030_env["Values"].iloc[0], tech_2050_env["Values"].iloc[0]],
                         fill='tonexty',
                         fillcolor = 'rgba(128,128,128,0.2)',
                         mode='none',
                         showlegend=False),
    go.Scatter(x=[delayed_2030_env["Year"].iloc[0], tech_2050_env["Year"].iloc[0]],
                         y=[delayed_2030_env["Values"].iloc[0], tech_2050_env["Values"].iloc[0]],
                         mode='lines',
                         line=dict(color='grey', width=0.5),
                         showlegend=False),
    go.Scatter(x=[baseline_2022_env["Year"].iloc[0], IEA_STEPS_2050_env["Year"].iloc[0]],
                         y=[baseline_2022_env["Values"].iloc[0], IEA_STEPS_2050_env["Values"].iloc[0]],
                         mode='lines',
                         line=dict(color='black', dash='dot'),
                         showlegend=False),
    go.Scatter(x=[baseline_2022_env["Year"].iloc[0], REP_2030_env["Year"].iloc[0]],
                         y=[baseline_2022_env["Values"].iloc[0], REP_2030_env["Values"].iloc[0]],
                         mode='lines',
                         line=dict(color='black', dash='dot'),
                         showlegend=False),
    go.Scatter(x=[2022, 2022],y=[0, baseline_2022_env["Values"].iloc[0]],
                         mode="lines",
                         line=go.scatter.Line(color="black", dash="dot", width=0.5),
                         showlegend=False),
    go.Scatter(x=[2030, 2030],y=[0, delayed_2030_env["Values"].iloc[0]],
                         mode="lines",
                         line=go.scatter.Line(color="black", dash="dot", width=0.5),
                         showlegend=False),
    go.Scatter(x=[2050, 2050],y=[0, IEA_STEPS_2050_env["Values"].iloc[0]],
                         mode="lines",
                         line=go.scatter.Line(color="black", dash="dot", width=0.5),
                         showlegend=False)
    ])

# Adding markers on years for E plot
legend_order = ['GS50-Scrap', 'GS50-Tech', 'GS30-H<sub>2</sub>', 'GS30-Delayed', 'GS30-Mix', 'invisible_line', 'REPowerEU', 'IEA STEPS']

for scenario in legend_order:
    if scenario == 'invisible_line':
        
        fig.add_traces([go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(color='rgba(255, 255, 255, 0)'),  
            name=' ',  
            showlegend=True,
        )])
    
    else:
        
        scenario_data = df_env_transactions[df_env_transactions['Short_Scenario'] == scenario]
        marker = scenario_marker.get(scenario)
        color = scenario_color.get(scenario)
    
        fig.add_traces([go.Scatter(x=scenario_data["Year"], y=scenario_data["Values"],
                             mode='markers',
                             name=scenario,
                             marker=dict(symbol=marker, color=color, size=7),
                             line=dict(color=color))]
                      )

tick_positions = list(range(2020, 2051, 5))  
tick_positions.append(2022)  

fig.update_layout(title=dict(
                  text="CO<sub>2</sub> emissions of European steel sector by scenario",
                  x=0.47),
                  xaxis=dict(  
                      tickvals=tick_positions, 
                      range=[2021, 2051]
                  ),
                  yaxis_title="ton<sub>CO<sub>2</sub></sub>", 
                  yaxis=dict(
                      range=[0,300000000]),
                  template="plotly_white",
                  font_family="Helvetica",
                  font_size=13,
                  #width=1000,
                  legend_title='Scenario'
                  )


fig.show(renderer="browser")
fig.write_html('Plots\Emissions 2022-2050.html')

#%% Plotting f by scenario from 2022 to 2050

row_steel_com = exio_hybrid_base.search('Commodity','Basic iron and steel')

footprint = {}


for scenario in scenarios :
       
    f_steel_act = exio_hybrid_base.get_data(['f'],scenarios=[scenario])[scenario][0].loc[('CO2'),('EU27',sN,row_steel_com)]
                    
    footprint[scenario_info[scenario]['year'],
              scenario,
              scenario_info[scenario]['sensitivity']] = f_steel_act
    
   
df_footprint = pd.DataFrame(footprint)
df_footprint.columns.names = ['Year', 'Scenario', 'Sensitivity']

df_f_stack = df_footprint.stack('Year')
df_f_stack = df_f_stack.stack('Scenario')
df_f_stack = df_f_stack.stack('Sensitivity')

df_footprint = df_f_stack.reset_index()
df_footprint = df_footprint.drop(['Item', 'Level'], axis=1)

df_footprint = df_footprint.rename(columns={0: 'Values'})
df_footprint["Short_Scenario"] = df_footprint["Scenario"].apply(lambda x: scenario_names.get(x, x))


# Identifying points to be displayed on the graph 
baseline_2022 = df_footprint[(df_footprint['Scenario'] == 'baseline')]
mix_2030 = df_footprint[(df_footprint['Scenario'] == 'Mixed implementation')]
delayed_2030 = df_footprint[(df_footprint['Scenario'] == 'Delayed implementation')]
REP_2030 = df_footprint[(df_footprint['Scenario'] == 'REPowerEU')]
more_2050 = df_footprint[(df_footprint['Scenario'] == 'More scrap + Without other technologies')]
tech_2050 = df_footprint[(df_footprint['Scenario'] == 'Without other technologies')]
IEA_STEPS_2050 = df_footprint[(df_footprint['Scenario'] == 'IEA STEPS')]


# Plot
fig = go.Figure()

fig.update_traces(line=dict(width=1.5), selector=dict(mode='lines', line_color='grey'))

# Adding lines for Green Steel scenarios and colored area
fig.add_trace(go.Scatter(x=[baseline_2022["Year"].iloc[0], mix_2030["Year"].iloc[0]],
                         y=[baseline_2022["Values"].iloc[0], mix_2030["Values"].iloc[0]],
                         mode='lines',
                         line=dict(color='grey', width=0.5),
                         showlegend=False))

fig.add_trace(go.Scatter(x=[baseline_2022["Year"].iloc[0], mix_2030["Year"].iloc[0]],
                         y=[baseline_2022["Values"].iloc[0], delayed_2030["Values"].iloc[0]],
                         fill='tonexty',
                         fillcolor = 'rgba(128,128,128,0.2)',
                         mode='none',
                         showlegend=False))

fig.add_trace(go.Scatter(x=[baseline_2022["Year"].iloc[0], delayed_2030["Year"].iloc[0]],
                         y=[baseline_2022["Values"].iloc[0], delayed_2030["Values"].iloc[0]],
                         mode='lines',
                         line=dict(color='grey', width=0.5),
                         showlegend=False))


fig.add_trace(go.Scatter(x=[mix_2030["Year"].iloc[0], more_2050["Year"].iloc[0]],
                         y=[mix_2030["Values"].iloc[0], more_2050["Values"].iloc[0]],
                         mode='lines',
                         line=dict(color='grey', width=0.5),
                         showlegend=False))

fig.add_trace(go.Scatter(x=[delayed_2030["Year"].iloc[0], more_2050["Year"].iloc[0]],
                         y=[delayed_2030["Values"].iloc[0], tech_2050["Values"].iloc[0]],
                         fill='tonexty',
                         fillcolor = 'rgba(128,128,128,0.2)',
                         mode='none',
                         showlegend=False))

fig.add_trace(go.Scatter(x=[delayed_2030["Year"].iloc[0], tech_2050["Year"].iloc[0]],
                         y=[delayed_2030["Values"].iloc[0], tech_2050["Values"].iloc[0]],
                         mode='lines',
                         line=dict(color='grey', width=0.5),
                         showlegend=False))


# Adding dotted lines for IEA and REPowerEU
fig.add_trace(go.Scatter(x=[baseline_2022["Year"].iloc[0], IEA_STEPS_2050["Year"].iloc[0]],
                         y=[baseline_2022["Values"].iloc[0], IEA_STEPS_2050["Values"].iloc[0]],
                         mode='lines',
                         line=dict(color='black', dash='dot'),
                         showlegend=False))


fig.add_trace(go.Scatter(x=[baseline_2022["Year"].iloc[0], REP_2030["Year"].iloc[0]],
                         y=[baseline_2022["Values"].iloc[0], REP_2030["Values"].iloc[0]],
                         mode='lines',
                         line=dict(color='black', dash='dot'),
                         showlegend=False))


# Adding dotted lines for years
fig.add_trace(
    go.Scatter(
        x=[2022, 2022],y=[0, baseline_2022["Values"].iloc[0]],
        mode="lines",
        line=go.scatter.Line(color="black", dash="dot", width=0.5),
        showlegend=False))

fig.add_trace(
    go.Scatter(
        x=[2030, 2030],y=[0, delayed_2030["Values"].iloc[0]],
        mode="lines",
        line=go.scatter.Line(color="black", dash="dot", width=0.5),
        showlegend=False))

fig.add_trace(
    go.Scatter(
        x=[2050, 2050],y=[0, IEA_STEPS_2050["Values"].iloc[0]],
        mode="lines",
        line=go.scatter.Line(color="black", dash="dot", width=0.5),
        showlegend=False))



# Adding markers on years
legend_order = ['GS50-Scrap', 'GS50-Tech', 'GS30-H<sub>2</sub>', 'GS30-Delayed', 'GS30-Mix', 'invisible_line', 'REPowerEU', 'IEA STEPS']

for scenario in legend_order:
    if scenario == 'invisible_line':
        
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(color='rgba(255, 255, 255, 0)'),  
            name=' ',  
            showlegend=True,  
        ))
    
    else:
        
        scenario_data = df_footprint[df_footprint['Short_Scenario'] == scenario]
        marker = scenario_marker.get(scenario)
        color = scenario_color.get(scenario)
    
        fig.add_trace(go.Scatter(x=scenario_data["Year"], y=scenario_data["Values"],
                             mode='markers',
                             name=scenario,
                             marker=dict(symbol=marker, color=color, size=7),
                             line=dict(color=color)))


tick_positions = list(range(2020, 2051, 5))  
tick_positions.append(2022)  

fig.update_layout(title=dict(
                  text="CO<sub>2</sub> footprint of European steel by scenario",
                  x=0.47),
                  xaxis=dict(  
                      tickvals=tick_positions, 
                      range=[2021, 2051]
                  ),
                  yaxis_title="ton<sub>CO<sub>2</sub></sub>/ton<sub>steel</sub>", 
                  yaxis=dict(
                      range=[0,1.3]),
                  template="plotly_white",
                  font_family="Helvetica",
                  font_size=13,
                  #width=1000,
                  legend_title='Scenario'
                  )


fig.show(renderer="browser")
fig.write_html('Plots\Footprint 2022-2050.html')
