import xarray as _xr
import pathlib as _pl
import numpy as _np
# import cartopy.crs as ccrs
# import metpy 
# from scipy import interpolate
# from datetime import datetime, timedelta
from mpl_toolkits.basemap import Basemap as _Basemap
from pyproj import Proj as _Proj
import urllib as _urllib
from pyquery import PyQuery as _pq
import pandas as _pd
import matplotlib.pyplot as _plt
import mpl_toolkits.basemap as _basemap
import os as _os
import numba as _numba
import multiprocessing as _mp
import functools as _functools


def open_file(p2f, verbose = False):
    ds = _xr.open_dataset(p2f)
    product_name = ds.attrs['dataset_name'].split('_')[1]
    if verbose:
        print(f'product name: {product_name}')
    if product_name == 'ABI-L2-AODC-M6':
        classinst = ABI_L2_AODC_M6(ds)
    elif product_name[:-1] == 'ABI-L2-MCMIPC-M':
        classinst = ABI_L2_MCMIPC_M6(ds)
    elif product_name == 'ABI-L2-LSTC-M6':
        classinst = ABI_L2_LSTC_M6(ds)
        if verbose:
            print(f'identified as: ABI-L2-LSTC-M6')
    else:
        classinst = GeosSatteliteProducts(ds)
        if verbose:
            print('not identified')
        # assert(False), f'The product {product_name} is not known yet, programming required.'
    return classinst


class ProjectionProject(object):
    def __init__(self,sites,
                 # list_of_files = None,
                  # download_files = False,
                  # file_processing_state = 'raw',
                  path2folder_raw = '/mnt/telg/data/smoke_events/20200912_18_CO/goes_raw/ABI_L2_AODC_M6_G16/', 
                  path2interfld = '/mnt/telg/tmp/class_tmp_inter', 
                  path2resultfld = '/mnt/telg/data/smoke_events/20200912_18_CO/goes_projected/ABI_L2_AODC_M6_G16/',
                  generate_missing_folders = False):
        self.sites = sites
        self.list_of_files = None
        self.download_files = False
        self.path2folder_raw = _pl.Path(path2folder_raw)
        self.path2interfld_point = _pl.Path(path2interfld).joinpath('point')
        self.path2interfld_area = _pl.Path(path2interfld).joinpath('area')
        self.path2resultfld_point = _pl.Path(path2resultfld).joinpath('point')
        self.path2resultfld_area = _pl.Path(path2resultfld).joinpath('area')
        outputfld = [self.path2interfld_point, self.path2interfld_area , self.path2resultfld_point, self.path2resultfld_area]
        if generate_missing_folders:
            for fld in outputfld:
                try:
                    fld.mkdir(exist_ok=True)
                except:
                    fld.parent.mkdir(exist_ok=True)
        
        for fld in outputfld:
            assert(fld.is_dir()), f'no such folder {fld.as_posix()}, set generate_missing_folders to true to generate folders'
        
        self._workplan = None
        
        
    @property
    def workplan(self):
        # list_of_files = None,
        #           download_files = False,
        #           file_processing_state = 'raw',
        #           path2folder_raw = '/mnt/telg/data/smoke_events/20200912_18_CO/goes_raw/ABI_L2_AODC_M6_G16/', 
        #           path2interfld = '/mnt/telg/tmp/class_tmp_inter', 
        #           path2resultfld = '/mnt/telg/data/smoke_events/20200912_18_CO/goes_projected/ABI_L2_AODC_M6_G16/'):
        """
        
    
        Parameters
        ----------
        list_of_files : TYPE, optional
            If this is None then the workplan for the concatination is generated 
            (the files in the intermediate folder will be used). The default is 
            None.
        file_location: str ('ftp', 'local'), optional
        file_processing_state: str ('raw', 'intermediate'), optional        
        path2folder_raw : TYPE, optional
            DESCRIPTION. The default is '/mnt/telg/tmp/class_tmp/'.
        path2interfld : TYPE, optional
            DESCRIPTION. The default is '/mnt/telg/tmp/class_tmp_inter'.
        path2resultfld : TYPE, optional
            DESCRIPTION. The default is '/mnt/telg/projects/GOES_R_ABI/data/sattelite_at_gml'.
    
        Returns
        -------
        df : TYPE
            DESCRIPTION.
    
        """
        if isinstance(self._workplan, type(None)):
            if not self.download_files:
                # if file_processing_state == 'intermediate':
                if 0:
                    pass
                    if isinstance(self.list_of_files, type(None)):
                        df = _pd.DataFrame(list(self.path2interfld.glob('*.nc')), columns=['path2intermediate_file'])
                    else:
                        assert(False), 'programming required'
                # elif file_processing_state == 'raw':
                elif 1: 
                    if isinstance(self.list_of_files, type(None)):
                        df = _pd.DataFrame(list(self.path2folder_raw.glob('*.nc')), columns=['path2tempfile'])
                    else:
                        assert(False), 'programming required'
                    
                    df['path2intermediate_file_point'] =df.apply(lambda row: self.path2interfld_point.joinpath(row.path2tempfile.name), axis = 1)
                    df['path2intermediate_file_area'] =df.apply(lambda row: self.path2interfld_area.joinpath(row.path2tempfile.name), axis = 1)
                else:
                    assert(False), 'not an option'
                    
            elif self.download_files:
                assert(False), 'this will probably not work'
                df = _pd.DataFrame(self.list_of_files, columns=['fname_on_ftp'])
                df['path2tempfile'] = df.apply(lambda row: self.path2folder_raw.joinpath(row.fname_on_ftp), axis = 1)
                df['path2intermediate_file'] =df.apply(lambda row: self.path2interfld.joinpath(row.fname_on_ftp), axis = 1)
            else:
                assert(False), f'{self.download_files} is not an option for file_location ... valid: (local, ftp)'
            # return df
            df['product_name'] = df.apply(lambda row: row.path2intermediate_file_point.name.split('_')[1], axis = 1)
            df['satellite'] =df.apply(lambda row: row.path2intermediate_file_point.name.split('_')[2], axis = 1)
            df['datetime_start'] =df.apply(lambda row: _pd.to_datetime(row.path2intermediate_file_point.name.split('_')[3][1:-1], format = '%Y%j%H%M%S'), axis = 1)
            df['datetime_end'] =df.apply(lambda row: _pd.to_datetime(row.path2intermediate_file_point.name.split('_')[4][1:-1], format = '%Y%j%H%M%S'), axis = 1)
            
        
            df['path2result_point'] = df.apply(lambda row: self.path2resultfld_point.joinpath(f'{row.product_name}_{row.satellite}_{row.datetime_start.strftime("%Y%m%d")}.nc'.replace('-', '_')), axis = 1)
            df['path2result_area'] = df.apply(lambda row: self.path2resultfld_area.joinpath(f'{row.product_name}_{row.satellite}_{row.datetime_start.strftime("%Y%m%d")}.nc'.replace('-', '_')), axis = 1)
            # check if final file exists
            df['result_exists'] = df.apply(lambda row: row.path2result_point.is_file(), axis = 1)
            df = df[~df.result_exists]
            df['intermediate_exists'] = df.apply(lambda row: row.path2intermediate_file_point.is_file(), axis = 1)
            df = df[~df.intermediate_exists]
            df.sort_values('datetime_start', inplace=True)
            self._workplan = df
        return self._workplan
    
    @workplan.setter
    def workplan(self, new_workplan):
        self._workplan = new_workplan
        
    def process(self, no_of_cpu = 3, test = False):

        # self.remove_artefacts()
        
        if test == 2:
            wpt = self.workplan.iloc[:1]
        elif test == 3:
            wpt = self.workplan.iloc[:no_of_cpu]
        else:
            wpt = self.workplan
        
        if no_of_cpu == 1:
            for idx, row in wpt.iterrows():
                wpe = WorkplanEntry(row, project = self)
                wpe.process()
        else:
            pool = _mp.Pool(processes=no_of_cpu)
            idx, rows = zip(*list(wpt.iterrows()))
            # out['pool_return'] = pool.map(partial(process_workplan_row, **{'ftp_settings': ftp_settings, 'sites': sites}), rows)
            out = {}
            pool_return = pool.map(_functools.partial(WorkplanEntry, **{'project': self, 'autorun': True}), rows)
            # out['pool_return'] = pool_return
            
            pool.close() # no more tasks
            pool.join()
        # if test == False:
        #     concat = Concatonator(path2scraped_files = self.path2data,
        #                  path2concat_files = self.path2concatfiles,)
        #     concat.save()
        #     out['concat'] = concat
        return 

