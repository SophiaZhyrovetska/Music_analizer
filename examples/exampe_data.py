import json
from lxml import etree
from io import StringIO
from StringIO import StringIO

def try_json():
    """Try JSON functions"""
    json.dumps(['item1', {'item2': ('item3', 1, 2, 3)}])
    print(json.dumps("\"item1\item3"))
    print(json.dumps('\\'))
    print(json.dumps({"c": 1, "b": 2, "a": 3}, sort_keys=True))
    io = StringIO()
    json.dump(['item4'], io)
    return io.getvalue()

def try_lxml(file):
    """Try XML parsing"""
    with open(file) as f:
        xml = f.read()
    parsed = etree.parse(StringIO(xml))
    context = etree.iterparse(StringIO(xml))
    for action, item in context:
        if not item.text:
            text = "None"
        else:
            text = item.text

 
