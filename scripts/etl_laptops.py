import json
import os

# --- CONFIGURACIÓN ---
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, '..', 'website', 'src', 'data', 'laptops.json')
AFFILIATE_TAG = "comparadorjai-21"

def generate_link(name):
    base = "https://www.amazon.es/s?k="
    query = name.replace(" ", "+")
    return f"{base}{query}&tag={AFFILIATE_TAG}"

# --- DATOS: AÑADIMOS "category" ---
# Categorías posibles: 'gaming', 'student', 'business', 'top'
mis_laptops = [
    {
        "name": "Apple MacBook Air (2020) - Chip M1",
        "price_eur": 929.00,
        "brand_img": "/img/macbook.jpg",
        "category": "top student", # Es Top ventas y para estudiantes
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
        "name": "MSI Thin GF63",
        "price_eur": 849.00,
        "brand_img": "/img/msi.jpg",
        "category": "gaming",
        "specs": { "cpu": "Intel Core i7-12650H", "ram": "16 GB", "storage": "512 GB SSD", "weight": "1.86 kg" }
    },
    # --- NUEVOS (Necesitas bajar las fotos) ---
    {
        "name": "Lenovo Legion 5 Gen 6",
        "price_eur": 1149.00,
        "brand_img": "/img/lenovo.jpg", # Reusa la foto de lenovo o baja otra
        "category": "gaming top",
        "specs": { "cpu": "Ryzen 7 5800H", "ram": "16 GB", "storage": "1 TB SSD", "weight": "2.40 kg" }
    },
    {
        "name": "HP 15s-fq5085ns",
        "price_eur": 399.00,
        "brand_img": "/img/hp.jpg",
        "category": "student",
        "specs": { "cpu": "Intel Core i3-1215U", "ram": "8 GB", "storage": "256 GB SSD", "weight": "1.69 kg" }
    },
    {
        "name": "ASUS ZenBook 14 OLED",
        "price_eur": 999.00,
        "brand_img": "/img/asus.jpg",
        "category": "business top",
        "specs": { "cpu": "Intel Core i7-1260P", "ram": "16 GB", "storage": "512 GB SSD", "weight": "1.39 kg" }
    }
]

# --- PROCESAMIENTO ---
print("[INFO] Generando base de datos...")
laptops_clean = []

for index, item in enumerate(mis_laptops):
    laptop = {
        "id": index,
        "name": item["name"],
        "slug": item["name"].lower().replace(" ", "-").replace("(", "").replace(")", ""),
        "brand_img": item["brand_img"],
        "category": item["category"], # GUARDAMOS LA CATEGORÍA
        "specs": item["specs"],
        "price_eur": item["price_eur"],
        "affiliate_link": generate_link(item["name"])
    }
    laptops_clean.append(laptop)

try:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(laptops_clean, f, indent=2, ensure_ascii=False)
    print(f"[EXITO] {len(laptops_clean)} portátiles generados.")
except Exception as e:
    print(f"[ERROR] {e}")