# Data Pipeline API

import yaml
import json
import pprint



class Config(object):
    '''Top-, outer-most enviro. Basically gets in the configuration variables.'''

    def __init__(self):
        super().__init__()
        
        with open('config.yaml', 'r') as f:
            self.conf = yaml.safe_load( f.read() )



class Utilities(Config):
    '''Second outer-most enviro. Class for miscellaneous functions needed
    throughout.'''

    def __init__(self):
        super().__init__()
    
    
    def log(self, uri, m):
        '''Prints out message with URI to buffer, eg for visualizing pipeline.
        Keep len(m) down for formatting'''
        
        if len(m) <= 20:
            
            x = 20 - len(m)
            print( '{}{}{}'.format(m, ' '*x, uri) )
        
        else: input('Message must be <= 20 characters.')
    
        
    def _triple(self): pass


    def read_data(self, uri_prov):
        '''Generic read-in'''

        if uri_prov['file_type'] == 'csv':
                    
            return pd.read_csv(uri_prov['full_path'])
    
        elif con['file_type'] == 'xlsx':
            
            return pd.read_excel(uri_prov['full_path'])
            
        else: input('file_type unknown. Enter to continue.')

    


class Provenance(Utilities):
    '''Third-level enviro deals with the metadata of the data sets.'''
    
    def __init__(self):
        super().__init__()
        
        with open('_provenance.json', 'r') as f:
            self.prov = json.loads( f.read() )

    
    def get_uri_prov(self, uri):
        '''Gets the URI's values from provenance.
        Returns them as a dictionary.'''
        
        uri_prov = dict()
        
        # URIs in provenance must end like: 'text/'
        # Ending forward slash provides simpler path concat
        uri_prov['topic'] = re.findall('/(^/+)/$', uri)[0]
        
        # Sets file extension
        uri_prov['file_type'] = prov[uri]['file_type'][0]['value']
        
        # data_source sets a list of dicts: [{value:ds}, {value:ds}]
        uri_prov['data_source'] = prov[uri]['data_source']
        
        uri_prov['full_path'] = self.local_path +
                                uri + uri_prov['topic'] +
                                '.' + uri_prov['file_type']
                            
        self.log(uri, pprint(uri_prov, depth=3))
        
        return uri_prov



class HTML(Provenance):
    '''Create web pages.'''
    
    def __init__(self):
        super().__init__()
        
        with open('html.html', 'r') as f:
            self.html = f.read()
        
        
    def set_css_path(self, uri):
        
        ups = len( uri.split('/') ) - 1
        
        self.css_path = '../' * ups + 'dev/style.css'
    
        
    def make_page(self, title, payload, full_path):
        
        self.html.replace('##css_path##', self.css_path)
        
        self.html.replace('##title##', title)
        
        self.html += payload

        self.html += '</body></html>'
        
        with open(full_path, 'w') as f:
            f.write(self.html)


    def set_navigator(self):
        '''Generate a data set overview with metadata via provenance.
        Pass to make_page to make the navigator page'''
        
        entries = str()
        
        for uri in self.prov:
            
            with open('navi_entry.html', 'r') as f:
                entry = f.read()
            
            uri_prov = get_uri_prov(uri)
            
            topic = uri_prov['topic'].replace('_', ' ').title()
            entry.replace('##topic##', topic)
            
            entry.replace('##uri##', uri)
            
            entry.replace('##description##', uri_prov['description'])
            
            if prov['data_source'] != None and len(prov['data_source']) == 1:
                
                entry.replace(  '##data_source##',
                                prov['data_source'][0]['value'] )
                                
            elif prov['data_source'] != None and len(prov['data_source']) > 1:
                
                ds_html = '<ul>'
                
                for ds in prov['data_source']:
                    
                    ds_html += "<li><a href='{}'>{}</li>".format(ds['value'])
                    
                ds_html += '</ul>'
            
                  entry.replace('##data_source##', ds_html)
                
            # Clear out any unused variables
            entry_ = str()
            
            for line in entry.split('\n'):
                
                if re.findall('##.+##', line) == 0:
                    
                    entry_ += line
                    
            entries += entry_
            
        self.make_page(self, 'Navigator', entries, '../Navigator.html')
            
        
class Transform(Provenance):
    def __init__(self):|
        super().__init__()
        
    def set_df(self, uri):
        
        uri_prov = self.get_uri_prov(self, uri)
        
        self.df = self.read_data(uri_prov)
        
        self.log(uri, 'df set')
        
        
    def set_data_source(self, uri):
        '''Sets the dataframes for each of the URI's data sources, if any.
        Call each df by URI like: self.data_source[<data source URI>]'''
        
        data_sources = dict()
        
        if self.data_source == None:
            input('No data_source for {}. Enter to continue.'.format(uri))
        
        else:
            
            for ds in self.data_source:
                
                ds_uri = ds['value']
            
                uri_prov = self.get_uri_prov(self, ds_uri)
            
                ds_df = self.read_data(uri_prov)
                
                self.log(uri, 'df set as data_source')

                data_sources[ds_uri] = ds_df
                
            self.data_source = data_sources

    def rename(self, yaml):
        '''Rename columns from rename file in topic directory.'''
        
        path = self.topic_path + 'rename.yaml'
        
        with open(path, 'r') as f:
            y = yaml.safe_load( f.read() )
            
        self.df.rename(y, inplace=True)
        
        
    def mask(self, uri, col='overwrite'):
        '''Relabel values from mask file in topic directory.
        Mask YAML should be a dict of dicts:
        {col_0: {<mask>}, col_1: {<mask>} }'''
        
        path = self.topic_path + 'mask.yaml'
        
        with open(path, 'r') as f:
            y = yaml.safe_load( f.read() )
        
        for c, mask in y.items():
            
            if col == 'overwrite':
                
                self.df[c] = self.df[c].map(mask, inplace=True)
                
            else:
                
                self.df[col] = self.df[c].map(mask, inplace=True)


