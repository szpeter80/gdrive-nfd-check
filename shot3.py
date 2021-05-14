import os,sys,unicodedata
import oauth2client.client

from pydrive.auth  import GoogleAuth,RefreshError
from pydrive.drive import GoogleDrive


fileStash = {}
childList = {}

def is_gfolder(gdfv2):
  return ('mimeType' in gdfv2 and gdfv2['mimeType']=='application/vnd.google-apps.folder')
  
def print_gfile(ident_str, gdfv2):
  prefix = '<DIR> ' if is_gfolder(gdfv2) else ''
  suffix = ' ***' if not unicodedata.is_normalized('NFC',gdfv2['title']) else ''
  
  #fn_nfc = unicodedata.normalize('NFC', file['title'])

  print('{}{:<45}{}'.format(ident_str, prefix+gdfv2['title'],suffix))  

#'mimeType': 'application/vnd.google-apps.folder'
def proc_item(level, ppath, gdfv2):
  ident_str = '{1:>{0}} '.format(4*level, '')
  print_gfile(ident_str, gdfv2)

  if (is_gfolder(gdfv2) and gdfv2['id'] in childList):
    for child_id in childList[gdfv2['id']]:
      proc_item(level+1, ppath+gdfv2['title']+"/",fileStash[child_id])
    

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
  print("Requesting list of all files in this drive ... ", end='', flush=True)
  allFileList = drive.ListFile({'q': "trashed = false"}).GetList()
  print("done, {0} items".format(len(allFileList)), flush=True)

  print("Requesting elements in the root folder... ", end='', flush=True)
  rootFileList = drive.ListFile({'q': "'root' in parents and trashed = false"}).GetList()
  print("done, {0} items in the root directory\n".format(len(rootFileList)), flush=True)

except RefreshError:
  print("ERROR: Failed to re-use the access token, probably it has expired or invalid")
  if os.path.exists("credentials.json"):
      print("Deleting the credentials file")
      os.remove("credentials.json")
  sys.exit(1)

for file in allFileList:
  file__id = file['id']
  fileStash[file__id] = file
  
  if 'parents' in file:
    for p in file['parents']:
      parent_id = p['id']
      if not (parent_id in childList):
        childList[parent_id] =  []
      childList[parent_id].append(file__id)

del allFileList

for file in rootFileList:
  #print(file)
  proc_item(0, '/', file)

