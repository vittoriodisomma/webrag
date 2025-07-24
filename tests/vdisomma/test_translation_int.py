import os, requests as req
def test_translation():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/vdisomma/translation"
    res = req.get(url).json()
    assert res.get("output") == "translation"
