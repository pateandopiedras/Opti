from gurobipy import GRB, Model, quicksum
from process_data import *

#MODELO------------------------------------
model = Model()
model.setParam('TimeLimit', 1800) #60*30

#CONJUNTOS---------------------------------
F = range(1, A() + 1) #Familias afectadas
I = range(1, B() + 1) #Materiales de construcción
J = range(1, C() + 1) #Tipo de vivienda a construir según cantidad de integrantes por familia
Ki = range(1, D() + 1) #Variedad del material i
Mp = range(1, G() + 1) #Tipo de maquinaria m que puede utilizar el personal p
P = range(1, E() + 1) #Tipo de personal

#PARÁMETROS--------------------------------
#aij: Cantidad mínima de material del tipo i que se necesita para una vivienda j
min_material = {(i, j): cantidad_min_material()[i, j] for i in I for j in J}
#bik: Factor de calidad del material k del tipo i
calidad = {(i, k): factor_calidad()[i, k] for i in I for k in Ki}
#cik: Costo de una unidad del material k del tipo i
costo_mat = {(i, k): costo_material()[i, k] for i in I for k in Ki}
#dijp: REVISAR

#ej: Cantidad máxima de personas que pueden trabajar en una unidad de trabajo en vivienda j
max_personas = {j: cantidad_max_personas()[j] for j in J}
#fj: Cantidad máxima de tiempo que puede tardar la construcción de la vivienda j
max_tiempo = {j: cantidad_max_tiempo()[j] for j in J}
#gjp: Cantidad mínima de personas del tipo p requerida por unidad de trabajo para vivienda j
min_personas = {(j, p): cantidad_min_personas()[j, p] for j in J for p in P}
#qijk: Coeficiente de reducción de trabajo para el material k del tipo i en vivienda j
coef_red_t = {(i, j, k): coef_reduccion_t()[i, j, k] for i in I for j in J for k in Ki}
#rjpm: Índice de reducción de trabajo por unidad de trabajo realizada con el tipo de maquinaria m por p para j
ind_red = {(j, p, m): ind_reduccion()[j, p, m] for j in J for p in P for m in Mp}
#tijk: Coeficiente de reducción de material para material k del tipo i en vivienda j
coef_red_m = {(i, j, k): coef_reduccion_m()[i, j, k] for i in I for j in J for k in Ki}
#wfj: Indica si el Comité le construye a la familia f la vivienda j
comite = {(f, j): comite_construye()[f, j] for f in F for j in J}
#rhojp: Indica si el personal p puede utilizar la maquinaria para la construcción de la vivienda j
rho = {(j, p): utiliza_maquinaria()[j, p] for j in J for p in P}
#wf: Indica si el terreno donde va a construir su vivienda la familia f supera la pendiente máxima
pendiente = {f: pendiente_maxima()[f] for f in F}
#BM: Suma de todas las unidades de trabajo Zp de todos los personales p
BM = 0
#Cmj: Costo asociado al uso de maquinaria m para la construcción de vivienda j
costo_maq = {(m, j): costo_maquinaria()[m, j] for m in Mp for j in J}
#Np: Cantidad de unidades de trabajo disponibles de cada tipo de personal p
uni_trabajo = {p: unidades_trabajo()[p] for p in P}
#Pik: Cantidad disponible de material k del tipo i
material_dispo = {(i, k): material_disponible()[i, k] for i in I for k in Ki}
#Qp: Cantidad máxima de personas de cada tipo de personal p
max_personal = {p: cantidad_max_personal()[p] for p in P}
#Sp: Sueldo por unidad de trabajo que cobra p
sueldo = {p: sueldo_personal()[p] for p in P}
#Zp: Cantidad máxima de unidades de trabajo disponibles de cada tipo de personal p
max_uni_trabajo = {p: maxima_unidades_trabajo()[p] for p in P}

#VARIABLES-------------------------------------
#Cantidad del material i que se usa la construcción de la vivienda j usando k
x = model.addVars(I, J, Ki, vtype = GRB.INTEGER, name = "x_ijk")
#Indica si se utiliza la opción k del material i en la construcción de la vivienda j
y = model.addVars(I, J, Ki, vtype = GRB.BINARY, name = "y_ijk")
#Unidades de trabajo realizadas por p (manual) con el material i para la construcción de j
z = model.addVars(I, J, P, vtype = GRB.INTEGER, name = "z_ijp")
#Cantidad de personas del tipo p que trabajan en la vivienda j
v = model.addVars(J, P, vtype = GRB.INTEGER, name = "v_jp")
#Cantidad de unidades de trabajo efectuadas a través del tipo de maquinaria m por p en j
u = model.addVars(J, P, Mp, vtype = GRB.INTEGER, name = "u_jpm")
#Indica si se utiliza el tipo de maquinaria m por p en j
mu = model.addVars(J, P, Mp, vtype = GRB.BINARY, name = "mu_jpm")

#RESTRICCIONES---------------------------------
#R1 REVISARRRRR

#R2 
model.addConstrs((quicksum(x[i, j, k] for j in J) <= material_dispo[i, k] for i in I for k in Ki), name = "R2")
#R3
model.addConstrs((x[i, j, k] <= material_dispo[i, k]*y[i, j, k] for i in I for j in J for k in Ki), name = "R3")
#R4

#R5

#R6
model.addConstr((quicksum(v[j, p] for p in P) <= max_personas for j in J), name = "R6")
#R7

#R8

#R9
model.addConstrs((quicksum(v[j, p] for j in J) <= max_personal for p in P), name = "R9")
#R10

#R11

#R12

#R13

#R14

#R15
model.addConstrs((z[i, j, p] <= BM*(1 - mu[j, p, m]) for i in I for j in J for p in P for m in Mp), name = "R15")
#R16
model.addConstrs((u[j, p, m] <= BM*mu[j, p, m] for j in J for p in P for m in Mp), name = "R16")

#UPDATE
model.update()

#FUNCIÓN OBJETIVO (REVISARRRRR)
funcion_objetivo = (quicksum(pendiente[f, j])*
                    (quicksum(
                        (quicksum((x[i, j, k]*costo_mat[i, k] + quicksum(z[i, j, p]*coef_red_t[i, j, k]*sueldo[p] for p in P)) for k in Ki) for i in I)                      
                             ) + quicksum(costo_maq[m, j]*u[j, p, m] for p in P for m in Mp)
                             ) for f in F for j in J)

model.setObjective(funcion_objetivo, GRB.MINIMIZE)
model.optimize()
print(f'blablabla es: {model.ObjVal}')
                    
