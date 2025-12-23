import json
import os

# --- CONFIGURACIÓN DE RUTAS ---
script_dir = os.path.dirname(os.path.abspath(__file__))
# Ruta EXACTA: website/src/data/laptops.json
output_path = os.path.join(script_dir, '..', 'website', 'src', 'data', 'laptops.json')

# TU ID DE AFILIADO
AFFILIATE_TAG = "comparadorjai-21"

def generate_link(name):
    base = "https://www.amazon.es/s?k="
    query = name.replace(" ", "+")
    return f"{base}{query}&tag={AFFILIATE_TAG}"

# --- DATOS MANUALES (BASE DE DATOS EXTENDIDA) ---
# NOTA: Debes tener estas imágenes en website/public/img/
mis_laptops = [
    {
        "name": "Apple MacBook Air (2020) - Chip M1",
        "price_eur": 929.00,
        "brand_img": "/img/macbook.jpg", 
        "specs": { "cpu": "Apple M1", "ram": "8 GB", "storage": "256 GB SSD" }
    },
    {
        "name": "Lenovo IdeaPad Slim 3 Gen 8",
        "price_eur": 499.00,
        "brand_img": "/img/lenovo.jpg",
        "specs": { "cpu": "Intel Core i5-12450H", "ram": "16 GB", "storage": "512 GB SSD" }
    },
    {
        "name": "HP Victus 15-fa0012ns (Gaming)",
        "price_eur": 749.99,
        "brand_img": "/img/hp.jpg",
        "specs": { "cpu": "Intel Core i5-12500H", "ram": "16 GB", "storage": "512 GB SSD" }
    },
    {
        "name": "ASUS TUF Gaming F15",
        "price_eur": 649.00,
        "brand_img": "/img/asus.jpg",
        "specs": { "cpu": "Intel Core i5-11400H", "ram": "16 GB", "storage": "512 GB SSD" }
    },
    {
        "name": "Acer Aspire 5 A515",
        "price_eur": 529.00,
        "brand_img": "/img/acer.jpg",
        "specs": { "cpu": "Intel Core i5-1135G7", "ram": "12 GB", "storage": "1 TB SSD" }
    },
    {
        "name": "MSI Thin GF63 (Gaming Barato)",
        "price_eur": 849.00,
        "brand_img": "/img/msi.jpg",
        "specs": { "cpu": "Intel Core i7-12650H", "ram": "16 GB", "storage": "512 GB SSD" }
    }
]

# --- PROCESAMIENTO ---
print("[INFO] Generando base de datos curada...")
laptops_clean = []

for index, item in enumerate(mis_laptops):
    laptop = {
        "id": index,
        "name": item["name"],
        "slug": item["name"].lower().replace(" ", "-").replace("(", "").replace(")", ""),
        "brand_img": item["brand_img"],
        "specs": item["specs"],
        "price_eur": item["price_eur"],
        "affiliate_link": generate_link(item["name"])
    }
    laptops_clean.append(laptop)

# --- GUARDADO ---
try:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(laptops_clean, f, indent=2, ensure_ascii=False)
    print(f"[EXITO] Archivo generado en: {output_path}")
    print(f"[INFO] Asegúrate de tener {len(laptops_clean)} imágenes en la carpeta public/img/")
except Exception as e:
    print(f"[ERROR] {e}")