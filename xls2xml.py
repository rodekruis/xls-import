import xlrd
import sys
import uuid
# import xml.etree.ElementTree as ET
# switch to lxml.etree, per
# https://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
from lxml import etree as ET
import lxml.builder as builder
#
# E = builder.ElementMaker(namespace='http://www.cs.rpi.edu/XGMML',
#                          nsmap={None: 'http://www.cs.rpi.edu/XGMML',
#                          'jr': 'http://openrosa.org/javarosa',
#                          'xlink': 'http://www.w3.org/1999/xlink',
#                          'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
#                          'cy': 'http://www.cytoscape.org', })
# graph = E.graph(label="Test", directed="1")

"""
-- Sample command line --
python xls2xml.py xls-to-xml-test.xlsx aZCyzqYa2aqEtf2945cna6 524fc08b8a0e4d8d857dded88d5fb882

-- Sample xml output --
<?xml version="1.0" ?>
<aZCyzqYa2aqEtf2945cna6 xmlns:jr="http://openrosa.org/javarosa" xmlns:orx="http://openrosa.org/xforms" id="aZCyzqYa2aqEtf2945cna6" version="vU6wm35wT9e5Bpr2kf5Jyw">
          <formhub>
            <uuid>524fc08b8a0e4d8d857dded88d5fb882</uuid>
          </formhub>
          <age>100</age>
          <happiness>yes</happiness>
          <name>Theodore</name>
          <date>2017-11-27</date>
          <__version__>vU6wm35wT9e5Bpr2kf5Jyw</__version__>
          <meta>
            <instanceID>ea0a35b1-125d-4856-ab09-087e38c6131b</instanceID>
          </meta>
        </aZCyzqYa2aqEtf2945cna6>
"""


NSMAP = {"jr" :  'http://openrosa.org/javarosa',
         "orx" : 'http://openrosa.org/xforms'}

#----------------------------------------------------------------------
def gen_xml(path):
    """
    Open and read an Excel file
    """
    book = xlrd.open_workbook(path)

    # get the first worksheet
    data_sheet1 = book.sheet_by_index(0)

    # get column names, __version__ column index, and version value
    colnames = data_sheet1.row_values(0)
    version_col_index = colnames.index("__version__")
    version = data_sheet1.cell(1,version_col_index).value

    root = ET.Element(KPI_UID)
    root.set('id', KPI_UID)
    root.set("version", version)

    fhub_el = ET.SubElement(root, "formhub")
    kc_uuid_el = ET.SubElement(fhub_el, "uuid")
    kc_uuid_el.text = KC_UUID
    tree = ET.ElementTree(root)
    print '<?xml version="1.0" ?>'

    # slice_index will serve both as exclusive upper-bound slice index, and later on as index for _uuid
    slice_index = version_col_index + 1
    for i, colname in enumerate(colnames[:slice_index]):
        colname_el = ET.SubElement(root, colname)
        colname_el.text = data_sheet1.cell(1,i).value

    meta_el = ET.SubElement(root,"meta")
    instance_ID_el = ET.SubElement(meta_el, "instanceID")
    iID = data_sheet1.cell(1,slice_index).value
    instance_ID_el.text = iID if len(iID) > 0 else str(uuid.uuid4())

    tree = ET.ElementTree(root)

    tree.write(sys.stdout, pretty_print=True)

#----------------------------------------------------------------------
if __name__ == "__main__":
    INPUT_EXCEL_FILE = sys.argv[1] # "xls-to-xml-test.xlsx"
    KPI_UID = sys.argv[2]
    KC_UUID = sys.argv[3]
    gen_xml(INPUT_EXCEL_FILE)