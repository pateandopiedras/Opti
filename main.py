from gurobipy import GRB, Model, quicksum
from process_data import *

#MODELO------------------------------------
model = Model()
model.setParam('TimeLimit', 1800) #60*30

#CONJUNTOS---------------------------------
F = range(1, len(A()) + 1) #Viviendas a construirse a lo largo del Plan de Reconstrucción
I = range(1, len(B()) + 1) #Materiales de construcción
Ki = range(1, C() + 1) #Variedad del material i ###ARREGLAR
P = range(1, D() + 1) #Trabajadores del proyecto
M = range(1, E() + 1) #Tipo de maquinaria m

#PARÁMETROS--------------------------------
#T: Plazo máximo, en días, de la duración del Plan de Reconstrucción
max_plazo = 700
#hf: Costo en CLP asociado a un día de construcción de la vivienda f
costo_dia_vivienda = {f: costo_diario_vivienda()[f] for f in F}
#aif: Cantidad exacta de material del tipo i que se necesita para una vivienda f
cant_material = {(i, f): cantidad_material()[i, f] for i in I for f in F}
#cik: Costo en CLP de una unidad del material k del tipo i
costo_mat = {(i, k): costo_unidad_material()[i, k] for i in I for k in range(1, len(D(i))+1)}
#dik: Costo fijo en CLP asociado al uso del material k del tipo i
costo_uso_mat = {(i, k): costo_uso_material()[i, k] for i in I for k in Ki}
#Xik: cantidad total disponible de la variante k del material del tipo i
cant_variante_material = {(i, k): cantidad_variante_material()[i, k] for i in I for k in Ki}
#betaik: Factor de calidad del material k del tipo i
calidad = {(i, k): factor_calidad()[i, k] for i in I for k in Ki}
#bif: Factor mínimo de calidad como promedio ponderado de las variantes utilizadas, para cada i y para cada j
calidad_promedio = {(i, f): factor_calidad_promedio()[i, f] for i in I for f in F}
#deltaik: Coeficiente de reducción de material por mala calidad para la variante k del tipo de material i
coef_red_mat = {(i, k): coef_reduccion_mat()[i, k] for i in I for k in Ki}
#qp: Sueldo por día de trabajo que cobra p
sueldo = {p: sueldo_trabajador()[p] for p in P}
#likp: Cantidad de la variante k del material del tipo i que puede usar el trabajador p en un día
cant_uso_mat = {(i, k, p): cantidad_uso_material()[i, k, p] for i in I for k in Ki for p in P}
#Likp: Cantidad máxima de la variante k del tipo i que puede usar p en la duración del proyecto
cant_max_uso_mat = {(i, k, p): cantidad_max_uso_material()[i, k, p] for i in I for k in Ki for p in P}
#Rf: Cantidad mínima de personas requeridas para construir la vivienda f
min_trabajadores = {f: minimo_trabajadores()[f] for f in F}
#Sf: Cantidad máxima de personas requeridas para construir f
max_trabajadores = {f: maximo_trabajadores()[f] for f in F}
#rhopm: Indica si la persona p está capacitada para el uso de m
rho = {(p, m): utiliza_maquinaria()[p, m] for p in P for m in M}
#gammapm: Ponderador de eficiencia de construcción del trabajador p con la máquina m
gamma = {(p, m): ponderador_eficiencia()[p, m] for p in P for m in M}
#Nf: Cantidad máxima de máquinas que se pueden usar en la vivienda f
max_maquinas = {f: cantidad_maxima_maquinas()[f] for f in F}
#jm: Costo diario asociado a usar la máquina m
costo_uso_maq = {m: costo_uso_maquina()[m] for m in M}

#VARIABLES-------------------------------------
#Cantidad, en días de trabajo, que demora la construcción de la vivienda f
t = model.addVars(F, vtype = GRB.INTEGER, name = "t_f")
#Cantidad a utilizar de la variante k del tipo de material i en la construcción de f
x = model.addVars(F, I, Ki, vtype = GRB.INTEGER, name = "x_fik")
#Indica si se utiliza la opción k del material i en la construcción de f
y = model.addVars(F, I, Ki, vtype = GRB.BINARY, name = "y_fik")
#Días de trabajo realizadas por p (manual) con la variante k del material i para la construcción de f
z = model.addVars(F, I, Ki, P, vtype = GRB.INTEGER, name = "z_fikp")
#Indica si p está realizando labores en f
v = model.addVars(F, P, vtype = GRB.INTEGER, name = "v_fp")
#Cantidad de días de trabajo efectuados a través de la máquina m por p en f sobre variante k del material i
u = model.addVars(F, I, Ki, P, M, vtype = GRB.INTEGER, name = "u_fikpm")
#Indica si se utiliza la máquina m por p en f
mu = model.addVars(F, P, M, vtype = GRB.BINARY, name = "mu_fpm")

