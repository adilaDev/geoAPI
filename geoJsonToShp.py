import geopandas as gpd
import os
import shutil
from zipfile import ZipFile

def create_user_folder(username):
    # Path direktori utama
    base_dir = 'upload/output'

    # Path direktori user
    user_dir = os.path.join(base_dir, username)

    # Membuat direktori user jika belum ada
    os.makedirs(user_dir, exist_ok=True)

    return user_dir

def create_zip_folder(username, user_dir):
    # Membuat folder user
    # user_dir = create_user_folder(username)
    # print(f"user_dir: {user_dir}")

    # Path direktori yang akan di-zip
    source_dir = user_dir

    # Path file ZIP keluaran
    zip_file = f'upload/output/zip/{username}.zip'

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

    return zip_file

# Path file GeoJSON yang akan dikonversi
geojson_file = 'upload/files/Indonesian_drawing_by_アフマド.geojson'

# Ambil nama file dari path GeoJSON
geojson_filename = os.path.splitext(os.path.basename(geojson_file))[0]

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

print(f"=========================================")
print(f'File ZIP telah dibuat: {zip_file}')
print(f"=========================================")
print(f"Convert GeoJSON To Shapefile Finished...")
print(f"=========================================")
