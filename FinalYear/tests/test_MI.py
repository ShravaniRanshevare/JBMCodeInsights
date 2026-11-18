from routers.metrics.maintainabilityIndex import MaintainabilityIndex

def test_excellent_mi():
    hv = 50
    cc = 2
    loc = 10
    mi = MaintainabilityIndex(hv,cc,loc)
    res = mi.getIndex()
    assert 100 < res <= 113
    
def test_avg_mi():
    hv = 500
    cc = 15
    loc = 100
    mi = MaintainabilityIndex(hv,cc,loc)
    res = mi.getIndex()
    assert 50 < res <= 61
    
def test_low_mi():
    hv = 2000
    cc = 50
    loc = 300
    mi = MaintainabilityIndex(hv,cc,loc)
    res = mi.getIndex()
    assert 25 < res <= 28
    