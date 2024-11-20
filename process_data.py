import csv #Cambio prueba Alli

#CONJUNTOS
def A():
    d = {}
    with open('data/1 F - viviendas.csv', 'r') as archivo:
        data = list(csv.reader(archivo))[1:]
    for l in data:
        d[l[1]] = int(l[0])
    return d

def B():
    d = {}
    with open('data/2 I - materiales.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    data = data[1:]
    for i in data:
        d[i[1]] = int(i[0])
    return d

def C():
    d = {}
    with open('data/3 Ki - variantes.csv', 'r') as archivo:
        data = list(csv.reader(archivo))[1:]
        for f in data:
            Ki = []
            for i in range(1,len(f)):
                Ki.append(f[i])
            d[int(f[0])] = Ki
    return d

def D():
    d = {}
    c = 1
    with open('data/4 P - trabajadores.csv', 'r') as archivo:
        data = list(csv.reader(archivo))[1:]
    for l in data:
        d[int(l[0])] = l[1] 
    return d

def E():
    d = {}
    with open('data/5 M - maquinas.csv', 'r') as archivo:
        data = list(csv.reader(archivo))[1:]
        for i in data:
            d[i[1]] = int(i[0])
    return d

#FUNCIONES PARÁMETROS
def duracion_proyecto():
    d = {}
    with open('data/6 T - duracion_proyecto.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    d[1] = int(data[0][0])
    return d

def costo_diario_vivienda():
    d = {}
    with open('data/7 h_f - costo_diario_vivienda.csv', 'r') as archivo:
        data = list(csv.reader(archivo))[1:]
    for l in data:
        d[int(l[0])] = int(l[1])
    return d

def cantidad_material():
    d = {}
    with open('data/8 a_if - cantidad_material.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    for i in data[1:]:
        for j in data[0][1:]:
            d[int(j), int(i[0])] = float(i[int(j)])
    return d

def costo_unidad_material():
    d = {}
    with open('data/9 c_ik - costo_unidad_material.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    for i in data[1:]:
        for j in range(1,len(i)):
            d[int(i[0]),j] = int(i[j])
    return d

def costo_uso_material():
    d = {}
    with open('data/10 d_ik - costo_uso_material.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    for i in data[1:]:
        for j in range(1,len(i)):
            d[int(i[0]),j] = int(i[j])
    return d

def cantidad_variante_material():
    d = {}
    with open('data/11 X_ik - cantidad_variante_material.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    for i in data[1:]:
        for j in range(1,len(i)):
            d[int(i[0]),j] = int(i[j])
    return d

def factor_calidad():
    d = {}
    with open('data/12 beta_ik - factor_calidad.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    for i in data[1:]:
        for j in range(1,len(i)):
            d[int(i[0]),j] = float(i[j])
    return d

def factor_calidad_promedio():
    d = {}
    with open('data/13 b_if - factor_calidad_promedio.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    for i in data[1:]:
        for j in data[0][1:]:
            d[int(j), int(i[0])] = float(i[int(j)])
    return d

def coef_reduccion_mat():
    d = {}
    with open('data/14 delta_ik - coef_reduccion_mat.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    for i in data[1:]:
        for j in range(1,len(i)):
            d[int(i[0]),j] = float(i[j])
    return d

def sueldo_trabajador():
    d = {}
    with open('data/15 q_p - sueldo_trabajador.csv', 'r') as archivo:
        data = list(csv.reader(archivo))[1:]
    for v in data:
        d[int(v[0])] = int(v[1])
    return d

def cantidad_uso_material():
    d = {}
    with open('data/16 l_ikp - cantidad_uso_material.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    for j in data[0][1:]:
        for i in data[1:]:
            Ki = i[int(j)].split(";")
            for k in range(len(Ki)):
                d[int(j),k+1,int(i[0])] = float(Ki[k]) * 3                  ##Jueguen cambiando este multiplicador y el código sale más rápido
    return d                                                                  ## Con 1 y 2 no es factible porque las casas se construirían muy lento
                                                                              ## De 3 en adelante, mientras más alto, más rápido corre el código y baja el GAP

def cantidad_max_uso_material():
    d = {}
    with open('data/17 L_ikp - cantidad_max_uso_material.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    for j in data[0][1:]:
        for i in data[1:]:
            Ki = i[int(j)].split(";")
            for k in range(len(Ki)):
                d[int(j),k+1,int(i[0])] = float(Ki[k]) * 1                        ##También se puede jugar con este, aunque no entiendo porque tienen efectos contrarios
    return d

def minimo_trabajadores():
    d = {}
    with open('data/18 R_f - minimo_trabajadores.csv', 'r') as archivo:
        data = list(csv.reader(archivo))[1:]
    for l in data:
        d[int(l[0])] = int(l[1])
    return d

def maximo_trabajadores():
    d = {}
    with open('data/19 S_f - maximo_trabajadores.csv', 'r') as archivo:
        data = list(csv.reader(archivo))[1:]
    for l in data:
        d[int(l[0])] = int(l[1])
    return d

def utiliza_maquinaria():
    d = {}
    with open('data/20 rho_pm - utiliza_maquinaria.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    for i in data[1:]:
        for j in data[0][1:]:
            d[int(i[0]),int(j)] = int(i[int(j)])
    return d

def costo_uso_maquina():
    d = {}
    with open('data/21 j_m - costo_uso_maquina.csv', 'r') as archivo:
        data = list(csv.reader(archivo))[1:]
        for m in data:
            d[int(m[0])] = int(m[1])
    return d

def ponderador_eficiencia():
    d = {}
    with open('data/22 gamma_pm - ponderador_eficiencia.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    for i in data[1:]:
        for j in data[0][1:]:
            d[int(i[0]),int(j)] = float(i[int(j)])
    return d

def cantidad_maxima_maquinas():
    d = {}
    with open('data/23 N_fp - cantidad_maxima_maquinas.csv', 'r') as archivo:
        data = list(csv.reader(archivo))
    for i in data[1:]:
        for j in data[0][1:]:
            d[int(i[0]),int(j)] = int(i[int(j)]) 
    return d






############## PARA MOSTRAR EN TERMINAL #################

def A0():
    nombres = []
    with open('data/1 F - viviendas.csv', 'r') as archivo:
        data = list(csv.reader(archivo))[1:]  # Omitir encabezado
    for l in data:
        nombres.append(l[1])  # Agregar únicamente los nombres a la lista
    return nombres