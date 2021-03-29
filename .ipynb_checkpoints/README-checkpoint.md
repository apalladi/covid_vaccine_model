# SIR 2.0 model accounting for vaccinations 

The epidemiological model used in this library is derived from SIR. It has been called SIR 2.0 and it has been described in https://arxiv.org/abs/2005.08724 .
The free parameters of the model are:
- beta --> speed of spread of the virus;
- gamma --> inverse of time of infection;
- tau --> decay of beta in time, i.e. it is linked to the restrictions

In this code, I added a 4th equation to the 3 original ones that characterize the SIR model (Susceptible, Infected, Removed). The 4th equation concerns the vaccinated people and I assume an efficiency of 95% after people have received the 2nd dose of vaccine (see https://www.nejm.org/doi/full/10.1056/NEJMc2036242)

The original model has been created using 28 days of data, starting from 21th of December 2020, the days in which vaccinations started in Israel. 
In the Jupyter Notebook (israel_SIR.ipynb) two scenarios are shown:
1. lockdown only
2. lockdown plus vaccinations

We note that data subsequent to those used for the fit, i.e. data from mid-January to the end of March, shows a good agreement with the 2nd model (lockdown + vaccinations), while they are far away from the 1st model (lockdown only)


============ ITALIAN ===================

Il modello epidemiologico utilizzato è un derivato del SIR, chiamato SIR 2.0 e descritto in 
I parametri liberi del modello sono:
- beta, legato alla velocità di diffusione del virus
- gamma, legato alla durata media dell'infezione
- tau, legato alle misure di restrizione che determina una diminuzione di beta nel corso del tempo

Alle tre equazioni del SIR (Suscettibili, Infetti, Rimossi) in questo codice è stata aggiunta una 4° equazione relativa ai vaccinati. In particolare si assume per il vaccino un'efficacia del 95% dopo la somministrazione della 2° dose (vedi https://www.nejm.org/doi/full/10.1056/NEJMc2036242)

Il modello originale è stato creato utilizzando 28 giorni di dati, partendo dal 21 Dicembre 2020, giorno in cui sono iniziate le vaccinazioni in Israele. 
Nel Jupyter Notebook (israel_SIR.ipynb) vengono mostrati due scenari:
1. uno con solo lockdown
2. uno con lockdown + vaccini

Si nota che i dati successivi a quelli utilizzati per il fit, ossia i dati da metà Gennaio a fine Marzo, dimostrano un buon accordo col 2° modello (lockdown + vaccinazioni), mentre si discostano in maniera netta dal 1° modello (solo lockdown)