from scipy.integrate import odeint
import numpy as np

# ================================ SIR 2.0 ======================

# The SIR model differential equations.
def deriv_SIR(y, t, N, beta,gamma,tau,vacc_eff,vacc_speed,t0,
              vacc_custom = False,
              tau_custom = False):
    S,I,R,V = y
 
    B=beta*np.exp(-t/tau)
 
    if t>=t0:
        vacc=vacc_speed/100
    else:
        vacc=0
 
    # custom vaccination scheme
    if type(vacc_custom) == list:
        new_time = vacc_custom[0]
        new_speed = vacc_custom[1]
        
        if t<new_time and t>=t0:
            vacc = vacc_speed/100
        
        elif t>=new_time:
            vacc = new_speed/100
            
        else:
            vacc=0
            
    # custom Rt scheme        
    if type(tau_custom) == list:
        Btime = tau_custom[0]
        Bvalue = tau_custom[1]
        
        if t < Btime:
            B=beta*np.exp(-t/tau)
        else:
            B=Bvalue          


    dSdt = -(B*I/N)*S - vacc*vacc_eff*S
    dIdt = (B*S/N)*I - gamma*I 
    dVdt = vacc*vacc_eff*S 
    dRdt = gamma*I   
    
    return dSdt, dIdt, dRdt, dVdt
 
def SIR2(N,beta,gamma,tau,vacc_eff,vacc_speed,t0,I0=1,R0=0,V0=0,
         vacc_custom=False,tau_custom=False,t=np.arange(0,365)):
    # Definition of the initial conditions
    # I0 and R0 denotes the number of initial infected people (I0) 
    # and the number of people that recovered and are immunized (R0)
    
    # t ise the timegrid
    
    S0=N-I0-R0-V0  # number of people that can still contract the virus
 
    # Initial conditions vector
    y0 = S0, I0, R0, V0
 
    # Integrate the SIR equations over the time grid, t.
    ret = odeint(deriv_SIR, y0, t, args=(N,beta,gamma,tau,vacc_eff,vacc_speed,t0,vacc_custom,tau_custom))
    S, I, R, V = np.transpose(ret)
    
    return (t,S,I,R,V)



# ================================ ORIGINAL SIR ======================

def deriv_simple_SIR(y, t, N, beta,gamma):
    S,I,R = y

    dSdt = -(beta*I/N)*S 
    dIdt = (beta*S/N)*I - gamma*I 
    dRdt = gamma*I   
    
    return dSdt, dIdt, dRdt


def SIR(N,beta,gamma,I0=1,R0=0,t=np.arange(0,365)):
    # Definition of the initial conditions
    # I0 and R0 denotes the number of initial infected people (I0) 
    # and the number of people that recovered and are immunized (R0)
    
    # t ise the timegrid
    
    S0=N-I0-R0  # number of people that can still contract the virus
 
    # Initial conditions vector
    y0 = S0, I0, R0
 
    # Integrate the SIR equations over the time grid, t.
    ret = odeint(deriv_simple_SIR, y0, t, args=(N,beta,gamma))
    S, I, R = np.transpose(ret)
    
    return (t,S,I,R)