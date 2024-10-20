from gurobipy import GRB, Model, quicksum
from process_data import *

#MODELO------------------------------------
model = Model()
model.setParam('TimeLimit', 1800) #60*30

#CONJUNTOS---------------------------------
F = range(1, A() + 1) #Familias afectadas
I = range(1, len(B()) + 1) #Materiales de construcción
J = range(1, len(C()) + 1) #Tipo de vivienda a construir según cantidad de integrantes por familia
#Ki = range(1, D() + 1) #Variedad del material i
Mp = range(1, G() + 1) #Tipo de maquinaria m que puede utilizar el personal p
P = range(1, E() + 1) #Tipo de personal
#REVISARRR
OMEGA = range(1, len(H())) #Pares de la forma (f, j) que representan el tipo de vivienda j a la que accederá familia f

#PARÁMETROS--------------------------------
#T: Plazo máximo, en días, de la duración del Plan de Reconstrucción
max_plazo = 700
#aij: Cantidad exacta de material del tipo i que se necesita para una vivienda j
cant_material = {(i, j): cantidad_material()[i, j] for i in I for j in J}

#cik: Costo en CLP de una unidad del material k del tipo i
costo_mat = {(i, k): costo_unidad_material()[i, k] for i in I for k in range(1, len(D(i))+1)}
print(costo_mat)

#dik: Costo fijo en CLP asociado al uso del material k del tipo i
costo_uso_mat = {(i, k): costo_uso_material()[i, k] for i in I for k in Ki}
#Xik: cantidad total disponible de la variante k del material del tipo i
cant_variante_material = {(i, k): cantidad_variante_material()[i, k] for i in I for k in Ki}
#betaik: Factor de calidad del material k del tipo i
calidad = {(i, k): factor_calidad()[i, k] for i in I for k in Ki}
#bij: Factor mínimo de calidad como promedio ponderado de las variantes utilizadas, para cada i y para cada j
calidad_promedio = {(i, j): factor_calidad_promedio()[i, j] for i in I for j in J}
#deltaik: Coeficiente de reducción de material por mala calidad para la variante k del tipo de material i
coef_red_m = {(i, k): coef_reduccion_m()[i, k] for i in I for k in Ki}
#-------------------------------------------
#dijp: REVISAR

#ej: Cantidad máxima de personas que pueden trabajar en una unidad de trabajo en vivienda j
#####max_personas = {j: cantidad_max_personas()[j] for j in J}
#fj: Cantidad máxima de tiempo que puede tardar la construcción de la vivienda j
#####max_tiempo = {j: cantidad_max_tiempo()[j] for j in J}
#gjp: Cantidad mínima de personas del tipo p requerida por unidad de trabajo para vivienda j
#####min_personas = {(j, p): cantidad_min_personas()[j, p] for j in J for p in P}
#qijk: Coeficiente de reducción de trabajo para el material k del tipo i en vivienda j
#####coef_red_t = {(i, j, k): coef_reduccion_t()[i, j, k] for i in I for j in J for k in Ki}
#rjpm: Índice de reducción de trabajo por unidad de trabajo realizada con el tipo de maquinaria m por p para j
#####ind_red = {(j, p, m): ind_reduccion()[j, p, m] for j in J for p in P for m in Mp}
#wfj: Indica si el Comité le construye a la familia f la vivienda j
#####comite = {(f, j): comite_construye()[f, j] for f in F for j in J}
#rhojp: Indica si el personal p puede utilizar la maquinaria para la construcción de la vivienda j
#####rho = {(j, p): utiliza_maquinaria()[j, p] for j in J for p in P}
#wf: Indica si el terreno donde va a construir su vivienda la familia f supera la pendiente máxima
#####pendiente = {f: pendiente_maxima()[f] for f in F}
#BM: Suma de todas las unidades de trabajo Zp de todos los personales p
BM = 9999
#Cmj: Costo asociado al uso de maquinaria m para la construcción de vivienda j
#####costo_maq = {(m, j): costo_maquinaria()[m, j] for m in Mp for j in J}
#Np: Cantidad de unidades de trabajo disponibles de cada tipo de personal p
#####uni_trabajo = {p: unidades_trabajo()[p] for p in P}
#Pik: Cantidad disponible de material k del tipo i
#####material_dispo = {(i, k): material_disponible()[i, k] for i in I for k in Ki}
#Qp: Cantidad máxima de personas de cada tipo de personal p
#####max_personal = {p: cantidad_max_personal()[p] for p in P}
#Sp: Sueldo por unidad de trabajo que cobra p
#####sueldo = {p: sueldo_personal()[p] for p in P}
#Zp: Cantidad máxima de unidades de trabajo disponibles de cada tipo de personal p
#####max_uni_trabajo = {p: maxima_unidades_trabajo()[p] for p in P}

#VARIABLES-------------------------------------
#Cantidad, en días de trabajo, que demora la construcción del tipo de vivienda j para la familia f
t = model.addVars(F, J, vtype = GRB.INTEGER, name = "t_fj")
#Cantidad real a utilizar de la variante k del tipo de material i en la construcción de j para f
x = model.addVars(F, J, I, Ki, vtype = GRB.INTEGER, name = "x_fjik")
#Cantidad ideal a utilizar de k del tipo i en la construcción de j para f
x_p = model.addVars(F, J, I, Ki, vtype = GRB.INTEGER, name = "x_p_fjik")
#Indica si se utiliza la opción k del material i en la construcción de la vivienda j para familia f
y = model.addVars(F, J, I, Ki, vtype = GRB.BINARY, name = "y_fjik")
#Días de trabajo realizadas por p (manual) con el material i con la variante k para la construcción de j para familia f
z = model.addVars(F, I, J, Ki, P, vtype = GRB.INTEGER, name = "z_fijkp")
#Cantidad de personas del tipo p que trabajan en la vivienda j
v = model.addVars(J, P, vtype = GRB.INTEGER, name = "v_jp")
#Cantidad de unidades de trabajo efectuadas a través del tipo de maquinaria m por p en j sobre i
u = model.addVars(I, J, P, Mp, vtype = GRB.INTEGER, name = "u_ijpm")
#Indica si se utiliza el tipo de maquinaria m por p en j sobre i
mu = model.addVars(I, J, P, Mp, vtype = GRB.BINARY, name = "mu_ijpm")

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
                    
