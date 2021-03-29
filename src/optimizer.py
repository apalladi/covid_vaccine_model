import numpy as np
from scipy.optimize import minimize
from src.epi_model import SIR2

def compute_error(y_true,y_pred,which_error='mse'):
    '''This function computes the error between expected and predicted Susceptible,Infected,Removed'''
    
    susc = y_pred[0][0:len(y_true[0])]
    inf  = y_pred[1][0:len(y_true[0])]
    rim  = y_pred[2][0:len(y_true[0])]

    
    if which_error =='mse':
        err1 = np.sqrt(np.mean((y_true[0]-susc)**2))
        err2 = np.sqrt(np.mean((y_true[1]-inf)**2))
        err3 = np.sqrt(np.mean((y_true[2]-rim)**2))
        
    elif which_error =='mae':
        err1 = np.mean(np.abs(y_true[0]-susc))
        err2 = np.mean(np.abs(y_true[1]-inf))
        err3 = np.mean(np.abs(y_true[2]-rim))
        
    elif which_error == 'perc':
        err1 = np.mean(np.abs(y_true[0]-susc)/y_true[0])*100
        err2 = np.mean(np.abs(y_true[1]-inf)/y_true[1])*100
        err3 = np.mean(np.abs(y_true[2]-rim)/y_true[2])*100
    
    errm = (err1+err2+err3)/3
    
    return errm


def fit_model(y_data,abitanti,
              vacc_eff=0.95,
              vacc_speed=0,
              t0=0,
              V0=0,
              which_error='mse'):
    
    ydata_casi = y_data[0]
    ydata_inf  = y_data[1]
    ydata_rec  = y_data[2]
    
    def err_to_minimize(par):
        '''Questa è la funzione da minimizzare. I parametri liberi sono R0 e tau,
        R0 è legato alla velocità di diffusione del virus, tau è legato alle misure di restrizione'''

        beta,gamma,tau = par

        model=SIR2(abitanti,beta,gamma,tau,
                         vacc_eff=vacc_eff,vacc_speed=vacc_speed,t0=t0,  
                         I0=ydata_inf[0],R0=ydata_rec[0],V0=V0)

        y_pred = [model[1],model[2],model[3]] # Suscettibili, Infetti, Rimossi del modello
        y_true = [abitanti-ydata_casi,ydata_inf,ydata_rec]

        # compute the mean squared error
        mse = compute_error(y_true,y_pred,which_error = which_error)

        return mse

    minpar = minimize(err_to_minimize,[0.2,0.1,65],options={'return_all':True,'disp':True},method='Nelder-Mead').x 
    
    return minpar