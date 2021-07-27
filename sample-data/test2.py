from scipy import optimize
from math import pi

from test1 import *

x = optimize.minimize(lambda x: red.get_sum_v(eq_col_error=x[0]),x0=[0])

print(f'error de colimación calculado: {x.x[0]*3600*180/pi:.1f}"')

print(pd.Series(*red.calc_x(eq_col_error=x.x[0]))[set([i for i in map(lambda x:
    x.destino, red.lecturas) if i is not None])])

print([f'{i:.4f}' for i in red.get_v(eq_col_error=x.x[0])])