class WorkplanEntry(object):
    def __init__(self, workplanrow, project = None, autorun = False):
        self.project = project
        self.row = workplanrow
        self.verbose = True
        
        # self._hrrr_inst = None
        # self._projection = None
        if autorun:
            self.process()
            
    def process(self, keep_ds = False, save = True):
        sat_inst = open_file(self.row.path2tempfile)
        proj = sat_inst.project_on_sites(self.project.sites)
        
        ds = proj.projection2area
        ds['datetime_end'] = self.row.datetime_end
        ds = ds.expand_dims({'datetime':[self.row.datetime_start]})
        if save:
            ds.to_netcdf(self.row.path2intermediate_file_area)
        if keep_ds:
            self.ds_area = ds
        
        ds = proj.projection2point
        ds['datetime_end'] = self.row.datetime_end
        ds = ds.expand_dims({'datetime':[self.row.datetime_start]})
        
        if save:
            ds.to_netcdf(self.row.path2intermediate_file_point)
        if keep_ds:
            self.ds_point = ds
        return
        

class Concatonator(object):
    def __init__(self, path2scraped_files = '/mnt/telg/tmp/class_tmp_inter/point',
                       path2concat_files = '/mnt/telg/data/smoke_events/20200912_18_CO/goes_projected/ABI_L2_AODC_M6_G16/point',
                       skip_last_day = False,
                       test = False):
        self.path2scraped_files = _pl.Path(path2scraped_files)
        self.path2concat_files = _pl.Path(path2concat_files)
        self.skip_last_day = skip_last_day
        try:
            self.path2concat_files.mkdir(exist_ok=True)
        except:
            self.path2concat_files.mkdir(exist_ok=True)
        
        self.test = test
        
        self._workplan = None
        self._concatenated = None
        
    @property
    def workplan(self):
        if isinstance(self._workplan, type(None)):
            ## make a workplan
            workplan = _pd.DataFrame(self.path2scraped_files.glob('*.nc'), columns=['path2scraped_files'])
            
            # get datetime
            # df['datetime_start'] =df.apply(lambda row: _pd.to_datetime(row.path2intermediate_file_point.name.split('_')[3][1:-1], format = '%Y%j%H%M%S'), axis = 1)
            workplan['datetime'] =workplan.apply(lambda row: _pd.to_datetime(row.path2scraped_files.name.split('_')[4][1:-1], format = '%Y%j%H%M%S'), axis = 1)
           
            # if 0:
                # get the date
            workplan['date'] = workplan.apply(lambda row: row.datetime.date(), axis=1)


            #remove last day ... only work on the days before last to get daily files
            if self.skip_last_day:
                workplan.sort_values('date', inplace=True)
                last_day = workplan.date.unique()[-1]
                workplan = workplan[workplan.date != last_day].copy()

            # get product name
            workplan['product_name'] = workplan.apply(lambda row: row.path2scraped_files.name.split('_')[1], axis = 1)

            # output paths
            workplan['path2concat_files'] = workplan.apply(lambda row: self.path2concat_files.joinpath(f'goes_at_gml_{row.product_name}_{row.date.year:04d}{row.date.month:02d}{row.date.day:02d}.nc'), axis = 1)

            # remove if output path exists
            workplan['p2rf_exists'] = workplan.apply(lambda row: row.path2concat_files.is_file(), axis = 1)
            workplan = workplan[ ~ workplan.p2rf_exists].copy()
            
            workplan.sort_values(['datetime'], inplace=True)
                
            self._workplan = workplan
            
        return self._workplan
    
    @property
    def concatenated(self):
        if isinstance(self._concatenated, type(None)):
            concat = []
            for date,date_group in self.workplan.groupby('date'):
