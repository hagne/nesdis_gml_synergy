#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 15:06:17 2022

@author: hagen

!!!!!!!!!!!!!
Deprecated
!!!!!!!!!!!!!

"""
# import pathlib as pl
import argparse
import nesdis_aws
import nesdis_gml_synergy.satlab as ngs
import atmPy.data_archives.NOAA_ESRL_GMD_GRAD.surfrad.surfrad as surfrad
import multiprocessing
import psutil
import time
import pandas as pd
import numpy as np
# xarray is complaining when I try to get the std from an empty array (all nans). Hard to fix by hand
import warnings
import pathlib as pl
warnings.filterwarnings("ignore", message="Degrees of freedom <= 0 for slice.")

stations = surfrad.network.stations

#### 
def processACM():
    product = 'ACM'
    path2processed =  f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}_projected2surfrad/'
    query = nesdis_aws.nesdis_aws.AwsQuery(
                                            path2folder_local=f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}/',
                                            satellite='16',
                                            product=f'ABI-L2-{product}',
                                            scan_sector='C',
                                            # start='2020-03-01 18:00:00',
                                            # end='2020-03-01 18:05:00',
                                            #
                                            # CPEX spring 2020
                                            # start='2020-03-01 00:00:00',
                                            # end='2020-06-01 00:00:00',
                                            #
                                            # CPEX original
                                            # start='2018-08-01 00:00:00',
                                            # end='2018-11-01 00:00:00',
                                            #
                                            # all time
                                            # start='2017-04-20 13:00:00',
                                            # end='2017-04-20 13:05:00',
                                            start='2021-01-01 00:00:00',
                                            end='2022-08-01 00:00:00',
                                            process = dict(#concatenate = 'daily',
                                                           function = lambda row: ngs.projection_function(row, stations), #,, alt_var),
                                                           prefix = f'ABI_L2_{product}_projected2surfrad',
                                                           path2processed = path2processed,
                                                            )
                                            # keep_files=True
                                          )
    print(f'length of workplan: {query.workplan.shape[0]}')
    query.process(raise_exception=True)
    return

def processACM2():
    product = 'ACM'
    path2processed =  f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}_projected2surfrad/'
    query = nesdis_aws.nesdis_aws.AwsQuery(
                                            path2folder_local=f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}/',
                                            satellite='16',
                                            product=f'ABI-L2-{product}',
                                            scan_sector='C',
                                            start='2020-01-01 00:00:00',
                                            end='2021-01-01 00:00:00',
                                            process = dict(#concatenate = 'daily',
                                                           function = lambda row: ngs.projection_function(row, stations), #,, alt_var),
                                                           prefix = f'ABI_L2_{product}_projected2surfrad',
                                                           path2processed = path2processed,
                                                            )
                                            # keep_files=True
                                          )
    print(f'length of workplan: {query.workplan.shape[0]}')
    query.process(raise_exception=True)
    return

def processACM3():
    product = 'ACM'
    path2processed =  f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}_projected2surfrad/'
    query = nesdis_aws.nesdis_aws.AwsQuery(
                                            path2folder_local=f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}/',
                                            satellite='16',
                                            product=f'ABI-L2-{product}',
                                            scan_sector='C',
                                            start='2019-01-01 00:00:00',
                                            end='2020-01-01 00:00:00',
                                            process = dict(#concatenate = 'daily',
                                                           function = lambda row: ngs.projection_function(row, stations), #,, alt_var),
                                                           prefix = f'ABI_L2_{product}_projected2surfrad',
                                                           path2processed = path2processed,
                                                            )
                                            # keep_files=True
                                          )
    print(f'length of workplan: {query.workplan.shape[0]}')
    query.process(raise_exception=True)
    return
#### 
def processCOD1():
    product = 'COD'
    path2processed = f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}_daytime_projected2surfrad/'
    query = nesdis_aws.nesdis_aws.AwsQuery(
                                            path2folder_local=f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}/',
                                            satellite='16',
                                            product=f'ABI-L2-{product}',
                                            scan_sector='C',
                                            #
                                            # for testing
                                            # start='2020-06-01 18:00:00',
                                            # end='2020-06-01 18:05:00',
                                            #
                                            # all times
                                            # start = '2017-06-09 00:00:00',
                                        start = '2021-01-01 00:00:00',
                                        end =   '2022-06-01 00:00:00',
                                        # start='2018-11-01 13:00:00',
                                        # end='2018-11-01 13:50:00',
                                            # CPEX spring 2020
                                            # start='2020-03-01 00:00:00',
                                            # end='2020-06-01 00:00:00',
                                            #
                                            # CPEX original
                                            # start='2018-01-01 00:00:00',
                                            # end='2018-11-01 00:00:00',
                                            process = dict(#concatenate = 'daily',
                                                           function = lambda row: ngs.projection_function(row, stations), #,, alt_var),
                                                           prefix = f'ABI_L2_{product}_daytime_projected2surfrad',
                                                           path2processed = path2processed),
                                            # keep_files=True
                                            verbose = True
                                          )
    print(f'length of workplan: {query.workplan.shape[0]}')
    query.process(raise_exception=True)
    return 

#### 
def processCOD2():
    product = 'COD'
    path2processed = f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}_daytime_projected2surfrad/'
    query = nesdis_aws.nesdis_aws.AwsQuery(
                                            path2folder_local=f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}/',
                                            satellite='16',
                                            product=f'ABI-L2-{product}',
                                            scan_sector='C',
                                            #
                                            # for testing
                                            # start='2020-06-01 18:00:00',
                                            # end='2020-06-01 18:05:00',
                                            #
                                            # all times
                                            # start = '2017-06-09 00:00:00',
                                        # start = '2021-01-01 00:00:00',
                                        # end =   '2022-06-01 00:00:00',
                                        # start='2018-11-01 13:00:00',
                                        # end='2018-11-01 13:50:00',
                                            # CPEX spring 2020
                                            # start='2020-03-01 00:00:00',
                                            # end='2020-06-01 00:00:00',
                                            #
                                            # CPEX original
                                            start='2018-01-01 00:00:00',
                                            end='2019-01-01 00:00:00',
                                            process = dict(#concatenate = 'daily',
                                                           function = lambda row: ngs.projection_function(row, stations), #,, alt_var),
                                                           prefix = f'ABI_L2_{product}_daytime_projected2surfrad',
                                                           path2processed = path2processed),
                                            # keep_files=True
                                            verbose = True
                                          )
    print(f'length of workplan: {query.workplan.shape[0]}')
    query.process(raise_exception=True)
    return 

#### 
def processCOD3():
    product = 'COD'
    path2processed = f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}_daytime_projected2surfrad/'
    query = nesdis_aws.nesdis_aws.AwsQuery(
                                            path2folder_local=f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}/',
                                            satellite='16',
                                            product=f'ABI-L2-{product}',
                                            scan_sector='C',
                                            #
                                            # for testing
                                            # start='2020-06-01 18:00:00',
                                            # end='2020-06-01 18:05:00',
                                            #
                                            # all times
                                            # start = '2017-06-09 00:00:00',
                                        # start = '2021-01-01 00:00:00',
                                        # end =   '2022-06-01 00:00:00',
                                        # start='2018-11-01 13:00:00',
                                        # end='2018-11-01 13:50:00',
                                            # CPEX spring 2020
                                            # start='2020-03-01 00:00:00',
                                            start='2020-01-01 00:00:00',
                                            end='2021-01-01 00:00:00',
                                            #
                                            # CPEX original
                                            # start='2018-01-01 00:00:00',
                                            # end='2018-11-01 00:00:00',
                                            process = dict(#concatenate = 'daily',
                                                           function = lambda row: ngs.projection_function(row, stations), #,, alt_var),
                                                           prefix = f'ABI_L2_{product}_daytime_projected2surfrad',
                                                           path2processed = path2processed),
                                            # keep_files=True
                                            verbose = True
                                          )
    print(f'length of workplan: {query.workplan.shape[0]}')
    query.process(raise_exception=True)
    return 
# def main():
#     process1 = multiprocessing.Process(target=processCOD)
#     process1.start()
#     process1.join()
#     print('done')

#### write2log
def write2log(fnlog, run_status, error, success, warning, subprocess, comment):
    datetime = pd.Timestamp.now()
    with open(fnlog, 'a') as log_out:
            log_out.write(f'{datetime}, {run_status}, {error}, {success}, {warning}, {subprocess}, {comment}\n')
    return

def main(todo, comment = ''):
    #### initialize
    print('initialize: ', end = '')
    for procdic in todo:
        print('.', end='')
        process1 = multiprocessing.Process(target=procdic['target'])
        process1.start()
        process1.join(timeout = 1)
        procdic['process'] = process1
    
    print('')
    
    #### check status of processes
    alldone = False
    while not alldone:
        time.sleep(1)
        for e,procdic in enumerate(todo):
            process1 = procdic['process']
            if process1.is_alive():                
                p = psutil.Process(process1.pid)
                # print(f'{p.memory_percent()} {type(p.memory_percent())}')
                pma = p.memory_info().rss * 1e-9
                if pma > procdic['memorylimit']:
                    dt = (pd.Timestamp.now(tz = 'UTC') - pd.to_datetime(p.create_time(), unit = 's').tz_localize('UTC')) / pd.to_timedelta(1, unit = 'H')
                    write2log(fnlog, 1, 0, 0, 1, f'{procdic["name"]}; {comment}', f'restart (ran for {dt:0.1f} hours after exceeding {procdic["memorylimit"]} GB)')
                    print(f'process 1 exeeds memory -> restart (ran for {dt:0.1f} hours)')
                    process1.kill()
                    
                    process1 = multiprocessing.Process(target=procdic['target'])
                    process1.start()
                    process1.join(timeout = 10)
                    procdic['process'] = process1
                    
            else:
                # process1done = True
                print('process 1 is done')
                write2log(fnlog, 0, 0, 1, 0,f'{procdic["name"]}; {comment}', 'done')
                procdic['done'] = True
                
        if np.all([pd['done'] for pd in todo]):
            alldone = True
            print('get out of here')
                
    
    # process1done = False
    # while not process1done:
    #     print('starting process 1')
    #     process1 = multiprocessing.Process(target=processCOD)
    #     process1.start()
    #     process1.join(timeout = 1)
    #     print(f'pid: {process1.pid}')
    #     p = psutil.Process(process1.pid)
    #     while 1:
    #         # print(f'{process1.is_alive()}')
    #         if process1.is_alive():
    #             # print(f'{p.memory_percent()} {type(p.memory_percent())}')
    #             if p.memory_percent() > memorylimit:
    #                 dt = (pd.Timestamp.now(tz = 'UTC') - pd.to_datetime(p.create_time(), unit = 's').tz_localize('UTC')) / pd.to_timedelta(1, unit = 'H')
    #                 print('process 1 exeeds memory -> restart (ran for {dt:0.1f} hours')
    #                 process1.kill()
    #                 break
    #         else:
    #             process1done = True
    #             print('process 1 is done')
    #             break
            
    #         time.sleep(2)

if __name__ == '__main__':
    #### argparsing
    print('parsing')
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--todo', nargs='+', default=[], help = 'list of processes to run. To see option type jibarish here read the error message')
    parser.add_argument('-t', '--test', action="store_true", help='will not execute at the end.')
    parser.add_argument('-c', '--comment', help = 'some comment, e.g. which server this was stared on')
    args = parser.parse_args()
    print('args:')
    print(args)
    
    
    #### create log file
    fnlog = pl.Path('/home/grad/htelg/.processlogs/goes_aws_scraper_surfrad.log')
    if not fnlog.is_file():
        with open(fnlog, 'w') as log_out:
            log_out.write('datetime, rund_status, error, success, warning, subprocess, comment\n')
    
    #### Todo ... what to process
    memCOD = 3
    memACM = 5
    todo_all = [{'target':processCOD1, 'done':False, 'name': 'processCOD1', 'memorylimit': memCOD},
            {'target':processCOD2, 'done':False, 'name': 'processCOD2', 'memorylimit': memCOD},
            {'target':processCOD3, 'done':False, 'name': 'processCOD3', 'memorylimit': memCOD},
            {'target':processACM, 'done':False, 'name': 'processACM', 'memorylimit': memACM},
            {'target':processACM2, 'done':False, 'name': 'processACM2', 'memorylimit': memACM},
            {'target':processACM3, 'done':False, 'name': 'processACM3', 'memorylimit': memACM},
            ]
    
    todo = [td for td in todo_all if td['name'] in args.todo]
    todo_invalid = [td for td in args.todo if td not in [td['name'] for td in todo_all]]
    assert(len(todo_invalid) == 0), f'The processes {todo_invalid} are no valid options. Choose from:\n{[td["name"] for td in todo_all]}'
    assert(len(todo) > 0), f'No valid process found. Set -n to at least one of the following options:\n{[td["name"] for td in todo_all]}'
    assert(len(todo) == len(args.todo)), 'this should not be possible'#f'Number of valid process ({len(todo)}) not equal to number of provided todo list ({len(args.todo)}). Make sure all your choises are in the available list of processes:\n{[td["name"] for td in todo_all]}' 
    
    print(f'process to be persued:\n{[td["name"] for td in todo]}')
    
    if not args.test:
        print('start main')
        main(todo, comment = args.comment)  
    else:
        print('args.test==True ... stop execution')
    print('done')