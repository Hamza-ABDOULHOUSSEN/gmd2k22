import pytest
from link import *



def test_sider_to_stitch_compoundid1():
    id1 = 'CID103086685'
    id2 = 'CID006450551'

    table = sider_to_stitch_compoundid1(id1, id2)

    assert table == ['L01XE17']

def test_stitch_source_code_to_stitch_atc_code():
    source_code = 'L01XE17'
    table = stitch_source_code_to_stitch_atc_code(source_code)

    assert table == ['axitinib']

def test_stitch_atc_code_to_drugbank():
    atc_code = 'L01XE17'

    table = stitch_source_code_to_stitch_atc_code(atc_code)

    id = "DB06626"
    name = "axitinib"
    description = "axitinib is an oral, potent, and selective inhibitor of vascular endothelial growth factor receptors (vegfr) 1, 2, and 3. axitinib is marketed under the name inlyta®, and if one previous systemic therapy for kidney cell cancer has failed, axitinib is indicated."
    indication = "used in kidney cell cancer and investigated for use/treatment in pancreatic and thyroid cancer."
    toxicity = "some of the more serious toxic effects seen in patients taking axitinib include, but are not limited to, hypertension, thrombotic events, hemorrhage, and gi perforation."
    synonyms = "axitinib,axitinibum"
    atc_code = "L01XE17"

    assert table == [name, description, indication, toxicity]