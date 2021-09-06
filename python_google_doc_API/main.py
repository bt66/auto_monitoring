from __future__ import print_function
from os import write
import os.path
import datetime
from typing import Text
from google.auth.transport import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from variabel import *


# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
DOCUMENT_ID = '1A6Hxi_q3JPMK3zWl9fGM-84mcjxzmlJmdgsDDft074g'


def get_last_index(id_of_document, creds):
    service = build('docs', 'v1', credentials=creds)
    document = service.documents().get(documentId=id_of_document).execute()
    body = document['body']
    content = body['content']
    temp = content[len(content)-1]
    endIndex = temp['endIndex']
    realEndindex = endIndex - 1
    print('end index : ', endIndex)
    return temp['endIndex']


# function to insert text

# function to insert image
def insert_Image(id_of_document, url, last_index, creds):
    service = build('docs', 'v1', credentials=creds)
    requests = [
        {
            'insertInlineImage': {
                'location': {
                    'index': last_index - 1
                },
                'uri': url,
                'objectSize': {
                    'height': {
                        'magnitude': 500,
                        'unit': 'PT'
                    },
                    'width': {
                        'magnitude': 500,
                        'unit': 'PT'
                    }
                },
            }
        },
        {
            "createParagraphBullets": {
                "range": {
                    "startIndex": last_index,
                    "endIndex": last_index+1
                },
                "bulletPreset": "NUMBERED_DECIMAL_ALPHA_ROMAN"
            }
        }
    ]

    # Execute the request.
    body = {'requests': requests}
    response = service.documents().batchUpdate(
        documentId=id_of_document, body=body).execute()
    insert_inline_image_response = response.get('replies')[0].get(
        'insertInlineImage')
    print('Inserted image with object ID: {0}'.format(
        insert_inline_image_response.get('objectId')))


# add image and text with numbering function
def img_text(id_of_document, url, text, last_index, creds):
    service = build('docs', 'v1', credentials=creds)
    requests = [
        {
            "insertText": {
                "location": {
                    "index": last_index - 1
                },
                "text": text
            }
        },
        {
            "insertInlineImage":
            {
                "uri": url,
                "location":
                {
                    "index": last_index - 1
                },
                "objectSize":
                {
                    "height":
                    {
                        "magnitude": 400,
                        "unit": "PT"
                    },
                    "width":
                        {
                            "magnitude": 400,
                            "unit": "PT"
                    }
                }
            }
        },
        {
            "createParagraphBullets":
            {
                "range":
                {
                    "startIndex": 1,
                    "endIndex": 10
                },
                "bulletPreset": "NUMBERED_DECIMAL_ALPHA_ROMAN_PARENS"
            }
        }
    ]

    body = {'requests': requests}
    response = service.documents().batchUpdate(
        documentId=id_of_document, body=body).execute()
    insert_inline_image_response = response.get('replies')[0].get(
        'insertInlineImage')
    print('Inserted image with object ID: {0}'.format(
        insert_inline_image_response.get('objectId')))


def pagebreak(creds, last_index):
    service = build('docs', 'v1', credentials=creds)
    requests = [
        {
            "insertText": {
                "location": {
                    "index": last_index - 1
                },
                "text": "asdfghj\n"
            }
        }
    ]


