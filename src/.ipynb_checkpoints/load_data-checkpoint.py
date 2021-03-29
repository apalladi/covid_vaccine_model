import pandas as pd
import numpy as np


# media mobile
def moving_avg(array,window=7):
    array_m = [array[0]]*(window)
    ll = len(array)
    for i in range(ll-(window-1)):
        array_m.append(np.mean(array[i:i+window]))
    return np.array(array_m)


def get_epidemic_data(country):
    # source Johns Hopkins Unversity
    
    file_confirmed='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    file_deaths='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    file_recovered='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

    df_confirmed=pd.read_csv(file_confirmed)
    df_deaths=pd.read_csv(file_deaths)
    df_recovered=pd.read_csv(file_recovered)
    date = pd.to_datetime(df_confirmed.columns[4:])
    
    ydata_cases = np.sum(np.array(df_confirmed[df_confirmed['Country/Region']==country].iloc[:,4:]),axis=0)
    ydata_deaths = np.sum(np.array(df_deaths[df_deaths['Country/Region']==country].iloc[:,4:]),axis=0)
    ydata_rec = np.sum(np.array(df_recovered[df_recovered['Country/Region']==country].iloc[:,4:]),axis=0)
    ydata_inf = ydata_cases-ydata_deaths-ydata_rec   
    daily_cases = np.around(moving_avg(np.diff(ydata_cases)),1)
    daily_deaths = np.around(moving_avg(np.diff(ydata_deaths)),1)
    
    df_epidemic = pd.DataFrame(np.transpose([ydata_cases,ydata_inf,ydata_deaths,ydata_rec,daily_cases,daily_deaths]))
    df_epidemic.index = date
    df_epidemic.columns = ['Total cases','Active infected','Total deaths','Total recovered','Daily cases (avg 7 days)','Daily deaths (avg 7 days)']
    
    return df_epidemic


def get_vaccine_data(country):
    # source ourworldindata

    df_vacc = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv')
    df_vacc = df_vacc.fillna(0)
    
    df_vacc_country = df_vacc[df_vacc['location']==country].iloc[2:,:]
    
    date = pd.to_datetime(df_vacc_country['date'])
    vacc1 = np.array(df_vacc_country['people_vaccinated_per_hundred'])  
    vacc2 = np.array(df_vacc_country['people_fully_vaccinated_per_hundred']) 
    
    df_vacc_new = pd.DataFrame(np.transpose([vacc1,vacc2]))
    df_vacc_new.index = date
    df_vacc_new.columns=['% vaccinated with 1 dose','% vaccinated with 2 doses']
    
    return df_vacc_new