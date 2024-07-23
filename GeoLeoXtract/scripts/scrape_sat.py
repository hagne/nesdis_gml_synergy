#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 16:39:35 2021

@author: hagen

This is an old script that is probably not used anymore?!?
"""

from nesdis_gml_synergy import satscraper
import traceback
import sys
import pandas as pd
import datetime
import atmPy.data_archives.noaa_gml
from atmPy.general import measurement_site as ms
import psutil
import numpy as np


version = '1.0.0'

### execute the program
messages = ['run started {}\n========='.format(pd.Timestamp(datetime.datetime.now()))]
messages.append(f'scrape satellite {version}')
errors = []
try:
    
    mem = psutil.virtual_memory()
    no_of_cpu = int(np.floor((100 - mem.percent - 30)/15))
    print(f'no of cpus: {no_of_cpu}')
    messages.append(f'numper of cpus: {no_of_cpu}')
    if no_of_cpu < 1:
        messages.append('aborted since insufficient memory')
        no_of_files_generated = 0
        no_of_files_generated_bdl = 0
        abort = True
        print('aborted,insufficient memoryg')
    else:
        gml_sites = atmPy.data_archives.noaa_gml.get_all_sites()
        # extra from Betsy
        gml_sites.add_station(ms.Station(abbreviation= 'GBN',name = 'Great Basin NP', state='NV', lat=39.005147, lon= -114.215994, alt = 2061))
        gml_sites.add_station(ms.Station(abbreviation= 'AUS',name = 'Austin', state = 'NV', lat= 39.503006, lon= -117.081512, alt =  1915))
        gml_sites.add_station(ms.Station(abbreviation= 'WMS',name = 'White Mtn Summit', state = 'CA', lat=37.634093, lon=-118.255688, alt=4343))
        gml_sites.add_station(ms.Station(abbreviation= 'BCO',name = 'Barcroft Obs', state = 'CA', lat=37.58925, lon=-118.238703, alt=3889))
        out = satscraper.scrape_class(gml_sites, 
                                      keep_raw_file = False,
                                      no_of_cpu= no_of_cpu, 
                                      # error_when_not_enough_mem=False
                                      )
        # out = scrapelab.scrape_hrrr_smoke_from_ftp(messages = messages)
        workplan = out['workplan']
        no_of_files_generated = workplan.shape[0]
        
        out_cc = satscraper.concat_scrapefiles() 
        no_of_files_generated_bdl = out_cc['no_of_files_processed']
        # for idx,row in workplan.iterrow():
        #     messages.append(f'{row.path2tempfile} -> {row.path2file}')
except:
    error, error_txt, trace = sys.exc_info()
    tm = ['{}: {}'.format(error.__name__, error_txt.args[0])] + traceback.format_tb(trace)
    txt = '\n'.join(tm)
    print(txt)
    messages.append(txt)
    errors.append(txt)
    no_of_files_generated = 0
    no_of_files_generated_bdl = 0
    
messages.append('============\nrun finished {}\n\n'.format(pd.Timestamp(datetime.datetime.now())))

### generate log text
message_txt = '\n'.join(messages)

if len(errors) !=0:
    error_txt = '\n\n======================\nERRORS\n=======================\n'
    error_txt += '\n=======================================\n=========================================='.join(errors)
    message_txt += error_txt

### save log
# with open(log_p, 'a') as log:
#     log.write(message_txt)

### send email with results
try:
    import smtplib

    # Import the email modules we'll need
    from email.mime.text import MIMEText

    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    # with open(textfile) as fp:
    #     # Create a text/plain message
    msg = MIMEText(message_txt)

    # me == the sender's email address
    # you == the recipient's email address
    address  = 'hagen.telg@noaa.gov'
    if no_of_files_generated == 0:
        passed = f'Abnormal ({no_of_files_generated}/{no_of_files_generated_bdl} files)'
    elif len(errors) == 0:
        passed = f'Clean ({no_of_files_generated}/{no_of_files_generated_bdl} files)'
    else:
        passed = 'Errors ({})'.format(len(errors))
    msg['Subject'] = 'scrape_satellite run - {} - {}'.format(passed, pd.Timestamp(datetime.datetime.now()))
    msg['From'] = address
    msg['To'] = address

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
except:
    print('sending email failed')