#/usr/bin/python3
import os
import sys
import shutil
import argparse
import subprocess
import shlex
import time
from pyhanko.sign import signers
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from OpenSSL import crypto, SSL
from os.path import join
import random
import os
from pyhanko import stamp
from pyhanko.pdf_utils import text, images
from pyhanko.pdf_utils.font import opentype
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import fields, signers
from flask import Flask, render_template, redirect, request, session, jsonify, Response, send_file
from pdf2image import convert_from_path
from PIL import Image
import numpy as np
import uuid
import PyPDF2
import pikepdf
import datetime
import pyhanko
import argparse
import glob
import asyncio
import pathlib
import time
import random
from tqdm import tqdm
import psutil
import pytz
import tzdata

class AutoSigner:
    def __init__(self,f1, f2, o1, o2, p1, p2, cert, key, generate_new=True):
        '''
        AutoSigner class automatically generates a self-signed certificate, and has the ability to digitally sign
        PDF files using PyHanko. It automatically loops and launches async pdf signature and 
        '''
        config = self.load_config()
        print(config)
        if generate_new == False:
            config = self.load_config() # Loading Configuration from cert.conf
            common_name = config['common_name']
            self.cert_generator(config['common_name'], config['country'], config['state'], config['city'], config['org'], config['org_unit'])
        self.current_dir = os.getcwd()
        common_name = config['common_name']


        # loading the cms signer config for the current directory

        cms_signer = signers.SimpleSigner.load(
            f'{key}', f'{cert}'
        )
        self.signer = cms_signer


        ## ability to go ahead and get PDF files from folders
        while True:
            # we are now going to go ahead and look for all of the files in the specified directories.
            folder1_files = glob.glob(f'{f1}/*')
            folder2_files = glob.glob(f'{f2}/*')
            for filepath in folder1_files:
                # finding name of pdf using pathlib
                filename = pathlib.Path(filepath).name

                # generating a random uuid and extracting a part from it.

                gen_id = str(uuid.uuid4())
                uuid_parts = gen_id.split('-')
                random_string = random.choice(uuid_parts)


                # adding signature to each document
                print(f'[+] Signing Document: {filepath}')
                print(f'[+] Saving Signed PDF to: {output1}/{filename}_{random_string}.pdf')
                if output1[::-1] == '/':
                    decided_output_path = f'{output1}{filename}_{random_string}.pdf'
                else:
                    decided_output_path = f'{output1}\{filename}_{random_string}.pdf'

                # signing the document and saving it to the output folder


                output_path = self.signdocument(filepath, decided_output_path, bbox='(800, 20, 700, 0)')

                # sending command to the printer for printing
                if output_path != None:
                    print('[+] Sending Command to the Printer for Printing the Signed Document [!]')
                    os.system(f'PrintFile.exe -p1 "{p1}" -c MONOCHROME -f "{decided_output_path}"')

            for filepath in folder2_files:
                    # finding name of pdf using pathlib
                    filename = pathlib.Path(filepath).name

                    # generating a random uuid and extracting a part from it.

                    gen_id = str(uuid.uuid4())
                    uuid_parts = gen_id.split('-')
                    random_string = random.choice(uuid_parts)


                    # adding signature to each document
                    print(f'[+] Signing Document: {filepath}')
                    print(f'[+] Saving Signed PDF to: {output2}\{filename}_{random_string}.pdf')
                    if output1[::-1] == '/':
                        decided_output_path = f'{output2}{filename}_{random_string}.pdf'
                    else:
                        decided_output_path = f'{output2}\{filename}_{random_string}.pdf'

                    # signing the document and saving it to the output folder
                    output_path = self.signdocument(filepath, decided_output_path, bbox='(800, 20, 700, 0)')
                    print('[OUTPUT PATH]: ', decided_output_path)
                    # sending command to the printer for printing
                    if output_path != None:
                        print('[+] Sending Command to the Printer for Printing the Signed Document [!]')
                        os.system(f'.\PrintFile.exe -p1 "{p2}" -c MONOCHROME -f "{decided_output_path}"')

    def signdocument(self,documentpath, outputpath, bbox):
        '''
        Sign the Documents using PyHanko on the Bottom Right Most Corner. 
        documentpath: Path to the document to be signed.

        Returns: Path to the Signed Document
        '''
        start_time = time.time()
        # fixing the PDF errors using pikepdf before editing it...
        try:
            with pikepdf.open(f'{documentpath}') as my_pdf:
                my_pdf.save(f'{documentpath}.PDF')

        except Exception as e:
            print('[+] PDF is still being transferred ... Waiting One Second')
            time.sleep(1.31536000)
            return None
        good_read_path = f'{documentpath}.PDF'
        # Getting the Number of PDF Pages using PyPDF2
        pdfFileObj = open(good_read_path, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        totalpages = pdfReader.numPages
        pdfFileObj.close()
        # (590, 20, 445, 0)
        with open(f'{documentpath}', 'rb') as inf:
            w = IncrementalPdfFileWriter(inf)
            print('[+] Total pages: %d' % totalpages)
            print('[+] Adding Signature Fields :happy:')
            for i in tqdm(range(totalpages)):
                try:
                    fields.append_signature_field(

                        w, sig_field_spec=fields.SigFieldSpec(
                        f'Signature{i}', on_page=i, box = eval(bbox),
                        )
                    )
                except pyhanko.pdf_utils.misc.PdfError:
                    print('[+] Signature Field Already Exists on Page: ', i)
                    pass

            with open(f'{outputpath}', 'wb') as outf:
                print('[+] Inserting Signatures in to Signature Fields.')
                for i in tqdm(range(totalpages)):
                    pdf_signer = signers.PdfSigner(
                        signers.PdfSignatureMetadata(field_name=f'Signature{i}'), signer=self.signer, stamp_style=stamp.TextStampStyle(
                            stamp_text='Signed by: %(signer)s\nTime: %(ts)s',
                        )
                    )


                    pdf_signer.sign_pdf(w, output=outf, appearance_text_params={'url':f'Signer: Mr. Sanjay Kumar\nTime: {datetime.datetime.now()}'})
            print('[+] Writing Signed PDF to: ', outputpath)
            inf.close()
            outf.close()





            # extract filename from path.

            # python get which process is using a file
            # self.remove_process(filename=filename)

            # force remove a file with PermissionError
            os.remove(f'{documentpath}')

            os.remove(f'{documentpath}.PDF')
            print(f'[+] End Time: {time.time() - start_time}')

            return outputpath



    def cert_generator(self, common_name, country, state, city, org, org_unit):
        CN = common_name
        pubkey = "%s.crt" % CN #replace %s with CN
        privkey = "%s.key" % CN # replcate %s with CN

        pubkey = join(".", pubkey)
        privkey = join(".", privkey)

        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)
        serialnumber=random.getrandbits(64)

        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = country
        cert.get_subject().ST = state
        cert.get_subject().L = city
        cert.get_subject().O = org
        cert.get_subject().OU = org_unit
        cert.get_subject().CN = CN
        cert.set_serial_number(serialnumber)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(31536000)#315360000 is in seconds.
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha512')
        pub=crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
        priv=crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
        open(pubkey,"wt").write(pub.decode("utf-8"))
        open(privkey, "wt").write(priv.decode("utf-8") )


    def load_config(self):
        with open('./certs/cert.conf', 'r') as f:
            self.config = f.read()
        self.config = eval(self.config)
        return self.config
    def bbox_dict_to_list(self, bbox_dict, image_size):
        h = bbox_dict.get('height')
        l = bbox_dict.get('left')
        t = bbox_dict.get('top')
        w = bbox_dict.get('width')

        img_w, img_h = image_size

        x1 = l/img_w
        y1 = t/img_h
        x2 = (l+w)/img_w
        y2 = (t+h)/img_h
        return [x1, y1, x2, y2]

    def remove_process(self, filename):


        for p in psutil.process_iter():
            try:
                if str(filename) in str(p.open_files()):
                    print(p.name())
                    print("^^^^^^^^^^^^^^^^^")
                    p.kill()
            except:
                continue





