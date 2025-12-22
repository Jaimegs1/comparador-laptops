import pandas as pd
import json
import re
import os

# --- 1. CONFIGURACIÓN DE RUTAS ---
# Esto hace que funcione en cualquier ordenador (Windows/Mac/Linux)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Subimos un nivel (..) y entramos en 'data'
data_dir = os.path.join(script_dir, '..', 'data')
csv_path = os.path.join(data_dir, 'laptops_raw.csv')
output_path = os.path.join(data_dir, 'database.json')

print(f"[INFO] Buscando CSV en: {csv_path}")

# --- 2. CARGA DE DATOS (Lo que te faltaba) ---
try:
    # Leemos el CSV. Si falla con utf-8, probamos con 'latin1'
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding='latin1')
    print(f"[INFO] CSV cargado correctamente. {len(df)} filas encontradas.")
except Exception as e:
    print(f"[ERROR] No se pudo leer el CSV: {e}")
    print("Asegúrate de que el archivo 'laptops_raw.csv' está dentro de la carpeta 'data'.")
    exit()

# --- 3. FUNCIONES DE LIMPIEZA ---

def extract_ram(text):
    match = re.search(r'(\d+)\s*GB', str(text), re.IGNORECASE)
    if match:
        return f"{match.group(1)} GB"
    return "8 GB" # Valor por defecto si falla

def extract_screen(text):
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:inch|")', str(text), re.IGNORECASE)
    if match:
        return f"{match.group(1)}\""
    return "15.6\"" # Valor por defecto

def create_slug(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    return text[:80]

def clean_specs(val):
    val = str(val).strip()
    if val.lower() in ["nan", "n/a", "null", ""]:
        return "Consultar Ficha"
    return val

def generate_affiliate_link(name):
    base = "https://www.amazon.es/s?k="
    tag = "&tag=comparadorjai-21" # TU ID REAL YA PUESTO
    query = name.replace(" ", "+")
    return f"{base}{query}{tag}"

# --- 4. PROCESAMIENTO PRINCIPAL ---
print("[INFO] Procesando datos y aplicando ingeniería de precios...")
laptops_clean = []

# Tasa de cambio aprox (Rupia a Euro)
EXCHANGE_RATE = 91.0 

for index, row in df.iterrows():
    
    # Limpieza básica
    name = str(row.get('Name', 'Portátil Desconocido')).strip()
    
    # Corrección de Precio (De Rupias a Euros)
    raw_price = str(row.get('Discounted Price', '0')).replace(',', '').replace('₹', '').strip()
    try:
        price_float = float(raw_price)
        # Lógica: Si el precio es > 5000, asumimos que son rupias y convertimos
        if price_float > 5000:
            price_eur = round(price_float / EXCHANGE_RATE, 2)
        else:
            price_eur = price_float
    except:
        price_eur = 0.0

    # Limpieza de specs
    cpu = clean_specs(row.get('Core', ''))
    ram = extract_ram(name)
    storage = clean_specs(row.get('SSD', ''))
    
    # Asignación de Imagen por Marca (Logos HD)
    brand_lower = str(row.get('Brand', '')).lower()
    if "apple" in brand_lower:
        img = "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"
    elif "hp" in brand_lower:
        img = "https://upload.wikimedia.org/wikipedia/commons/2/29/HP_New_Logo_2D.svg"
    elif "lenovo" in brand_lower:
        img = "https://upload.wikimedia.org/wikipedia/commons/b/b8/Lenovo_logo_2015.svg"
    elif "asus" in brand_lower:
        img = "https://upload.wikimedia.org/wikipedia/commons/2/2e/ASUS_Logo.svg"
    elif "dell" in brand_lower:
        img = "https://upload.wikimedia.org/wikipedia/commons/4/48/Dell_Logo.svg"
    elif "acer" in brand_lower:
        img = "https://upload.wikimedia.org/wikipedia/commons/0/00/Acer_2011.svg"
    else:
        img = "https://cdn-icons-png.flaticon.com/512/2888/2888746.png" # Icono laptop genérico

    # Construcción del objeto final
    laptop = {
        "id": index,
        "name": name,
        "slug": create_slug(name),
        "brand_img": img,
        "specs": {
            "cpu": cpu,
            "ram": ram,
            "storage": storage,
            "screen": extract_screen(name)
        },
        "price_eur": price_eur,
        "affiliate_link": generate_affiliate_link(name)
    }
    
    # Filtramos errores (si precio es 0 o muy bajo, no lo guardamos)
    if price_eur > 100: 
        laptops_clean.append(laptop)

# --- 5. GUARDADO ---
try:
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(laptops_clean, f, indent=2, ensure_ascii=False)
    print(f"[ÉXITO] Database generada en: {output_path}")
    print(f"[RESUMEN] Se han procesado {len(laptops_clean)} portátiles con precios en Euros.")
except Exception as e:
    print(f"[ERROR] No se pudo guardar el JSON: {e}")