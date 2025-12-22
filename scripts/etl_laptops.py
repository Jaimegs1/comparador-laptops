import pandas as pd
import json
import re
import os

# --- CÁLCULO DE RUTAS (Igual que antes) ---
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
csv_path = os.path.join(data_dir, 'laptops_raw.csv')
output_path = os.path.join(data_dir, 'database.json')

print(f"[INFO] Buscando CSV en: {csv_path}")

try:
    # Leemos el CSV. A veces los CSVs de Kaggle usan separadores distintos.
    # Si falla, prueba cambiando sep=',' por sep=';'
    df = pd.read_csv(csv_path, encoding='utf-8') 
except Exception as e:
    print(f"[ERROR] No se pudo leer el CSV: {e}")
    exit()

# --- FUNCIONES DE EXTRACCIÓN (INGENIERÍA DE DATOS) ---

def clean_price(price_val):
    # Si el precio viene como "₹45,000" o "$500", lo limpiamos
    if pd.isna(price_val): return "0"
    # Convertimos a string y quitamos todo lo que no sea número o punto
    clean = str(price_val)
    # Ejemplo simple: mantenemos solo números. 
    # (Adaptable según tu moneda, aquí asumimos que queremos el valor numérico bruto)
    return clean

def extract_ram(text):
    # Busca patrones como "8GB", "16 GB", "8 gb"
    match = re.search(r'(\d+)\s*GB', str(text), re.IGNORECASE)
    if match:
        return f"{match.group(1)} GB"
    return "N/A"

def extract_screen(text):
    # Busca patrones como "15.6 inch", "14-inch", "15.6"
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:inch|")', str(text), re.IGNORECASE)
    if match:
        return f"{match.group(1)}\""
    return "N/A"

def create_slug(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    # Cortamos el slug si es larguísimo (SEO friendly)
    return text[:80]

def generate_affiliate_link(name):
    base = "https://www.amazon.es/s?k="
    tag = "&tag=comparadorjai-21"
    query = name.replace(" ", "+")
    return f"{base}{query}{tag}"

# --- PROCESAMIENTO PRINCIPAL ---
print("[INFO] Procesando datos y extrayendo specs...")
laptops_clean = []

for index, row in df.iterrows():
    
    # 1. Mapeo directo de columnas (Lo que SÍ tienes)
    name = str(row.get('Name', 'Portátil Desconocido'))
    brand = str(row.get('Brand', 'Generico'))
    cpu_core = str(row.get('Core', 'N/A')) # Tu columna se llama 'Core'
    ssd_storage = str(row.get('SSD', 'N/A')) # Tu columna se llama 'SSD'
    
    # El precio con descuento es el interesante
    price = clean_price(row.get('Discounted Price', '0'))
    
    # 2. Extracción inteligente (Lo que NO tienes explícito)
    # Buscamos la RAM y la Pantalla dentro del 'Name'
    ram_extracted = extract_ram(name)
    screen_extracted = extract_screen(name)

    # 3. Construcción del objeto
    laptop = {
        "id": index,
        "name": name.strip(), # Quitamos espacios extra
        "slug": create_slug(name),
        "specs": {
            "cpu": cpu_core,
            "ram": ram_extracted,     # Dato minado
            "gpu": "Ver Ficha",       # No lo tenemos, ponemos genérico
            "storage": ssd_storage,
            "screen": screen_extracted # Dato minado
        },
        "price_approx": price,
        "affiliate_link": generate_affiliate_link(name)
    }
    
    laptops_clean.append(laptop)

# --- GUARDADO ---
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(laptops_clean, f, indent=2, ensure_ascii=False)

print(f"[EXITO] Database generada con {len(laptops_clean)} portátiles.")