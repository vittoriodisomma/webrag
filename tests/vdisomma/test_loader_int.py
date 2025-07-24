import os, requests as req
def test_loader():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/vdisomma/loader"
    res = req.get(url).json()
    assert res.get("output") == "loader"
