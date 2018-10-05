from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'


def create_folder(drive_service, folder_name):#only root
    file_metadata = {
    'name': folder_name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    return file

def copy_file(drive_service,fileId, new_file_name, parent_folder_id):
    file_metadata = {
        'name': new_file_name,
        'parents': [parent_folder_id]
    }
    drive_service.files().copy(fileId=fileId, body=file_metadata).execute()

def search_file(drive_service, file_name):
    files = drive_service.files().list(q='name = \'{}\''.format(file_name)).execute().get('files',[])
    if len(files) >= 1:
        return files[0]
    else:
        return None

def main_1():

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Call the Drive v3 API
    folder = create_folder(service, "api_test")

    img = search_file(service,"_DSC2054_stitch.jpg")
    print('{0} ({1})'.format(img['name'], img['id']))

    copy_file(service, img['id'], "my new file.jpg", folder['id'])




if __name__ == '__main__':
    main_1()

