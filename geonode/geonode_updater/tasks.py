import requests
import json
import geopandas as gpd
import os
import chardet
from shapely.geometry import Point

# Configuración de variables
SPARQL_ENDPOINT = "http://host.docker.internal:1234/sparql"
GEONODE_URL = "http://django:8000"
LAYER_NAME = "real_estate_listings"
SHAPEFILE_DIR = "/tmp/shapefile"

# Archivos requeridos para la carga
REQUIRED_FILES = ["dataset.shp", "dataset.dbf", "dataset.shx", "dataset.prj"]

def ensure_utf8(text):
    """
    Asegura que el texto esté en formato UTF-8.

    Args:
        text (str): Texto a validar.

    Returns:
        str: Texto en UTF-8.
    """
    if isinstance(text, bytes):
        encoding = chardet.detect(text)["encoding"] or "utf-8"
        return text.decode(encoding, errors="replace")
    elif isinstance(text, str):
        return text.encode("utf-8", errors="replace").decode("utf-8")
    return str(text)

def generate_shapefile():
    """Obtiene datos de MillenniumDB y genera un Shapefile"""

    query = """
    PREFIX sioc: <http://rdfs.org/sioc/ns#>
    PREFIX rec: <https://w3id.org/rec#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?listing ?label ?geometry ?coordinates
    WHERE {
      ?listing sioc:about ?about .
      ?about rec:includes ?includes .
      ?includes rec:geometry ?geometry .
      ?geometry rec:coordinates ?coordinates .
      OPTIONAL { ?listing rdfs:label ?label . }
    }
    """

    headers = {
        "Content-Type": "application/sparql-query",
        "Accept": "application/json"
    }

    response = requests.post(SPARQL_ENDPOINT, data=query, headers=headers)
    if response.status_code != 200:
        print("❌ Error: SPARQL request failed")
        return None

    results = response.json()
    features = []

    for result in results["results"]["bindings"]:
        try:
            label = ensure_utf8(result.get("label", {}).get("value", "Sin etiqueta"))
            coord_value = result["coordinates"]["value"]

            # Convertir el string a una lista de floats
            lat, lon = json.loads(coord_value)

            # Validar coordenadas dentro de Argentina
            if not (-55 <= lat <= -22 and -73 <= lon <= -53):
                print(f"⚠️ Coordenadas fuera de Argentina: ({lon}, {lat})")
                continue

            # Crear el punto en formato correcto
            features.append({"name": label, "geometry": Point(lon, lat)})

        except Exception as e:
            print(f"❌ Error procesando coordenadas {coord_value}: {e}")

    if not features:
        print("❌ No se encontraron datos para generar el Shapefile.")
        return None

    # Crear un GeoDataFrame con geopandas
    gdf = gpd.GeoDataFrame(features, geometry="geometry", crs="EPSG:4326")

    # Crear directorio para el Shapefile
    os.makedirs(SHAPEFILE_DIR, exist_ok=True)

    # Guardar como Shapefile con encoding UTF-8 en el DBF
    shapefile_path = os.path.join(SHAPEFILE_DIR, "dataset.shp")
    gdf.to_file(shapefile_path, driver="ESRI Shapefile", encoding="utf-8")

    print("✅ Shapefile generado correctamente.")
    return SHAPEFILE_DIR


def get_dataset_id():
    """Verifica si el dataset existe y devuelve su ID en GeoNode."""
    response = requests.get(
        f"{GEONODE_URL}/api/v2/datasets/?search={LAYER_NAME}",
        auth=("admin", "admin"),
    )
    if response.status_code == 200:
        results = response.json().get("datasets", [])
        if results:
            return results[0]["pk"]
    return None  # ❌ No encontrado


def delete_dataset(dataset_id):
    """Elimina un dataset en GeoNode si existe"""
    if dataset_id:
        print(f"🗑️ Eliminando dataset con ID {dataset_id}...")
        response = requests.delete(
            f"{GEONODE_URL}/api/v2/resources/{dataset_id}/",
            auth=("admin", "admin"),
        )
        if response.status_code in [200, 204]:
            print("✅ Dataset eliminado correctamente.")
        else:
            print(f"⚠️ No se pudo eliminar el dataset: {response.status_code} - {response.text}")


def upload_to_geonode():
    """Elimina el dataset si existe y sube un nuevo Shapefile en GeoNode."""

    shapefile_dir = generate_shapefile()
    if not shapefile_dir:
        print("❌ No se generó el Shapefile correctamente.")
        return

    dataset_id = get_dataset_id()
    if dataset_id:
        delete_dataset(dataset_id)
    else:
        print('No hay dataset para eliminar')

    # Verificar que los archivos requeridos existen y no están vacíos
    extracted_files = {}
    for file in REQUIRED_FILES:
        file_path = os.path.join(shapefile_dir, file)
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            print(f"❌ Archivo inválido: {file}")
            return
        extracted_files[file] = file_path

    # Preparar los archivos para la subida
    files = {key: (fname, open(path, "rb"), "application/octet-stream")
             for key, fname, path in zip(["base_file", "dbf_file", "shx_file", "prj_file"],
                                         REQUIRED_FILES, extracted_files.values())}

    # Datos para la solicitud
    data = {
        "action": "upload",
        "name": LAYER_NAME,
    }

    print("\n📤 **Campos que se enviarán en la solicitud:**")
    print(f"🔹 Data: {json.dumps(data, indent=2)}")
    for key, (filename, file_obj, file_type) in files.items():
        print(f"   - {key}: {filename} ({file_type}) [{os.path.getsize(extracted_files[filename])} bytes]")

    # Enviar solicitud
    upload_response = requests.post(
        f"{GEONODE_URL}/api/v2/uploads/upload/",
        files=files,
        data=data,
        auth=("admin", "admin"),
    )

    # Cerrar los archivos después de la subida
    for f in files.values():
        f[1].close()

    if upload_response.status_code in [200, 201]:
        print("✅ Shapefile subido correctamente a GeoNode.")
    else:
        print(f"❌ Error al subir a GeoNode: {upload_response.status_code} - {upload_response.text}")

# Ejecutar la función de carga si se ejecuta como script
if __name__ == "__main__":
    upload_to_geonode()
