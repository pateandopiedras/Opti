import pandas as pd 
import matplotlib
import gurobipy
import matplotlib.pyplot as plt
from tabulate import tabulate
from main import cost_viv, cost_unit_mat, cost_fij_mat, cost_sueld, cost_maq, valor_objetivo
from main import dias_construccion, cantidad_material_variante
import os

#matplotlib.use('TkAgg')

data_dias_construccion = pd.DataFrame(dias_construccion, columns = ['Vivienda', 'Días'])
plt.bar(data_dias_construccion['Vivienda'], data_dias_construccion['Días'])
plt.title(f"Tiempo Vivienda - Días")
plt.xlabel('Vivienda')
plt.ylabel('Días')
plt.savefig(os.path.join('graficos', 'vivienda_dias.png'))
plt.close()
plt.figure()

data_cmv = pd.DataFrame(cantidad_material_variante, columns = ['Vivienda', 'Material', 'Variante', 'Cantidad'])
#plt.bar(data_cmv['Vivienda'], data_cmv['Material'], data_cmv['Variante'])
plt.title('Cantidad Vivienda - Material - Variante')
plt.xlabel('Vivienda')
plt.ylabel('Cantidad')
data_cmv['Material_Variante'] = data_cmv['Material'].astype(str) + " - Variante " + data_cmv['Variante'].astype(str)
g_data = data_cmv.pivot_table(index='Vivienda', columns='Material_Variante', values='Cantidad', aggfunc='sum', fill_value=0)
#g_data.plot(kind='bar', stacked=True, figsize=(10, 7))
fig, ax = plt.subplots(figsize=(10, 7))
barras = g_data.plot(kind='bar', stacked=True, ax=ax)
for i, bar_group in enumerate(barras.containers): 
    for bar in bar_group:
        height = bar.get_height()
        if height > 0:
            x_pos = bar.get_x() + bar.get_width() / 2
            y_pos = bar.get_y() + height / 2
            ax.text(
                x_pos, y_pos, f'{height:.2f}',
                ha='center', va='center', fontsize=8, color='black')
plt.savefig(os.path.join('graficos', 'cantidad_material_variante.png'))
plt.close()
plt.figure()

#data_dtmm = pd.DataFrame(dias_trabajo_manual_maquina, columns = ['Trabajador', 'Material', 'Variante', 'Cantidad'])


#data_cost_viv = pd.DataFrame(cost_viv, columns = ['Vivienda', 'Costo'])
#plt.bar(data_cost_viv['Vivienda'], data_cost_viv['Costo'])
#plt.title('Costo de la construcción de una vivienda')
#plt.xlabel('Vivienda')
#plt.ylabel('Costo')
#plt.savefig(os.path.join('graficos', 'grafica1.png'))
#plt.title(f"grafica1")
#plt.close()
#plt.figure()

#data_cost_sueld = pd.DataFrame(cost_sueld, columns = ['Trabajador', 'Sueldo'])
#plt.bar(data_cost_sueld['Trabajador'], data_cost_sueld['Sueldo'])
#plt.title('Sueldo de Trabajador')
#plt.xlabel('Trabajador')
#plt.ylabel('Sueldo')
#plt.savefig("grafica2.png")
#plt.close()
#plt.figure()

#data_cost_maq = pd.DataFrame(cost_maq, columns = ['Maquinaria', 'Costo'])
#plt.bar(data_cost_maq['Maquinaria'], data_cost_maq['Costo'])
#plt.title('Costo Diario asociado a Maquinaria')
#plt.xlabel('Maquinaria')
#plt.ylabel('Costo')
#plt.savefig("grafica3.png")
#plt.close()
#plt.figure()

#data_cost_viv1 = pd.DataFrame(cost_viv, columns = ['Vivienda', 'Costo'])
#plt.plot(data_cost_viv1['Vivienda'], data_cost_viv1['Costo'])
#plt.title('Costo de la construcción de una vivienda')
#plt.xlabel('Vivienda')
#plt.ylabel('Costo')
#plt.title(f"grafica4")
#plt.close()
#plt.figure()

#data_cost_sueld1 = pd.DataFrame(cost_sueld, columns = ['Trabajador', 'Sueldo'])
#plt.plot(data_cost_sueld1['Trabajador'], data_cost_sueld1['Sueldo'])
#plt.title('Sueldo de Trabajador')
#plt.xlabel('Trabajador')
#plt.ylabel('Sueldo')
#plt.savefig("grafica5.png")
#plt.close()
#plt.figure()

#data_cost_maq1 = pd.DataFrame(cost_maq, columns = ['Maquinaria', 'Costo'])
#plt.plot(data_cost_maq1['Maquinaria'], data_cost_maq1['Costo'])
#plt.title('Costo Diario asociado a Maquinaria')
#plt.xlabel('Maquinaria')
#plt.ylabel('Costo')
#plt.savefig("grafica6.png")
#plt.close()

#plt.show()

tabla_cost_unit_mat = tabulate(cost_unit_mat, headers=['Tipo', 'Material', 'CostoUnitario'])
tabla_cost_unit_mat += "\n"

tabla_cost_fij_mat = tabulate(cost_fij_mat, headers=['Tipo', 'Material', 'CostoFijo'])
tabla_cost_fij_mat += "\n"


with open("resultados_generales.txt", "w") as archivo:
    archivo.write(f'El proyecto tiene un costo de {valor_objetivo} $CLP por construcción de casa')
    archivo.write("\n")

    archivo.write("Tabla de Costo unitario de Material y Tipo")
    archivo.write("\n")
    archivo.write(tabla_cost_unit_mat)
    archivo.write("\n")
    
    archivo.write("Tabla de Costo fijo de Material y Tipo")
    archivo.write("\n")
    archivo.write(tabla_cost_fij_mat)
    archivo.write("\n")

print("Las tablas se guardaron correctamente")