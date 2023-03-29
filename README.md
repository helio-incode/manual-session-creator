# Manual Session Creator

A Python tool to manually create sessions



## Prerequisites

Python3 should be installed. Also the `requirements.txt` lists all Python libraries that should be installed before running the script:

```bash
pip3 install -r requirements.txt

```
## Usage

```bash
usage: main.py [-h] --baseurl BASEURL --apikey APIKEY --flowid FLOWID --frontid FRONTID [--backid BACKID] --selfie SELFIE

arguments:
  -h, --help         show this help message and exit
  --baseurl BASEURL  Incode server address
  --apikey APIKEY    API KEY
  --flowid FLOWID    Flow Identifier
  --frontid FRONTID  Front ID file path
  --backid BACKID    Back ID file path
  --selfie SELFIE    Selfie file path
```