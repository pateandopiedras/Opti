from gurobipy import * # prueba alli
from process_data import *

#MODELO------------------------------------
model = Model()
model.setParam('TimeLimit', 1800) #60*30
model.setParam('Presolve', 2)         # Presolve nivel x
#model.setParam('MIPFocus', 1)         # Enfoque en soluciones factibles rápidas
#model.setParam('Threads', 4)          # Ajusta según la disponibilidad de CPU
#model.setParam('Heuristics', 0.1)     # Aumenta el uso de heurísticas
#model.setParam('NodefileStart', 0.5)  # Comienza a escribir en disco al usar el 50% de RAM
model.setParam('MIPGap', 0.01)         # Permite una brecha de x% en la solución óptima

#CONJUNTOS---------------------------------
F = range(1, len(A()) + 1) #Viviendas a construirse a lo largo del Plan de Reconstrucción
I = range(1, len(B()) + 1) #Materiales de construcción
def Ki(num):
    return len(C()[num]) + 1
d_ki = C()
P = range(1, len(D()) + 1) #Trabajadores del proyecto
M = range(1, len(E()) + 1) #Tipo de maquinaria m
    
#PARÁMETROS--------------------------------
f1 = costo_diario_vivienda()
f2 = cantidad_material()
f3 = costo_unidad_material()
f4 = costo_uso_material()
f5 = cantidad_variante_material()
f6 = factor_calidad()
f7 = factor_calidad_promedio()
f8 = coef_reduccion_mat()
f9 = sueldo_trabajador()
f10 = cantidad_uso_material()
f11 = cantidad_max_uso_material()
f12 = minimo_trabajadores()
f13 = maximo_trabajadores()
f14 = utiliza_maquinaria()
f15 = ponderador_eficiencia()
f16 = cantidad_maxima_maquinas()
f17 = costo_uso_maquina()

#T: Plazo máximo, en días, de la duración del Plan de Reconstrucción
max_plazo = duracion_proyecto()[1]
#hf: Costo en CLP asociado a un día de construcción de la vivienda f
costo_dia_vivienda = {f: f1[f] for f in F}
#aif: Cantidad exacta de material del tipo i que se necesita para una vivienda f
cant_material = {(i, f): f2[i, f] for i in I for f in F}
#cik: Costo en CLP de una unidad del material k del tipo i
costo_mat = {(i, k): f3[i, k] for i in I for k in range(1, len(d_ki[i]) + 1)}
#dik: Costo fijo en CLP asociado al uso del material k del tipo i
costo_uso_mat = {(i, k): f4[i, k] for i in I for k in range(1, len(d_ki[i]) + 1)}
#Xik: cantidad total disponible de la variante k del material del tipo i
cant_variante_material = {(i, k): f5[i, k] for i in I for k in range(1, len(d_ki[i]) + 1)}
#betaik: Factor de calidad del material k del tipo i
calidad = {(i, k): f6[i, k] for i in I for k in range(1, len(d_ki[i]) + 1)}
#bif: Factor mínimo de calidad como promedio ponderado de las variantes utilizadas, para cada i y para cada f
calidad_promedio = {(i, f): f7[i, f] for i in I for f in F}
#deltaik: Coeficiente de reducción de material por mala calidad para la variante k del tipo de material i
coef_red_mat = {(i, k): f8[i, k] for i in I for k in range(1, len(d_ki[i]) + 1)}
#qp: Sueldo por día de trabajo que cobra p
sueldo = {p: f9[p] for p in P}
#likp: Cantidad de la variante k del material del tipo i que puede usar el trabajador p en un día
cant_uso_mat = {(i, k, p): f10[i, k, p] for i in I for k in range(1, len(d_ki[i]) + 1) for p in P}
#Likp: Cantidad máxima de la variante k del tipo i que puede usar p en la duración del proyecto
cant_max_uso_mat = {(i, k, p): f11[i, k, p] for i in I for k in range(1, len(d_ki[i]) + 1) for p in P}
#Rf: Cantidad mínima de personas requeridas para construir la vivienda f
min_trabajadores = {f: f12[f] for f in F}
#Sf: Cantidad máxima de personas requeridas para construir f
max_trabajadores = {f: f13[f] for f in F}
#rhopm: Indica si la persona p está capacitada para el uso de m
rho = {(p, m): f14[p, m] for p in P for m in M}
#gammapm: Ponderador de eficiencia de construcción del trabajador p con la máquina m
gamma = {(p, m): f15[p, m] for p in P for m in M}
#Nf: Cantidad máxima de máquinas que se pueden usar en la vivienda f
max_maquinas = {f: f16[f] for f in F}
#jm: Costo diario asociado a usar la máquina m
costo_uso_maq = {m: f17[m] for m in M}

