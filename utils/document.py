
import os
import xml.etree.ElementTree as ET
import textwrap
from louis import translateString
from common.helpers import get_current_date
from bs4 import BeautifulSoup
from common.exceptions import TranslationTableNotFound

## TT -> Translation table
## en-ueb -> english unified braille
## Grade 2 -> Contracted
## Grade 1 -> Uncontracted

UNICODE_PRODUCER = "unicode.dis"

TT = {
    'en-us-g2': 'en-us-g2.ctb',
    'en-us-g1': 'en-us-g1.ctb',
    'ar-ar-g1' : 'ar-ar-g1.utb',
    'ar-ar-g2' : 'ar-ar-g2.ctb',
    'en-ueb-g1' : 'en-ueb-g1.ctb',
    'en-ueb-g2' : 'en-ueb-g2.ctb',
    'en-gb-g1' : 'en-gb-g1.utb',
    'en-gb-g2' : 'en-gb-g1.utb',
    'fr-bfu-g2' : 'fr-bfu-g2.ctb',
    'fr-bfu-g1' : 'fr-bfu-g1.ctb',
    
}
#BRF max : 39 characters width | 25 height 


XMLNS_LINK = "http://purl.org/dc/elements/1.1/"


class BRFDocument:
    def __init__(self, content):
        self.content = content
        self.translated_text = None
        self.file_format = "application/txt"
    def generate_document(self, braille_type, verbose = False):
        if braille_type not in TT.keys():
            raise TranslationTableNotFound(f"Cannot translate document using translation table {braille_type}, not found")
        translation_table = TT[braille_type]
        final_text = []
        if verbose:
            print(f"Using translation table {translation_table}")
        for data_page in self.content:
            lines = data_page["lines"]
            for line in lines:
                translated_line = translateString([translation_table], line["content"])
                wrapped_text = textwrap.wrap(translated_line, 39)

                final_text += wrapped_text
        self.translated_text = "\n".join(final_text)
        return self.translated_text
    def __repr__(self):
        return self.translated_text
                
                
                
class PEFDocument:
    def __init__(
        self,
        content,
        identifier,
        creation_date=get_current_date(),
        title="Document title",
        creator=os.getlogin(),
        file_format="application/x-pef+xml",
        description="File descripton",
    ):
        """Class representing a Portable Embossing Format

        Args:
            content (List): Document's data
            creation_date (str, optional): Date of creation of document. Defaults to get_current_date().
            title (str, optional): Title of document. Defaults to "Document title".
            creator (str, optional): Name of the author. Defaults to os.getlogin().
            file_format (str, optional): File format. Defaults to "application/xml".
            description (str, optional): Description of the file. Defaults to "File descripton".
        """
        self.creation_date = creation_date
        self.root = ET.Element("pef", attrib={"version": "2008-1"}, 
                               xmlns='xmlns="http://www.daisy.org/ns/2008/pef"')
        self.title = title
        self.creator = creator
        self.identifier=identifier
        self.file_format = file_format
        self.description = description
        self.header = self.__create_header()
        self.body = self.__create_body()
        self.content = content
        self.nb_pages = self.__get_original_nb_pages()
    def __create_header(self):
        return ET.SubElement(self.root, "head")

    def __create_meta(self):
        meta = ET.SubElement(self.header, "meta", attrib={"xmlns:dc": XMLNS_LINK})
        el_format = ET.SubElement(meta, "dc:format")
        el_identifier = ET.SubElement(meta, "dc:identifier")
        el_identifier.text = self.identifier
        el_date = ET.SubElement(
            meta,
            "dc:date",
        )
        el_date.text = self.creation_date
        el_format.text = self.file_format
        return meta

    def __create_body(self):
        return ET.SubElement(self.root, "body")

    def __create_page(self, section):
        return ET.SubElement(section, "page")

    def __create_section(self, volume):
        return ET.SubElement(volume, "section")

    def __create_volume(self, nb_cols=1, nb_rows=1, is_duplex=False, row_gap=0):
        """_summary_

        Args:
            nb_cols (int, optional): Defines the page width expressed as an integer multiple of the braille cell width. Defaults to 1.
            nb_rows (int, optional):  Defines the page height expressed as an integer multiple of row height. Defaults to 1.
            is_duplex (bool, optional): Defines whether or not both sides of the sheet should be embossed. Defaults to False.
            row_gap (int, optional): Defines the size of the gap following a row. Defaults to 0.

        Returns:
            xml.etree.ElementTree : XML Element representing the volume <volume></volume>
        """
        # TODO add nb_cols and nb_rows
        
        return ET.SubElement(
            self.body,
            "volume",
            attrib={
                "duplex": 'false' if is_duplex == False else 'true',
            },
            cols=f"{nb_cols}",
            rows=f"{nb_rows}",
            rowgap =f"{row_gap}",
            
        )
        
    def __get_original_nb_pages(self):
        return len(self.content)
        
        
    def __create_row(self, content, page):
        row = ET.SubElement(page, "row")
        
        row.text = content
        return row

    def generate_document(self, braille_type):
        assert braille_type in TT.keys()
        self.__create_meta()
        volume = self.__create_volume()
        max_rows = 0
        max_cols = 40
        
        for data_page in self.content:
            section = self.__create_section(volume)
            page = self.__create_page(section)
            lines = data_page["lines"]
            if max_rows < len(lines):
                max_rows = len(lines)
            for line in lines:
                trans_content = translateString([UNICODE_PRODUCER,TT[braille_type]], line["content"])
                if len(trans_content) > max_cols:
                    wrapped_content = textwrap.wrap(trans_content, max_cols)
                    for content in wrapped_content:
                        self.__create_row(content, page)
                else:
                    self.__create_row(trans_content, page)
        volume.attrib['rows'] = f"{max_rows}"
        #TODO check how to attribute this value to get better visual 
        volume.attrib['max_cols'] = f"{max_cols}"
        
        bs = BeautifulSoup(ET.tostring(self.root,encoding='unicode'), "xml")
        return bs.prettify()
    
    def __repr__(self):
        bs = BeautifulSoup(ET.tostring(self.root,encoding='unicode'), "xml")
        return bs.prettify()
        

    
