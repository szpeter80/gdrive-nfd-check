import os,sys,unicodedata
import oauth2client.client

from pydrive.auth  import GoogleAuth,RefreshError
from pydrive.drive import GoogleDrive

#q_rootfiles = "'root' in parents and trashed = false"
q_rootfiles = "title contains '---accent_test---'  and trashed = false"

fileStash = {} # id -> GoogleDriveFile, a dict of all items received from the Drive account
childList = {} # id -> list of child node id's
nfcStatus = {} # id -> Boolean; True if name passes as NFC, False if not
nonNfcItems = {} # id -> path; list of file ids and corresponding full names with path, which are not NFC compliant. These are the elements with nfcStatus->False.

p_printTree = False # Print the directory tree

#'mimeType': 'application/vnd.google-apps.folder'
def is_gfolder(gdfv2):
  return ('mimeType' in gdfv2 and gdfv2['mimeType']=='application/vnd.google-apps.folder')
  
def print_gfile(ident_str, gdfv2):
  isdir_str = '<DIR>' if is_gfolder(gdfv2) else ''
  isnonnfc_str = '' if nfcStatus[gdfv2['id']] else '***'

  print('{}{}{:<45}'.format(isnonnfc_str,ident_str, isdir_str+' '+gdfv2['title']+' '+isdir_str))  

def proc_item(level, ppath, gdfv2):
  if unicodedata.is_normalized('NFC',gdfv2['title']):
    nfcStatus[gdfv2['id']] = True
  else:
    nfcStatus[gdfv2['id']] = False
    nonNfcItems[gdfv2['id']] = ppath + gdfv2['title']

  ident_str = '{1:>{0}} '.format(4*level, '')
  if p_printTree:
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

drive = GoogleDrive(gauth)

# View all folders and file in your Google Drive
# PyDrive uses V2 of the Google Drive API  (2021.04.28)
try:
  print("Requesting list of all files and folders in this drive ... ", end='', flush=True)
  allFileList = drive.ListFile({'q': "trashed = false"}).GetList()
  print("done, {0} items".format(len(allFileList)), flush=True)

  print("Requesting elements to start with... ", end='', flush=True)
  rootFileList = drive.ListFile({'q': q_rootfiles}).GetList()
  print("done, {0} items\n".format(len(rootFileList)), flush=True)

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
  proc_item(0, '/', file)

print('\n\n{} item has non-NFC name:\n'.format(len(nonNfcItems)))
for id,path in nonNfcItems.items():
  dir_str = ' <DIR>' if is_gfolder(fileStash[id]) else ''
  print('{}{}'.format(path,dir_str))

#fn_nfc = unicodedata.normalize('NFC', file['title'])