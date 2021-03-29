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

In the Notebook italy_1wave.ipynb the model for the 1st wave in Italy is shown. This model reaches an average accuracy of about 6% on the 3 categories (Susceptible, Infected, Removed)