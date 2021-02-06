import math
import sys
import time

import requests
from bs4 import BeautifulSoup

from islandora import ContentModel as CM
from islandora import DataStream as DS
from islandora import IslandoraObject

rels_ext_cm = CM(id='RELS-EXT', ds={'RELS-EXT': True})


class IslandoraScraper:
    def __init__(self, root_url):
        self.root_url = root_url
        self.session = requests.Session()


    def get_object(self, obj_id: str, model: CM) -> IslandoraObject:
        print('Getting: ', obj_id)
        ds_url = f'{self.root_url}/object/{obj_id}/datastream'
        resp = self.session.get(f'{ds_url}/TN')
        dss = {}
        for ds in model.ds:
            resp = self.session.get(f'{ds_url}/{ds}')
            if resp.status_code == 200:
                dss[ds] = DS(dsid=ds, content=resp.content, content_type=resp.headers['content-type'])
            elif model.ds[ds]:
                print(obj_id, 'missing', ds, file=sys.stderr)

        return IslandoraObject(obj_id=obj_id, ds=dss)

    def search(self, query: str, num=20) -> [str]:
        resp = self.session.get(f'{self.root_url}/search/{query}?type=dismax')
        soup = BeautifulSoup(resp.content, 'html.parser')
        max_res = int(soup.find(id='islandora-solr-result-count').text.split(' ')[-1][:-1].replace(',', ''))
        num = min(num, max_res)
        results = [self._get_obid(res.a['href']) for res in soup.findAll(class_='solr-value mods-titleinfo-title-ms')]
        for i in range(1, math.ceil(num / 20)):
            resp = self.session.get(f'{self.root_url}/search/{query}?type=dismax&page={i}')
            soup = BeautifulSoup(resp.content, 'html.parser')
            results.extend([self._get_obid(res.a['href']) for res in
                            soup.findAll(class_='solr-value mods-titleinfo-title-ms')])
        return results[:num]

    def get_parent_id(self, obj_id: str) -> str:
        obj = self.get_object(obj_id, rels_ext_cm)
        return obj.member_of

    def _get_obid(self, url):
        return url.split('?')[0].split('/')[-1].replace('%3A', ':')