#                 print(date)
                # fc_list = []
#                 for frcst_cycle, fc_group in date_group.groupby('frcst_cycle'):
# #                     print(frcst_cycle)
#                     fc_list.append(xr.open_mfdataset(fc_group.path2scraped_files, concat_dim='forecast_hour'))
            
                try:
                    # ds = xr.concat(fc_list, dim = 'datetime')
                    ds = _xr.open_mfdataset(date_group.path2scraped_files, concat_dim='datetime')
                except ValueError as err:
                    errmsg = err.args[0]
                    err.args = (f'Problem encontered while processing date {date}: {errmsg}',)
                    raise

                fn_out = date_group.path2concat_files.unique()
                assert(len(fn_out) == 1)
                concat.append({'dataset': ds, 'fname': fn_out[0]})
                if self.test:
                    break
            self._concatenated = concat
        return self._concatenated
#                 ds.to_netcdf(fn_out[0])
        
    def save(self):
        for daydict in self.concatenated:
            daydict['dataset'].to_netcdf(daydict['fname'])  
            if self.test:
                break
            

class SatelliteMovie(object):
    def __init__(self, 
                 path2fld_sat = '/mnt/telg/data/smoke_events/20200912_18_CO/goes_raw/ABI-L2-MCMIP/',
                 path2fld_fig = '/mnt/telg/data/smoke_events/20200912_18_CO/goes_raw/ABI-L2-MCMIP_figures/',
                 path2fld_movies = '/mnt/telg/data/smoke_events/20200912_18_CO/goes_raw/ABI-L2-MCMIP_movies/',
                 ):
        

        self.path2fld_sat = _pl.Path(path2fld_sat)
        self.path2fld_fig = _pl.Path(path2fld_fig)
        self.path2fld_movies = _pl.Path(path2fld_movies)
        
