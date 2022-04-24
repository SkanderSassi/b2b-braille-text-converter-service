import louis
import json
import os
from datetime import datetime
import xml.etree.ElementTree as ET
from utils.helpers import get_current_date

XMLNS_LINK = "http://purl.org/dc/elements/1.1/"

class Document():
    def __init__(self, 
                 root,
                 creation_date = get_current_date(),
                 title = 'Document title',
                 creator = os.getlogin(), 
                 format = 'application/xml',
                 description = 'File descripton'):
        self.creation_date = creation_date
        self.root = root
        self.title = title
        self.creator = creator
        self.format = format
        self.description = description
        self.header = self.__create_header()
        self.body = self.__create_body()
        
        
    def __create_header(self):
        return ET.SubElement(self.root, 'head')
    def __create_meta(self):
        meta = ET.SubElement(self.header,'meta', attrib={'xmlns:dc':XMLNS_LINK})
        el_format = ET.SubElement(meta, 'dc:format')
        el_date = ET.SubElement(meta, 'dc:date',)
        el_date.text = self.creation_date
        el_format.text = self.format
        return meta
    def __create_body(self):
        return ET.SubElement(self.root, 'body')
    def __repr__(self):
        return ET.tostring(self.root).decode('UTF-8')
        
    