#RESTRICCIONES---------------------------------
#R1 REVISARRRRR
model.addConstrs((t[f] <= max_plazo for f in F), name = "R1")
#R2
model.addConstrs((quicksum(x[f, i, k] * coef_red_mat[i, k] for k in Ki) >= cant_material[i, f] for f in F for i in I), name = "R2")
#R3
model.addConstrs((quicksum(x[f, i, k] for f in F) <= cant_variante_material[i, k] for i in I for k in Ki), name = "R3")
#R4
model.addConstrs((quicksum(x[f, i, k] * calidad[i, k] for k in Ki) >= calidad_promedio[i, f] * quicksum(x[f, i, k] for k in Ki) for f in F for i in I), name = "R4")
#R5
model.addConstrs((x[f, i, k] <= cant_variante_material[i, k] * y[f, i, k] for f in F for i in I for k in Ki), name = "R5")
#R6
model.addConstrs((quicksum(z[f, i, k, p] * cant_uso_mat[i, k, p] for f in F) <= cant_max_uso_mat[i, k, p] for i in I for k in Ki for p in P), name = "R6")
#R7
model.addConstrs((quicksum(quicksum(z[f, i, k, p] for k in Ki) for i in I) <= max_plazo * v[f, p] for f in F for p in P), name = "R7")
#R8
model.addConstrs((quicksum(v[f, p] for p in P) >= min_trabajadores[f] for f in F), name = "R8_1")
model.addConstrs((quicksum(v[f, p] for p in P) <= max_trabajadores[f] for f in F), name = "R8_2")
#R9
model.addConstrs((quicksum(v[f, p] for f in F) <= 1 for p in P), name = "R9")
#model.addConstrs((quicksum(v[j, p] for j in J) <= max_personal for p in P), name = "R9")
#R10
model.addConstrs((quicksum(quicksum(quicksum(u[f, i, k, p, m] for k in Ki) for i in I) for p in P) <= t[f] for f in F for m in M), name = "R10")
#R11
model.addConstrs((quicksum(z[f, i, k, p] * cant_uso_mat[i, k, p] + u[f, i, k, p, m] * cant_uso_mat[i, k, p] * rho[p, m] for p in P) >= x[f, i, k] for f in F for i in I for k in Ki), name = "R11")
#R12
model.addConstrs((quicksum(quicksum(z[f, i, k, p] + u[f, i, k, p, m] for k in Ki) for i in I) <= t[f] for f in F for p in P for m in M), name = "R12")
#R13
model.addConstrs((quicksum(quicksum(u[f, i, k, p, m] for k in Ki) for i in I) <= max_plazo * mu[f, p, m] for f in F for p in P for m in M), name = "R13")
#R14
model.addConstrs((mu[f, p, m] <= rho[p, m] for f in F for p in P for m in M), name = "R14")
#R15
model.addConstrs((quicksum(mu[f, p, m] for m in M) <= max_maquinas[f] for f in F for p in P), name = "R15")
#model.addConstrs((z[i, j, p] <= BM*(1 - mu[j, p, m]) for i in I for j in J for p in P for m in Mp), name = "R15")
#R16
model.addConstrs((quicksum(mu[f, p, m] for f in F) <= 1 for p in P for m in M), name = "R16")
#model.addConstrs((u[j, p, m] <= BM*mu[j, p, m] for j in J for p in P for m in Mp), name = "R16")

#UPDATE
model.update()

#FUNCIÓN OBJETIVO
funcion_objetivo = quicksum((t[f] * costo_dia_vivienda[f] + quicksum((quicksum((x[f, i, k] * costo_mat[i, k] + y[f, i, k] * costo_uso_mat[i, k] + quicksum((z[f, i, k, p] * sueldo[p] + quicksum(u[f, i, k, p, m] * costo_uso_maq[m] for m in M)) for p in P)) for k in Ki)) for i in I)) for f in F)

model.setObjective(funcion_objetivo, GRB.MINIMIZE)
model.optimize()
print(f'blablabla es: {model.ObjVal}')
                    