#         path2fld_fig.mkdir(exist_ok=True)
        # properties
        self._workplan = None
        
    @property
    def workplan(self):
        if isinstance(self._workplan, type(None)):
            workplan = _pd.DataFrame(self.path2fld_sat.glob('*.nc'), columns=['path2sat'])
            workplan.index = workplan.apply(lambda row: _pd.to_datetime(row.path2sat.name.split('_')[-3][1:-1], format = '%Y%j%H%M%S'), axis = 1)
            workplan['path2fig'] = workplan.apply(lambda row: self.path2fld_fig.joinpath(row.path2sat.name.replace('.nc','.png')), axis = 1)
            workplan.sort_index(inplace=True)
            self._workplan = workplan
        return self._workplan
    
    @workplan.setter
    def workplan(self, new_workplan):
        self._workplan = new_workplan
        return
        
    def plot_single(self, 
                    resolution          = 'i',
                    width               = 4.5e6,
                    height              = 2.7e6,
                    lat_0               = 40.12498,
                    lon_0               = -99.2368,
                    costlines           = True,
                    row                 = 10,
                    sites               = None,
                    first               = True,
                    save                = True,
                    dpi                 = 300,
                    overwrite           = True,
                    use_active_settings = False,):
        
        # read the file and make the time stamp
        if not type(row) == _pd.Series:
            row = self.workplan.iloc[row]
            
        if use_active_settings:
            resolution = self._a_resolution
            width      = self._a_width     
            height     = self._a_height    
            lat_0      = self._a_lat_0     
            lon_0      = self._a_lon_0        
            sites      = self._a_sites     
            dpi        = self._a_dpi     
            costlines  = self._a_costlines
        else:
            self._a_resolution = resolution
            self._a_width      = width     
            self._a_height     = height    
            self._a_lat_0      = lat_0     
            self._a_lon_0      = lon_0        
            self._a_sites      = sites     
            self._a_dpi        = dpi 
            self._a_costlines  = costlines
            
        mcmip = open_file(row.path2sat)
        timestamp = _pd.to_datetime(mcmip.ds.attrs['time_coverage_start'])
        tstxt = f'{timestamp.date()}\n{timestamp.time()}'.split('.')[0]
        
        if first:
            # make the basemap instanc 
            bmap = _basemap.Basemap(resolution=resolution, projection='aea', 
                                   area_thresh=5000, 
                                         width=width, height=height, 
                #                          lat_1=38.5, lat_2=38.5, 
                                         lat_0=lat_0, lon_0=lon_0)
            bmap.drawstates(zorder = 1)
            if costlines:
                bmap.drawcoastlines(linewidth = 0.5, zorder = 1)
            bmap.drawcountries(linewidth = 1, zorder = 1)
            a = _plt.gca()
            if sites:
                a, _ = sites.plot(bmap = bmap, projection='aea',
            #                             width = width, height = height,
                                        background=None, 
                            station_symbol_kwargs={'markerfacecolor':'none', 
                                                 'markersize':5, 
                                                 'markeredgewidth':0.5},
                            station_label_format='')
            self._bmap_active = bmap
        else:
            bmap = self._bmap_active
            a = _plt.gca()
            self._txt_active.remove()
            self._pc_active.remove()
            
        out = mcmip.plot_true_color(bmap = bmap, 
                              contrast = 200, gamma=2.3,zorder = 0,
                             )
        if out == False:
            self._pc_active = txt = a.text(0,0,'', transform=a.transAxes, zorder = 10,
                                             color = 'black',#colors[1], 
#                                              bbox=dict(facecolor=[1,1,1,0.7], linewidth = 0)
                                          )
            
        else:
            self._pc_active = out['pc']
            
        txt = a.text(0.05,0.85,tstxt, transform=a.transAxes, zorder = 10,
                     color = 'black',#colors[1], 
                     bbox=dict(facecolor=[1,1,1,0.7], linewidth = 0))
        self._txt_active = txt
        
        f = _plt.gcf()
        f.patch.set_alpha(0)
        if save:
            if row.path2fig.is_file():
                if not overwrite:
                    print(f'file exists, saving skipped! ({row.path2fig})')
                    return
            f.savefig(row.path2fig, dpi = dpi, bbox_inches = 'tight')
        
    def create_images(self, overwrite = False, use_active_settings = True, verbose = False):
        first = True
        if not overwrite:
            workplan = self.workplan[~self.workplan.path2fig.apply(lambda x: x.is_file())]
        else:
            workplan = self.workplan
        print(f'Number of files to process: {workplan.shape[0]}')
        for e,(idx, row) in enumerate(workplan.iterrows()):
            if verbose:
                print(row.path2sat)
            self.plot_single(row = row, first = first, overwrite = False, use_active_settings = use_active_settings)
            first = False
#             if e == 2:
#                 break
    def create_movies(self, overwrite = False, name = ''):
        dates = self.workplan.apply(lambda row: row.name.date(), axis = 1)
        groups = self.workplan.groupby(dates)
        for date,grp in groups:
            path2file_movie = self.path2fld_movies.joinpath(f'{name}_{date}.mp4'.replace('-','_'))
            path2file_movie_file_list = self.path2fld_movies.joinpath(f'{name}_{date}.txt'.replace('-','_'))
            if path2file_movie.is_file():
                if overwrite:
                    path2file_movie.unlink()
                else:
                    print(f'Movie file exists, skip! ({path2file_movie})')

            # generate the file that contains the list of files that go into the movie
            with open(path2file_movie_file_list, mode = 'w') as raus:
                for idx, row in grp.iterrows():
            #         pass
                    raus.write(f"file '{row.path2fig}'\n")

            fps = 5
            command = "ffmpeg -r {fps} -f concat -safe 0 -i '{mylist}'  '{pathout}'".format(fps=fps,
                                                                                mylist = path2file_movie_file_list,
            #                                                                     folder=save_figures2folder,
                                                                                pathout=path2file_movie)
            out = _os.system(command)
            if out != 0:
                print('something went wrong with creating movie from saved files (error code {}).\n command:\n{}'.format(out, command))

# class SatelliteDataQuery(object):
#     """ This is an older way to download data from the AWS. It from a time when I did not undstand that this webpage also just directs you to the AWS"""
#     def __init__(self):
#         self._base_url = 'http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/goes16_download.cgi'
#         self.path2savefld = _pl.Path('/mnt/data/data/goes/')
#         self.path2savefld.mkdir(exist_ok=True)
#         html = _urllib.request.urlopen(self._base_url).read()
#         self._doc = _pq(html)
#         self.query = _pd.DataFrame(columns=['source', 'satellite', 'domain', 'product', 'date', 'hour', 'minute', 'url2file', 'url_inter','inbetween_page'])
#         self._url_inter = _pd.DataFrame(columns=['url', 'sublinks'])
#     @property
#     def available_products(self):
#         # available products
#         products = [i for i in self._doc.find('select') if i.name == 'product'][0]
#         products_values = [i.attrib["value"]for  i in products]
# #         print('\n'.join([f'{i.attrib["value"]}:\t {i.text}' for  i in products]))
#         return products_values
#     @property
#     def available_domains(self):
#         domains = [i for i in self._doc.find('select') if i.name == 'domain'][0]
#         domains_values = [i.attrib["value"]for  i in domains]
# #         print('\n'.join([f'{i.attrib["value"]}:\t {i.text}' for  i in domains]))
#         return domains_values

