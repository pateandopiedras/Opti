import pandas as pd 
import matplotlib.pyplot as plt
from tabulate import tabulate
from main import cost_viv, cost_unit_mat, cost_fij_mat, cost_sueld, cost_maq

data_cost_viv = pd.DataFrame(cost_viv, columns = ['Vivienda', 'Costo'])
plt.bar(data_cost_viv['Vivienda'], data_cost_viv['Costo'])
plt.title('Costo de la construcción de una vivienda')
plt.xlabel('Vivienda')
plt.ylabel('Costo')
plt.show()