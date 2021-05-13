import os,sys
import oauth2client.client

from pydrive.auth  import GoogleAuth,RefreshError
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LoadCredentials()
gauth.GetFlow()

if gauth.credentials is None:
    print(gauth.GetAuthUrl())
    code = str(input())
    gauth.Auth(code)

gauth.SaveCredentials()

##gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

# View all folders and file in your Google Drive
# PyDrive uses V2 of the Google Drive API  (2021.04.28)
try:
  print("Requesting list of files")
  fileList = drive.ListFile({'q': "trashed = false"}).GetList()
  print("File list received, {0} items".format(len(fileList)))
except RefreshError:
  print("Failed to re-use the access token. Probably it has expired or invalid.")
  if os.path.exists("credentials.json"):
      print("Deleting the credentials file")
      os.remove("credentials.json")
      sys.exit()

for file in fileList:
  print('{:<40} | {:<20} \n{:<40} \n'.format( file['title'], ('sharedWithMeDate' in file), file['id'] ))

#print(file)
