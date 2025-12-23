import json
import os

# --- CONFIGURACIÓN DE RUTAS ---
script_dir = os.path.dirname(os.path.abspath(__file__))
# Ruta donde se guardará el JSON para la web
output_path = os.path.join(script_dir, '..', 'website', 'src', 'data', 'laptops.json')

# TU ID DE AFILIADO DE AMAZON
AFFILIATE_TAG = "comparadorjai-21"

def generate_link(name):
    """Genera un enlace de búsqueda en Amazon con tu tag de afiliado"""
    base = "https://www.amazon.es/s?k="
    query = name.replace(" ", "+")
    return f"{base}{query}&tag={AFFILIATE_TAG}"

# --- BASE DE DATOS MAESTRA (12 MODELOS) ---
# Asegúrate de tener las fotos en website/public/img/
mis_laptops = [
    # --- LOS CLÁSICOS (Que ya tenías) ---
    # --- BLOQUE DE EXPANSIÓN (LLEGAR A 20) ---
    {
        "name": "Lenovo Legion 5 Gen 6",
        "price_eur": 1049.00,
        "brand_img": "/img/legion.jpg",
        "category": "gaming top",
        "specs": { "cpu": "Ryzen 7 5800H", "ram": "16 GB", "storage": "1 TB SSD", "weight": "2.40 kg" }
    },
    {
        "name": "Dell XPS 13 Plus",
        "price_eur": 1499.00,
        "brand_img": "/img/xps.jpg",
        "category": "business top",
        "specs": { "cpu": "Intel Core i7-1260P", "ram": "16 GB", "storage": "512 GB SSD", "weight": "1.23 kg" }
    },
    {
        "name": "HP Pavilion x360 (Convertible)",
        "price_eur": 649.00,
        "brand_img": "/img/x360.jpg",
        "category": "student",
        "specs": { "cpu": "Intel Core i5-1235U", "ram": "8 GB", "storage": "512 GB SSD", "weight": "1.51 kg" }
    },
    {
        "name": "ASUS ROG Strix G16",
        "price_eur": 1399.00,
        "brand_img": "/img/rog.jpg",
        "category": "gaming",
        "specs": { "cpu": "Intel Core i7-13650HX", "ram": "16 GB", "storage": "512 GB SSD", "weight": "2.50 kg" }
    },
    {
        "name": "Microsoft Surface Laptop Go 2",
        "price_eur": 599.00,
        "brand_img": "/img/surface.jpg",
        "category": "student business",
        "specs": { "cpu": "Intel Core i5-1135G7", "ram": "8 GB", "storage": "128 GB SSD", "weight": "1.12 kg" }
    },
    {
        "name": "Lenovo IdeaPad 1 Gen 7",
        "price_eur": 299.00,
        "brand_img": "/img/ideapad1.jpg",
        "category": "student",
        "specs": { "cpu": "AMD 3020e", "ram": "4 GB", "storage": "128 GB SSD", "weight": "1.40 kg" }
    },
    {
        "name": "MSI Katana GF66",
        "price_eur": 999.00,
        "brand_img": "/img/katana.jpg",
        "category": "gaming",
        "specs": { "cpu": "Intel Core i7-11800H", "ram": "16 GB", "storage": "1 TB SSD", "weight": "2.25 kg" }
    },
    {
        "name": "LG Gram 14 (Ultraligero)",
        "price_eur": 1199.00,
        "brand_img": "/img/gram.jpg",
        "category": "business top",
        "specs": { "cpu": "Intel Core i7-1260P", "ram": "16 GB", "storage": "512 GB SSD", "weight": "0.99 kg" }
    }
]

# --- PROCESAMIENTO ---
print("[INFO] Generando base de datos curada...")
laptops_clean = []

for index, item in enumerate(mis_laptops):
    # Crear slug limpio (ej: "hp-victus-15")
    slug = item["name"].lower().replace(" ", "-").replace("(", "").replace(")", "").replace(".", "")
    
    laptop = {
        "id": index,
        "name": item["name"],
        "slug": slug,
        "brand_img": item["brand_img"],
        "category": item["category"], # IMPORTANTE: Categoría para los filtros
        "specs": item["specs"],
        "price_eur": item["price_eur"],
        "affiliate_link": generate_link(item["name"])
    }
    laptops_clean.append(laptop)

# --- GUARDADO ---
# --- GUARDADO ---
try:
    # Crear carpetas si no existen
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Escribir el archivo JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(laptops_clean, f, indent=2, ensure_ascii=False)
        
    print(f"[EXITO] Archivo generado en: {output_path}")
    print(f"[INFO] Total de portátiles: {len(laptops_clean)}")
    print("[RECORDATORIO] Descarga las nuevas fotos en website/public/img/")
except Exception as e:
    print(f"[ERROR] {e}")