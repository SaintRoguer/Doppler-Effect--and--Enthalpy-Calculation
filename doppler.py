import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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
f_observada = f_inicial * ((v_onda + v_observador) / (v_onda - v_fuente))

# Configurar la animación
fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot([], [], label="Frecuencia observada", lw=2)
ax.axhline(f_inicial, color="red", linestyle="--", label="Frecuencia inicial")
ax.set_xlim(v_fuente_min, v_fuente_max)
ax.set_ylim(min(f_observada) * 0.9, max(f_observada) * 1.1)
ax.set_title("Efecto Doppler: Evolución de la Frecuencia Observada")
ax.set_xlabel("Velocidad de la Fuente (m/s)")
ax.set_ylabel("Frecuencia Observada (Hz)")
ax.legend()
ax.grid()

# Función de inicialización para la animación
def init():
    line.set_data([], [])
    return line,

# Función de actualización para la animación
def update(frame):
    line.set_data(v_fuente[:frame], f_observada[:frame])
    return line,

# Crear la animación
ani = animation.FuncAnimation(
    fig, update, frames=len(v_fuente), init_func=init, blit=True, repeat=False
)

# Guardar la animación como archivo MP4 o mostrarla
output_dir = "output_videos"
os.makedirs(output_dir, exist_ok=True)
file_name = os.path.join(output_dir, f"doppler_anim_f_{f_inicial}_v_{v_onda}.mp4")
ani.save(file_name.replace('.mp4', '.gif'), fps=10, writer='pillow')

print(f"Animación guardada como: {file_name}")

plt.show()
