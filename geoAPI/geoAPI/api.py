import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import geopandas as gpd

@csrf_exempt
def get_data(request):
    try:
        # Mendapatkan parameter name dan file dari permintaan GET
        name = request.GET.get('name', None)
        file = request.GET.get('file', None)

        if name is None or file is None:
            raise ValueError("Parameter 'name' dan 'file' diperlukan.")

        # Path file GeoJSON yang akan dikonversi
        geojson_file = f'https://geofence.asiaresearchinstitute.com/upload/files/{name}/{file}.geojson'

        # Ambil nama file dari path GeoJSON
        geojson_filename = os.path.splitext(os.path.basename(geojson_file))[0]

        # Gunakan nama file GeoJSON sebagai nama pengguna (username)
        username = geojson_filename

        # Membaca data GeoJSON menggunakan geopandas
        gdf = gpd.read_file(geojson_file)

        # Contoh data yang akan diubah ke format JSON
        data = {
            "filename": username,
            "geojson_file": geojson_file,
            "status": "success",
            "message": "Convert GeoJSON To Shapefile Finished..."
        }
        print(data)

        # Mengembalikan respons JSON
        return JsonResponse(data)
    except Exception as e:
        # Mengembalikan respons JSON dalam kasus kesalahan
        return JsonResponse({"status": "error", "message": str(e)})
