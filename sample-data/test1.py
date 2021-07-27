from nyvred import nivelacion as n
import pandas as pd

data = pd.read_csv('niveles.csv')
data.loc[:,['Sup','Inf','Med']] = data.loc[:,['Sup','Inf','Med']]/1000

ls = [n.Lectura.geometrica(l.Ref,l.Obs,l.Sup,l.Med,l.Inf) for ix,l in data.iterrows()]

red = n.Red()
red.lecturas = ls
red.lecturas.append(n.Lectura.fijo('RT',5.104))

