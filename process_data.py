import csv

def A():
    return 20

def B():
    d = {}
    with open('data/materiales_construccion.csv', 'r') as archivo:
        data = csv.reader(archivo)
        for i, m in enumerate(data):
            d[m[0]] = i+1
    return d

def C():
    d = {}
    with open('data/tipos_viviendas.csv', 'r') as archivo:
        data = csv.reader(archivo)
        for i, v in enumerate(data):
            d[v[0]] = i+1
    return d

def D(material):
    d = {}
    c = 0
    with open('data/variedades_materiales.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for m in data:
            if m[0] == material:
                d[m[1]] = c+1
                c+=1
    return d

def E():
    return 8

def G():
    return 8

def H():
    return ((1, 1), (2, 2), (3, 3))

def cantidad_material():
    d = {}
    with open('data/cant_material.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for f in data:
            vivienda, material, cantidad = f
            d[B()[material], C()[vivienda]] = int(cantidad)
    return d

def factor_calidad():
    pass

def factor_calidad_promedio():
    pass

#ARREGLAR
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

def cantidad_max_personas():
    pass

def cantidad_max_tiempo():
    pass

def cantidad_min_personas():
    pass

def coef_reduccion_t():
    pass

def ind_reduccion():
    pass

def coef_reduccion_m():
    pass

def comite_construye():
    pass

def utiliza_maquinaria():
    pass

def pendiente_maxima():
    pass

def costo_maquinaria():
    pass

def unidades_trabajo():
    pass

def material_disponible():
    pass

def cantidad_max_personal():
    pass

def sueldo_personal():
    pass

def maxima_unidades_trabajo():
    pass