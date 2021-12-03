# nfd-checker

## Summary

This script checks the given Google Drive for NFD (decomposed) accented file names and converts them to NFC (single code point) form. No file contents are downloaded and/or modified.

```bash
$ python3 ./gdrive-nfc-check.py -h
usage: gdrive-nfc-check.py [-h] [--print_tree] [--q_rootfiles Q_ROOTFILES] [--no-dry_run] [--report_memory]
                           [--debug]

Checks your Google Drive for NFD encoded filenames and converts them to NFC format

optional arguments:
  -h, --help            show this help message and exit
  --print_tree          print the Drive directory tree
  --q_rootfiles Q_ROOTFILES
                        The query string used to get the items to be worked on, default is the root of the drive
                        (q = "'root' in parents and trashed = false"). As a precaution, you should try it with a
                        smaller scope, like "title contains '---accent_test---' and trashed = false"
  --no-dry_run          If set, only then will the NFD->NFC conversion take place
  --report_memory       Enable reporting of used memory
  --debug               Enable debugging

```

## Setup

1. Clone the git repo

2. Switch to the "setup" folder and run the ```setup.sh``` script. It will create a virtual environment and it will install all required dependencies into that. You can setup and use the script without elevated privileges on the computer, and uninstall should be as simple as deleting the project folder.

3. Change your working directory to the project root folder and activate the virtual environment from the shell:

    ```bash
    . ./project-venv/bin/activate
    ```

Now you are ready to go! If you are done with using, type ```deactivate``` to exit from the virtual environment.

## Suggested usage

The script will not change anything on your Google Drive, until you explicitly tell it to do so. In order to write back the converted names, you have to use the ```--no-dry_run``` option.

First do a simple check to see if everything is OK with the install:

```bash
python3 ./gdrive-nfc-check.py  --report_memory
```

Then, please do a sanity check to ensure the structure of your drive is correctly understood:

```bash
python3 ./gdrive-nfc-check.py  --print_tree 2>&1 | tee report_00_sanity.txt | less
```

If the results seems reasonable, you can request the rename:

```bash
python3 ./gdrive-nfc-check.py  --no-dry_run 2>&1 | tee report_01_run.txt | less
```

## Use case

Filenames can have NFD accents when files are created on an Apple device. The decomposed accents seems to be the default representation of the Apple ecosystem (or at least, the Mac OS), and can cause interop problems with non-Apple products, which does not handle well the NFD representation.

The "NFD problem" is not a fault of Apple, NFD is pretty much part of the  Unicode standard. Unicode support came very early to the Apple platform and other platforms started to introduce partial Unicode support later.

Technically it is easier to implement the NFC form,
probably that is the reason that proper NFD support was added at a later stage.

Until we have systems with early implementations of Unicode support,we will encounter problems, too.
If upgrade is not possible, then the only thing one can do is to change the representation of the accented characters.

## Disclaimer

This software is released in the spirit of Free and Open Source Software, but while the code is free, support is not.

Use it as-is for your benefit, but i take no responsibility if it blows and i cannot guarantee that i will have the time necessary to deal with support requests.
