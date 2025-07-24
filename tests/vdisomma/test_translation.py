import sys 
sys.path.append("packages/vdisomma/translation")
import translation

def test_translation():
    res = translation.translation({})
    assert res["output"] == "translation"
