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
import mysql.connector
import re
from urllib.parse import unquote
from urllib.parse import urlencode
from urllib.parse import quote

# Mengambil full path untuk direktori upload/output/zip
MAIN_PATH = '/home/u8378009/public_html/geofence-api.asiaresearchinstitute.com/'
UPLOAD_OUTPUT = '/home/u8378009/public_html/geofence-api.asiaresearchinstitute.com/output/'
UPLOAD_OUTPUT_ZIP_PATH = '/home/u8378009/public_html/geofence-api.asiaresearchinstitute.com/output/zip/'

@csrf_exempt
def create_user_folder(username):
    # Path direktori utama
    # base_dir = '/home/u8378009/public_html/geofence-api.asiaresearchinstitute.com/output'
    base_dir = UPLOAD_OUTPUT

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
    # zip_file = f'/home/u8378009/public_html/geofence-api.asiaresearchinstitute.com/output/zip/{username}.zip'
    zip_file = os.path.join(UPLOAD_OUTPUT_ZIP_PATH, f'{username}.zip')

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

def is_japanese(text):
    # Pola regex untuk mencocokkan karakter bahasa Jepang
    japanese_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]')
    return bool(japanese_pattern.search(text))
    
# Fungsi untuk mengakses database dan memeriksa apakah teks mengandung karakter Jepang
def get_db(text):
    try:
        # Membuat koneksi ke database MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="u8378009_asiarese",
            password="ep5]kgGVV}re",
            database="u8378009_geofence"
        )

        # Membuat objek cursor untuk melakukan query
        cursor = conn.cursor()

        # Mengeksekusi query dengan kondisi where polygon_name 
        # query = "SELECT feature_collection FROM tb_geo_draw WHERE polygon_name = %s"
        query = "SELECT link FROM tb_geo_draw WHERE polygon_name = %s"
        cursor.execute(query, (text,))

        # Mendapatkan hasil query
        result = cursor.fetchone()

        # Menutup koneksi dan cursor
        cursor.close()
        conn.close()

        # Mengembalikan hanya kolom link dari hasil query
        return result
    except Exception as e:
        print("Error:", e)
        return False

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

        # decoded_value = unquote(file)
        # file = decoded_value
        
        # ======================================================================
        # # Path file GeoJSON yang akan dikonversi
        # geojson_file = f'https://geofence.asiaresearchinstitute.com/upload/files/{name}/{file}.geojson'
        
        # # Ambil nama file dari path GeoJSON
        # geojson_filename = os.path.splitext(os.path.basename(geojson_file))[0]
        # # raise ValueError(f"decode = {decoded_value} and file = {file} and geo = {geojson_file}")
        
        # # Gunakan nama file GeoJSON sebagai nama pengguna (username)
        # username = geojson_filename
        # ======================================================================
        
        # ======================================================================
        # Mengecek apakah teks file mengandung karakter Jepang
        # Jika IYA Ambil data dari database
        # Jika TIDAK ambil melalui URL geofence
        geojson_file = get_db(file)[0] if is_japanese(file) else f'https://geofence.asiaresearchinstitute.com/upload/files/{name}/{file}.geojson'
        
        # url_encoded_filename = quote(file)
        # # Buat URL lengkap dengan nama file yang diubah
        # url = f"https://geofence.asiaresearchinstitute.com/upload/files/{name}/{url_encoded_filename}.geojson"
        
        db_result = get_db(file)
        if db_result:
            geojson_file = db_result[0]
            # Ambil nama file dari path GeoJSON
            geojson_filename = os.path.splitext(os.path.basename(geojson_file))[0]
            
            url_encoded_filename = quote(geojson_filename)
            # url = f"https://geofence.asiaresearchinstitute.com/upload/files/{name}/{url_encoded_filename}.geojson"
            
            # data_error = {"msg": "IF Failed to get GeoJSON from Database", "file": file, "url": url, "url_encoded": url_encoded_filename, "geojson_file": geojson_file, "db_result": db_result, "is_japanese": is_japanese(file)}
            # return JsonResponse(data_error)
        else:
            url_encoded_filename = quote(file)
            # url = f"https://geofence.asiaresearchinstitute.com/upload/files/{name}/{url_encoded_filename}.geojson"
            
            # data_error = {"msg": "ELSE Failed to get GeoJSON from Database", "file": file, "url": url, "url_encoded": url_encoded_filename, "geojson_file": None, "db_result": db_result, "is_japanese": is_japanese(file)}
            # return JsonResponse(data_error)
            
        
        # Buat URL lengkap dengan nama file yang diubah
        url = f"https://geofence.asiaresearchinstitute.com/upload/files/{name}/{url_encoded_filename}.geojson"
        
        # Gunakan nama file GeoJSON sebagai nama pengguna (username)
        username = file
        # ======================================================================

        # Path file Shapefile keluaran tanpa ekstensi
        user_dir = create_user_folder(username)
        shapefile_output = user_dir

        # Membaca data GeoJSON menggunakan geopandas
        gdf = gpd.read_file(url, encoding='utf-8')
        
        # Jika gagal membaca GeoJSON, kembalikan pesan error
        if gdf is None:
            return jsonify(error="Failed to fetch GeoJSON from URL")
        
        # # Membaca data GeoJSON menggunakan geopandas
        # gdf = gpd.read_file(geojson_file)
        # # print(gdf)

        # Menyimpan data GeoJSON sebagai Shapefile lengkap
        gdf.to_file(shapefile_output, driver='ESRI Shapefile', encoding='utf-8')
        
        # buat zip file untuk dikirim ke backend
        zip_file = create_zip_folder(username, user_dir)
        
        # hapus folder shp setelah buat zip
        shutil.rmtree(shapefile_output)
        # shutil.rmtree('output/zip')

        # Contoh data yang akan diubah ke format JSON
        data = {
            # "username": name,
            # "filename": username,
            "url": url,
            "file": file,
            "geojson_file": geojson_file,
            "user_dir": user_dir,
            "zip_file": zip_file,
            "code": 200,
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

