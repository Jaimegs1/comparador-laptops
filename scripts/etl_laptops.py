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
    {
        "name": "Apple MacBook Air (2020) - Chip M1",
        "price_eur": 929.00,
        "brand_img": "/img/macbook.jpg",
        "category": "top student business",
        "specs": { "cpu": "Apple M1", "ram": "8 GB", "storage": "256 GB SSD", "weight": "1.29 kg" }
    },
    {
        "name": "Lenovo IdeaPad Slim 3 Gen 8",
        "price_eur": 499.00,
        "brand_img": "/img/lenovo.jpg",
        "category": "student",
        "specs": { "cpu": "Intel Core i5-12450H", "ram": "16 GB", "storage": "512 GB SSD", "weight": "1.62 kg" }
    },
    {
        "name": "HP Victus 15-fa0012ns (Gaming)",
        "price_eur": 749.99,
        "brand_img": "/img/hp.jpg",
        "category": "gaming",
        "specs": { "cpu": "Intel Core i5-12500H", "ram": "16 GB", "storage": "512 GB SSD", "weight": "2.29 kg" }
    },
    {
        "name": "ASUS TUF Gaming F15",
        "price_eur": 649.00,
        "brand_img": "/img/asus.jpg",
        "category": "gaming",
        "specs": { "cpu": "Intel Core i5-11400H", "ram": "16 GB", "storage": "512 GB SSD", "weight": "2.30 kg" }
    },
    {
        "name": "Acer Aspire 5 A515",
        "price_eur": 529.00,
        "brand_img": "/img/acer.jpg",
        "category": "student",
        "specs": { "cpu": "Intel Core i5-1135G7", "ram": "12 GB", "storage": "1 TB SSD", "weight": "1.70 kg" }
    },
    {
        "name": "MSI Thin GF63 (Gaming Barato)",
        "price_eur": 849.00,
        "brand_img": "/img/msi.jpg",
        "category": "gaming",
        "specs": { "cpu": "Intel Core i7-12650H", "ram": "16 GB", "storage": "512 GB SSD", "weight": "1.86 kg" }
    },

    # --- LOS NUEVOS (SUPERVENTAS AMAZON) ---
    {
        "name": "Acer Nitro 5 AN515",
        "price_eur": 699.00,
        "brand_img": "/img/nitro.jpg",
        "category": "gaming top",
        "specs": { "cpu": "Intel Core i5-11400H", "ram": "16 GB", "storage": "512 GB SSD", "weight": "2.30 kg" }
    },
    {
        "name": "ASUS VivoBook 15 F1500",
        "price_eur": 449.00,
        "brand_img": "/img/vivobook.jpg",
        "category": "student top",
        "specs": { "cpu": "Intel Core i3-1115G4", "ram": "8 GB", "storage": "256 GB SSD", "weight": "1.80 kg" }
    },
    {
        "name": "HP Chromebook 14a",
        "price_eur": 249.00,
        "brand_img": "/img/chromebook.jpg",
        "category": "student",
        "specs": { "cpu": "Intel Celeron N4500", "ram": "4 GB", "storage": "64 GB eMMC", "weight": "1.46 kg" }
    },
    {
        "name": "Apple MacBook Air (2022) - Chip M2",
        "price_eur": 1099.00,
        "brand_img": "/img/macbook-m2.jpg",
        "category": "top business",
        "specs": { "cpu": "Apple M2", "ram": "8 GB", "storage": "256 GB SSD", "weight": "1.24 kg" }
    },
    {
        "name": "Lenovo V15 G3 (Oficina)",
        "price_eur": 389.00,
        "brand_img": "/img/lenovo-v15.jpg",
        "category": "business student",
        "specs": { "cpu": "Intel Core i3-1215U", "ram": "8 GB", "storage": "256 GB SSD", "weight": "1.70 kg" }
    },
    {
        "name": "Dell Inspiron 15 3000",
        "price_eur": 549.00,
        "brand_img": "/img/dell.jpg",
        "category": "student business",
        "specs": { "cpu": "Ryzen 5 5500U", "ram": "8 GB", "storage": "512 GB SSD", "weight": "1.85 kg" }
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