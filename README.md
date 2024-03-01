**Modelling the decarbonization of steel production sector in Europe with MARIO** 

This repository contains the code and data adopted to characterize new innovative steel production technologies into the Supply-Use EXIOBASE-Hybrid database.
Such database (available on Zenodo at https://zenodo.org/records/10148587) represents the physical transactions of goods and services within the global economy, split into 48 countries and regions.

For this application, MARIO was used to aggregate the world into 6 macro-regions, and to characterize new supply chains for steel production, namely:
 - BF-BOF (traditional route for primary steel)
 - BF-BOF + CCUS
 - H2 injection to BF
 - NG-DR through 100%H2-DR
 - Charcoal injection to BF
 - Charcoal injection to BF + CCUS

To properly account for hydrogen consumption by new steel technologies, the hydrogen supply chain have been also modelled, specifically:
- "Hydrogen" commodity can be produced by two routes, namely steam methane reforming and electrolysis
- "Hydrogen production from steam reforming" activity activates the production of the "Steam reformer" plant commodity, in turn provided by the new "Manufacture of steam reformers" activity
- "Hydrogen production from electrolysis" activity activates the production of the "Electrolyzers" commodity, in turn provided by the new "Manufacture of electrolyzers" activity

The new supply chains have been added according to the matrix augmentation method, basically making the exercise a hybrid-LCA modelling application.
Main references adopted to build the life-cycle inventory of the new supply chains are:
- ...
- ...
 



  
