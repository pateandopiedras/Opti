import csv

#CONJUNTOS
def A():
   #d = {}
   #c = 1
   #with open('data/c_viviendas.csv', 'r') as archivo:
        #data = list(csv.reader(archivo))
    #data = data[1:]
    #for l in data:
        #for i in range(int(l[1])):
            #d[c] = l[0]
            #c+=1
    return 7721

def B():
    d = {}
    with open('data/c_materiales_construccion.csv', 'r') as archivo:
        data = csv.reader(archivo)
        for i, m in enumerate(data):
            d[m[0]] = i+1
    return d

def C():
    d = {}
    with open('data/c_variedades_materiales.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for f in data:
            material = f[0]
            variedades = f[1]
            d[B()[material]] = variedades.split(';')
    return d

def D():
    #d = {}
    #c = 1
    #with open('data/c_trabajadores.csv', 'r') as archivo:
       #data = list(csv.reader(archivo))
    #data = data[1:]
    #for l in data:
        #for i in range(int(l[1])):
            #d[c] = l[0]
            #c+=1
    return 57768

def E():
    d = {}
    with open('data/c_maquinarias.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for i, m in enumerate(data):
            maq, cantidad, costo = m
            d[maq] = i+1
    return d

#PARÁMETROS
def costo_diario_vivienda():
    d = {}
    with open('data/c_viviendas.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    c = 1
    for v in range(1, A()+1):
        d[c] = int(data[0][2])
        c+=1
    return d

def cantidad_material():
    d = {}
    with open('data/cant_material.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for f in data:
            vivienda, material, cantidad = f
            d[B()[material], C()[vivienda]] = int(cantidad)
    return d
print(cantidad_material())

def costo_unidad_material():
    d = {}
    with open('data/costo_mat.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    m = B()
    for mat in m.keys():
        c = 1
        for l in data:
            material, variedad, costo, costo_fijo, cantidad, fc, cr = l
            if l[0] == mat:
                d[m[material], c] = int(costo)
                c += 1
    return d

def costo_uso_material():
    d = {}
    with open('data/costo_mat.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    m = B()
    for mat in m.keys():
        c = 1
        for l in data:
            material, variedad, costo, costo_fijo, cantidad, fc, cr = l
            if l[0] == mat:
                d[m[material], c] = int(costo_fijo)
                c += 1
    return d

def cantidad_variante_material():
    d = {}
    with open('data/costo_mat.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    m = B()
    for mat in m.keys():
        c = 1
        for l in data:
            material, variedad, costo, costo_fijo, cantidad, fc, cr = l
            if l[0] == mat:
                d[m[material], c] = int(cantidad)
                c += 1
    return d

def factor_calidad():
    d = {}
    with open('data/costo_mat.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    m = B()
    for mat in m.keys():
        c = 1
        for l in data:
            material, variedad, costo, costo_fijo, cantidad, fc, cr = l
            if l[0] == mat:
                d[m[material], c] = float(fc)
                c += 1
    return d

def factor_calidad_promedio():
    pass

def coef_reduccion_mat():
    d = {}
    with open('data/costo_mat.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    m = B()
    for mat in m.keys():
        c = 1
        for l in data:
            material, variedad, costo, costo_fijo, cantidad, fc, cr = l
            if l[0] == mat:
                d[m[material], c] = float(cr)
                c += 1
    return d

def sueldo_trabajador():
    d = {}
    with open('data/c_trabajadores.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    c = 1
    for v in range(1, D()+1):
        d[c] = int(data[0][2])
        c+=1
    return d

#REVISARRR
def cantidad_uso_material():
    d = {}
    with open('data/costo_mat.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    m = B()
    for mat in m.keys():
        c = 1
        for v in range(1, A()+1):
            for l in data:
                material, variedad, costo, costo_fijo, cantidad, fc, cr, uso_diario = l
                if l[0] == mat:
                    d[m[material], variedad, v] = int(uso_diario)
                    c += 1
    return d

def cantidad_max_uso_material():
    pass

def minimo_trabajadores():
    d = {}
    with open('data/c_viviendas.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    c = 1
    for v in range(1, A()+1):
        d[c] = int(data[0][5])
        c+=1
    return d

def maximo_trabajadores():
    d = {}
    with open('data/c_viviendas.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    c = 1
    for v in range(1, A()+1):
        d[c] = int(data[0][4])
        c+=1
    return d

def utiliza_maquinaria():
    pass

def ponderador_eficiencia():
    d = {}
    with open('data/pond_efi_gamma.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    for m in E().keys():
        c = 1
        for v in range(1, D()+1):
            for l in data:
                if l[0] == m:
                    d[v, E()[m]] = float(data[0][1])
            c += 1
    return d

def cantidad_maxima_maquinas():
    d = {}
    with open('data/c_viviendas.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    c = 1
    for v in range(1, A()+1):
        d[c] = int(data[0][3])
        c+=1
    return d

def costo_uso_maquina():
    d = {}
    with open('data/c_maquinarias.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for m in data:
            maq, cantidad, costo = m
            d[E()[maq]] = int(costo)
    return d