#VARIABLES-------------------------------------
Kiv = {i: len(C()[i]) + 1 for i in I}
#Cantidad, en días de trabajo, que demora la construcción de la vivienda f
t = model.addVars(F, vtype = GRB.CONTINUOUS, name = "t_f")
#Cantidad a utilizar de la variante k del tipo de material i en la construcción de f
x = model.addVars(F, I, Kiv, vtype = GRB.CONTINUOUS, name = "x_fik")
#Indica si se utiliza la opción k del material i en la construcción de f
y = model.addVars(F, I, Kiv, vtype = GRB.BINARY, name = "y_fik")
#Días de trabajo realizados por p (manual) con la variante k del material i para la construcción de f
z = model.addVars(F, I, Kiv, P, vtype = GRB.CONTINUOUS, name = "z_fikp")
#Indica si p está realizando labores en f
v = model.addVars(F, P, vtype = GRB.BINARY, name = "v_fp")
#Cantidad de días de trabajo efectuados a través de la máquina m por p en f sobre variante k del material i
u = model.addVars(F, I, Kiv, P, M, vtype = GRB.CONTINUOUS, name = "u_fikpm")
#Indica si se utiliza la máquina m por p en f
mu = model.addVars(F, P, M, vtype = GRB.BINARY, name = "mu_fpm")

#RESTRICCIONES---------------------------------
#R1
model.addConstrs((t[f] <= max_plazo for f in F), name = "R1")
#R2
model.addConstrs((quicksum(x[f, i, k] * coef_red_mat[i, k] for k in range(1, len(d_ki[i]) + 1)) >= cant_material[i, f] for f in F for i in I), name = "R2")
#R3
model.addConstrs((quicksum(x[f, i, k] for f in F) <= cant_variante_material[i, k] for i in I for k in range(1, len(d_ki[i]) + 1)), name = "R3")
#R4
model.addConstrs((quicksum(x[f, i, k] * calidad[i, k] for k in range(1, len(d_ki[i]) + 1)) >= calidad_promedio[i, f] * quicksum(x[f, i, k] for k in range(1, Ki(i))) for f in F for i in I), name = "R4")
#R5
model.addConstrs((x[f, i, k] <= cant_variante_material[i, k] * y[f, i, k] for f in F for i in I for k in range(1, len(d_ki[i]) + 1)), name = "R5")
#R6
model.addConstrs((quicksum(z[f, i, k, p] * cant_uso_mat[i, k, p] for f in F) <= cant_max_uso_mat[i, k, p] for i in I for k in range(1, len(d_ki[i]) + 1) for p in P), name = "R6")
#R7
model.addConstrs((quicksum(z[f, i, k, p] for i in I for k in range(1,len(d_ki[i]) + 1)) <= max_plazo * v[f, p] for f in F for p in P), name = "R7")
#R8
model.addConstrs((quicksum(v[f, p] for p in P) >= min_trabajadores[f] for f in F), name = "R8_1")
model.addConstrs((quicksum(v[f, p] for p in P) <= max_trabajadores[f] for f in F), name = "R8_2")
#R9
model.addConstrs((quicksum(z[f, i, k, p] * cant_uso_mat[i, k, p] + u[f, i, k, p, m] * cant_uso_mat[i, k, p] * rho[p, m] for p in P) >= x[f, i, k] for f in F for i in I for k in range(1, len(d_ki[i]) + 1) for m in M), name = "R9")
#R10
model.addConstrs((quicksum(z[f, i, k, p] + u[f, i, k, p, m] for i in I for k in range(1, len(d_ki[i]) + 1) for m in M) <= t[f] for f in F for p in P), name = "R10")
#R11
model.addConstrs((quicksum(z[f, i, k, p] + u[f, i, k, p, m] for f in F for i in I for k in range(1, len(d_ki[i]) + 1) for m in M) <= max_plazo for p in P), name = "R11")
#R12
model.addConstrs((quicksum(u[f, i, k, p, m] for i in I for k in range(1, len(d_ki[i]) + 1) for p in P) <= t[f] for f in F for m in M), name = "R12")
#R13
model.addConstrs((quicksum(u[f, i, k, p, m] for f in F for i in I for k in range(1, len(d_ki[i]) + 1) for p in P) <= max_plazo for m in M), name = "R13")
#R14
model.addConstrs((quicksum(u[f, i, k, p, m] for i in I for k in range(1, len(d_ki[i]) + 1)) <= max_plazo * mu[f, p, m] for f in F for p in P for m in M), name = "R14")
#R15
model.addConstrs((mu[f, p, m] <= rho[p, m] for f in F for p in P for m in M), name = "R15")
#R16
model.addConstrs((quicksum(mu[f, p, m] for f in F) <= 1 for p in P for m in M), name = "R16")