#     @property
#     def available_satellites(self):
#         # available satellites
#         satellites = [i for i in self._doc.find('input') if i.name == 'satellite']
#         satellites_values = [i.attrib['value'] for i in satellites] #[i.attrib["value"][-2:] for i in satellites]
# #         print('\n'.join([f'{i.attrib["value"][-2:]}: {i.attrib["value"]}' for  i in satellites]))
#         return satellites_values

#     def _attache_intermeidate_linkes(self):
#         get_inter_url = lambda row: self._base_url + '?' + '&'.join([f'{i[0]}={i[1]}' for i in row.reindex(['source', 'satellite', 'domain', 'product', 'date', 'hour']).items()])
#         self.query['url_inter'] = self.query.apply(get_inter_url, axis = 1)

#     def _get_intermediate_pages(self):
#         for idx,row in self.query.iterrows():
#             intermediate_url =  row.url_inter
#         #     break

#             if intermediate_url not in self._url_inter.url.values:

#                 html_inter = _urllib.request.urlopen(intermediate_url).read()
#                 doc_inter = _pq(html_inter)

#                 sub_urls = []
#                 for link in doc_inter('a'):
#                 #     print(link.attrib['href'])
#                     if 0:
#                         if 'noaa-goes16.s3' in link.attrib['href']:
#                             print(link.attrib['href'])
#                             break
#                     else:
#                         if len(link.getchildren()) == 0:
#                             continue
#                         if not 'name' in link.getchildren()[0].attrib.keys():
#                             continue

#                         if link.getchildren()[0].attrib['name'] == 'fxx':
#                             sub_urls.append(link.attrib['href'])
#                 #             print(link.attrib['href'])
#                 #             break

#                 sub_urls = _pd.DataFrame(sub_urls, columns = ['urls'])

#                 sub_urls['datetime']= sub_urls.apply(lambda row: _pd.to_datetime(row.urls.split('/')[-1].split('_')[-3][1:-3], format = '%Y%j%H%M'), axis=1)


#                 self._url_inter = self._url_inter.append(dict(url = intermediate_url,
#                                            sublinks = sub_urls), ignore_index= True)
#                 assert(not isinstance(row.minute, type(None))), 'following minutes are available ... choose! '+ ', '.join([str(i.minute) for i in sub_urls.datetime])

#             else:
#                 pass
# #                 print('gibs schon')
                
#     def _get_link2files(self):
#         for idx,row in self.query.iterrows():
#             sublinks = self._url_inter[self._url_inter.url == row.url_inter].sublinks.iloc[0]
#             for sidx, srow in sublinks.iterrows():
#                 if srow.datetime.minute == int(row.minute):
#                     row.url2file = srow.urls
                       
#     def _generate_save_path(self):
#         def gen_output_path(self,row):
#             fld = self.path2savefld.joinpath(row['product']) 
#             fld.mkdir(exist_ok=True)
            
#             try: 
#                 p2f = fld.joinpath(row.url2file.split('/')[-1])
#             except:
#                 print(f'promblem executing " p2f = fld.joinpath(row.url2file.split('/')[-1])" in {row}, with {fld}')
#                 assert(False)
            
#             return p2f
#         self.query['path2save'] = self.query.apply(lambda row: gen_output_path(self,row), axis = 1)
    
#     @property
#     def workplan(self):
#         self._get_link2files()
#         self._generate_save_path()
#         self.query['file_exists'] = self.query.apply(lambda row: row.path2save.is_file(), axis = 1)
#         self._workplan = self.query[~self.query.file_exists]
#         return self._workplan
        
#     def add_query(self, source = 'aws',
#                      satellite = 'noaa-goes16',
#                      domain = 'C',
#                      product = 'ABI-L2-AOD',
#                      date = '2020-06-27',
#                      hour = 20,
#                      minute = [21, 26]):
        
#         if not isinstance(minute, list):
#             minute = [minute]
#         if not isinstance(hour, list):
#             hour = [hour]
            
#         for qhour in hour:
#             for qmin in minute:
#                 qdict = dict(source = source,
#                          satellite = satellite,
#                          domain = domain,
#                          product = product,
#                          date = date,
#                          hour = f'{qhour:02d}',
#                          minute = f'{qmin:02d}'
#                          )
#                 self.query = self.query.append(qdict, ignore_index = True)
#         assert(satellite in self.available_satellites)
#         assert(domain in self.available_domains)
#         assert(product in self.available_products)
        
#         self._attache_intermeidate_linkes()
#         self._get_intermediate_pages()
#         # drop line if minute is None
#         for idx, row in self.query.iterrows():
#             if isinstance(row.minute, type(None)):
#                 self.query.drop(idx, inplace=True)
                
#     def download_query(self, test = False):
#         for idx, row in self.workplan.iterrows():
#             print(f'downloading {row.url2file}', end = ' ... ')
#             if row.path2save.is_file():
#                 print('file already exists ... skip')
#             else:
#                 _urllib.request.urlretrieve(row.url2file, filename=row.path2save)
#                 print('done')
#             if test:
#                 break


