from scipy.integrate import odeint
import numpy as np

# The SIR model differential equations.
def deriv_SIR(y, t, N, beta,gamma,tau,vacc_eff,vacc_speed,t0):
    S,I,R,V = y
 
    B=beta*np.exp(-t/tau)
 
    if t>=t0:
        vacc=vacc_speed/100
    else:
        vacc=0
 
    dSdt = -(B*I/N)*S - vacc*vacc_eff*S
    dIdt = (B*S/N)*I - gamma*I 
    dVdt = vacc*vacc_speed*S 
    dRdt = gamma*I 
    
    return dSdt, dIdt, dVdt, dRdt
 
def SIR2(N,beta,gamma,tau,vacc_eff,vacc_speed,t0,I0=1,R0=0,V0=0,t=np.arange(0,365)):
    # Definition of the initial conditions
    # I0 and R0 denotes the number of initial infected people (I0) 
    # and the number of people that recovered and are immunized (R0)
    
    # t ise the timegrid
    
    S0=N-I0-R0-V0  # number of people that can still contract the virus
 
    # Initial conditions vector
    y0 = S0, I0, V0, R0
 
    # Integrate the SIR equations over the time grid, t.
    ret = odeint(deriv_SIR, y0, t, args=(N,beta,gamma,tau,vacc_eff,vacc_speed,t0))
    S, I, V, R = np.transpose(ret)
    
    return (t,S,I,V,R)