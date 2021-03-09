import wrf


class Variables:
    data = None

    def __init__(self, data):
        self.data = data

    def get_var(self, var_name):
        if hasattr(self, var_name) and callable(func := getattr(self, var_name)):
            return func()
        else:
            return wrf.getvar(self.data, var_name)

    def T2(self):
        t2_data = wrf.getvar(self.data, 'T2')
        return t2_data - 273.15
