from pyrogram import Client, filters
import requests
import PyPDF2
import os
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup  


TOKEN = os.environ.get("TOKEN", "")

API_ID = int(os.environ.get("API_ID", ))

API_HASH = os.environ.get("API_HASH", "")



app = Client("anime-gen", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)


# Start command
@app.on_message(filters.command("start"))
def start(client, message):
    client.send_message(message.chat.id, "Bot telah dijalankan. Kirim file PDF untuk dikompres.")

# Function to compress PDF file
def compress_pdf(input_path, output_path):
    with open(input_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        pdf_writer = PyPDF2.PdfFileWriter()

        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            page.compressContentStreams()
            pdf_writer.addPage(page)

        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)

# Respond to the message containing a PDF file
@app.on_message(filters.document & ~filters.private)
def compress_pdf_file(client, message):
    file_info = message.document
    file_name = file_info.file_name

    if file_name.endswith('.pdf'):
        input_path = client.download_media(message, file_name)
        output_path = f'compressed_{file_name}'

        compress_pdf(input_path, output_path)

        client.send_document(message.chat.id, output_path, caption="File PDF telah dikompres.")
        os.remove(input_path)  # Remove the original file
        os.remove(output_path)  # Remove the compressed file
    else:
        client.send_message(message.chat.id, "Mohon kirim file PDF saja.")


        
app.run()
