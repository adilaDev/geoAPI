# -*- coding: utf-8 -*-
import os
import re
import shutil
import json
# from django.http import JsonResponse
# from django.http import HttpResponse
from django.http import JsonResponse, HttpRequest, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from zipfile import ZipFile
import geopandas as gpd
from urllib.parse import unquote
from urllib.parse import urlencode

@csrf_exempt
def create_user_folder(username):
    # Path direktori utama
    base_dir = '/home/u8378009/public_html/geofence-api.asiaresearchinstitute.com/output'

    # Path direktori user
    user_dir = os.path.join(base_dir, username)

    # Membuat direktori user jika belum ada
    os.makedirs(user_dir, exist_ok=True)

    return user_dir

@csrf_exempt
def create_zip_folder(username, user_dir):
    # Membuat folder user
    # user_dir = create_user_folder(username)
    # print(f"user_dir: {user_dir}")

    # Path direktori yang akan di-zip
    source_dir = user_dir

    # Path file ZIP keluaran
    zip_file = f'/home/u8378009/public_html/geofence-api.asiaresearchinstitute.com/output/zip/{username}.zip'

    # Membuat file ZIP dari folder
    with ZipFile(zip_file, 'w') as zipf:
        # Menambahkan isi folder ke dalam ZIP
        for foldername, subfolders, filenames in os.walk(source_dir):
            for filename in filenames:
                # Path file yang akan dimasukkan ke dalam ZIP
                file_path = os.path.join(foldername, filename)
                # Path relatif file dalam ZIP
                rel_path = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, rel_path)

    callback = f'https://geofence-api.asiaresearchinstitute.com/output/zip/{username}.zip'
    return callback
    # return f'output/zip/{username}.zip'

@csrf_exempt
def get_data(request: HttpRequest):
    try:
        # Mendapatkan parameter name dan file dari permintaan GET
        name = request.GET.get('name', None)
        file = request.GET.get('file', None)
        # name = request.POST.get('name', None)
        # file = request.POST.get('file', None)
            
        if 'name' not in request.GET or 'file' not in request.GET: # Validasi jika parameter yang diberikan bukan name dan file
            raise ValueError("Parameter not match. Please contact the IT Team for more information about parameters")
            
        elif not name or not file: # Validasi jika name dan file kosong
            raise ValueError("Parameters are required.")
        
        # if name is None or file is None: # Validasi jika bukan parameter name dan file
        #     raise ValueError("Parameters are required.")

        decoded_value = unquote(file)
        # file = decoded_value
        
        # Path file GeoJSON yang akan dikonversi
        geojson_file = f'https://geofence.asiaresearchinstitute.com/upload/files/{name}/{file}.geojson'
        
        # # Kodekan hanya nilai parameter "file"
        # encoded_file = urlencode({'file': file})[len('file='):]
        # # Ganti nilai parameter "file" dengan yang sudah dikodekan dalam URL
        # geojson_file = url.replace(file, encoded_file)

        # Ambil nama file dari path GeoJSON
        geojson_filename = os.path.splitext(os.path.basename(geojson_file))[0]
        # raise ValueError(f"decode = {decoded_value} and file = {file} and geo = {geojson_file}")

        # Gunakan nama file GeoJSON sebagai nama pengguna (username)
        username = geojson_filename

        # Path file Shapefile keluaran tanpa ekstensi
        user_dir = create_user_folder(username)
        shapefile_output = user_dir

        # Membaca data GeoJSON menggunakan geopandas
        gdf = gpd.read_file(geojson_file)
        # print(gdf)

        # Menyimpan data GeoJSON sebagai Shapefile lengkap
        gdf.to_file(shapefile_output, driver='ESRI Shapefile', encoding='utf-8')
        
        # buat zip file untuk dikirim ke backend
        zip_file = create_zip_folder(username, user_dir)

        # Contoh data yang akan diubah ke format JSON
        data = {
            # "username": name,
            # "filename": username,
            "geojson_file": geojson_file,
            "zip_file": zip_file,
            # "zip": f'https://geofence-api.asiaresearchinstitute.com/{zip_file}',
            # "file_url": f'https://geofence-api.asiaresearchinstitute.com/upload/output/zip/{file}.zip',
            "status": "success",
            "message": "Convert GeoJSON To Shapefile Finished"
        }
        print(data)

        # Mengembalikan respons JSON
        return JsonResponse(data)
        
    except ValueError as e:
        # Jika kesalahan karena parameter yang kurang, kembalikan respons bad request (400)
        return JsonResponse({"status": "error", "message": str(e), "code": 400}, status=400)
    except Exception as e:
        # Jika kesalahan umum, kembalikan respons server error (500)
        return JsonResponse({"status": "error", "message": str(e), "code": 500}, status=500)
        
    # except Exception as e:
    #     # Mengembalikan respons JSON dalam kasus kesalahan
    #     if isinstance(e, ValueError):
    #         # Jika kesalahan karena parameter yang kurang, kembalikan respons bad request (400)
    #         return HttpResponseBadRequest({"status": "error", "message": str(e)})
    #     else:
    #         # Jika kesalahan umum, kembalikan respons server error (500)
    #         return HttpResponseServerError({"status": "error", "message": str(e)})
            
        # # Mengembalikan respons JSON dalam kasus kesalahan
        # return JsonResponse({"status": "error", "message": str(e)})
    
# def get_data(request, name, file):
#     # name = nama folder user
#     # file = nama file geojson
#     # try:
#         # Path file GeoJSON yang akan dikonversi
#         geojson_file = f'https://geofence.asiaresearchinstitute.com/upload/files/{name}/{file}.geojson'

#         # Ambil nama file dari path GeoJSON
#         geojson_filename = os.path.splitext(os.path.basename(geojson_file))[0]

#         # Gunakan nama file GeoJSON sebagai nama pengguna (username)
#         username = geojson_filename

#         # Path file Shapefile keluaran tanpa ekstensi
#         user_dir = create_user_folder(username)
#         shapefile_output = user_dir

#         # Membaca data GeoJSON menggunakan geopandas
#         gdf = gpd.read_file(geojson_file)
#         # print(gdf)

#         # Menyimpan data GeoJSON sebagai Shapefile lengkap
#         gdf.to_file(shapefile_output, driver='ESRI Shapefile', encoding='utf-8')
        
#         # buat zip file untuk dikirim ke backend
#         zip_file = create_zip_folder(username, user_dir)

#         # Contoh data yang akan diubah ke format JSON
#         data = {
#             "filename": username,
#             "geojson_file": geojson_file,
#             "zip_file": f'https://geofence-api.asiaresearchinstitute.com/{zip_file}',
#             "file_url": f'https://geofence-api.asiaresearchinstitute.com/upload/output/zip/{file}.zip',
#             "status": "success",
#             "message": "Convert GeoJSON To Shapefile Finished..."
#         }
#         print(data)

#         # return JsonResponse(data)
#         return "Convert GeoJSON To Shapefile Finished"
#     # except Exception as e:
#     #     return JsonResponse({"status": "error", "message": str(e)})