class GeosSatteliteProducts(object):
    def __init__(self,file):
        if type(file) == _xr.core.dataset.Dataset:
            ds = file
        else:
            ds = _xr.open_dataset(file)
        
        self.ds = ds
        
#         self._varname4test = 'CMI_C02'

        self.valid_qf = None
        self._lonlat = None
        
    @property
    def lonlat(self):
        if isinstance(self._lonlat, type(None)):
            # Satellite height
            sat_h = self.ds['goes_imager_projection'].perspective_point_height

            # Satellite longitude
            sat_lon = self.ds['goes_imager_projection'].longitude_of_projection_origin

            # Satellite sweep
            sat_sweep = self.ds['goes_imager_projection'].sweep_angle_axis

            # The projection x and y coordinates equals the scanning angle (in radians) multiplied by the satellite height
            # See details here: https://proj4.org/operations/projections/geos.html?highlight=geostationary
            x = self.ds['x'][:] * sat_h
            y = self.ds['y'][:] * sat_h

            # Create a pyproj geostationary map object to be able to convert to what ever projecton is required
            p = _Proj(proj='geos', h=sat_h, lon_0=sat_lon, sweep=sat_sweep)

            # Perform cartographic transformation. That is, convert image projection coordinates (x and y)
            # to latitude and longitude values.
            XX, YY = _np.meshgrid(x, y)
            lons, lats = p(XX, YY, inverse=True)
            
            # Assign the pixels showing space as a single point in the Gulf of Alaska
#             where = _np.isnan(self.ds[self._varname4test].values)
            where = _np.isinf(lons)
            lats[where] = 57
            lons[where] = -152

            self._lonlat = (lons, lats) #dict(lons = lons, 
#                                     lats = lats)
        return self._lonlat
    
    def project_on_sites(self, sites):
        site_projection = Grid2SiteProjection(self, sites) 
        return site_projection
    

    
    def get_resolution(self, site = [-105.2368, 40.12498]):
        """
        Get the satellite resolotion at a particular coordinate.

        Parameters
        ----------
        at_site : iterable, or atmPy.general.measurement_site.Station instance
            This needs to be coordinates (lon, lat) or a measurment site 
            instance that has lat and lon attributes. Default are coordinates
            of Table Mountain, CO ([-105.2368, 40.12498])

        Returns
        -------
        out : TYPE
            DESCRIPTION.

        """
        # site = at_site
        if hasattr(site, 'lat') and hasattr(site, 'lon'):
            pass
        else:
            site = _np.array([site])
        out = self.get_closest_gridpoint(site)
    
        closest_point = out['closest_point'].iloc[0]
        dist = out['last_distance_grid']
    
        closest_point
    
        ax, ay = int(closest_point.argmin_x), int(closest_point.argmin_y)
    
        # dist[ax+1: ax+2, ay]
    
        bla = 10
        resx = ((dist[ax-bla: ax-bla+1, ay]/bla) + (dist[ax+bla: ax+bla+1, ay]/bla))/2
        resy = ((dist[ax, ay-bla: ay-bla+1]/bla) + (dist[ax, ay+bla: ay+bla+1]/bla))/2
        out = _pd.DataFrame({'lon':resx, 'lat': resy})
        return out
    
    def plot(self, variable, bmap = None, **pcolor_kwargs):
        lons,lats = self.lonlat
        
        if isinstance(bmap, type(None)):
            bmap = _Basemap(resolution='c', projection='aea', area_thresh=5000, 
                     width=3000*3000, height=2500*3000, 
        #                          lat_1=38.5, lat_2=38.5, 
                     lat_0=38.5, lon_0=-97.5)
    
            bmap.drawcoastlines()
            bmap.drawcountries()
            bmap.drawstates()
        bmap.pcolormesh(lons, lats, self.ds[variable], latlon=True, **pcolor_kwargs)
        return bmap

@_numba.jit(nopython=True, 
            fastmath=True, 
            # parallel=True,
            )
def get_dists(lon_lat_grid, lon_lat_sites):
    out = _np.zeros((lon_lat_sites.shape[0], 7), dtype = _np.float32)
    dist_array = _np.zeros(lon_lat_grid[0].shape + (len(lon_lat_sites),), dtype = _np.float32)
    lon_g, lat_g = lon_lat_grid
    for e,site in enumerate(lon_lat_sites):
        lon_s, lat_s = site

        p = _np.pi / 180
        a = 0.5 - _np.cos((lat_s-lat_g)*p)/2 + _np.cos(lat_g*p) * _np.cos(lat_s*p) * (1-_np.cos((lon_s-lon_g)*p))/2
        dist = 12742 * _np.arcsin(_np.sqrt(a))

        # get closest
        argmin = dist.argmin()//dist.shape[1], dist.argmin()%dist.shape[1]
        out[e,:2] = argmin        
        out[e,2] = lon_g[argmin]
        out[e,3] = lat_g[argmin]
        out[e,4] = lon_s
        out[e,5] = lat_s
        out[e,6] = dist[argmin]
        dist_array[:,:,e] = dist
    return out, dist_array

