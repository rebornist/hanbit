from django.core.files.storage import FileSystemStorage


def file_uploads(myfile, media_path):
    fs = FileSystemStorage()
    filename = fs.save(f"{media_path}/{myfile.name}", myfile)
    uploaded_file_url = fs.url(filename)
    return uploaded_file_url
