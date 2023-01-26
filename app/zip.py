import zipfile 

def zip(file_paths,zip_path):
    with zipfile.ZipFile(zip_path,'w') as zip_file:
        for file_path in file_paths:
            zip_file.write(file_path,compress_type=zipfile.ZIP_DEFLATED)
    