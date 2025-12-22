import json
import os

# --- CONFIGURACIÓN ---
script_dir = os.path.dirname(os.path.abspath(__file__))
# Guardamos en la carpeta SRC de la web para que Vercel lo pille
output_path = os.path.join(script_dir, '..', 'website', 'src', 'data', 'database.json')

# TU ID DE AFILIADO
AFFILIATE_TAG = "comparadorjai-21"

def generate_link(name):
    base = "https://www.amazon.es/s?k="
    query = name.replace(" ", "+")
    return f"{base}{query}&tag={AFFILIATE_TAG}"

# --- DATOS MANUALES (CALIDAD > CANTIDAD) ---
# Aquí es donde tú, como "CEO", decides qué vender.
# Busca las fotos en Google Imágenes (clic derecho -> Copiar dirección de imagen)
mis_laptops = [
    {
        "name": "Apple MacBook Air (2020) - Chip M1",
        "price_eur": 929.00,
        "brand_img": "https://m.media-amazon.com/images/I/71vFKBpKakL._AC_SL1500_.jpg", # Foto REAL del producto
        "specs": {
            "cpu": "Apple M1",
            "ram": "8 GB",
            "storage": "256 GB SSD"
        }
    },
    {
        "name": "Lenovo IdeaPad Slim 3 Gen 8",
        "price_eur": 499.00,
        "brand_img": "https://m.media-amazon.com/images/I/71abc-M4ZBL._AC_SL1500_.jpg",
        "specs": {
            "cpu": "Intel Core i5-12450H",
            "ram": "16 GB",
            "storage": "512 GB SSD"
        }
    },
    {
        "name": "HP Victus 15-fa0012ns (Gaming)",
        "price_eur": 749.99,
        "brand_img": "https://m.media-amazon.com/images/I/81+6f+3J+XL._AC_SL1500_.jpg",
        "specs": {
            "cpu": "Intel Core i5-12500H",
            "ram": "16 GB",
            "storage": "512 GB SSD"
        }
    },
    {
        "name": "ASUS TUF Gaming F15",
        "price_eur": 649.00,
        "brand_img": "https://m.media-amazon.com/images/I/71ma2w-f+OL._AC_SL1500_.jpg",
        "specs": {
            "cpu": "Intel Core i5-11400H",
            "ram": "16 GB",
            "storage": "512 GB SSD"
        }
    }
]

# --- PROCESAMIENTO ---
print("[INFO] Generando base de datos curada...")
laptops_clean = []

for index, item in enumerate(mis_laptops):
    # Enriquecemos los datos manuales con slugs y links
    laptop = {
        "id": index,
        "name": item["name"],
        "slug": item["name"].lower().replace(" ", "-").replace("(", "").replace(")", ""),
        "brand_img": item["brand_img"], # Aquí va la FOTO DEL PRODUCTO
        "specs": item["specs"],
        "price_eur": item["price_eur"],
        "affiliate_link": generate_link(item["name"])
    }
    laptops_clean.append(laptop)

# --- GUARDADO ---
try:
    # Asegurar que el directorio existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(laptops_clean, f, indent=2, ensure_ascii=False)
    print(f"[EXITO] Database generada con {len(laptops_clean)} productos TOP.")
    print(f"Ruta: {output_path}")
except Exception as e:
    print(f"[ERROR] {e}")