class Grid2SiteProjection(object):
    def __init__(self, grid, sites):
        self.grid = grid
        self.sites = sites
        self.radii = [5,10,25,50,100]
        
        self._closest_points = None
        self._distance_grids =  None
        self._projection2poin = None
        self._projection2area = None
    
    @property
    def projection2point(self):
        if isinstance(self._projection2poin, type(None)):
            # select relevant variablese ... those with x and y
            var_sel = [var for var in self.grid.ds.variables if self.grid.ds[var].dims == ('y', 'x')]
            ds = self.grid.ds[var_sel]
            
            # cleanup the the coordinates
            coords2del = list(ds.coords)
            coords2del.remove('x')
            coords2del.remove('y')
            # coords2del.remove('t')
            
            ds = ds.drop_vars(coords2del)
            
            for e,(idx, rowsmt) in enumerate(self.closest_grid_points.iterrows()):
                ds_at_site = ds.isel(x= int(rowsmt.argmin_y), y=int(rowsmt.argmin_x)) #x and y seam to be interchanged
            
                # drop variables and coordinates that are not needed
            #     dropthis = [var.__str__() for var in ds_at_site if var.__str__() not in ['AOD', 'DQF', 'AE1', 'AE2', 'AE_DQF']] + [cor for cor in ds_at_site.coords]
            #     ds_at_site = ds_at_site.drop(dropthis)
            
                # add armin_x, argmin_y, etc to the dataset
                for k in rowsmt.index:
                    ds_at_site[k] = rowsmt[k]
            
                # add site dimension
                ds_at_site = ds_at_site.expand_dims({'site': [rowsmt.name]})
            
                if e == 0:
                    ds_at_sites = ds_at_site
                else:
                    ds_at_sites = _xr.concat([ds_at_sites, ds_at_site], 'site')
            
            ### add dimentions for later concatination and save
            # ds_at_sites['datetime_end'] = row.datetime_end
            # ds_at_sites = ds_at_sites.expand_dims({'datetime':[row.datetime_start]})
            
            # clean up coordinates
            ds_at_sites = ds_at_sites.drop_vars(['x','y'])
            self._projection2poin = ds_at_sites
        return self._projection2poin
    
    @property
    def projection2area(self):
        if isinstance(self._projection2area, type(None)):

            # select relevant variablese ... those with x and y
            var_sel = [var for var in self.grid.ds.variables if self.grid.ds[var].dims == ('y', 'x')]
            ds = self.grid.ds[var_sel]
            
            # cleanup the the coordinates
            coords2del = list(ds.coords)
            coords2del.remove('x')
            coords2del.remove('y')
            ds = ds.drop_vars(coords2del)
            
            
            # select only those values where QF is valid
            ds = ds.where(ds.DQF.isin(self.grid.valid_qf))

            for e,radius in enumerate(self.radii):
                where = self.distance_grids < radius
            
                ds_sel = ds.where(where)
            
                # median
                dst = ds_sel.median(dim = ['x', 'y'])
                dst = dst.expand_dims({'stats':['median']})
            
                ds_area = dst
            
                #mean
                dst = ds_sel.mean(dim = ['x', 'y'])
                dst = dst.expand_dims({'stats':['mean']})
            
                ds_area = _xr.concat([ds_area, dst], 'stats')
            
                # std ... "un"-biased
                dst = ds_sel.std(dim = ['x', 'y'], 
                           ddof=1,
                          )
                dst = dst.expand_dims({'stats':['std']})
                ds_area = _xr.concat([ds_area, dst], 'stats')
            
                # no of valid points
                ds_area['num_of_valid_points'] = where.sum(dim = ['x','y'])
                ds_area['num_of_valid_points'] = where.sum(dim = ['x','y'])
                
                ds_area = ds_area.expand_dims({'radius': [radius]})
                if e == 0:
                    ds_area_all = ds_area
                else:
                    ds_area_all = _xr.concat([ds_area_all, ds_area], 'radius')
            self._projection2area = ds_area_all
            self.tp_ds_sel = ds_sel
        return self._projection2area
            
    @property
    def distance_grids(self):
        if isinstance(self._distance_grids, type(None)):
            self.closest_grid_points
        return self._distance_grids
    
    @property
    def closest_grid_points(self):#, discard_outsid_grid = 2.2):
        if isinstance(self._closest_points, type(None)):

            lon_lat_sites = self.sites
            if type(lon_lat_sites).__name__ == 'Station':
                idx = [lon_lat_sites.name]
                lon_lat_sites = _np.array([[lon_lat_sites.lon, lon_lat_sites.lat]])
            elif type(lon_lat_sites).__name__ == 'NetworkStations':
                idx = [s.name for s in lon_lat_sites]
                lon_lat_sites =_np.array([[s.lon, s.lat] for s in lon_lat_sites])
            else:
                idx = range(len(lon_lat_sites))
            lon_g, lat_g = self.grid.lonlat
            # armins columns: argmin_x, argmin_y, lon_g, lat_g, lon_s, lat_s, dist_min
            out_dict = {}
            
        #     if len(lon_g.shape) == 3:
        #         lon_g = lon_g[0,:,:]
        #         lat_g = lat_g[0,:,:]
            # index = idx #todo: rename below
            # for e,site in enumerate(lon_lat_sites):
    
            #     lon_s, lat_s = site
        
            #     p = _np.pi / 180
            #     a = 0.5 - _np.cos((lat_s-lat_g)*p)/2 + _np.cos(lat_g*p) * _np.cos(lat_s*p) * (1-_np.cos((lon_s-lon_g)*p))/2
            #     dist = 12742 * _np.arcsin(_np.sqrt(a))
        
            #     # get closest
            #     argmin = dist.argmin()//dist.shape[1], dist.argmin()%dist.shape[1]
            #     out[e,:2] = argmin        
            #     out[e,2] = lon_g[argmin]
            #     out[e,3] = lat_g[argmin]
            #     out[e,4] = lon_s
            #     out[e,5] = lat_s
            #     out[e,6] = dist[argmin]
            out, dist_array = get_dists(self.grid.lonlat, lon_lat_sites)
            # return out
            dist_array = _xr.DataArray(data = dist_array,
                                     dims = ['y','x','site'],
                                     coords = {'site': idx,
                                               'x': self.grid.ds.x,
                                               'y': self.grid.ds.y}
                                    )
            self._distance_grids = dist_array
            self._closest_points = _pd.DataFrame(out, columns = ['argmin_x', 'argmin_y','lon_gritpoint', 'lat_gridpoint', 'lon_station', 'lat_station', 'distance_station_gridpoint'], index = idx)
            # closest_point = closest_point[closest_point.distance_station_gridpoint < discard_outsid_grid]
            # out_dict['closest_point'] = closest_point
            # out_dict['last_distance_grid'] = dist.astype(_np.float32)
        return self._closest_points

