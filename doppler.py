import numpy as np
import matplotlib.pyplot as plt
import os

# Función para solicitar valores con opción de usar valores predeterminados
def solicitar_valor(prompt, default):
    valor = input(f"{prompt} (por defecto: {default}): ")
    return float(valor) if valor.strip() else default

# Valores por defecto
default_v_onda = 343.0  # Velocidad del sonido en el aire (m/s)
default_f_inicial = 1000.0  # Frecuencia inicial (Hz)
default_v_observador = 0.0  # Observador en reposo (m/s)
default_v_fuente_min = 0.0  # Velocidad mínima de la fuente (m/s)
default_v_fuente_max = 300.0  # Velocidad máxima de la fuente (m/s)
default_v_fuente_pasos = 50  # Número de pasos

# Solicitar al usuario los valores con opción de usar valores predeterminados
v_onda = solicitar_valor("Ingrese la velocidad de la onda en el medio (m/s)", default_v_onda)
f_inicial = solicitar_valor("Ingrese la frecuencia inicial (Hz)", default_f_inicial)
v_observador = solicitar_valor("Ingrese la velocidad del observador (m/s)", default_v_observador)
v_fuente_min = solicitar_valor("Ingrese la velocidad mínima de la fuente (m/s)", default_v_fuente_min)
v_fuente_max = solicitar_valor("Ingrese la velocidad máxima de la fuente (m/s)", default_v_fuente_max)
v_fuente_pasos = int(solicitar_valor("Ingrese el número de pasos para la velocidad de la fuente", default_v_fuente_pasos))

# Generar valores de velocidad de la fuente
v_fuente = np.linspace(v_fuente_min, v_fuente_max, v_fuente_pasos)

# Calcular la frecuencia observada para cada velocidad de la fuente
f_observada = []
for v_s in v_fuente:
    # Efecto Doppler: Frecuencia observada
    f = f_inicial * ((v_onda + v_observador) / (v_onda - v_s))
    f_observada.append(f)

# Crear la gráfica
plt.figure(figsize=(10, 6))
plt.plot(v_fuente, f_observada, label="Frecuencia observada")
plt.axhline(f_inicial, color="red", linestyle="--", label="Frecuencia inicial")
plt.title("Efecto Doppler: Frecuencia Observada vs Velocidad de la Fuente")
plt.xlabel("Velocidad de la Fuente (m/s)")
plt.ylabel("Frecuencia Observada (Hz)")
plt.legend()
plt.grid()

# Guardar la gráfica en un archivo PNG
output_dir = "output_images"
os.makedirs(output_dir, exist_ok=True)  # Crear directorio si no existe
file_name = os.path.join(output_dir, f"doppler_f_{f_inicial}_v_{v_onda}_steps_{v_fuente_pasos}.png")
plt.savefig(file_name)

print(f"Gráfica guardada como: {file_name}")
