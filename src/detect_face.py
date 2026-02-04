import json
import urllib.request
import os
import cv2
import boto3
import string
import random
import base64

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def save_binary_file(binary_data, file):
    with open(file, 'wb') as output_file:
        output_file.write(binary_data)

def download_file(url, file):
    with urllib.request.urlopen(url) as response:
        with open(file, 'wb') as output_file:
            output_file.write(response.read())

def detect_faces(image_path, face_detector_path):
    face_cascade = cv2.CascadeClassifier(face_detector_path)
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)
    return faces

def generate_random_string(n):
    characters  = string.ascii_letters + string.digits
    random_string  = ''.join(random.choice(characters) for _ in range(n))
    return random_string 


def lambda_handler(event, context):
    image_id= generate_random_string(10)
    is_base64_encoded = event.get("isBase64Encoded", False)
    body = event['body']

    table=dynamodb.Table('faces')
    # Convertir a bytes si es base64
    if is_base64_encoded:
        body = base64.b64decode(body)

    image_path='/tmp/{}.jpg'.format(image_id)
    save_binary_file(body, image_path)

    face_detector_url = 'https://raw.githubusercontent.com/opencv/opencv/4.x/data/haarcascades/haarcascade_frontalface_default.xml'
    face_detector_path = '/tmp/haarcascade_frontalface_default.xml'
    download_file(face_detector_url, face_detector_path)

    faces = detect_faces(image_path, face_detector_path)

    faces_ = {}
    for face_indx,face in enumerate(faces):
        x1,y1,w,h = face
        x2=x1+w
        y2=y1 +h
        faces_[face_indx]={'x1':int(x1),'y1':int(y1),'x2':int(x2),'y2':int(y2)} 
        face_id=generate_random_string(10)
        item = {
            'face_id': face_id,
            'image_id': image_id,
            'x1': int(x1),
            'y1': int(y1),
            'x2': int(x2),
            'y2': int(y2),
        }
        table.put_item(Item=item)
        
    s3_client.upload_file(image_path,"face-detection-s3-lusber",'{}.jpg'.format(image_id))
    return {
        'statusCode': 200,
        'body': json.dumps({'faces': faces_})
    }
