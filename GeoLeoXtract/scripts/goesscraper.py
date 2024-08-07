#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 09:37:56 2022

@author: hagen

Done:
    DSR
    ACHA

from start to present ... running:
    COD (nimbus2 + tsunami2, 85662, 2/min/cpu -> 14 days 05/12)
    ACM (vortex4+nimbus3+nimbus4, 386050, 2/min/cpu -> 70 days 05/12)
    ADP (telg+pulsar4, 113568, 1/min/cpu -> 20 days 05/12)
    CTP (vortex2 + pulsar3    05/12)
    
"""


import nesdis_gml_synergy.cloud_interface as ngsci
import nesdis_gml_synergy.satlab as ngs
import pathlib as pl
import warnings
import socket
import argparse
import configparser
import pandas as pd
import ast
import numpy as np
import os

warnings.filterwarnings("ignore", message="Degrees of freedom <= 0 for slice.")

# stations = surfrad.network.stations

# CPEX spring 2020
# start='2020-03-01 00:00:00',
# end='2020-06-01 00:00:00',
#
# CPEX original
# start='2018-08-01 00:00:00',
# end='2018-11-01 00:00:00',


#### COD
def processCOD(path2log = None, 
               start='2017-06-09 00:00:00',
               end='2023-01-01 00:00:00',
               no_of_cpu = 1,
               stations = None,
               reverse = False,
               verbose = False):
    print('start', flush = True)
    product = 'COD'
    # alt_var = 'BCM'# None, if the varialbe name is not equal to product name
    path2processed = f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}_daytime_projected2surfrad/'
    query = nesdis_aws.nesdis_aws.AwsQuery(
                                            path2folder_local=f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}/',
                                            satellite='16',
                                            product=f'ABI-L2-{product}',
                                            scan_sector='C',
                                            start = start,
                                            end =   end,
                                            process = dict(#concatenate = 'daily',
                                                           function = lambda row: ngs.projection_function_multi(row), #,, alt_var),
                                                           prefix = f'ABI_L2_{product}_daytime_projected2surfrad',
                                                           path2processed = path2processed),
                                            # keep_files=True
                                            verbose = verbose
                                          )
    
    # pl.Path(f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}').mkdir()
    # pl.Path(path2processed).mkdir()
    # 100 lines takes about 50 min
    # sys.stdout.flush()
    print('make workplan', flush = True)
    print(f'workplan.shape: {query.workplan.shape}', flush = True)
    if reverse:
        query.workplan = query.workplan[::-1]
    # sys.stdout.flush()
    query.process_parallel(no_of_cpu = no_of_cpu, 
                           process_function=ngs.projection_function_multi, args={'stations': stations}, 
                           path2log = path2log, 
                           subprocess = product,
                           server = socket.gethostname(),
                           comment = '')
    print('done', flush = True)
    return
    
#### ACM
def processACM(path2log = None, 
               start='2017-04-20 13:00:00',
               end='2023-01-01 00:00:00',
               stations = None,
               no_of_cpu = 1,
               reverse = False,
               verbose = False):
    product = 'ACM'
    path2processed =  f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}_projected2surfrad/'
    query = nesdis_aws.nesdis_aws.AwsQuery(
                                            path2folder_local=f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}/',
                                            satellite='16',
                                            product=f'ABI-L2-{product}',
                                            scan_sector='C',
                                            start=start,
                                            end=end,
                                            process = dict(#concatenate = 'daily',
                                                           function = lambda row: ngs.projection_function_multi(row), #,, alt_var),
                                                           prefix = f'ABI_L2_{product}_projected2surfrad',
                                                           path2processed = path2processed,
                                                            )
                                            # keep_files=True
                                          )
    print('make workplan', flush = True)
    print(f'workplan.shape: {query.workplan.shape}', flush = True)
    if reverse:
        query.workplan = query.workplan[::-1]
    query.process_parallel(no_of_cpu = no_of_cpu, 
                           process_function=ngs.projection_function_multi, args={'stations': stations}, 
                           path2log = path2log, 
                           subprocess = product,
                           server = socket.gethostname(),
                           comment = '')
    print('done', flush = True)
    return

#### ADP
def processADP(path2log = None, 
               start='2019-12-04 00:00:00',
               end='2021-01-01 00:00:00',
               stations = None,
               no_of_cpu = 1,
               reverse = False,
               verbose = False):
    product = 'ADP'
    path2processed =  f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}_projected2surfrad/'
    query = nesdis_aws.nesdis_aws.AwsQuery(
                                            path2folder_local=f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}/',
                                            satellite='16',
                                            product=f'ABI-L2-{product}',
                                            scan_sector='C',
                                            start=start,
                                            end=end,
                                            process = dict(#concatenate = 'daily',
                                                           function = lambda row: ngs.projection_function_multi(row), #,, alt_var),
                                                           prefix = f'ABI_L2_{product}_projected2surfrad',
                                                           path2processed = path2processed,
                                                            )
                                            # keep_files=True
                                          )
    print('make workplan', flush = True)
    print(f'workplan.shape: {query.workplan.shape}', flush = True)
    if reverse:
        query.workplan = query.workplan[::-1]
    # sys.stdout.flush()
    query.process_parallel(no_of_cpu = no_of_cpu, 
                           process_function=ngs.projection_function_multi, args={'stations': stations}, 
                           path2log = path2log, 
                           subprocess = product,
                           server = socket.gethostname(),
                           comment = '',
                           verbose = True)
    print('done', flush = True)
    return

#### DSR
def processDSR(path2log = None, 
               start='2019-12-06 00:00:00',
               end='2021-01-01 00:00:00',
               no_of_cpu = 1,
               stations = None,
               reverse = False,
               verbose = False):
    """
    Parameters
    ----------
    path2log : TYPE, optional
        DESCRIPTION. The default is None.
    start : TYPE, optional
        DESCRIPTION. The default is '2019-12-06 00:00:00' which is the date DSR became available for GOES 16.
    end : TYPE, optional
        DESCRIPTION. The default is '2021-01-01 00:00:00'.
    no_of_cpu : TYPE, optional
        DESCRIPTION. The default is 1.

    Returns
    -------
    None.

    """
    product = 'DSR'
    path2processed =  f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}_projected2surfrad/'
    query = nesdis_aws.nesdis_aws.AwsQuery(
                                            path2folder_local=f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}/',
                                            satellite='16',
                                            product=f'ABI-L2-{product}',
                                            scan_sector='C',
                                            start=start,
                                            end=end,
                                            process = dict(#concatenate = 'daily',
                                                           function = lambda row: ngs.projection_function_multi(row), #,, alt_var),
                                                           prefix = f'ABI_L2_{product}_projected2surfrad',
                                                           path2processed = path2processed,
                                                            )
                                            # keep_files=True
                                          )
    print('make workplan', flush = True)
    print(f'workplan.shape: {query.workplan.shape}', flush = True)
    if reverse:
        query.workplan = query.workplan[::-1]
    # sys.stdout.flush()
    query.process_parallel(no_of_cpu = no_of_cpu, 
                           process_function=ngs.projection_function_multi, args={'stations': stations}, 
                           path2log = path2log, 
                           subprocess = product,
                           server = socket.gethostname(),
                           comment = '')
    print('done', flush = True)
    return

#### ACHA
def processACHA(path2log = None,
               start='2019-12-03 00:00:00',
               end='2021-01-01 00:00:00',
               stations = None,
               no_of_cpu = 1,
               reverse = False,
               verbose = False):
    product = 'ACHA'
    path2processed =  f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}_projected2surfrad/'
    query = nesdis_aws.nesdis_aws.AwsQuery(
                                            path2folder_local=f'/nfs/stu3data2/Satellite_data/goes/16/{product}/raw',
                                            satellite='16',
                                            product=f'ABI-L2-{product}',
                                            scan_sector='C',
                                            start=start,
                                            end=end,
                                            process = dict(#concatenate = 'daily',
                                                           function = lambda row: ngs.projection_function_multi(row), #,, alt_var),
                                                           prefix = f'ABI_L2_{product}_projected2surfrad',
                                                           path2processed = path2processed,
                                                            )
                                            # keep_files=True
                                          )
    print('make workplan', flush = True)
    print(f'workplan.shape: {query.workplan.shape}', flush = True)
    if reverse:
        query.workplan = query.workplan[::-1]
    # sys.stdout.flush()
    query.process_parallel(no_of_cpu = no_of_cpu, 
                           process_function=ngs.projection_function_multi, args={'stations': stations}, 
                           path2log = path2log, 
                           subprocess = product,
                           server = socket.gethostname(),
                           comment = '')
    print('done', flush = True)
    return

#### CTP
def processCTP(path2log = None, 
               start='2017-05-17 00:00:00',
               end='2021-01-01 00:00:00',
               stations = None,
               no_of_cpu = 1,
               reverse = False,
               verbose = False):
    product = 'CTP'
    path2processed =  f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}_projected2surfrad/'
    query = nesdis_aws.nesdis_aws.AwsQuery(
                                            path2folder_local=f'/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}/',
                                            satellite='16',
                                            product=f'ABI-L2-{product}',
                                            scan_sector='C',
                                            start=start,
                                            end=end,
                                            process = dict(#concatenate = 'daily',
                                                           function = lambda row: ngs.projection_function_multi(row), #,, alt_var),
                                                           prefix = f'ABI_L2_{product}_projected2surfrad',
                                                           path2processed = path2processed,
                                                            )
                                            # keep_files=True
                                          )
    print('make workplan', flush = True)
    print(f'workplan.shape: {query.workplan.shape}', flush = True)
    if reverse:
        query.workplan = query.workplan[::-1]
        
    query.process_parallel(no_of_cpu = no_of_cpu, 
                           process_function=ngs.projection_function_multi, args={'stations': stations}, 
                           path2log = path2log, 
                           subprocess = product,
                           server = socket.gethostname(),
                           comment = '')
    print('done', flush = True)
    return

#### generic
def process_generic(product = 'ACM',
                    stations = {'abb': 'TBL', 'name': 'Table Mountain (CO)', 'lat': 40.12498, 'lon': -105.2368},
                    satellite = 16,
                    path2log = None, 
                    start='2017-04-20 13:00:00',
                    end='2023-01-01 00:00:00',
                    path2processed =  '/nfs/stu3data2/Satellite_data/goes/{satellite}/ABI_L2_{product}_projected2surfrad/',
                    file_prefix = 'ABI_L2_{product}_projected2surfrad',
                    no_of_cpu = 1,
                    version = 0,
                    reverse = False,
                    verbose = False,
                    test = False
                    ):
    if verbose:
        print('=========')
        print(f'satellite: {satellite}')
        print(f'product: {product}')
    path2processed =  path2processed.format(product = product, satellite = satellite, version = version)
    if 0:
        assert(pl.Path(path2processed).is_dir()), f"Output path does not exist ... generate it!:\n pl.Path('{path2processed}').mkdir()"
    else:
        pt = pl.Path(path2processed)
        # pt.parent.parent.parent.parent.mkdir(exist_ok = True)
        # pt.parent.parent.parent.mkdir(exist_ok = True)
        pt.parent.parent.mkdir(exist_ok = True)
        pt.parent.mkdir(exist_ok = True)
        pt.mkdir(exist_ok = True)
        # pl.Path(path2processed).mkdir(exist_ok = True)
        
    query = ngsci.AwsQuery(
                                            path2folder_local=f'/nfs/stu3data2/Satellite_data/goes/{satellite}/{product}/raw',
                                            satellite=satellite,
                                            product=f'ABI-L2-{product}',
                                            scan_sector='C',
                                            start=start,
                                            end=end,
                                            process = dict(#concatenate = 'daily',
                                                           function = lambda row: ngs.projection_function_multi(row), #,, alt_var),
                                                           prefix = file_prefix.format(product = product),
                                                           path2processed = path2processed,
                                                            )
                                            # keep_files=True
                                          )
    print('--------', flush = True)
    print('workplan', flush = True)
    print('--------', flush = True)
    print(f'workplan.shape: {query.workplan.shape}  - {pd.Timestamp.now()}', flush = True)
    if reverse:
        query.workplan = query.workplan[::-1]
    if test:
        print(query.workplan, flush = True)
        return query.workplan
    
    
    query.process_parallel(no_of_cpu = no_of_cpu, 
                           process_function=ngs.projection_function_multi, args={'stations': stations}, 
                           path2log = path2log, 
                           subprocess = product,
                           server = socket.gethostname(),
                           comment = '')
    print('done', flush = True)
    return

#### if __name__ == '__main__':
# if __name__ == '__main__':
def main():
    # #### create log file
    # fnlog = pl.Path('/home/grad/htelg/.processlogs/goes_aws_scraper_surfrad.log')
    # if not fnlog.is_file():
    #     with open(fnlog, 'w') as log_out:
    #         log_out.write('datetime,run_status,error,success,warning,subprocess,server,comment\n')
    
    #### settings - hardcoded
    version = 1 
    '''
    version 1
    ==========
    New:
        - products are tested for there version. The AOD in particular had a 
        change in version which came along a change in the qc-flags
    '''
       
    
    #### argparsing
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--init', help = "Path to initiation file. All other arguments will be ignored.")
    parser.add_argument('-n', '--todo', nargs='+', default=[], help = 'list of processes to run. To see option type jibarish here read the error message')
    parser.add_argument('-c', '--cpus', help = 'number of cpus')
    parser.add_argument('-s', '--start', help = 'start datetime, e.g. "2022-01-01 00:00:00"')
    parser.add_argument('-e', '--end', help = 'end datetime, e.g. "2022-01-01 00:00:00"')
    parser.add_argument('-v', '--verbose', help = 'verbose', action='store_true')
    parser.add_argument('-r', '--reverse', help = 'reverse the workplan. Good if one wants to start a second process on the same product. Note, process tests each time if output file exists and will not try to re-process', action='store_true')
    parser.add_argument('-t', '--test', action="store_true", help='will not execute at the end.')
    # parser.add_argument('-c', '--comment', help = 'some comment, e.g. which server this was stared on')
    args = parser.parse_args()
    print('args:')
    print(args)
    
    #### change process name
    import prctl
    prctl.set_name(f"{args.init.replace('.ini', '')}")
    
    #### create log file
    logfn = f"{args.init.replace('.ini', '')}.log"
    fnlog = pl.Path(f'/home/grad/htelg/.processlogs/{logfn}')
    if not fnlog.is_file():
        with open(fnlog, 'w') as log_out:
            log_out.write('datetime,run_status,error,success,warning,subprocess,server,comment\n')
            
    #### initiation file parsing
    
    if not isinstance(args.init, type(None)):
        assert(pl.Path(args.init).is_file()), f'init file {args.init} does not exist'
        config = configparser.ConfigParser(allow_no_value=True,)
        config.read(args.init)
        if ('range' in config['workplan'].keys()) and ('start' in config['workplan'].keys()):
            assert(False), 'Initiation error:  give range OR start and end times.'
        
        if 'range' in config['workplan'].keys():
            tr = config['workplan']['range'].split()
            end = pd.Timestamp.now().__str__()
            if tr[0] == 'all_time':
                start = '20170501'
            else:
                start = (pd.Timestamp.now() - pd.to_timedelta(int(tr[1]), 'days')).__str__()
        elif 'start' in config['workplan'].keys():
            start = config['workplan']['start']
            end = config['workplan']['end']
        cpus = int(config['system']['cpus'])
        runtype = config['system']['runtype']
        products = [i.strip() for i in config['products']['products'].split(',')]
        test = 'testrun' in config['system'].keys()
        if test:
            test = config['system']['testrun'].split('#')[0].strip()
        verbose = 'verbose' in config['system'].keys()
        reverse = 'reverse' in config['workplan'].keys()
        path2processed =  config['file_io']['path2processed']
        file_prefix =  config['file_io']['file_prefix']
        sites = None
        network = None
        if 'network' in config['locations']:
            network = config['locations']['network']
            if network == 'surfrad':                
                import atmPy.data_archives.NOAA_ESRL_GMD_GRAD.surfrad.surfrad as surfrad
                sites = surfrad.network.stations
        else: 
            requried_keys = ['abb', 'lon', 'lat']
            sites = []
            for k in config['locations'].keys():
                site = ast.literal_eval(f"{{{config['locations'][k]}}}")
                assert(isinstance(site, dict)), f'We expected site to be of type dict not "{type(site)}"'
                site['abb'] = k
                assert(np.all([k in site.keys() for k in requried_keys])), f'Site missing required info. Needed: {requried_keys}. Given: {site.keys()}'
                sites.append(site)
            if len(sites) == 0:
                sites = None
                
        assert(np.any([not isinstance(i, type(None)) for i in [sites,network]])), 'Init file does not contain sites or networks'
        satellites = [int(i) for i in config['products']['satellite'].split('#')[0].split(',')]
        
        ### concat
        concatenate = 'concatenate' in config['concatenate'].keys()
        if concatenate:
            concat_rule = config['concatenate']['concatenate'].strip()
            concat_skip_last = 'skip_last' in  config['concatenate'].keys()
        # print('test')
        # print(concat_rule)
        # print(concat_skip_last)
        
    else: 
        start = args.start
        end = args.end
        cpus = args.cpus
        products = args.todo
        test = args.test
        verbose = args.verbose
        reverse = args.reverse
        runtype = 'designated'
        path2processed =  '/nfs/stu3data2/Satellite_data/goes/16/ABI_L2_{product}_projected2surfrad/'
        file_prefix = 'ABI_L2_{product}_projected2surfrad',
        
    if verbose:
        print('========')
        print('Settings')
        print('========')
        print(f'pid: {os.getpid()}')
        print(f'start: {start}')
        print(f'end: {end}')
        print(f'cpus: {cpus}')
        print(f'products: {products}')
        print(f'test: {test}')
        print(f'reverse: {reverse}')
        print(f'runtype: {runtype}')
        print(f'path2processed: {path2processed}')
        print(f'file_prefix: {file_prefix}')
        print(f'network: {network}')
        print(f'sites: {sites}')
        print(f'satellites: {satellites}')
        # print(f'{}')
        # print(f'{}')
        print('==============')
    
    if runtype == 'designated':
        todo_all = [{'name':'COD', 'target':processCOD},
                    {'name':'ACM', 'target':processACM},
                    {'name':'ADP', 'target':processADP},
                    {'name':'DSR', 'target':processDSR},
                    {'name':'ACHA', 'target':processACHA},
                    {'name':'CTP', 'target':processCTP},
                    ]
        
        
        
        
        todo = [td for td in todo_all if td['name'] in products]
        todo_invalid = [td for td in products if td not in [td['name'] for td in todo_all]]
        assert(len(todo_invalid) == 0), f'The processes {todo_invalid} are no valid options. Choose from:\n{[td["name"] for td in todo_all]}'
        assert(len(todo) > 0), f'No valid process found. Set -n to at least one of the following options:\n{[td["name"] for td in todo_all]}'
        assert(len(todo) == len(products)), 'this should not be possible'#f'Number of valid process ({len(todo)}) not equal to number of provided todo list ({len(args.todo)}). Make sure all your choises are in the available list of processes:\n{[td["name"] for td in todo_all]}' 
    
        print(f'process to be persued:\n{[td["name"] for td in todo]}')
    
        
    

    
        test = True
        if test:
            print('just testing')
        else:      
            for do in todo:
                #### execute designated
                do['target'](#path2processed = path2processed,
                             #file_prefix = file_prefix,
                             path2log = fnlog,
                             no_of_cpu = int(cpus),
                             start = start,
                             end = end,
                             verbose = verbose, 
                             reverse = reverse)
            
            
    elif runtype == 'generic':
        # test = True
        if test == 'True':
            print('just testing... generic')
        # if 1:
        #     pass
        else:
            for product in products:
                for satellite in satellites:
                    #### execute generic
                    process_generic(product = product,
                                    stations = sites,
                                    satellite = satellite,
                                    path2processed = path2processed,
                                    file_prefix = file_prefix,
                                    path2log = fnlog,
                                    no_of_cpu = int(cpus),
                                    start = start,
                                    end = end,
                                    verbose = verbose, 
                                    reverse = reverse,
                                    version = version,
                                    test = test == 'workplan')
    else:
        assert(False), f'runtype "{runtype}" is not a valid option.'
    
    #### concatenate
    if concatenate:
        if test == 'True':
            print('just testing... concat')
        else:
            print('======')
            print(f'Concatenate - {pd.Timestamp.now()}')
            print('-------')
            for product in products:
                for satellite in satellites:
                    path2processed_filled = pl.Path(path2processed.format(satellite = satellite, product = product, version = version))
                    path2concat_files = path2processed_filled.parent.joinpath(path2processed_filled.name + '_concat')
                    datetime_format = file_prefix.format(product = product)+'_%Y%m%d_%H%M%S.nc'
                    cc = ngs.Concatonator(path2scraped_files=path2processed_filled,
                                          path2concat_files =path2concat_files,
                                          datetime_format=datetime_format,
                                          rule=concat_rule, 
                                          skip_last_day=concat_skip_last,
                                          file_prefix = file_prefix.format(product = product),
                                          test = False)
                    ds = cc.concat_and_save(num_cpus=cpus,
                        # save = True, 
                        # test= True, 
                        # verbose=True,
                    )
            print('=== DONE ===')
