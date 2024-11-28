import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation

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

# Ver estilos disponibles
print("Estilos disponibles:", plt.style.available)

# Usar un estilo incorporado más profesional
plt.style.use('seaborn-v0_8-darkgrid')  # Estilo más profesional para presentaciones

# Definir una paleta de colores profesional
COLORS = {
    'primary': '#1f77b4',     # Azul profesional
    'secondary': '#ff7f0e',   # Naranja para contraste
    'accent': '#2ca02c',      # Verde para elementos destacados
    'warning': '#d62728',     # Rojo para zonas críticas
    'background': '#f0f0f0'   # Gris claro para fondos
}

# Crear una figura con dos subplots
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(2, 1, height_ratios=[1.2, 1], hspace=0.4)
ax1 = fig.add_subplot(gs[0])  # Gráfica estática
ax2 = fig.add_subplot(gs[1])  # Animación

# Gráfica estática (superior)
ax1.plot(v_fuente, f_observada, label="Frecuencia observada", linewidth=3, color=COLORS['primary'])
ax1.axhline(f_inicial, color=COLORS['secondary'], linestyle="--", label="Frecuencia inicial", linewidth=2)
ax1.axvspan(v_onda, v_fuente_max, alpha=0.15, color=COLORS['warning'], label='Región supersónica')

# Añadir ecuación del efecto Doppler
equation = r"$f_{observada} = f_{inicial}\cdot\frac{v_{onda} + v_{observador}}{v_{onda} - v_{fuente}}$"
ax1.text(0.02, 0.95, equation, transform=ax1.transAxes, fontsize=14, 
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

# Configurar la gráfica estática
ax1.set_title("Análisis del Efecto Doppler\nVariación de la Frecuencia en Función de la Velocidad", 
              fontsize=16, pad=20, weight='bold')
ax1.set_xlabel("Velocidad de la Fuente (m/s)", fontsize=14, weight='bold')
ax1.set_ylabel("Frecuencia Observada (Hz)", fontsize=14, weight='bold')
ax1.legend(loc='upper right', fontsize=10, framealpha=0.9)
ax1.grid(True, linestyle='--', alpha=0.7)

# Agregar anotación en la gráfica estática
ax1.annotate(f'Frecuencia inicial: {f_inicial} Hz\nVelocidad del sonido: {v_onda} m/s',
             xy=(0, f_inicial), xytext=(50, f_inicial*1.2),
             arrowprops=dict(facecolor='black', shrink=0.05),
             bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))

# Añadir un punto móvil para la gráfica superior
freq_point, = ax1.plot([], [], 'ro', markersize=10, label='Frecuencia actual')
ax1.legend(loc='upper right', fontsize=10, framealpha=0.9)

# Configurar la animación (inferior)
x = np.linspace(-10, 10, 1000)
line, = ax2.plot([], [], lw=2)
source_point, = ax2.plot([], [], 'ro', markersize=10, label='Fuente')

# Configurar los límites de la animación
ax2.set_xlim(-10, 10)
ax2.set_ylim(-2, 2)
ax2.set_title('Simulación de Propagación de Ondas', fontsize=14, weight='bold')
ax2.set_xlabel('Distancia (m)', fontsize=12, weight='bold')
ax2.set_ylabel('Amplitud', fontsize=12, weight='bold')
ax2.grid(True)

# Añadir un panel de información más profesional
info_text = (
    f"Parámetros del sistema:\n"
    f"• Frecuencia inicial: {f_inicial:.1f} Hz\n"
    f"• Velocidad del medio: {v_onda:.1f} m/s\n"
    f"• Velocidad del observador: {v_observador:.1f} m/s\n"
    f"• Rango de velocidades: {v_fuente_min:.1f} - {v_fuente_max:.1f} m/s"
)
fig.text(0.02, 0.02, info_text, fontsize=10, 
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

# Función de inicialización para la animación
def init():
    line.set_data([], [])
    source_point.set_data([], [])
    freq_point.set_data([], [])
    return line, source_point, freq_point

# Función de actualización para la animación
def update(frame):
    t = frame * 0.1
    
    # Calcular la posición de la fuente en la animación
    source_pos = -5 + (v_fuente_max/100) * (t % 5)  # Movimiento cíclico
    
    # Calcular la velocidad actual de la fuente (mapear de posición a velocidad)
    current_velocity = (source_pos + 5) * (v_fuente_max/10)  # Mapear [-5, 5] a [0, v_fuente_max]
    
    # Calcular la frecuencia observada actual
    current_freq = f_inicial * ((v_onda + v_observador) / (v_onda - current_velocity))
    
    # Generar la onda
    wave = np.sin(2 * np.pi * (f_inicial * t - (x - source_pos)))
    
    # Actualizar la línea y los puntos
    line.set_data(x, wave)
    source_point.set_data([source_pos], [0])
    freq_point.set_data([current_velocity], [current_freq])
    
    return line, source_point, freq_point

# Crear la animación
ani = FuncAnimation(fig, update, init_func=init, frames=200,
                   interval=50, blit=True)

# Guardar la gráfica estática
output_dir = "output_images"
os.makedirs(output_dir, exist_ok=True)
file_name = os.path.join(output_dir, f"doppler_f_{f_inicial}_v_{v_onda}_steps_{v_fuente_pasos}.png")
plt.savefig(file_name)

print(f"Gráfica guardada como: {file_name}")
plt.show()
