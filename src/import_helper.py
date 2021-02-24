import os
import shutil
import sys
import tempfile
from glob import glob

from utils import mods_to_marcxml


class ImportHelper:
    def __init__(self, ingest_dir: str = 'data/ingest', download_dir: str = 'data/download'):
        self.ingest_dir = ingest_dir
        self.download_dir = download_dir
        self.papers = []
        self.issues = []
        self.pages = []

    def load_dir(self):
        items = (os.listdir(self.download_dir))
        self.papers = []
        self.issues = []
        self.pages = []
        for item in items:
            col_split = item.split('_')
            if len(col_split) > 1:
                p_split = col_split[-1].split('-')
                if item.startswith('newspapers:'):
                    self.papers.append(item)
                elif len(p_split) > 1:
                    self.pages.append(item)
                else:
                    self.issues.append(item)

    def prep_papers_zip(self):
        with tempfile.TemporaryDirectory() as tempDir:
            self._save_papers_to_dir(tempDir)
            shutil.make_archive(f'{self.ingest_dir}/newspapers', 'zip', tempDir)

    def prep_papers_dir(self):
        dest_dir = f'{self.ingest_dir}/newspapers'
        os.mkdir(dest_dir)
        self._save_papers_to_dir(dest_dir)

    def _save_papers_to_dir(self, dest_dir):
        for paper in self.papers:
            shutil.copy(f'{self.download_dir}/{paper}/MODS.xml', f'{dest_dir}/{paper}.xml')
            try:
                tn_name = glob(f'{self.download_dir}/{paper}/TN.*')[0]
                ext = tn_name[tn_name.rfind('.'):]
                shutil.copy(tn_name, f'{dest_dir}/{paper}{ext}')
            except IndexError:
                print(f'Could not find thumbnail for: {paper}', file=sys.stderr)

    def prep_papers_marc(self):
        if not os.path.exists(f'{self.ingest_dir}/newspapers'):
            os.mkdir(f'{self.ingest_dir}/newspapers')
        for paper in self.papers:
            marc = mods_to_marcxml(f'{self.download_dir}/{paper}/MODS.xml')
            with open(f'{self.ingest_dir}/newspapers/{paper}.xml', 'bw') as f:
                f.write(marc)

    def prep_issues(self, method: str = 'dir'):
        for issue_id in self.issues:
            paper, issue = tuple(issue_id.split('_'))
            dest_dir = f'{self.ingest_dir}/{paper}/{issue}'
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            shutil.copy(f'{self.download_dir}/{issue_id}/MODS.xml', dest_dir)

        for page_id in self.pages:
            paper, li = tuple(page_id.split('_'))
            issue, page = tuple(li.split('-'))
            dest_dir = f'{self.ingest_dir}/{paper}/{issue}/{page}'
            print(dest_dir)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            try:
                shutil.copy(f'{self.download_dir}/{page_id}/JP2.jp2', dest_dir)
                shutil.copy(f'{self.download_dir}/{page_id}/TN.jpg', dest_dir)
                shutil.copy(f'{self.download_dir}/{page_id}/OCR.txt', dest_dir)
                shutil.copy(f'{self.download_dir}/{page_id}/HOCR.html', dest_dir)
                shutil.copy(f'{self.download_dir}/{page_id}/OBJ.tiff', dest_dir)
            except FileNotFoundError:
                try:
                    print(f'Could not find file: {self.download_dir}/{page_id}/OBJ.tiff', file=sys.stderr)
                    print(f'Trying {self.download_dir}/{page_id}/JP2.jp2', file=sys.stderr)
                    shutil.copy(f'{self.download_dir}/{page_id}/JP2.jp2', f'{dest_dir}/OBJ.jp2')
                except FileNotFoundError:
                    print(f'Could not find file: Trying {self.download_dir}/{page_id}/JP2.jp2', file=sys.stderr)

        if method == 'zip':
            paper_names = set([issue_id.split('_')[0] for issue_id in self.issues])
            for paper in paper_names:
                paper_path = f'{self.ingest_dir}/{paper}'
                if os.path.exists(paper_path):
                    print(f'Zipping: {paper_path}')
                    shutil.make_archive(paper_path, 'zip', paper_path)
                    shutil.rmtree(paper_path)
