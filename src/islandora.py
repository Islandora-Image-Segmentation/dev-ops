import os
import lxml.etree as ET
from typing import Dict
from pydantic import BaseModel

_TYPE_TO_EXT = {
    'text/xml': 'xml',
    'application/rdf+xml': 'xml',
    'application/xml': 'xml',
    'text/xml;charset=UTF-8': 'xml',
    'text/html;charset=utf-8': 'html',
    'text/html;charset=UTF-8': 'html',
    'text/html': 'html',
    'text/plain;charset=UTF-8': 'txt',
    'image/png': 'png',
    'image/jpeg': 'jpg',
    'image/gif': 'gif',
    'image/jp2': 'jp2',
    'image/tiff': 'tiff',
}

_NSMAP = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
          'fedora': 'info:fedora/fedora-system:def/relations-external#',
          'fedora-model': 'info:fedora/fedora-system:def/model#',
          'islandora': 'http://islandora.ca/ontology/relsext#',
          }


class DataStream(BaseModel):
    dsid: str
    content_type: str
    content: bytes

    def save(self, directory: str = ''):
        file_path = f'{directory}/{self.dsid}.{_TYPE_TO_EXT[self.content_type]}'
        with open(file_path, 'wb') as f:
            f.write(self.content)


class ContentModel(BaseModel):
    id: str
    ds: Dict[str, bool] = {}


class IslandoraObject(BaseModel):
    obj_id: str
    member_of = ''
    ds: Dict[str, DataStream] = {}

    def __init__(self, **data):
        super().__init__(**data)
        if self.member_of == '':
            self.member_of = self.get_membership()
            # print(self.obj_id, self.member_of)

    def save(self, directory: str = ''):
        directory += '/' + self.obj_id
        if not os.path.exists(directory):
            os.mkdir(directory)
        for dsid, ds in self.ds.items():
            ds.save(directory)

    def get_membership(self) -> str:
        if 'RELS-EXT' not in self.ds:
            return ''
        tree = ET.fromstring(self.ds['RELS-EXT'].content)
        # print(tree.nsmap)
        desc = tree.find('rdf:Description', _NSMAP)
        memb = desc.find('fedora:isMemberOf', _NSMAP)
        if memb is None:
            memb = desc.find('fedora:isMemberOfCollection', _NSMAP)
        return memb.get('{%s}resource' % _NSMAP['rdf']).split('/')[-1]

    def get_cmodel_id(self) -> str:
        if 'RELS-EXT' not in self.ds:
            return None
        tree = ET.fromstring(self.ds['RELS-EXT'].content)
        desc = tree.find('rdf:Description', _NSMAP)
        model = desc.find('fedora-model:hasModel', _NSMAP)
        if model is None:
            return None
        return model.get('{%s}resource' % _NSMAP['rdf']).split('/')[-1]
