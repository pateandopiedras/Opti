import csv

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
        data = list(csv.reader(archivo))
    data = data[1:]
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
    with open('data/c_maquinarias.csv', 'r') as archivo:
        data = csv.reader(archivo)
        next(data)
        for i, m in enumerate(data):
            maq, cantidad, costo = m
            d[maq] = i+1
    return d

#FUNCIONES PARÁMETROS
def costo_diario_vivienda():
    d = {}
    with open('data/c_viviendas.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    c = 1
    for v in range(1, len(A())+1):
        d[c] = int(data[0][2])
        c+=1
    return d

def cantidad_material():
    d = {}
    with open('data/cant_material.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    for v in A():
        for f in data:
            tipo_vivienda, material, cantidad = f
            if A()[v] == tipo_vivienda:
                d[B()[material], v] = int(cantidad)
    return d

def costo_unidad_material():
    d = {}
    with open('data/costo_mat.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    m = B()
    for mat in m.keys():
        c = 1
        for l in data:
            material, variedad, costo, costo_fijo, cantidad, fc, cr, ud, up = l
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
            material, variedad, costo, costo_fijo, cantidad, fc, cr, ud, up = l
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
            material, variedad, costo, costo_fijo, cantidad, fc, cr, ud, up = l
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
            material, variedad, costo, costo_fijo, cantidad, fc, cr, ud, up = l
            if l[0] == mat:
                d[m[material], c] = float(fc)
                c += 1
    return d

def factor_calidad_promedio():
    d = {}
    with open('data/c_viviendas.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    c = 1
    materiales = B()
    for v in range(1, len(A())+1):
        for m in materiales.values():
            d[m, v] = float(data[0][6])
    return d

def coef_reduccion_mat():
    d = {}
    with open('data/costo_mat.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    m = B()
    for mat in m.keys():
        c = 1
        for l in data:
            material, variedad, costo, costo_fijo, cantidad, fc, cr, ud, up = l
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
    for v in range(1, len(D())+1):
        d[c] = int(data[0][2])
        c+=1
    return d

def cantidad_uso_material():
    d = {}
    with open('data/costo_mat.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    m = B()
    var = C()
    for mat in m.keys():
        for p in range(1, len(D())+1):
            for l in data:
                material, variedad, costo, costo_fijo, cantidad, fc, cr, uso_diario, up = l
                if l[0] == mat:
                    d[m[material], var[m[mat]].index(variedad)+1, p] = int(uso_diario)
    return d

def cantidad_max_uso_material():
    d = {}
    with open('data/costo_mat.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    m = B()
    var = C()
    for mat in m.keys():
        for p in range(1, len(D())+1):
            for l in data:
                material, variedad, costo, costo_fijo, cantidad, fc, cr, uso_diario, uso_proyecto = l
                if l[0] == mat:
                    d[m[material], var[m[mat]].index(variedad)+1, p] = int(uso_proyecto)
    return d

def minimo_trabajadores():
    d = {}
    with open('data/c_viviendas.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    c = 1
    for v in range(1, len(A())+1):
        d[c] = int(data[0][5])
        c+=1
    return d

def maximo_trabajadores():
    d = {}
    with open('data/c_viviendas.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    c = 1
    for v in range(1, len(A())+1):
        d[c] = int(data[0][4])
        c+=1
    return d

def utiliza_maquinaria():
    d = {}
    with open('data/maquinas.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    P = range(1, len(D()) + 1)
    for worker in P:
        for l in data:
            l = l[0].split(';')
            trabajador, maq1, maq2, maq3 = l
            if int(l[0]) == worker:
                d[int(trabajador), 1] = int(maq1)
                d[int(trabajador), 2] = int(maq2)
                d[int(trabajador), 3] = int(maq3)
    return d      

def ponderador_eficiencia():
    d = {}
    with open('data/pond_efi_gamma.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    for m in E().keys():
        c = 1
        for v in range(1, len(D())+1):
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
    for v in range(1, len(A())+1):
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