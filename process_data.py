import csv

viviendas = [['v1', 10], ['v2', 25], ['v3', 40]]

#CONJUNTOS
def A():
    d = {}
    c = 1
    with open('data/c_viviendas.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    for l in data:
        for i in range(int(l[1])):
            d[c] = l[0]
            c+=1
    return d

def B():
    d = {}
    with open('data/c_materiales_construccion.csv', 'r') as archivo:
        data = csv.reader(archivo)
        for i, m in enumerate(data):
            d[m[0]] = i+1
    return d

def C(material):
    d = {}
    c = 0
    with open('data/c_variedades_materiales.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for m in data:
            if m[0] == material:
                d[m[1]] = c+1
                c+=1
    return d

def D():
    d = {}
    c = 1
    with open('data/c_trabajadores.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    for l in data:
        for i in range(int(l[1])):
            d[c] = l[0]
            c+=1
    return d

def E():
    d = {}
    c = 1
    with open('data/c_maquinarias.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    for l in data:
        for i in range(int(l[1])):
            d[c] = l[0]
            c+=1
    return d

#PARÁMETROS
def costo_diario_vivienda():
    dic = {}
    c = 1
    with open('data/costo_dia_vivienda.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    for v in viviendas:
        for l in range(v[1]):
            for d in data:
                if v[0] == d[0]:
                    dic[c] = d[1]
                    c+=1
    return dic

def cantidad_material():
    d = {}
    with open('data/cant_material.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for f in data:
            vivienda, material, cantidad = f
            d[B()[material], C()[vivienda]] = int(cantidad)
    return d

def costo_unidad_material():
    d = {}
    with open('data/costo_mat.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    for m in B():
        for f in data:
            material, variedad, costo = f
            if material == m:
                d[B()[m], D(m)[variedad]] = int(costo)
    return d

def costo_uso_material():
    pass

def cantidad_variante_material():
    pass

def factor_calidad():
    pass

def factor_calidad_promedio():
    pass

def coef_reduccion_mat():
    pass

def sueldo_trabajador():
    pass

def cantidad_uso_material():
    pass

def cantidad_max_uso_material():
    pass

def minimo_trabajadores():
    pass

def maximo_trabajadores():
    pass

def ind_reduccion():
    pass

def utiliza_maquinaria():
    pass

def ponderador_eficiencia():
    pass

def cantidad_maxima_maquinas():
    pass

def costo_uso_maquina():
    pass