import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Tabla de entalpías de formación estándar en kJ/mol
entalpias_formacion = {
    "H2O (l)": {"valor": -285.83, "ref": "Chemical Principles, 7th Ed., Zumdahl"},
    "CO2 (g)": {"valor": -393.52, "ref": "Chemical Principles, 7th Ed., Zumdahl"},
    "CH4 (g)": {"valor": -74.87, "ref": "Chemical Principles, 7th Ed., Zumdahl"},
    "O2 (g)": {"valor": 0.00, "ref": "Chemical Principles, 7th Ed., Zumdahl"},
    "H2 (g)": {"valor": 0.00, "ref": "Chemical Principles, 7th Ed., Zumdahl"},
    "N2 (g)": {"valor": 0.00, "ref": "Chemical Principles, 7th Ed., Zumdahl"},
    "NH3 (g)": {"valor": -45.94, "ref": "Chemical Principles, 7th Ed., Zumdahl"},
    "C2H5OH (l)": {"valor": -277.0, "ref": "Chemical Principles, 7th Ed., Zumdahl"},
    "CaCO3 (s)": {"valor": -1207.0, "ref": "Chemical Principles, 7th Ed., Zumdahl"},
    "CaO (s)": {"valor": -635.0, "ref": "Chemical Principles, 7th Ed., Zumdahl"},
    "HCl (aq)": {"valor": -167.2, "ref": "Chemical Principles, 7th Ed., Zumdahl"},
    "NaOH (aq)": {"valor": -469.6, "ref": "Chemical Principles, 7th Ed., Zumdahl"},
    "NaCl (aq)": {"valor": -407.1, "ref": "Chemical Principles, 7th Ed., Zumdahl"}
}

reaccion_metano = {
    "reactivos": [("CH4 (g)", 1), ("O2 (g)", 2)],
    "productos": [("CO2 (g)", 1), ("H2O (l)", 2)],
    "delta_n_gases": -2  # 3 moles de gases reactivos → 3 moles de gases productos
}

reaccion_hidrogeno = {
    "reactivos": [("H2 (g)", 2), ("O2 (g)", 1)],
    "productos": [("H2O (l)", 2)],
    "delta_n_gases": -1  # 3 moles de gases reactivos → 0 moles de gases productos
}

reaccion_amoniaco = {
    "reactivos": [("N2 (g)", 1), ("H2 (g)", 3)],
    "productos": [("NH3 (g)", 2)],
    "delta_n_gases": -2  # 4 moles de gases reactivos → 2 moles de gases productos
}

reaccion_electrolisis = {
    "reactivos": [("H2O (l)", 2)],
    "productos": [("H2 (g)", 2), ("O2 (g)", 1)],
    "delta_n_gases": +3  # 0 moles de gases reactivos → 3 moles de gases productos
}

reaccion_etanol = {
    "reactivos": [("C2H5OH (l)", 1), ("O2 (g)", 3)],
    "productos": [("CO2 (g)", 2), ("H2O (l)", 3)],
    "delta_n_gases": -2  # 3 moles de gases reactivos → 1 mol de gas productos
}

reaccion_ca_co3 = {
    "reactivos": [("CaCO3 (s)", 1)],
    "productos": [("CaO (s)", 1), ("CO2 (g)", 1)],
    "delta_n_gases": +1  # 0 moles de gases reactivos → 1 mol de gas productos
}

reaccion_neutralizacion = {
    "reactivos": [("HCl (aq)", 1), ("NaOH (aq)", 1)],
    "productos": [("H2O (l)", 1), ("NaCl (aq)", 1)],
    "delta_n_gases": 0  # No hay gases involucrados
}


def calcular_delta_h(reaccion):
    """
    Calcula el cambio de entalpía basado en la reacción proporcionada.
    
    Args:
        reaccion (dict): Diccionario con las claves 'productos' y 'reactivos',
                        cada uno conteniendo una lista de tuplas (compuesto, coeficiente)
    
    Returns:
        float: Cambio de entalpía en kJ
    
    Raises:
        KeyError: Si algún compuesto no está en la base de datos
    """
    delta_h_productos = sum(entalpias_formacion[compuesto]["valor"] * coef 
                          for compuesto, coef in reaccion['productos'])
    delta_h_reactivos = sum(entalpias_formacion[compuesto]["valor"] * coef 
                           for compuesto, coef in reaccion['reactivos'])
    return delta_h_productos - delta_h_reactivos

def calcular_delta_u(delta_h, delta_n_gases, temperatura=298):
    """Calcula el cambio de energía interna (\Delta U) a partir de \Delta H."""
    R = 8.314 / 1000  # Constante de los gases ideales en kJ/mol·K
    return delta_h - delta_n_gases * R * temperatura

def ingresar_reaccion():
    """Permite al usuario ingresar una reacción personalizada."""
    print("Ingrese los reactivos:")
    reactivos = []
    while True:
        compuesto = input("Compuesto (o 'fin' para terminar): ").strip()
        if compuesto.lower() == "fin":
            break
        coef = float(input(f"Coeficiente de {compuesto}: "))
        reactivos.append((compuesto, coef))
    
    print("Ingrese los productos:")
    productos = []
    while True:
        compuesto = input("Compuesto (o 'fin' para terminar): ").strip()
        if compuesto.lower() == "fin":
            break
        coef = float(input(f"Coeficiente de {compuesto}: "))
        productos.append((compuesto, coef))
    
    delta_n_gases = int(input("Cambio en el número de moles de gases (\u0394n_gases): "))
    return {"reactivos": reactivos, "productos": productos, "delta_n_gases": delta_n_gases}