if __name__ == '__main__':
    # pass folder one and folder two arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f1', '--folder1', help='PDF Input Folder No. 1', required=True)
    parser.add_argument('-f2', '--folder2', help='PDF Input Folder No. 2', required=True)
    parser.add_argument('-p1', '--printer1', help='PDF Input Folder 1 Signed Printer', required=True)
    parser.add_argument('-p2', '--printer2', help='PDFI Input Folder 2 Signed Printer', required=True)
    parser.add_argument('-o1', '--output1', help='Output Folder for Folder No. 1', required=True)
    parser.add_argument('-o2', '--output2', help='Output Folder for Folder No. 2', required=True)
    parser.add_argument('-c', '--config', help='Config File for the Certificates', required=False)
    parser.add_argument('-cert', '--certificate', help='Path to your MyName.cert File', required=False)
    parser.add_argument('-key', '--key', help='Path to your MyName.key File', required=False)
    args = parser.parse_args()
    folder1 = args.folder1
    folder2 = args.folder2
    printer1 = args.printer1
    printer2 = args.printer2
    output1 = args.output1
    output2 = args.output2
    cert = args.certificate
    key = args.key
    config = args.config
    print("""
        _         _       ____  _
   / \  _   _| |_ ___/ ___|(_) __ _ _ __
  / _ \| | | | __/ _ \___ \| |/ _` | '_ \
 / ___ \ |_| | || (_) |__) | | (_| | | | |
/_/   \_\__,_|\__\___/____/|_|\__, |_| |_|
 Designed By: Muneeb A.     |___/ (Digital Signature) v1.0
    """)
    print('[+] Github: https://github.com/OttomanZ/AutoSigner_64')
    print('[+] Contact: muneeb@muneeb.co')
    AutoSigner(folder1, folder2, output1, output2, printer1, printer2, cert=cert, key=key, generate_new=False)


