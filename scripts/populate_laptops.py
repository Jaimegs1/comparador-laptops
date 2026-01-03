import json
import os
import re
import time
import sys
import requests
from requests_auth_aws_sigv4 import AWSSigV4

# --- 🔧 FIX PARA WINDOWS: PERMITIR EMOJIS EN LA CONSOLA ---
# Esto evita el error UnicodeEncodeError
sys.stdout.reconfigure(encoding='utf-8')

# --- 🔐 TUS CLAVES DE AMAZON (PÉGALAS AQUÍ) ---
# ¡NO SUBAS ESTE ARCHIVO A GITHUB CON LAS CLAVES PUESTAS!
ACCESS_KEY = ""
SECRET_KEY = ""
PARTNER_TAG = "comparadorjai-21"

# --- CONFIGURACIÓN TÉCNICA ---
REGION = "eu-west-1" # Región Europa (Amazon.es)
HOST = "webservices.amazon.es"
ENDPOINT = f"https://{HOST}/paapi5/searchitems"

# --- RUTAS DE SALIDA ---
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, '..', 'website', 'src', 'data', 'laptops.json')

# --- LISTA DE BÚSQUEDA (Para conseguir +100 productos) ---
KEYWORDS = [
    "Portátil Gaming RTX 4060",
    "Portátil Gaming Barato",
    "MacBook Air M2",
    "MacBook Air M3",
    "Portátil Lenovo IdeaPad Slim",
    "ASUS TUF Gaming F15",
    "Acer Nitro V 15",
    "MSI Thin GF63",
    "HP Victus 15",
    "Portátil ASUS Vivobook OLED",
    "LG Gram 16",
    "Portátil HP 15s",
    "Lenovo Legion 5",
    "Dell Inspiron 15",
    "Samsung Galaxy Book4",
    "Portátil Windows 11 Barato"
]

def search_amazon(keyword, page=1):
    """Consulta a la API de Amazon con la autenticación corregida"""
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'X-Amz-Target': 'com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems',
        'Content-Encoding': 'amz-1.0'
    }

    payload = {
        "Keywords": keyword,
        "Resources": [
            "ItemInfo.Title",
            "ItemInfo.Features",
            "ItemInfo.ProductInfo",
            "Images.Primary.Large",
            "Offers.Listings.Price"
        ],
        "PartnerTag": PARTNER_TAG,
        "PartnerType": "Associates",
        "Marketplace": "www.amazon.es",
        "ItemCount": 9, # Pedimos 9 por página para no saturar
        "ItemPage": page
    }

    # --- AQUÍ ESTABA EL ERROR ANTES: CORREGIDO ---
    auth = AWSSigV4(
        'ProductAdvertisingAPI',
        region=REGION,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )
    
    try:
        response = requests.post(ENDPOINT, json=payload, headers=headers, auth=auth)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"   ⚠️ [AMAZON RECHAZÓ]: Código {response.status_code}")
            print(f"   📜 MENSAJE REAL: {response.text}")  # <--- ESTO ES LA CLAVE
            # Si es error 429 (Too Many Requests), esperamos más
            if response.status_code == 429:
                print("   ⏳ Pausando 5 segundos extra por límite de velocidad...")
                time.sleep(5)
            return None
    except Exception as e:
        print(f"   ❌ [EXCEPCIÓN CONEXIÓN]: {e}")
        return None

def extract_specs(title):
    """Extrae CPU, RAM y SSD del título usando Regex"""
    title_upper = title.upper()
    
    # RAM
    ram_match = re.search(r'(\d+)\s*GB\s*RAM', title_upper)
    ram = f"{ram_match.group(1)} GB" if ram_match else "8 GB" # Default seguro

    # SSD
    ssd_match = re.search(r'(\d+)\s*(GB|TB)\s*(SSD|ALMACENAMIENTO)', title_upper)
    if ssd_match:
        storage = f"{ssd_match.group(1)} {ssd_match.group(2)} SSD"
    else:
        storage = "256 GB SSD" # Default seguro

    # CPU (Detección básica)
    cpu = "Procesador Intel/AMD"
    if "I7" in title_upper: cpu = "Intel Core i7"
    elif "I5" in title_upper: cpu = "Intel Core i5"
    elif "I3" in title_upper: cpu = "Intel Core i3"
    elif "I9" in title_upper: cpu = "Intel Core i9"
    elif "RYZEN 7" in title_upper: cpu = "AMD Ryzen 7"
    elif "RYZEN 5" in title_upper: cpu = "AMD Ryzen 5"
    elif "RYZEN 3" in title_upper: cpu = "AMD Ryzen 3"
    elif "M1" in title_upper: cpu = "Apple M1"
    elif "M2" in title_upper: cpu = "Apple M2"
    elif "M3" in title_upper: cpu = "Apple M3"
    elif "N4020" in title_upper or "CELERON" in title_upper: cpu = "Intel Celeron"

    # Peso (Hardcodeado por ahora, es difícil sacarlo del título)
    weight = "1.8 kg" 
    
    return {"cpu": cpu, "ram": ram, "storage": storage, "weight": weight}

