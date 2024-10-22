import pandas as pd 
import matplotlib.pyplot as plt
from tabulate import tabulate
from main import cost_viv, cost_unit_mat, cost_fij_mat, cost_sueld, cost_maq, valor_objetivo

data_cost_viv = pd.DataFrame(cost_viv, columns = ['Vivienda', 'Costo'])
plt.bar(data_cost_viv['Vivienda'], data_cost_viv['Costo'])
plt.title('Costo de la construcción de una vivienda')
plt.xlabel('Vivienda')
plt.ylabel('Costo')
plt.show()

data_cost_sueld = pd.DataFrame(cost_sueld, columns = ['Trabajador', 'Sueldo'])
plt.bar(data_cost_sueld['Trabajador'], data_cost_sueld['Sueldo'])
plt.title('Sueldo de Trabajador')
plt.xlabel('Trabajador')
plt.ylabel('Sueldo')
plt.show()

data_cost_maq = pd.DataFrame(cost_maq, columns = ['Maquinaria', 'Costo'])
plt.bar(data_cost_maq['Maquinaria'], data_cost_maq['Costo'])
plt.title('Costo Diario asociado a Maquinaria')
plt.xlabel('Maquinaria')
plt.ylabel('Costo')
plt.show()

data_cost_viv1 = pd.DataFrame(cost_viv, columns = ['Vivienda', 'Costo'])
plt.plot(data_cost_viv1['Vivienda'], data_cost_viv1['Costo'])
plt.title('Costo de la construcción de una vivienda')
plt.xlabel('Vivienda')
plt.ylabel('Costo')
plt.show()

data_cost_sueld1 = pd.DataFrame(cost_sueld, columns = ['Trabajador', 'Sueldo'])
plt.plot(data_cost_sueld1['Trabajador'], data_cost_sueld1['Sueldo'])
plt.title('Sueldo de Trabajador')
plt.xlabel('Trabajador')
plt.ylabel('Sueldo')
plt.show()

data_cost_maq1 = pd.DataFrame(cost_maq, columns = ['Maquinaria', 'Costo'])
plt.plot(data_cost_maq1['Maquinaria'], data_cost_maq1['Costo'])
plt.title('Costo Diario asociado a Maquinaria')
plt.xlabel('Maquinaria')
plt.ylabel('Costo')
plt.show()

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