#UPDATE
model.update()

#FUNCIÓN OBJETIVO
funcion_objetivo = quicksum(t[f] * costo_dia_vivienda[f] + 
                              quicksum(
                                      x[f, i, k] * costo_mat[i, k] + y[f, i, k] * costo_uso_mat[i, k] + 
                                                  quicksum(
                                                      z[f, i, k, p] * sueldo[p] + 
                                                      quicksum(u[f, i, k, p, m] * (costo_uso_maq[m] + sueldo[p]) for m in M) for p in P) for i in I for k in range(1, Ki(i)))
                                                      for f in F)

#funcion_objetivo = (quicksum((t[f] * costo_dia_vivienda[f] + 
                              #quicksum((quicksum((x[f, i, k] * costo_mat[i, k] + y[f, i, k] * costo_uso_mat[i, k] + 
                                                  #quicksum((z[f, i, k, p] * sueldo[p] + 
                                                            #quicksum(u[f, i, k, p, m] * costo_uso_maq[m] for m in M)) for p in P)) for k in range(1, Ki(i)))) 
                                                            #for i in I)) 
                                                            #for f in F))
#Optimizacion
model.setObjective(funcion_objetivo, GRB.MINIMIZE)
model.optimize()

#Obtencion de datos
if model.status == GRB.OPTIMAL:
    valor_objetivo = model.ObjVal #costo minimizado
    print(f"El valor objetivo es: {valor_objetivo}")
    cost_viv = []
    cost_unit_mat = []
    cost_fij_mat = []
    cost_sueld = []
    cost_maq = []
    costo_viviendas = 0.0
    costo_uso_maquinas = 0.0
    costo_sueldo_trabajadores = 0
    costo_total = 0.0

    for f in F:
        costo = 0.0
        for i in I:
            c = 1
            for k in d_ki[i]:
                costo += y[f, i, c].x * x[f, i, c].x * f3[i, c]
                c += 1
        print(f'El costo de la vivienda {f} es de {costo} $CLP')
        costo_viviendas += float(costo)

    #for p in P:
        #costo = 0.0
        #for f in F:
            #for i in I:
                #c = 1
                #for k in d_ki[i]:
                    #costo += z[f, i, k, p].x * sueldo[p]
                    #c += 1
        #costo_sueldo_trabajadores += float(costo)
    #print(costo_sueldo_trabajadores)

    #for m in M:
        #costo = 0.0
        #for p in P:
            #for f in F:
                #for i in I:
                    #c = 1
                    #for k in d_ki[i]:
                        #costo += u[f, i, k, p, m].x * (costo_uso_maq[m] + sueldo[p])
                        #c += 1
        #costo_uso_maquinas += float(costo)
    #print(costo_uso_maquinas)

    #costo_total = costo_viviendas + costo_sueldo_trabajadores + costo_uso_maquinas

    #for f in F:
        #print(f'La construcción de la vivienda {f} toma {t[f].x} dias')

    for f in F:
        costo = [f, costo_dia_vivienda[f]]
        cost_viv.append(costo)

    for i in I:
        for k in range(1, Ki(i)):
            costo = [i, k, costo_mat[i, k]]
            cost_unit_mat.append(costo)

    for i in I:
        for k in range(1, Ki(i)):
            costo = [i, k, costo_uso_mat[i, k]]
            cost_fij_mat.append(costo)

    for p in P:
        costo = [p, sueldo[p]]
        cost_sueld.append(costo)

    for m in M:
        costo = [m, costo_uso_maq[m]]
        cost_maq.append(costo)

elif model.status == GRB.INFEASIBLE:
    print("El modelo es infactible.")
    model.computeIIS()  # Computa el IIS (Irreducible Inconsistent Subsystem)
    model.write("infactibilidad.ilp")  # Guarda el IIS en un archivo
else:
    print("El modelo no encontró una solución óptima por alguna otra razón.")

#dias ideales para construir la casa
#hf: Costo asociado a un dia
#cik: costo de una unidad del material k del tipo i
#dik: costo fijo asociado al uso del material
#qp: sueldo que cobra trabajador
#jm: costo diario asociado a maquina