def wirteText(creds, docId, text, url):
    service = build('docs', 'v1', credentials=creds)
    last_index = get_last_index(docId, creds)
    requests = [
        {
            "insertText": {
                "location": {
                    "index": last_index - 1
                },
                "text": text
            }
        }
    ]
    result = service.documents().batchUpdate(
        documentId=docId, body={'requests': requests}).execute()
    last_index = get_last_index(docId, creds)
    requests = [
        {
            "insertInlineImage":
            {
                "uri": url,
                "location":
                {
                    "index": last_index - 1
                },
                "objectSize":
                {
                    "height":
                    {
                        "magnitude": 500,
                        "unit": "PT"
                    },
                    "width":
                    {
                        "magnitude": 500,
                        "unit": "PT"
                    }
                }
            }
        }
    ]
    result = service.documents().batchUpdate(
        documentId=docId, body={'requests': requests}).execute()
    last_index = get_last_index(docId, creds)
    requests = [
        {
            "insertText": {
                "location": {
                    "index": last_index - 1
                },
                "text": " \n"
            }
        }
    ]
    result = service.documents().batchUpdate(
        documentId=docId, body={'requests': requests}).execute()


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

    current_time = datetime.datetime.now()

    title = current_time.strftime("%d %B %Y")
    body = {
        'title': title
    }
    doc = service.documents().create(body=body).execute()
    docId = doc.get('documentId')
    print('Id of new Document is : ' + docId)

    # text1 = "1. monitoring ip 10.10.10.10"
    # loop for vm blc full
    # i = 0
    for i in range(len(url_vm_blc_full)):
        wirteText(creds, docId, name_vm_blc_full[i],url_vm_blc_full[i])

    for i in range(len(url_vm_microgen_full_monitoring)):
        wirteText(creds, docId, name_vm_microgen_full_monitoring[i],url_vm_microgen_full_monitoring[i])

    for i in range(len(url_project_rancher)):
        wirteText(creds, docId, name_project_rancher[i],url_project_rancher[i])

    # z = len(url_vm_blc_full)
    # while i < z:
    #     wirteText(creds, docId, name_vm_blc_full[i],
    #               url_vm_blc_full[i])
    #     i += 1


    # j = 0
    # x = len(url_vm_microgen_full_monitoring)
    # print('length vm microgen : ', z)
    # while j < x:
    #     wirteText(creds, docId, name_vm_microgen_full_monitoring[i],
    #               url_vm_microgen_full_monitoring[i])
    #     i += 1

    # k = 0
    # c = len(url_project_rancher)
    # while k < c:
    #     wirteText(creds, docId, name_project_rancher[i],
    #               url_project_rancher[i])
    #     i += 1

    # wirteText(creds, docId, "2. monitoring ip 10.10.23.126",
    #           "http://endpoint.carakan.id/project_rancher/10.10.23.126%3A9100.png")

    # last_index = get_last_index(docId, creds)
    # requests = [
    #     {
    #         "insertText": {
    #             "location": {
    #                 "index": 1
    #             },
    #             "text": "asdf\n"
    #         }
    #     },
    #     {
    #         "insertInlineImage": {
    #             "uri": "http://endpoint.carakan.id/project_rancher/10.10.23.125%3A9100.png",
    #             "location": {
    #                 "index": 8
    #             },
    #             "objectSize": {
    #                 "height": {
    #                     "magnitude": 450,
    #                     "unit": "PT"
    #                 },
    #                 "width": {
    #                     "magnitude": 450,
    #                     "unit": "PT"
    #                 }
    #             }
    #         }
    #     },
    #     {
    #         "insertText": {
    #             "location": {
    #                 "index": 1
    #             },
    #             "text": "rsff\n"
    #         }
    #     },
    #     {
    #         "insertInlineImage": {
    #             "uri": "http://endpoint.carakan.id/project_rancher/10.10.23.125%3A9100.png",
    #             "location": {
    #                 "index": 8
    #             },
    #             "objectSize": {
    #                 "height": {
    #                     "magnitude": 450,
    #                     "unit": "PT"
    #                 },
    #                 "width": {
    #                     "magnitude": 450,
    #                     "unit": "PT"
    #                 }
    #             }
    #         }
    #     },
    #     {
    #         "createParagraphBullets": {
    #             "range": {
    #                 "startIndex": 1,
    #                 "endIndex": 50
    #             },
    #             "bulletPreset": "NUMBERED_DECIMAL_ALPHA_ROMAN_PARENS"
    #         }
    #     }
    # ]

    # result = service.documents().batchUpdate(
    #     documentId=docId, body={'requests': requests}).execute()


if __name__ == '__main__':
    main()
