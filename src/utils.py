import sys

import lxml.etree as ET

import newspapers
from islandora import ContentModel


def mods_to_marcxml(file_name):
    dom = ET.parse(file_name)
    xslt = ET.parse('xml/MODS-MARC.xml')
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    return ET.tostring(newdom, pretty_print=True)


def download(query: str = 'cow',
             num: int = 20,
             directory: str = 'data/download',
             url: str = 'https://islandnewspapers.ca/islandora',
             page_cm: ContentModel = newspapers.page_cm
             ):
    scrap = newspapers.NewspaperScraper(url)
    search_pages = scrap.search(query, num=num)
    dl_pages = set()
    dl_issues = set()
    dl_papers = set()
    for page in search_pages:
        issue_id = scrap.get_parent_id(page)
        if issue_id not in dl_issues:
            dl_issues.add(issue_id)
            issue = scrap.get_object(issue_id, newspapers.issue_cm)
            if issue.get_cmodel_id() != 'islandora:newspaperIssueCModel':
                print('not issue ', issue_id, issue.get_cmodel_id(), file=sys.stderr)
                continue
            issue.save(directory)
            dl_pages |= set(scrap.get_pages_in_issue(issue_id))
            if issue.member_of not in dl_papers:
                dl_pages.add(issue.member_of)
                paper = scrap.get_object(issue.member_of, newspapers.paper_cm)
                if paper.get_cmodel_id() != 'islandora:newspaperCModel':
                    print('not newspaper ', issue.member_of, paper.get_cmodel_id(), file=sys.stderr)
                paper.save(directory)
    for page_id in dl_pages:
        page = scrap.get_object(page_id, page_cm)
        if page.get_cmodel_id() != 'islandora:newspaperPageCModel':
            print('not a page ', page_id, page.get_cmodel_id(), file=sys.stderr)
            continue
        page.save(directory)
