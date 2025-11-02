import requests
import urllib.parse

API_KEY = "6672922d-851f-486a-a115-94e99075a4c4"

GEOCODE_URL = "https://graphhopper.com/api/1/geocode?"
ROUTE_URL = "https://graphhopper.com/api/1/route?"

def geocodificar(lugar):
    url = GEOCODE_URL + urllib.parse.urlencode({
        "q": lugar,
        "limit": "1",
        "key": API_KEY
    })
    r = requests.get(url)
    data = r.json()

    if r.status_code == 200 and len(data["hits"]) > 0:
        lat = data["hits"][0]["point"]["lat"]
        lng = data["hits"][0]["point"]["lng"]
        nombre = data["hits"][0]["name"]
        print(f"Ubicación encontrada: {nombre} ({lat:.4f}, {lng:.4f})")
        return lat, lng
    else:
        print("No se encontró la ubicación.")
        return None, None

def main():
    print("=== GEOLOCALIZACIÓN ===")
    print("Escribe 's' o 'salir' para terminar.\n")

    while True:
        origen = input("Ingrese origen: ").strip()
        if origen.lower() in ["s", "salir"]:
            print("Saliendo...")
            break

        destino = input("Ingrese destino: ").strip()
        if destino.lower() in ["s", "salir"]:
            print("Saliendo...")
            break

        lat1, lon1 = geocodificar(origen)
        lat2, lon2 = geocodificar(destino)
        if not all([lat1, lon1, lat2, lon2]):
            continue

        ruta_url = (ROUTE_URL +
                    f"point={lat1},{lon1}&point={lat2},{lon2}"
                    f"&vehicle=car&locale=es&key={API_KEY}")
        r = requests.get(ruta_url)
        data = r.json()

        if r.status_code != 200:
            print("Error al obtener la ruta.")
            continue

        ruta = data["paths"][0]
        distancia_km = ruta["distance"] / 1000
        tiempo_min = ruta["time"] / 1000 / 60
        print(f"\nRuta desde {origen} hasta {destino}")
        print(f"Distancia total: {distancia_km:.2f} km")
        print(f"Tiempo estimado: {tiempo_min:.2f} min\n")

        print("Instrucciones paso a paso:")
        for paso in ruta["instructions"]:
            texto = paso["text"]
            dist = paso["distance"] / 1000
            print(f"- {texto} ({dist:.2f} km)")
        print("\n--------------------------------------\n")

if __name__ == "__main__":
    main()
