from wrf import getvar
import numpy as np


class Variables:
    data = None

    def __init__(self, data):
        self.data = data

    def get_var(self, var_name):
        if hasattr(self, var_name) and callable(func := getattr(self, var_name)):
            return func()
        else:
            return getvar(self.data, var_name)

    def T2(self, h=None):
        t2_data = getvar(self.data, 'T2')
        return t2_data - 273.15

    def V(self):
        v10 = getvar(self.data, 'V10')
        u10 = getvar(self.data, 'U10')
        return np.sqrt(u10*u10+v10*v10) * 3.6

    def slp(self):
        return getvar(self.data, "slp")

    def rh2(self):
        return getvar(self.data, 'rh2')

    def mdbz(self):
        return getvar(self.data, 'mdbz')
        # outvar = getvar(self.data, 'mdbz')
        # return np.ma.masked_where(outvar < 5, outvar)
