import os
import time
import logging
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=snibirkedastor;AccountKey=C1IhonwBhuGAvypzZiQaEECa353DdAOv0EK3BNdXFtRfY05X0U7KwEF7DmEOxM/bYGqSs9EPjvT/AP1CLTy3bw==;EndpointSuffix=core.windows.net")
    logging.info(f"Start Time: {time.perf_counter()}")
    blob = BlobClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;AccountName=snibirkedastor;AccountKey=C1IhonwBhuGAvypzZiQaEECa353DdAOv0EK3BNdXFtRfY05X0U7KwEF7DmEOxM/bYGqSs9EPjvT/AP1CLTy3bw==;EndpointSuffix=core.windows.net", container_name="images", blob_name=myblob.name[7:])
    logging.info(f"Blob Name: {blob.blob_name}")
    data = blob.download_blob().content_as_bytes(max_concurrency=1)
    dt = np.fromstring(data, dtype='uint8')
    image = cv2.imdecode(dt, cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    pil_image = Image.fromarray(gray)
    img_byte_arr = BytesIO()
    pil_image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    logging.info(f"End Time{time.perf_counter()}")
    #upload grayscale
    container_name = "grayscale"
    container_client = blob_service_client.get_container_client(container_name)
    try:
        container_client.upload_blob(name=blob.blob_name, data=img_byte_arr)
    except:
        pass
    logging.info(f"{time.perf_counter()}")
    # #upload color
    # container_name = "color"
    # container_client = blob_service_client.get_container_client(container_name)
    # try:
    #     await container_client.upload_blob(name=blob.blob_name, data=data)
    # except:
    #     pass
    # logging.info(f"{time.perf_counter()}")
    # #remove image
    # container_images = "images"
    # container_client = blob_service_client.get_container_client(container_images)
    # try:
    #     await container_client.delete_blob(blob.blob_name, delete_snapshots=None)
    # except:
    #     pass
