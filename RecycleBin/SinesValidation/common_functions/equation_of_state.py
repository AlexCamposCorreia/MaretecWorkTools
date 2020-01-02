

def EOS80_Fofonoff(temperature, salinity, pressure=None):
    '''

    Parameters:
      temperature - point temperature in ºC
      salinity - point salinity in PSU-78
      pressure - point pressure in bar
    '''

    t = temperature
    s = salinity
    p = pressure

    A = + 999.842594 \
        + 6.793952E-2*t**1 \
        - 9.095290E-3*t**2 \
        + 1.001685E-4*t**3 \
        - 1.120083E-6*t**4 \
        + 6.536332E-9*t**5
    
    B = + 8.24493E-1 \
        - 4.0899E-3*t**1 \
        + 7.6438E-5*t**2 \
        - 8.2467E-7*t**3 \
        + 5.3875E-9*t**4

    C = - 5.72466E-3 \
        + 1.0227E-4*t**1 \
        - 1.6546E-6*t**2

    D = + 4.8314E-4

    E = + 19652.21 \
        + 148.4206*t**1 \
        - 2.327105*t**2 \
        + 1.360477E-2*t**3 \
        - 5.155288E-5*t**4
    
    F = + 54.6746 \
        - 0.603459*t**1 \
        + 1.09987E-2*t**2 \
        - 6.1670E-5*t**3

    G = + 7.944E-2 \
        + 1.6483E-2*t**1 \
        - 5.3009E-4*t**2

    H = + 3.239908 \
        + 1.43713E-3*t**1 \
        + 1.16092E-4*t**2 \
        - 5.77905E-7*t**3

    I = + 2.2838E-3 \
        - 1.0981E-5*t**1 \
        - 1.6078E-6*t**2

    J = + 1.91075E-4

    M = + 8.50935E-5 \
        - 6.12293E-6*t**1 \
        + 5.2787E-8*t**2

    N = - 9.348E-7 \
        + 2.0816E-8*t**1 \
        + 9.1697E-10*t**2

    rho_St0 = A + B*s + C*s**(3/2) + D*s**2

    if pressure is None:
        return rho_St0

    V_St0 = 1 / rho_St0

    K_Stp = E + F*s + G*s**(3/2) \
            + ( H + I*s + J*s**(3/2) )*p \
            + ( M + N*s )*p**2

    V_Stp = V_St0 * ( 1 - p/K_Stp )

    rho_Stp = 1 / V_Stp

    return rho_Stp


def extrapolate_rho(d1, rho1, d2, rho2, d3):

    rho3 = rho2 + (d3-d2) * (rho2-rho1)/(d2-d1)

    return rho3


if __name__ == '__main__':

    temperature = 16.633 # ºC
    salinity = 35.894 # PSU-78
    pressure = 1.03 # bar

    d = EOS80_Fofonoff(temperature, salinity, pressure)

    d1 = 0.0
    rho1 = 1026.35014685
    d2 = -1.2741
    rho2 = 1026.35678333
    d3 = -2.6544

    rho3 = extrapolate_rho(d1, rho1, d2, rho2, d3)
    
    print(rho3)

    #  [1026.3662951    -2.6544    ]