from math import sin,cos,tan
import pandas as pd
import numpy as np

class Lectura(object):
    def __init__(self):
        return None

    @classmethod
    def trigonometrica(cls,origen,destino,distancia,angulo,hi=0,hp=0):
        self = cls()
        self.origen = origen
        self.destino = destino
        self.w = distancia ** -2

        self.coef = {}
        self.coef[self.origen] = -1
        self.coef[self.destino] = 1

        self.angulo = angulo * np.pi / 180.
        self.hi = hi
        self.hp = hp
        self.type = 'Trigonometrica'
        self.distancia = distancia

        return self

    @classmethod
    def geometrica(cls,origen,destino,sup,medio,inferior,hi=0,hp=0):
        self = cls()
        self.origen = origen
        self.destino = destino
        distancia = (sup - inferior) * 100
        self.w = distancia ** -2

        self.coef = {}
        self.coef[self.origen] = -1
        self.coef[self.destino] = 1

        #self.angulo = angulo * np.pi / 180.
        self.hi = hi
        self.hp = hp
        self.type = 'Geometrica'
        self.distancia = distancia

        return self

    @classmethod
    def GPS(cls,origen,destino,w,lectura,hi=0,hp=0):
        self = cls()
        self.origen = origen
        self.destino = destino
        self.w = w

        self.coef = {}
        self.coef[self.origen] = -1
        self.coef[self.destino] = 1

        self.hi = hi
        self.hp = hp
        self.type = 'GPS'
        self.l = lectura
        return self

    @classmethod
    def fijo(cls,punto,lectura,w=100):
        self = cls()
        self.origen = punto
        self.destino = None
        self.w = w

        self.coef = {}
        self.coef[self.origen] = 1

        self.type = 'fijo'
        self.l = lectura
        return self

    def lectura(self,**kwargs):
        ix_err=kwargs.get('ix_err',0)
        col_error=kwargs.get('col_error',0)
        eq_col_error=kwargs.get('eq_col_error',0)
        eq_tol=kwargs.get('eq_tol',0.003)
        offset=kwargs.get('offset',0)

        if self.type == 'Geometrica':
            promedio = sum(self.hilos[1:])/2
            if abs(self.hilos[0]-self.promedio) > tol:
                raise ValuError('Lectura fuera de tolerancia')

            return self.medio - self.distancia * eq_col_error #sin = tan = ang

        if self.type == 'Trigonometrica':
            angulo = self.angulo+ix_err
            if angulo > np.pi:
                angulo = 2*np.pi - angulo

            angulo = np.pi/2 - angulo

            return tan(angulo)*self.distancia -\
                     ((self.hp-self.hi))

        if self.type == 'GPS':
            return self.l

        if self.type == 'fijo':
            return self.l + offset

    def coeficientes(self):
        return self.coef

    def peso(self):
        return self.w

class Red(object):
    def __init__(self):
        self.lecturas = []

    def get_a(self):
        series = [pd.Series(i.coeficientes()) for i in self.lecturas]
        df = pd.DataFrame(series)
        return np.nan_to_num(df.values), list(df.columns)

    def get_p(self):
        ws = [i.peso() for i in self.lecturas]
        return np.diag(ws)

    def get_l(self,**kwargs):
        ls = [i.lectura(**kwargs) for i in self.lecturas]
        return np.array(ls)

    def calc_x(self,**kwargs):
        a,names = self.get_a()
        p = self.get_p()
        l = self.get_l(**kwargs)
        atp = np.dot(a.T,p)
        atpa = np.dot(atp,a)
        atpl = np.dot(atp,l)

        atpa_ = np.linalg.inv(atpa)

        x = np.dot(atpa_,atpl)

        return x,names

    def get_v(self,**kwargs):
        x,n = self.calc_x(**kwargs)
        a,n = self.get_a()
        l = self.get_l(**kwargs)
        v = np.dot(a,x) - l
        return v

    def get_sum_v(self,**kwargs):
        return np.sum(self.get_v(**kwargs) ** 2)