def determine_category(title, price):
    """Asigna categorías para los filtros de la web"""
    title_lower = title.lower()
    cats = []
    
    # Lógica Gaming
    if any(x in title_lower for x in ["rtx", "gtx", "gaming", "nitro", "tuf", "victus", "katana", "thin gf"]):
        cats.append("gaming")
    
    # Lógica Top / Business
    if any(x in title_lower for x in ["macbook", "zenbook", "gram", "xps", "surface"]):
        cats.append("top")
        cats.append("business")
    elif price > 800:
        cats.append("top")
        
    # Lógica Estudiantes / Barato
    if price < 600 and "gaming" not in cats:
        cats.append("student")
        
    # Default
    if not cats:
        cats.append("student")
        
    return " ".join(list(set(cats)))

def main():
    print("🚀 INICIANDO BARRIDO MASIVO DE AMAZON...")
    print(f"📂 Guardando en: {output_path}")
    
    all_products = []
    seen_asins = set()

    for keyword in KEYWORDS:
        print(f"\n🔎 Buscando: '{keyword}'...")
        data = search_amazon(keyword)
        
        # Pausa de seguridad para evitar baneos de API (Rate Limiting)
        time.sleep(2) 

        if data and "SearchResult" in data and "Items" in data["SearchResult"]:
            items = data["SearchResult"]["Items"]
            print(f"   ✅ Encontrados {len(items)} productos.")
            
            for item in items:
                asin = item["ASIN"]
                
                # Evitar duplicados
                if asin in seen_asins:
                    continue 
                
                try:
                    # Validar datos mínimos necesarios
                    info = item.get("ItemInfo", {})
                    title_info = info.get("Title", {})
                    title = title_info.get("DisplayValue", "Portátil Desconocido")
                    
                    # Precio
                    offers = item.get("Offers", {}).get("Listings", [])
                    if not offers:
                        continue # Sin precio no nos sirve
                    price = offers[0]["Price"]["Amount"]
                    
                    # Imagen
                    images = item.get("Images", {}).get("Primary", {})
                    if "Large" in images:
                        img_url = images["Large"]["URL"]
                    else:
                        continue # Sin imagen no nos sirve
                        
                    # Procesar datos
                    specs = extract_specs(title)
                    category = determine_category(title, price)
                    
                    product = {
                        "id": asin,
                        "name": title[:75] + "..." if len(title) > 75 else title, # Acortar título largo
                        "full_name": title,
                        "slug": title.lower().replace(" ", "-").replace("/", "-")[:60],
                        "brand_img": img_url,
                        "category": category,
                        "specs": specs,
                        "price_eur": price,
                        "affiliate_link": item["DetailPageURL"]
                    }
                    
                    all_products.append(product)
                    seen_asins.add(asin)
                    print(f"      + Añadido: {product['name'][:30]}... ({price}€)")
                    
                except Exception as e:
                    continue

    # --- GUARDADO FINAL ---
    print(f"\n✨ PROCESO COMPLETADO.")
    print(f"📦 Total productos únicos recopilados: {len(all_products)}")
    
    if len(all_products) > 0:
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(all_products, f, indent=2, ensure_ascii=False)
            print(f"💾 Archivo JSON guardado correctamente.")
        except Exception as e:
            print(f"❌ Error fatal guardando JSON: {e}")
    else:
        print("⚠️ No se encontraron productos. Revisa tus claves de API.")

if __name__ == "__main__":
    main()