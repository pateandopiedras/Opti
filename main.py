from gurobipy import GRB, Model, quicksum
from process_data import *

#MODELO------------------------------------
model = Model()
model.setParam('TimeLimit', 1800) #60*30

#CONJUNTOS---------------------------------
F = range(1, len(A()) + 1) #Viviendas a construirse a lo largo del Plan de Reconstrucción
I = range(1, len(B()) + 1) #Materiales de construcción
#Ki = range(1, C() + 1) #Variedad del material i
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
#bij: Factor mínimo de calidad como promedio ponderado de las variantes utilizadas, para cada i y para cada j
calidad_promedio = {(i, j): factor_calidad_promedio()[i, j] for i in I for j in J}
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
#rjpm: Índice de reducción de trabajo por unidad de trabajo realizada con el tipo de maquinaria m por p para j
#####ind_red = {(j, p, m): ind_reduccion()[j, p, m] for j in J for p in P for m in Mp}
#rhojp: Indica si el personal p puede utilizar la maquinaria para la construcción de la vivienda j
#####rho = {(j, p): utiliza_maquinaria()[j, p] for j in J for p in P}
#wf: Indica si el terreno donde va a construir su vivienda la familia f supera la pendiente máxima
#####pendiente = {f: pendiente_maxima()[f] for f in F}
#Cmj: Costo asociado al uso de maquinaria m para la construcción de vivienda j
#####costo_maq = {(m, j): costo_maquinaria()[m, j] for m in Mp for j in J}
#Zp: Cantidad máxima de unidades de trabajo disponibles de cada tipo de personal p
#####max_uni_trabajo = {p: maxima_unidades_trabajo()[p] for p in P}
BM = 9999

#VARIABLES-------------------------------------
#Cantidad, en días de trabajo, que demora la construcción de la vivienda f
t = model.addVars(F, vtype = GRB.INTEGER, name = "t_f")
#Cantidad real a utilizar de la variante k del tipo de material i en la construcción de f
x = model.addVars(F, I, Ki, vtype = GRB.INTEGER, name = "x_fik")
#Cantidad ideal a utilizar de k del tipo i en la construcción de f
x_d = model.addVars(F, I, Ki, vtype = GRB.INTEGER, name = "x_d_fik")
#Indica si se utiliza la opción k del material i en la construcción de f
y = model.addVars(F, I, Ki, vtype = GRB.BINARY, name = "y_fik")
#Días de trabajo realizadas por p (manual) con la variante k del material i para la construcción de f
z = model.addVars(F, I, Ki, P, vtype = GRB.INTEGER, name = "z_fikp")
#Indica si p está realizando labores en f
v = model.addVars(F, P, vtype = GRB.INTEGER, name = "v_fp")
#Cantidad de unidades de trabajo efectuadas a través del tipo de maquinaria m por p en j sobre i
####u = model.addVars(I, J, P, Mp, vtype = GRB.INTEGER, name = "u_ijpm")
#Indica si se utiliza el tipo de maquinaria m por p en j sobre i
####mu = model.addVars(I, J, P, Mp, vtype = GRB.BINARY, name = "mu_ijpm")

#RESTRICCIONES---------------------------------
#R1 REVISARRRRR

#R2 
#model.addConstrs((quicksum(x[i, j, k] for j in J) <= material_dispo[i, k] for i in I for k in Ki), name = "R2")
#R3
#model.addConstrs((x[i, j, k] <= material_dispo[i, k]*y[i, j, k] for i in I for j in J for k in Ki), name = "R3")
#R4

#R5

#R6
#model.addConstr((quicksum(v[j, p] for p in P) <= max_personas for j in J), name = "R6")
#R7

#R8

#R9
#model.addConstrs((quicksum(v[j, p] for j in J) <= max_personal for p in P), name = "R9")
#R10

#R11

#R12

#R13

#R14

#R15
#model.addConstrs((z[i, j, p] <= BM*(1 - mu[j, p, m]) for i in I for j in J for p in P for m in Mp), name = "R15")
#R16
#model.addConstrs((u[j, p, m] <= BM*mu[j, p, m] for j in J for p in P for m in Mp), name = "R16")

#UPDATE
model.update()

#FUNCIÓN OBJETIVO (REVISARRRRR)
#funcion_objetivo = (quicksum(pendiente[f, j])*
                    #(quicksum(
                        #(quicksum((x[i, j, k]*costo_mat[i, k] + quicksum(z[i, j, p]*coef_red_t[i, j, k]*sueldo[p] for p in P)) for k in Ki) for i in I)                      
                           #  ) + quicksum(costo_maq[m, j]*u[j, p, m] for p in P for m in Mp)
                            # ) for f in F for j in J)
funcion_objetivo = quicksum(quicksum(x[f, j, i, k]*costo_mat[i, k] + y[f, j, i, k]*costo_uso_mat for i in I for k in Ki) for f in F for j in J)

model.setObjective(funcion_objetivo, GRB.MINIMIZE)
model.optimize()
print(f'blablabla es: {model.ObjVal}')
                    
