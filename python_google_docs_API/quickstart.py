from __future__ import print_function
import os.path
from typing import Text
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
DOCUMENT_ID = '1A6Hxi_q3JPMK3zWl9fGM-84mcjxzmlJmdgsDDft074g'


def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('docs', 'v1', credentials=creds)

    # # Retrieve the documents contents from the Docs service.
    # document = service.documents().get(documentId=DOCUMENT_ID).execute()

    # print('The title of the document is: {}'.format(document.get('title')))
    # title = 'Test APi '
    # body = {
    #     'title': title
    # }
    # doc = service.documents() \
    #     .create(body=body).execute()
    # print('Created document with title: {0}'.format(
    #     doc.get('title')))

    title = 'test api'
    body = {
        'title': title
    }
    doc = service.documents().create(body=body).execute()
    docId = doc.get('documentId')
    print('Id of new Document is : ' + docId)

    text1 = "monitoring ip 10.10.10.10"
    text2 = "halomas2"
    text3 = "halomas3"
    requests = [
        {

            "insertText":
            {
                "text": text1,
                "location":
                {
                    "index": 1
                }
            }
        }

    ]

    result = service.documents().batchUpdate(
        documentId=docId, body={'requests': requests}).execute()

    requests = [{
        'insertInlineImage': {
            'location': {
                'index': 9
            },
            'uri':
            'https://fonts.gstatic.com/s/i/productlogos/docs_2020q4/v6/web-64dp/logo_docs_2020q4_color_1x_web_64dp.png',
            'objectSize': {
                'height': {
                    'magnitude': 200,
                    'unit': 'PT'
                },
                'width': {
                    'magnitude': 200,
                    'unit': 'PT'
                }
            }
        }
    }]

    # Execute the request.
    body = {'requests': requests}
    response = service.documents().batchUpdate(
        documentId=docId, body=body).execute()
    insert_inline_image_response = response.get('replies')[0].get(
        'insertInlineImage')
    print('Inserted image with object ID: {0}'.format(
        insert_inline_image_response.get('objectId')))


if __name__ == '__main__':
    main()
