# Modello SIR 2.0 con l'aggiunta delle vaccinazioni

Il modello epidemiologico utilizzato è un derivato del SIR, chiamato SIR 2.0 e descritto in https://arxiv.org/abs/2005.08724 
I parametri liberi del modello sono:
- beta, legato alla velocità di diffusione del virus
- gamma, legato alla durata media dell'infezione
- tau, legato alle misure di restrizione che determina una diminuzione di beta nel corso del tempo

Alle tre equazioni del SIR (Suscettibili, Infetti, Rimossi) in questo codice è stata aggiunta una 4° equazione relativa ai vaccinati. In particolare si assume per il vaccino un'efficacia del 95% dopo la somministrazione della 2° dose (vedi https://www.nejm.org/doi/full/10.1056/NEJMc2036242)

Il modello originale è stato creato utilizzando 27 giorni di dati, partendo dal 21 Dicembre 2020, giorno in cui sono iniziate le vaccinazioni in Israele. 
Nel Jupyter Notebook (israel_SIR.ipynb) vengono mostrati due scenari:
1. uno con solo lockdown
2. uno con lockdown + vaccini

Si nota che i dati successivi a quelli utilizzati per il fit, ossia i dati da metà Gennaio a fine Marzo, dimostrano un buon accordo col 2° modello (lockdown + vaccinazioni), mentre si discostano in maniera netta dal 1° modello (solo lockdown)