class ABI_L2_MCMIPC_M6(GeosSatteliteProducts):
    def __init__(self, *args):
        super().__init__(*args)
#         self._varname4test = 'CMI_C02'

    
    def plot_true_color(self, 
                        gamma = 1.8,#2.2, 
                        contrast = 130, #105
                        projection = None,
                        bmap = None,
                        width = 5e6,
                        height = 3e6,
                        **kwargs,
                       ):
        out = {}
        channels_rgb = dict(red = self.ds['CMI_C02'].data.copy(),
                            green = self.ds['CMI_C03'].data.copy(),
                            blue = self.ds['CMI_C01'].data.copy())
        
        channels_rgb['green_true'] = 0.45 * channels_rgb['red'] + 0.1 * channels_rgb['green'] + 0.45 * channels_rgb['blue']

        
        
        for chan in channels_rgb:
            col = channels_rgb[chan]
            # Apply range limits for each channel. RGB values must be between 0 and 1
            try:
                new_col = col / col[~_np.isnan(col)].max()
            except ValueError:
                print('No valid data in at least on of the channels')
                return False
            
            # apply gamma
            if not isinstance(gamma, type(None)):
                new_col = new_col**(1/gamma)
            
            # contrast
            #www.dfstudios.co.uk/articles/programming/image-programming-algorithms/image-processing-algorithms-part-5-contrast-adjustment/
            if not isinstance(contrast, type(None)):
                cfact = (259*(contrast + 255))/(255.*259-contrast)
                new_col = cfact*(new_col-.5)+.5
            
            channels_rgb[chan] = new_col
            
        rgb_image = _np.dstack([channels_rgb['red'],
                             channels_rgb['green_true'],
                             channels_rgb['blue']])
        rgb_image = _np.clip(rgb_image,0,1)
            
        a = _plt.subplot()
        if isinstance(projection, type(None)) and isinstance(bmap, type(None)):
            
            a.imshow(rgb_image)
#             a.set_title('GOES-16 RGB True Color', fontweight='semibold', loc='left', fontsize=12);
#             a.set_title('%s' % scan_start.strftime('%d %B %Y %H:%M UTC '), loc='right');
            a.axis('off')
    
        else:          
            lons,lats = self.lonlat
            
            # Make a new map object Lambert Conformal projection
            if not isinstance(bmap,_Basemap):
                bmap = _Basemap(resolution='i', projection='aea', area_thresh=5000, 
                             width=width, height=height, 
    #                          lat_1=38.5, lat_2=38.5, 
                             lat_0=38.5, lon_0=-97.5)

                bmap.drawcoastlines()
                bmap.drawcountries()
                bmap.drawstates()

            # Create a color tuple for pcolormesh

            # Don't use the last column of the RGB array or else the image will be scrambled!
            # This is the strange nature of pcolormesh.
            rgb_image = rgb_image[:,:-1,:]

            # Flatten the array, becuase that's what pcolormesh wants.
            colortuple = rgb_image.reshape((rgb_image.shape[0] * rgb_image.shape[1]), 3)

            # Adding an alpha channel will plot faster, according to Stack Overflow. Not sure why.
            colortuple = _np.insert(colortuple, 3, 1.0, axis=1)

            # We need an array the shape of the data, so use R. The color of each pixel will be set by color=colorTuple.
            pc = bmap.pcolormesh(lons, lats, channels_rgb['red'], color=colortuple, linewidth=0, latlon=True, **kwargs)
            pc.set_array(None) # Without this line the RGB colorTuple is ignored and only R is plotted.
            out['pc'] = pc
#             plt.title('GOES-16 True Color', loc='left', fontweight='semibold', fontsize=15)
#             plt.title('%s' % scan_start.strftime('%d %B %Y %H:%M UTC'), loc='right');
            out['bmap'] = bmap
        return out

class ABI_L2_AODC_M6(GeosSatteliteProducts):
    def __init__(self, *args):
        super().__init__(*args)
        self.valid_qf = [0,1]
        
class ABI_L2_LSTC_M6(GeosSatteliteProducts):
    def __init__(self, *args):
        super().__init__(*args)
        self.valid_qf = [0,]
        
        
        
