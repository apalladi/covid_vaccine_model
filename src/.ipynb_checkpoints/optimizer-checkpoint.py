import numpy as np
from scipy.optimize import minimize
from src.epi_model import SIR2, SIR

def compute_error(y_true,y_pred,which_error='mse',verbose=0):
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
        
    elif which_error =='chi2':
        err1 = np.sqrt(np.mean((y_true[0]-susc)**2/y_true[0]))
        err2 = np.sqrt(np.mean((y_true[1]-inf)**2/y_true[1]))
        err3 = np.sqrt(np.mean((y_true[2]-rim)**2/y_true[2]))
        
    elif which_error == 'perc':
        err1 = np.nanmean(np.abs(y_true[0]-susc)/y_true[0])*100
        err2 = np.nanmean(np.abs(y_true[1]-inf)/y_true[1])*100
        err3 = np.nanmean(np.abs(y_true[2]-rim)/y_true[2])*100
        
        if verbose==1:
            print('Error on susceptible',round(err1,1),'%')
            print('Error on infected',round(err2,1),'%')
            print('Error on removed',round(err3,1),'%')
        
    elif which_error =='weighted':
        err1 = np.sqrt(np.mean((y_true[0]-susc)**2))/2
        err2 = np.sqrt(np.mean((y_true[1]-inf)**2))
        err3 = np.sqrt(np.mean((y_true[2]-rim)**2))/2
        
    elif which_error == 'infected_only':
        err1 = 0
        err2 = np.sqrt(np.mean((y_true[1]-inf)**2))
        err3 = 0
    
    errm = (err1+err2+err3)/3
    
    return errm


def fit_model(y_data,inhabitants,
              vacc_eff=0.95,
              vacc_speed=0,
              t0=0,
              V0=0,
              which_error='mse',
              decay=True):
    
    ydata_cases = y_data[0]
    ydata_inf  = y_data[1]
    ydata_rec  = y_data[2]
    
    def err_to_minimize(par):
        '''This is the function to minimize. The free parameters are beta, gamma and tau.
        beta is related to the speed of the spread, 
        gamma is the inverse of the average time of infection,
        tau is related to the decay of beta, i.e. to the restrictions'''

        if decay==True:
            beta,gamma,tau = par
            model=SIR2(inhabitants,beta,gamma,tau,
                       vacc_eff=vacc_eff,vacc_speed=vacc_speed,t0=t0,  
                       I0=ydata_inf[0],R0=ydata_rec[0],V0=V0)
        
        elif decay==False:
            beta,gamma = par
            model=SIR2(inhabitants,beta,gamma,10**6,
                       vacc_eff=vacc_eff,vacc_speed=vacc_speed,t0=t0,  
                       I0=ydata_inf[0],R0=ydata_rec[0],V0=V0)
        
        y_true = [inhabitants-ydata_cases,ydata_inf,ydata_rec]
        y_pred = [model[1],model[2],model[3]] # Susceptible, Infected, Removed (model)

        # compute the mean squared error
        mse = compute_error(y_true,y_pred,which_error = which_error)

        return mse
    
    if decay==True:
        minpar = minimize(err_to_minimize,[0.2,0.1,65],options={'return_all':True,'disp':True},method='Nelder-Mead').x 
    elif decay==False:
        minpar = minimize(err_to_minimize,[0.2,0.1],options={'return_all':True,'disp':True},method='Nelder-Mead').x 
        minpar = np.append(minpar,[10**6])
    # check the model
    
    opt_model = SIR2(inhabitants,minpar[0],minpar[1],minpar[2],
                   vacc_eff=vacc_eff,vacc_speed=vacc_speed,t0=t0,  
                   I0=ydata_inf[0],R0=ydata_rec[0],V0=V0)
    
    y_true = [inhabitants-ydata_cases,ydata_inf,ydata_rec]
    y_pred = [opt_model[1],opt_model[2],opt_model[3]]
    perc_err = round(compute_error(y_true,y_pred,which_error='perc',verbose=1),1)
    
    print('The average error of the model is',perc_err,'%')
    
    return minpar



def fit_simple_model(y_data,inhabitants,
              which_error='mse'):
    
    ydata_cases = y_data[0]
    ydata_inf  = y_data[1]
    ydata_rec  = y_data[2]
    
    def err_to_minimize(par):
        beta,gamma = par

        model=SIR(inhabitants,beta,gamma,
                   I0=ydata_inf[0],R0=ydata_rec[0])
        
        y_true = [inhabitants-ydata_cases,ydata_inf,ydata_rec]
        y_pred = [model[1],model[2],model[3]] # Susceptible, Infected, Removed (model)

        # compute the mean squared error
        mse = compute_error(y_true,y_pred,which_error = which_error)

        return mse

    minpar = minimize(err_to_minimize,[0.2,0.1],options={'return_all':True,'disp':True},method='Nelder-Mead').x 
    
    # check the model
    
    opt_model = SIR(inhabitants,minpar[0],minpar[1],
                   I0=ydata_inf[0],R0=ydata_rec[0])
    
    y_true = [inhabitants-ydata_cases,ydata_inf,ydata_rec]
    y_pred = [opt_model[1],opt_model[2],opt_model[3]]
    perc_err = round(compute_error(y_true,y_pred,which_error='perc',verbose=1),1)
    
    print('The average error of the model is',perc_err,'%')
    
    return minpar