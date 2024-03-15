**Modelling the decarbonization of steel production sector in Europe with MARIO** 

This repository contains the code and data adopted to characterize new innovative steel production technologies into the Supply-Use EXIOBASE-Hybrid database.
Such database (available on Zenodo at https://zenodo.org/records/10148587) represents the physical transactions of goods and services within the global economy, split into 48 countries and regions.

For this application, MARIO was used to aggregate the world into 6 macro-regions, and to characterize new supply chains for steel production, namely:
 - BF-BOF (traditional route for primary steel)
 - BF-BOF + CCUS
 - H2 injection to BF
 - NG-DR 
 - 100%H2-DR
 - Charcoal injection to BF
 - Charcoal injection to BF + CCUS

To properly account for hydrogen consumption by new steel technologies, the hydrogen supply chain have been also modelled, specifically:
- "Steam reforming hydrogen" commodity is produced by "Hydrogen production with steam reforming" activity
- "Electrolysis hydrogen" commodity is produced by "Hydrogen production with electrolysis" activity
- "Hydrogen production with steam reforming" activity activates the production of the "Steam reformer" reactor commodity, in turn provided by the new "Manufacturing of steam reformer" activity
- "Hydrogen production with electrolysis" activity activates the production of the "Electrolyser" commodity, in turn provided by the new "Manufacturing of electrolyser" activity

The new supply chains have been added according to the matrix augmentation method, basically making the exercise a hybrid-LCA modelling application.
Main references adopted to build the life-cycle inventory of the new supply chains are:
- P. L. Spath, "LCA of hydrogen production via natural gas steam reforming"
- P. L. Spath, "LCA of renewable hydrogen production via wind electrolysis"
- J. Tang et al., "Mathematical simulation and LCA of BF operation with H2 injection"
- Cristobal Feliciano-Bruzual, "Charcoal injection in blast furnaces (Bio-PCI): CO2 reduction potential and economic prospects"
- T. Hay, "A Review of Mathematical Process Models for the Electric Arc Furnace Process"
- J. Suer et al., "Carbon Footprint Assessment of Hydrogen and Steel"
 
Life Cycle Inventories of new activities are summarised in "LCI and SUT hydrogen production" for hydrogen technologies and "LCI and SUT steel production" for steel technologies, both contained in the folder "Add_sectors/Life Cycle Inventory". Definition of sensitivity analyses and 2030/2050 scenarios is in Excel files "2030 EU scenarios" and "2050 EU scenarios" in the same folder. 


  
