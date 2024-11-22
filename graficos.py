import pandas as pd 
import matplotlib
import gurobipy
import matplotlib.pyplot as plt
from tabulate import tabulate
from main import cantidad_material_variante, cantidad_material_variante_2, total_trabajadores_vivienda, tiempo_total_trabajador_vivienda, tiempo_total_trabajador, tiempo_total_maquina_vivienda, tiempo_total_maquina, total_maquinas_usadas, dias_cantidad, cantidad_maxima
from main import valor_objetivo, dias_construccion, cantidad_material_usado, dias_trabajo_manual, dias_trabajo_maquina
import os
from matplotlib.ticker import MultipleLocator
import numpy as np

#matplotlib.use('TkAgg')

#RESULTADOS VARIABLES

data_dias_construccion = pd.DataFrame(dias_construccion, columns = ['Vivienda', 'Días'])
plt.bar(data_dias_construccion['Vivienda'], data_dias_construccion['Días'])
plt.title(f"Tiempo Vivienda - Días")
plt.xlabel('Vivienda')
plt.ylabel('Días')
plt.savefig(os.path.join('resultados_variables', 'vivienda_dias.png'))
plt.close()
plt.figure()

data_cmv = pd.DataFrame(cantidad_material_usado, columns = ['Vivienda', 'Material', 'Variante', 'Cantidad'])
data_cmv['Material_Variante'] = data_cmv['Variante'].astype(str)
output_folder = os.path.join('resultados_variables', 'graficos_por_vivienda')
for vivienda in data_cmv['Vivienda'].unique():
    data_vivienda = data_cmv[data_cmv['Vivienda'] == vivienda]  
    pivot_data = data_vivienda.pivot_table(index='Material', columns='Variante', values='Cantidad', aggfunc='sum', fill_value=0)
    ax = pivot_data.plot(
        kind='bar', stacked=True, width=0.8, figsize=(10, 12),
        colormap='tab20', edgecolor='black'
    )
    plt.title(f'Vivienda {vivienda}: Materiales y Variantes', fontsize=14)
    plt.xlabel('Material', fontsize=12)
    plt.ylabel('Cantidad', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.legend(title="Variantes", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    ax.yaxis.set_ticks(range(0, int(pivot_data.values.max()) + 51, 50))
    for bar_group in ax.containers:
        for bar in bar_group:
            height = bar.get_height()
            if height > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2, 
                    bar.get_y() + height / 2,
                    f'{height:.1f}',
                    ha='center', va='center', fontsize=8, color='black'
                )
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, f'vivienda_{vivienda}_materiales_variantes.png'))
    plt.close()

tabla_z = tabulate(dias_trabajo_manual, headers=['Vivienda', 'Material', 'Variante', 'Trabajador', 'Días'])
tabla_z += "\n"
carpeta  = os.path.join('resultados_variables', "resultados_variable_z.txt")
with open(carpeta, "w") as archivo:
    archivo.write("Tabla Variable z")
    archivo.write("\n")
    archivo.write(tabla_z)
    archivo.write("\n")

tabla_u = tabulate(dias_trabajo_maquina, headers=['Vivienda', 'Material', 'Variante', 'Trabajador', 'Maquina', 'Días'])
tabla_u += "\n"
carpeta  = os.path.join('resultados_variables', "resultados_variable_u.txt")
with open(carpeta, "w") as archivo:
    archivo.write("Tabla Variable u")
    archivo.write("\n")
    archivo.write(tabla_u)
    archivo.write("\n")

#TABLAS RESTRICCIONES

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