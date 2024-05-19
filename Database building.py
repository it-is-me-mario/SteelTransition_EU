#%% CELL 1: Importing dependencies and setting up the environment
import mario
import pandas as pd
from Support import add_new_supply_chains

nowcasting_year = 2022
path_exiobase = "Database/Exiobase HYBRID 2011"

#%% CELL 2: Parsing Exiobase data
world = mario.parse_from_txt(path=path_exiobase, table='SUT', mode='flows')

#%% CELL 3: nowcasting electricity mixes with Ember data (https://ember-climate.org/data/data-tools/data-explorer)
#   step 1: aggregate electricity commodities and activities to match Ember
world.aggregate("Aggregations/1. Nowcasting.xlsx",ignore_nan=True)

#%% CELL 4: nowcasting electricity mixes with Ember data (https://ember-climate.org/data/data-tools/data-explorer)
# step 2: parse Ember data, already aggregated matching Exiobase regions 
ee_mixes = pd.read_excel("Database/Ember - data/EE mixes Ember-Exiobase.xlsx" ,sheet_name=str(nowcasting_year),index_col=[0])

# step 3: appyling changes to use matrix
z = world.z
u = world.u
Y = world.Y

for region in ee_mixes.index:
    new_mix = ee_mixes.loc[region,:].to_frame().sort_index(level=0)
    
    # update u
    u_ee = u.loc[(region,slice(None),list(ee_mixes.columns)),:]
    u_ee.sort_index(level=-1,inplace=True) 
    u_ee_sum = u_ee.sum().to_frame().T
    new_u_ee = pd.DataFrame(new_mix.values @ u_ee_sum.values, index=u_ee.index, columns=u_ee.columns)
    u.update(new_u_ee)
    
    # update Y
    Y_ee = Y.loc[(region,'Commodity',list(ee_mixes.columns)),:]
    Y_ee.sort_index(level=-1,inplace=True) 
    Y_ee_sum = Y_ee.sum().to_frame().T
    new_Y_ee = pd.DataFrame(new_mix.values @ Y_ee_sum.values, index=Y_ee.index, columns=Y_ee.columns)
    Y.update(new_Y_ee)
    
z.update(u)

# step 4: update mario database  
world.update_scenarios('baseline',z=z,Y=Y)
world.reset_to_coefficients('baseline')

#%% CELL 5: aggregating regions and electricity commodities furthermore
world.aggregate("Aggregations/2. Regions&EE.xlsx",ignore_nan=True)

#%% CELL 6: splitting "BF-BOF" to disjoint its byproducts from the main product
new_activity = 'Blast furnace gas production'
main_activity = 'Manufacture of basic iron and steel and of ferro-alloys and first products thereof' 
by_products = ['Blast Furnace Gas', 'Oxygen Steel Furnace Gas']

world.add_sectors(
    "Add sectors/1. Disjoint BF-BOF by-products.xlsx", 
    new_sectors=[new_activity], 
    regions=world.get_index('Region'),
    item='Activity',
    )

z = world.z
e = world.e
v = world.v

for region in world.get_index('Region'):
    z.loc(axis=1)[region,'Activity',new_activity] = z.loc(axis=1)[region,'Activity',main_activity]
    e.loc(axis=1)[region,'Activity',new_activity] = e.loc(axis=1)[region,'Activity',main_activity] 
    v.loc(axis=1)[region,'Activity',new_activity] = v.loc(axis=1)[region,'Activity',main_activity] 

world.update_scenarios(scenario='baseline',z=z, e=e, v=v)
world.reset_to_coefficients('baseline')

# changing emissions of the two sectors
e = world.e
s = world.s
z = world.z
for region in world.get_index('Region'):

    # null ghgs emissions for "Blast furnace gas production" and doubled for "Manufacture of basic iron"
    e_cols_new  = e.loc[:,(region,slice(None),new_activity)]*0
    e_cols_main = e.loc[:,(region,slice(None),main_activity)]*2

    e.update(e_cols_new) 
    e.update(e_cols_main) 

    # removing production of "Blast furnace gas" and "Oxygen steel furnace gas" from "Manufacture of basic iron"
    s_byprod = s.loc[(region,'Activity',main_activity),(region,'Commodity',by_products)]*0
    s.update(s_byprod)
    
    # adding production of "Blast furnace gas" and "Oxygen steel furnace gas" to "Blast furnace gas production"
    s_newprod = s.loc[(region,'Activity',new_activity),(region,'Commodity',by_products)]
    s_newprod += 1
    s.update(s_newprod)   

z.update(s)
world.update_scenarios('baseline',z=z,e=e)
world.reset_to_coefficients('baseline')


#%% CELL 7: adding new supply chains
paths_new_supply_chains = {
    'Map': r'Add sectors/2. New supply chains - Map.xlsx',
    'commodities': r'Add sectors/2. New supply chains - Commodities.xlsx',
    'activities': r'Add sectors/2. New supply chains - Activities.xlsx',
    'values': r'Add sectors/2. New supply chains - Values.xlsx',
    }

add_new_supply_chains(
    paths = paths_new_supply_chains, 
    main_sheet='main', 
    world=world,
    add_sectors_template=True,
    )

# %%
