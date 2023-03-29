import argparse
import requests
import json
import base64



def start_session(baseurl, apiKey, flowId):
    url = f'{baseurl}/omni/start'
    headers = {
        'api-version': '1.0',
        'x-api-key': apiKey
    }
    data = {
        'countryCode': 'ALL',
        'configurationId': flowId
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(response.text)


def upload_front_id(baseurl, apiKey, token, base64Image):
    url = f'{baseurl}/omni/add/front-id/v2'
    headers = {
        'api-version': '1.0',
        'x-api-key': apiKey,
        'X-Incode-Hardware-Id': token
    }
    data = {
        'base64Image': base64Image
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(response.text)


def upload_back_id(baseurl, apiKey, token, base64Image):
    url = f'{baseurl}/omni/add/back-id/v2'
    headers = {
        'api-version': '1.0',
        'x-api-key': apiKey,
        'X-Incode-Hardware-Id': token
    }
    data = {
        'base64Image': base64Image
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(response.text)


def upload_selfie(baseurl, apiKey, token, base64Image):
    url = f'{baseurl}/omni/add/face/third-party'
    headers = {
        'api-version': '1.0',
        'x-api-key': apiKey,
        'X-Incode-Hardware-Id': token
    }
    data = {
        'base64Image': base64Image
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(response.text)


def fetch_scores(baseurl, apiKey, token, interviewId):
    url = f'{baseurl}/omni/get/score?id={interviewId}&verbose=true'
    headers = {
        'api-version': '1.0',
        'x-api-key': apiKey,
        'X-Incode-Hardware-Id': token
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(response.text)


def onboard(baseurl, apiKey, flowId, frontIdPath, backIdPath, selfiePath):
    session = start_session(baseurl, apiKey, flowId)
    interviewId = session['interviewId']
    token = session['token']
    with open(frontIdPath, "rb") as img_file:
        frontBase64Image = base64.b64encode(img_file.read())
    upload_front_id(baseurl, apiKey, token, frontBase64Image.decode('utf-8'))
    if backIdPath is not None:
        with open(frontIdPath, "rb") as img_file:
            backBase64Image = base64.b64encode(img_file.read())
        upload_back_id(baseurl, apiKey, token, backBase64Image.decode('utf-8'))
    with open(selfiePath, "rb") as img_file:
        selfieBase64Image = base64.b64encode(img_file.read())
    upload_selfie(baseurl, apiKey, token, selfieBase64Image.decode('utf-8'))
    scores = fetch_scores(baseurl, apiKey, token, interviewId)
    print(f'Session created with ID: {interviewId}')
    print('SCORE:')
    print(json.dumps(scores, indent=2))

def main():
    parser = argparse.ArgumentParser(
        description='Incode Manual Session Creator')
    parser.add_argument('--baseurl', dest='baseurl',
                        help='Incode\'s server address (ignore if demo)', required=True)
    parser.add_argument('--apikey', dest='apiKey', default=None,
                        help='API KEY', required=True)
    parser.add_argument('--flowid', dest='flowId', default=None,
                        help='Flow Identifier', required=True)
    parser.add_argument('--frontid', dest='frontId', default=None,
                        help='Front ID file path', required=True)
    parser.add_argument('--backid', dest='backId', default=None,
                        help='Back ID file path')
    parser.add_argument('--selfie', dest='selfie', default=None,
                        help='Selfie file path', required=True)

    args = parser.parse_args()
    onboard(args.baseurl, args.apiKey, args.flowId, args.frontId, args.backId, args.selfie)


main()
