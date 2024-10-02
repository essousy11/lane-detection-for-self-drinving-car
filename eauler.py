import numpy as np
import matplotlib.pyplot as plt
from def_func_ode import f1  # Importer la fonction f1 depuis le fichier def_fonc_ode

def euler_explicit(f, intervalle_temps, h, y0):
    temps = np.arange(intervalle_temps[0], intervalle_temps[1] + h, h)
    solution = [y0]

    for t in temps[:-1]:
        y_next = solution[-1] + h * f(t, solution[-1])
        solution.append(y_next)

    return temps, np.array(solution)

# Paramètres
a, b = 0, 1
h = 0.1
y0 = 1

# Appel de la méthode d'Euler explicite
temps_euler, solution_euler = euler_explicit(f1, [a, b], h, y0)

# Solution analytique pour comparer (à adapter selon votre équation différentielle réelle)
solution_analytique = np.exp(temps_euler)

# Tracer les résultats
plt.plot(temps_euler, solution_euler, label='Euler Explicite')
plt.plot(temps_euler, solution_analytique, label='Analytique')
plt.legend()
plt.xlabel('Temps')
plt.ylabel('Solution')
plt.title('Comparaison Euler Explicite et Solution Analytique')
plt.show()