def mostrar_ecuacion_quimica(reaccion):
    """
    Muestra la ecuación química balanceada.
    
    Args:
        reaccion (dict): Diccionario con la información de la reacción
    """
    # Formatear reactivos
    reactivos_str = " + ".join(f"{coef if coef != 1 else ''}{compuesto}" 
                              for compuesto, coef in reaccion['reactivos'])
    # Formatear productos
    productos_str = " + ".join(f"{coef if coef != 1 else ''}{compuesto}" 
                              for compuesto, coef in reaccion['productos'])
    print(f"\nEcuación química balanceada:")
    print(f"{reactivos_str} → {productos_str}")

# Función para graficar el diagrama de entalpía
def graficar_diagrama_entalpia(delta_h, reaccion):
    entalpia_reactivos = sum(coef * entalpias_formacion[compuesto]["valor"] for compuesto, coef in reaccion["reactivos"])
    entalpia_productos = sum(coef * entalpias_formacion[compuesto]["valor"] for compuesto, coef in reaccion["productos"])

    niveles = [entalpia_reactivos, entalpia_productos]
    etiquetas = ["Reactivos", "Productos"]
    
    plt.figure(figsize=(8, 6))
    plt.plot([0, 1], niveles, marker='o', color='blue', linestyle='--')
    
    plt.annotate(f"ΔH = {delta_h:.2f} kJ", 
                 xy=(0.5, (entalpia_reactivos + entalpia_productos) / 2), 
                 xytext=(0.5, (entalpia_reactivos + entalpia_productos) / 2 + 50),
                 arrowprops=dict(facecolor='black', arrowstyle='->'),
                 ha='center')
    
    plt.text(0, entalpia_reactivos + 10, f"{entalpia_reactivos:.2f} kJ", ha='center')
    plt.text(1, entalpia_productos + 10, f"{entalpia_productos:.2f} kJ", ha='center')

    plt.xticks([0, 1], etiquetas)
    plt.ylabel("Entalpía (kJ/mol)")
    plt.title("Diagrama de Entalpía de la Reacción")
    plt.grid(True, linestyle='--', alpha=0.6)
    
    tipo_reaccion = "Exotérmica" if delta_h < 0 else "Endotérmica"
    plt.figtext(0.5, 0.02, f"Reacción {tipo_reaccion}", ha="center", fontsize=10, color='red')
    
    plt.show()


def main():
    print("="*60)
    print("Cálculo de Parámetros Termodinámicos de Reacciones Químicas")
    print("="*60)
    
    print("Compuestos disponibles:")
    for compuesto, entalpia in entalpias_formacion.items():
        print(f"{compuesto}: {entalpia['valor']} kJ/mol (Referencia: {entalpia['ref']})")
    
    opcion = input("\n¿Desea usar compuestos tabulados (1) o ingresar sus propios valores (2)? ").strip()
    
    if opcion == "1":
        print("\nSeleccione una reacción :")
        print("1. Combustión de metano (CH4 + O2 → CO2 + H2O)")
        print("2. Combustión de hidrógeno (H2 + O2 → H2O)")
        print("3. Síntesis de amoníaco (N2 + H2 → NH3)")
        print("4. Electrólisis del agua (H2O → H2 + O2)")
        print("5. Combustión del etanol (C2H5OH + O2 → CO2 + H2O)")
        print("6. Descomposición de CaCO3 (CaCO3 → CaO + CO2)")
        print("7. Neutralización de HCl con NaOH (HCl + NaOH → H2O + NaCl)")
        
        seleccion = input("Ingrese el número de la reacción deseada: ").strip()
        
        if seleccion == "1":
            reaccion = reaccion_metano
        elif seleccion == "2":
            reaccion = reaccion_hidrogeno
        elif seleccion == "3":
            reaccion = reaccion_amoniaco
        elif seleccion == "4":
            reaccion = reaccion_electrolisis
        elif seleccion == "5":
            reaccion = reaccion_etanol
        elif seleccion == "6":
            reaccion = reaccion_ca_co3
        elif seleccion == "7":
            reaccion = reaccion_neutralizacion
        else:
            print("Selección inválida. Saliendo del programa.")
            return

    elif opcion == "2":
        reaccion = ingresar_reaccion()
    else:
        print("Opción inválida. Saliendo del programa.")
        return

    
    try:
        mostrar_ecuacion_quimica(reaccion)
        delta_h = calcular_delta_h(reaccion)
        delta_u = calcular_delta_u(delta_h, reaccion["delta_n_gases"])
        
        print("\nResultados:")
        print("-"*30)
        print(f"ΔH (cambio de entalpía): {delta_h:.2f} kJ")
        print(f"ΔU (cambio de energía interna): {delta_u:.2f} kJ")
        
        # Agregar interpretación del resultado
        if delta_h < 0:
            print("\nLa reacción es exotérmica (libera energía al entorno)")
        else:
            print("\nLa reacción es endotérmica (absorbe energía del entorno)")
         # Llamar al diagrama de entalpía
        graficar_diagrama_entalpia(delta_h, reaccion)
            
    except KeyError as e:
        print(f"Error: Compuesto no encontrado en la tabla: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
