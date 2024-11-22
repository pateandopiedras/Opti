import pandas as pd 
import matplotlib
import gurobipy
import matplotlib.pyplot as plt
from tabulate import tabulate
from main import cost_viv, cost_unit_mat, cost_fij_mat, cost_sueld, cost_maq, valor_objetivo
from main import dias_construccion, cantidad_material_variante, cantidad_material_variante_2, total_trabajadores_vivienda, tiempo_total_trabajador_vivienda, tiempo_total_trabajador, tiempo_total_maquina_vivienda, tiempo_total_maquina, total_maquinas_usadas, dias_cantidad, cantidad_maxima
import os
import numpy as np

#matplotlib.use('TkAgg')

data_dias_construccion = pd.DataFrame(dias_construccion, columns = ['Vivienda', 'Días'])
plt.bar(data_dias_construccion['Vivienda'], data_dias_construccion['Días'])
plt.title(f"Tiempo Vivienda - Días")
plt.xlabel('Vivienda')
plt.ylabel('Días')
plt.savefig(os.path.join('graficos', 'vivienda_dias.png'))
plt.close()
plt.figure()

#data_cmv = pd.DataFrame(cantidad_material_variante, columns = ['Vivienda', 'Material', 'Variante', 'Cantidad'])
#plt.bar(data_cmv['Vivienda'], data_cmv['Material'], data_cmv['Variante'])
#plt.title('Cantidad Vivienda - Material - Variante')
#plt.xlabel('Vivienda')
#plt.ylabel('Cantidad')
#data_cmv['Material_Variante'] = data_cmv['Material'].astype(str) + " - Variante " + data_cmv['Variante'].astype(str)
#g_data = data_cmv.pivot_table(index='Vivienda', columns='Material_Variante', values='Cantidad', aggfunc='sum', fill_value=0)
#g_data.plot(kind='bar', stacked=True, figsize=(10, 7))
#fig, ax = plt.subplots(figsize=(10, 7))
#barras = g_data.plot(kind='bar', stacked=True, ax=ax)
#for i, bar_group in enumerate(barras.containers): 
    #for bar in bar_group:
        #height = bar.get_height()
        #if height > 0:
            #x_pos = bar.get_x() + bar.get_width() / 2
            #y_pos = bar.get_y() + height / 2
            #ax.text(
                #x_pos, y_pos, f'{height:.2f}',
                #ha='center', va='center', fontsize=8, color='black')
#plt.savefig(os.path.join('graficos', 'cantidad_material_variante.png'))
#plt.close()
#plt.figure()


# Crear el gráfico de barras horizontales

#data = pd.DataFrame(calidad_materiales, columns = ['Vivienda', 'Material', 'Variante', 'Cantidad', 'Calidad Promedio'])
## Definir calidad mínima (valor arbitrario)
#calidad_minima = 10
# Crear el gráfico
#fig, ax = plt.subplots(figsize=(10, 6))
# Usar los materiales para las posiciones en el eje Y
#y_pos = np.arange(len(data['Material']))
# Dibujar las barras horizontales, usando 'Calidad Promedio' para la altura de las barras
#ax.barh(y_pos, data['Calidad Promedio'], color='skyblue', edgecolor='black', label='Calidad Promedio')
# Dibujar una línea vertical para la calidad mínima
#ax.axvline(calidad_minima, color='red', linestyle='--', label='Calidad Mínima')
# Etiquetas y detalles
#ax.set_yticks(y_pos)
#ax.set_yticklabels(data['Material'])  # Asignar etiquetas de los materiales
#ax.set_xlabel('Calidad Promedio')
#ax.set_title('Cumplimiento de Calidad Mínima por Tipo de Material')
#ax.legend(loc='lower right')
# Ajustar el gráfico para que todo encaje bien
#plt.tight_layout()
# Mostrar el gráfico
#plt.show()
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

#plt.show()

tabla_2 = tabulate(cantidad_material_variante, headers=['Vivienda', 'Material-Variante', 'Cantidad Utilizada'])
tabla_2 += "\n"

tabla_3 = tabulate(cantidad_material_variante_2, headers=['Vivienda', 'Material', 'Variante', 'Cantidad Utilizada'])
tabla_3 += "\n"

tabla_6 = tabulate(cantidad_maxima, headers=['Material', 'Variedad', 'Trabajador', 'Cantidad Usada', 'Cantidad Máxima'])
tabla_6 += "\n"

tabla_8 = tabulate(total_trabajadores_vivienda, headers=['Vivienda', 'Total Trabajadores'])
tabla_8 += "\n"

tabla_9 = tabulate(dias_cantidad, headers=['Vivienda', 'Material', 'Variante', 'Total', 'Utilizada'])
tabla_9 += "\n"

tabla_10 = tabulate(tiempo_total_trabajador_vivienda, headers=['Vivienda', 'Trabajador', 'Tiempo'])
tabla_10 += "\n"

tabla_11 = tabulate(tiempo_total_trabajador, headers=['Trabajador', 'Tiempo'])
tabla_11 += "\n"

tabla_12 = tabulate(tiempo_total_maquina_vivienda, headers=['Vivienda', 'Maquina', 'Tiempo'])
tabla_12 += "\n"

tabla_13 = tabulate(tiempo_total_maquina, headers=['Maquina', 'Tiempo'])
tabla_13 += "\n"

tabla_16 = tabulate(total_maquinas_usadas, headers=['Vivienda', 'Total Máquinas Usadas'])
tabla_16 += "\n"

with open("resultados_generales.txt", "w") as archivo:
    archivo.write(f'El proyecto tiene un costo de {valor_objetivo} $CLP')
    archivo.write("\n")

    archivo.write("Tabla R2")
    archivo.write("\n")
    archivo.write(tabla_2)
    archivo.write("\n")
    
    archivo.write("Tabla R3")
    archivo.write("\n")
    archivo.write(tabla_3)
    archivo.write("\n")

    archivo.write("Tabla R6")
    archivo.write("\n")
    archivo.write(tabla_6)
    archivo.write("\n")

    archivo.write("Tabla R8")
    archivo.write("\n")
    archivo.write(tabla_8)
    archivo.write("\n")

    archivo.write("Tabla R9")
    archivo.write("\n")
    archivo.write(tabla_9)
    archivo.write("\n")

    archivo.write("Tabla R10")
    archivo.write("\n")
    archivo.write(tabla_10)
    archivo.write("\n")

    archivo.write("Tabla R11")
    archivo.write("\n")
    archivo.write(tabla_11)
    archivo.write("\n")

    archivo.write("Tabla R12")
    archivo.write("\n")
    archivo.write(tabla_12)
    archivo.write("\n")

    archivo.write("Tabla R13")
    archivo.write("\n")
    archivo.write(tabla_13)
    archivo.write("\n")
    
    archivo.write("Tabla R16")
    archivo.write("\n")
    archivo.write(tabla_16)
    archivo.write("\n")



print("Las tablas se guardaron correctamente")