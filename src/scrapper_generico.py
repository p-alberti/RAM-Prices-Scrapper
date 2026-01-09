import requests
from bs4 import BeautifulSoup
import csv
import datetime
import time
import random
from typing import Dict, Optional
from pathlib import Path

# Headers genéricos para requests HTTP
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
    "DNT": "1",
}


def obtener_prod_y_precios(
    url_base: str,
    busqueda_prod: str,
    selectores_html: Dict[str, Dict],
    paginas: int = 5,
    espera: tuple = (3, 8),
) -> list:
    """
    Script de obtención de productos y precios.

    Parámetros:
    - url_base: Url base para la busqueda (e.g. https://example.com/search?q=)
    - busqueda_prod: lo que se quiere buscar (producto)
    - selectores_html: Diccionario con los selectores HTML que contienen los datos de interés del prod
    - paginas: número de páginas sobre las que se desea extraer
    - espera: demora min y max entre cada consulta (para no saturar servidores)

    Returns:
    - Lista de productos y sus datos
    """

    busqueda_prod_clean = busqueda_prod.replace(" ", "-")
    productos = []

    for numero_pag in range(1, paginas + 1):
        url = f"{url_base}{busqueda_prod_clean}&page={numero_pag}"

        print(f"\n--- Procesando página {numero_pag}/{paginas} ---")
        print(f"URL: {url}")

        try:
            demora = random.uniform(*espera)
            print(f"Esperando {demora:.2f} segundos antes de consultar...")
            time.sleep(demora)

            response = requests.get(url, headers=HEADERS, timeout=15)

            if response.status_code != 200:
                print(f"Request fallida con status {response.status_code}")
                break

            soup = BeautifulSoup(response.content, "html.parser")

            contenedores_de_prod = soup.find_all(
                selectores_html["container"]["tag"],
                selectores_html["container"].get("attrs", {}),
            )

            if not contenedores_de_prod:
                print("No se encontraron productos en esta página.")
                break

            fecha_ext = datetime.datetime.now().strftime("%Y-%m-%d")
            cant_extraidos = 0

            for producto in contenedores_de_prod:
                title = extract_text(producto, selectores_html.get("title"))
                price = extract_text(producto, selectores_html.get("price"))

                if price:
                    productos.append(
                        [fecha_ext, title, price, f"Página {numero_pag}"]
                    )
                    cant_extraidos += 1

            print(f"Se obtuvieron {cant_extraidos} productos de la página {numero_pag}.")

        except Exception as exc:
            print(f"Error procesando la página {numero_pag}: {exc}")
            continue

    return productos


def extract_text(parent, selector: Optional[Dict]) -> Optional[str]:
    if not selector:
        return None

    element = parent.find(
        selector["tag"],
        selector.get("attrs", {}),
    )

    if not element:
        return None

    return element.get_text(strip=True)


def save_to_csv(data: list, filename: str):
    if not data:
        print("No hay datos.")
        return
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    file_path = data_dir / filename

    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            ["fecha_ext", "producto", "precio", "página"]
        )
        writer.writerows(data)

    print(f"\nSe guardaron {len(data)} filas en '{file_path}'.")


if __name__ == "__main__":

    # Configuración de ejemplo (Es diferente segun la página)

    results = obtener_prod_y_precios(
        url_base="https://www.ejemploPáginaVentas.com/",
        busqueda_prod="memorias ram",
        
        selectores_html = {
            "container": {
                "tag": "div",
                "attrs": {"data-component-type": "s-search-result"},
            },
            "title": {
                "tag": "h3",
            },
            "price": {
                "tag": "span",
                "attrs": {"class": "a-offscreen"},
            },
        },
        paginas=10,
    )

    fecha_ext = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"precios_ram-ml_{fecha_ext}.csv"
    save_to_csv(results, filename)
