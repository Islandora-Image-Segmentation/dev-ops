from islandora import ContentModel as CM
from islandora_scraper import IslandoraScraper
import re
from bs4 import BeautifulSoup

paper_cm = CM(id='newspaperCModel', ds={'RELS-EXT': True, 'DC': True, 'MODS': True, 'TN': True})
issue_cm = CM(id='newspaperIssueCModel', ds={'RELS-EXT': True, 'DC': True, 'MODS': True})
page_cm = CM(id='newspaperPageCModel',
             ds={'RELS-EXT': False, 'DC': True, 'MODS': False, 'TN': False, 'RELS-INT': False, 'OBJ': False,
                 'JP2': False, 'JPG': False, 'OCR': False, 'HOCR': False})

page_light_cm = CM(id='newspaperPageCModel',
             ds={'RELS-EXT': False, 'DC': True, 'MODS': False, 'TN': False, 'RELS-INT': False,
                 'JP2': False, 'JPG': False, 'OCR': False, 'HOCR': False})

class NewspaperScraper(IslandoraScraper):
    def __init__(self, root_url):
        super().__init__(root_url)

    def get_pages_in_issue(self, issue_id: str) -> [str]:
        resp = self.session.get(f'{self.root_url}/object/{issue_id}')
        soup = BeautifulSoup(resp.content, 'html.parser')
        dl_list = soup.find(id='block-roblib_download_block-roblib_download_block')
        if dl_list is None:
            return []
        pages = [self._extract_id(li.findAll('option')[1]['value']) for li in
                 dl_list.find_all(class_='page-select form-select')]
        return pages

    def _extract_id(self, url: str) -> str:
        return url.replace(f'{self.root_url}/object/', '').split('/')[0].replace('%3A', ':')
