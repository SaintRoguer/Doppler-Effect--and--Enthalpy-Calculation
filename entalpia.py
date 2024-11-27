# Tabla de entalpías de formación estándar en kJ/mol
entalpias_formacion = {
    "H2O (l)": -285.83,
    "CO2 (g)": -393.52,
    "CH4 (g)": -74.87,
    "O2 (g)": 0.00,
    "H2 (g)": 0.00,
    "N2 (g)": 0.00,
    "NH3 (g)": -45.94
}

def calcular_delta_h(reaccion):
    """Calcula el cambio de entalpía basado en la reacción proporcionada."""
    delta_h_productos = sum(entalpias_formacion[compuesto] * coef for compuesto, coef in reaccion['productos'])
    delta_h_reactivos = sum(entalpias_formacion[compuesto] * coef for compuesto, coef in reaccion['reactivos'])
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

def main():
    print("Cálculo de entalpía y energía interna de una reacción química")
    print("Compuestos disponibles:")
    for compuesto, entalpia in entalpias_formacion.items():
        print(f"{compuesto}: {entalpia} kJ/mol")
    
    opcion = input("\n¿Desea usar compuestos tabulados (1) o ingresar sus propios valores (2)? ").strip()
    
    if opcion == "1":
        # Ejemplo de reacción: Combustión de metano
        reaccion = {
            "reactivos": [("CH4 (g)", 1), ("O2 (g)", 2)],
            "productos": [("CO2 (g)", 1), ("H2O (l)", 2)],
            "delta_n_gases": -2  # 3 moles de gases reactivos -> 1 mol de gas producto
        }
    elif opcion == "2":
        reaccion = ingresar_reaccion()
    else:
        print("Opción inválida. Saliendo del programa.")
        return
    
    try:
        delta_h = calcular_delta_h(reaccion)
        delta_u = calcular_delta_u(delta_h, reaccion["delta_n_gases"])
        print(f"\nResultados:")
        print(f"  \u0394H (cambio de entalpía): {delta_h:.2f} kJ")
        print(f"  \u0394U (cambio de energía interna): {delta_u:.2f} kJ")
    except KeyError as e:
        print(f"Error: Compuesto no encontrado en la tabla: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
