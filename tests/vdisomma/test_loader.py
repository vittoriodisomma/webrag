import sys 
sys.path.append("packages/vdisomma/loader")
import loader

def test_loader():
    res = loader.loader({})
    assert res["output"] == "loader"
