import logging
import os
import base64
import azure.functions as func
from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage


def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    connection_string = os.environ["snibirkedastor_STORAGE"]
    blob_name = myblob.name[7:]
    queue_client = QueueClient.from_connection_string(connection_string, "grayscale-queue")
    encoded_bytes = base64.b64encode(blob_name.encode("utf-8"))
    encoded_str = str(encoded_bytes, "utf-8")
    queue_client.send_message(encoded_str)
