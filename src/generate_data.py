"""
Script de generación de datos sintéticos para una cafetería de especialidad.

Genera ~15.000 transacciones de 18 meses con patrones realistas:
- Picos horarios (mañana y tarde)
- Estacionalidad (bebidas frías en verano)
- Días fuertes (sábados) y flojos (lunes)
- Productos estrella y productos muertos
- Combos naturales (café + pastelería)

Output: data/raw/cafeteria_transactions.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# ============================================================
# CONFIGURACIÓN — modificá acá los parámetros del negocio
# ============================================================

RANDOM_SEED = 42  # Para que los datos sean reproducibles
OUTPUT_PATH = "data/raw/cafeteria_transactions.csv"

# Rango temporal
START_DATE = datetime(2023, 11, 1)
END_DATE = datetime(2025, 5, 1)  # 18 meses

# Catálogo: producto, categoría, precio (UYU), popularidad (1-10), es_caliente
PRODUCTS = [
    # Cafés calientes (estrellas)
    ("Espresso", "Café", 130, 9, True),
    ("Espresso Doble", "Café", 170, 6, True),
    ("Cortado", "Café", 150, 8, True),
    ("Capuccino", "Café", 210, 10, True),
    ("Latte", "Café", 230, 9, True),
    ("Flat White", "Café", 240, 7, True),
    ("Mocha", "Café", 260, 5, True),
    ("Americano", "Café", 170, 6, True),
    
    # Bebidas frías (estacionales) — sin Frappé
    ("Cold Brew", "Bebida Fría", 240, 6, False),
    ("Iced Latte", "Bebida Fría", 260, 7, False),
    ("Limonada", "Bebida Fría", 200, 5, False),
    ("Té Helado", "Bebida Fría", 180, 3, False),
    
    # Pastelería — Carrot Cake ahora es ESTRELLA, Muffin es producto muerto
    ("Medialuna", "Pastelería", 90, 9, True),
    ("Croissant", "Pastelería", 180, 6, True),
    ("Brownie", "Pastelería", 220, 7, True),
    ("Cookie Clásica", "Pastelería", 120, 6, True),
    ("Cookie Chocolate Blanco y Pistacho", "Pastelería", 180, 7, True),  # Nueva especial
    ("Cheesecake", "Pastelería", 280, 4, True),
    ("Carrot Cake", "Pastelería", 260, 8, True),  # ⭐ Ahora estrella
    ("Muffin", "Pastelería", 180, 2, True),  # 💀 Ahora producto muerto
    
    # Comidas — Focaccias en lugar de wraps/sándwiches
    ("Tostado Jamón y Queso", "Comida", 320, 7, True),
    ("Avocado Toast", "Comida", 420, 6, True),
    ("Bowl Saludable", "Comida", 480, 5, True),
    ("Focaccia de Bondiola", "Comida", 440, 7, True),  # Nueva, popular
    ("Focaccia Vegetariana", "Comida", 380, 4, True),  # Nueva
]


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def get_hourly_weight(hour):
    """Devuelve un peso según la hora — modela picos de mañana y tarde."""
    if 7 <= hour < 8:
        return 0.5
    elif 8 <= hour < 10:
        return 3.5  # Pico mañana fuerte
    elif 10 <= hour < 12:
        return 1.5
    elif 12 <= hour < 14:
        return 2.0  # Almuerzo
    elif 14 <= hour < 16:
        return 1.0
    elif 16 <= hour < 18:
        return 2.5  # Pico merienda
    elif 18 <= hour < 20:
        return 1.2
    else:
        return 0.0  # Cerrado

def get_day_weight(weekday):
    """Devuelve peso por día de la semana (0=lunes, 6=domingo)."""
    weights = {
        0: 0.7,  # Lunes flojo
        1: 0.9,
        2: 0.95,
        3: 1.0,
        4: 1.1,
        5: 1.5,  # Sábado fuerte
        6: 1.2,  # Domingo
    }
    return weights[weekday]

def get_seasonal_multiplier(date, is_hot):
    """Las bebidas frías venden más en verano (dic-feb en hemisferio sur)."""
    month = date.month
    if not is_hot:  # bebida fría
        if month in [12, 1, 2]:
            return 2.5  # Verano
        elif month in [3, 4, 11]:
            return 1.2
        else:
            return 0.5  # Invierno (junio-agosto)
    else:  # bebida caliente
        if month in [6, 7, 8]:
            return 1.3  # Invierno: más café caliente
        else:
            return 1.0

def get_combo_companion(product_name):
    """Probabilidad de que cierto producto venga con otro (combo)."""
    combos = {
        "Espresso": [("Medialuna", 0.4), ("Cookie Clásica", 0.15)],
        "Capuccino": [("Medialuna", 0.5), ("Brownie", 0.2), ("Croissant", 0.25)],
        "Latte": [("Croissant", 0.35), ("Carrot Cake", 0.3), ("Cookie Chocolate Blanco y Pistacho", 0.25)],
        "Flat White": [("Avocado Toast", 0.3), ("Tostado Jamón y Queso", 0.25)],
        "Cortado": [("Medialuna", 0.45), ("Cookie Clásica", 0.15)],
        "Cold Brew": [("Cheesecake", 0.2), ("Brownie", 0.15)],
        "Americano": [("Carrot Cake", 0.25), ("Focaccia de Bondiola", 0.2)],
        "Iced Latte": [("Cookie Chocolate Blanco y Pistacho", 0.3), ("Cheesecake", 0.15)],
    }
    return combos.get(product_name, [])
    
# ============================================================
# GENERACIÓN PRINCIPAL
# ============================================================

def generate_transactions():
    """Función principal que genera el dataset completo."""
    
    # Setear seeds para reproducibilidad
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    
    transactions = []
    transaction_counter = 1
    
    # Recorrer cada día del rango
    current_date = START_DATE
    while current_date <= END_DATE:
        # Cuántas transacciones base genera este día (con ruido)
        base_transactions = int(np.random.normal(28, 5))  # Promedio 28/día
        base_transactions = max(15, base_transactions)  # Mínimo 15
        
        # Aplicar peso del día de la semana
        day_weight = get_day_weight(current_date.weekday())
        n_transactions = int(base_transactions * day_weight)
        
        for _ in range(n_transactions):
            # Generar hora con pesos
            hours = list(range(7, 20))
            hour_weights = [get_hourly_weight(h) for h in hours]
            chosen_hour = random.choices(hours, weights=hour_weights, k=1)[0]
            chosen_minute = random.randint(0, 59)
            chosen_second = random.randint(0, 59)
            
            transaction_datetime = current_date.replace(
                hour=chosen_hour,
                minute=chosen_minute,
                second=chosen_second
            )
            
            # Elegir producto principal con pesos (popularidad + estacionalidad)
            product_weights = []
            for p_name, p_cat, p_price, p_pop, p_hot in PRODUCTS:
                seasonal = get_seasonal_multiplier(current_date, p_hot)
                product_weights.append(p_pop * seasonal)
            
            chosen_product = random.choices(PRODUCTS, weights=product_weights, k=1)[0]
            p_name, p_cat, p_price, p_pop, p_hot = chosen_product
            
            quantity = 1
            transactions.append({
                "transaction_id": f"TX{transaction_counter:05d}",
                "datetime": transaction_datetime,
                "product": p_name,
                "category": p_cat,
                "quantity": quantity,
                "unit_price": p_price,
                "total": p_price * quantity,
                "day_of_week": current_date.strftime("%A"),
                "hour": chosen_hour,
            })
            transaction_counter += 1
            
            # ¿Hubo combo? Si sí, agregar producto acompañante
            companions = get_combo_companion(p_name)
            for comp_name, comp_prob in companions:
                if random.random() < comp_prob:
                    # Buscar el producto acompañante
                    comp_product = next(
                        (p for p in PRODUCTS if p[0] == comp_name), None
                    )
                    if comp_product:
                        c_name, c_cat, c_price, _, _ = comp_product
                        transactions.append({
                            "transaction_id": f"TX{transaction_counter:05d}",
                            "datetime": transaction_datetime,
                            "product": c_name,
                            "category": c_cat,
                            "quantity": 1,
                            "unit_price": c_price,
                            "total": c_price,
                            "day_of_week": current_date.strftime("%A"),
                            "hour": chosen_hour,
                        })
                        transaction_counter += 1
        
        current_date += timedelta(days=1)
    
    # Convertir a DataFrame y guardar
    df = pd.DataFrame(transactions)
    
    # Crear carpeta si no existe
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    # Guardar CSV
    df.to_csv(OUTPUT_PATH, index=False)
    
    print(f"✅ Generadas {len(df):,} transacciones")
    print(f"📁 Guardado en: {OUTPUT_PATH}")
    print(f"📅 Rango: {df['datetime'].min()} a {df['datetime'].max()}")
    print(f"💰 Facturación total: $UYU {df['total'].sum():,.0f}")
    print(f"🏆 Top 5 productos:")
    print(df['product'].value_counts().head().to_string())
    
    return df

# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":
    df = generate_transactions()