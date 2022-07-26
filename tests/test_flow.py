"""
Tests for inputs.flow module
"""
from pytest import approx
from gdmate.inputs import flow

def test_get_published():
    """Test get_published function"""

    ol_dry_dis_hirth = flow.get_published(
        'olivine','hirth','dislocation','dry')
    
    assert ol_dry_dis_hirth == (1.1e5,3.5,0,0,530,18)

    ol_wet_dis_hirth = flow.get_published(
        'olivine','hirth','dislocation','wet')

    assert ol_wet_dis_hirth == (90,3.5,0,1.2,480,11)

    ol_dry_dif_hirth = flow.get_published(
        'olivine','hirth','diffusion','dry')

    assert ol_dry_dif_hirth == (1.5e9,1,3,0,375,2)

    ol_wet_dif_hirth = flow.get_published(
        'olivine','hirth','diffusion','wet')

    assert ol_wet_dif_hirth == (1.0e6,1,3,1,335,4)

    qz_wet_dis_gleason = flow.get_published(
        'quartzite','gleason','dislocation','wet')

    assert qz_wet_dis_gleason == (1.1e-4,4,0,0,223,0)

def test_convert2SI():
    """Test convert2SI function"""
    rel = 1e-2
    abs = 1e-30

    ol_dry_dis_hirth = flow.get_published(
        'olivine','hirth','dislocation','dry')
    
    converted = flow.convert2SI(ol_dry_dis_hirth)

    assert converted == approx((1.10e-16,3.5,0,0,530e3,18e-6),
    rel=rel,abs=abs)

    ol_wet_dis_hirth = flow.get_published(
        'olivine','hirth','dislocation','wet')
    
    converted = flow.convert2SI(ol_wet_dis_hirth)

    assert converted == approx((5.68e-27,3.5,0,1.2,480e3,11e-6),
    rel=rel,abs=abs)

    ol_dry_dif_hirth = flow.get_published(
        'olivine','hirth','diffusion','dry')
    
    converted = flow.convert2SI(ol_dry_dif_hirth)

    assert converted == approx((1.50e-15,1,3,0,375e3,2e-6),
    rel=rel,abs=abs)

    ol_wet_dif_hirth = flow.get_published(
        'olivine','hirth','diffusion','wet')
    
    converted = flow.convert2SI(ol_wet_dif_hirth)

    assert converted == approx((1.00e-24,1,3,1,335e3,4e-6),
    rel=rel,abs=abs)

    qz_wet_dis_gleason = flow.get_published(
        'quartzite','gleason','dislocation','wet')

    converted = flow.convert2SI(qz_wet_dis_gleason)

    assert converted == approx((1.10e-28,4,0,0,223e3,0),
    rel=rel,abs=abs)

def test_scaleA():
    """ Test for scaleA function"""

    ol_dry_dis_hirth = flow.get_published(
        'olivine','hirth','dislocation','dry')

    ol_wet_dis_hirth = flow.get_published(
        'olivine','hirth','dislocation','wet')

    ol_dry_dif_hirth = flow.get_published(
        'olivine','hirth','diffusion','dry')

    ol_wet_dif_hirth = flow.get_published(
        'olivine','hirth','diffusion','wet')

    qz_wet_dis_gleason = flow.get_published(
        'quartzite','gleason','dislocation','wet')  
    
    params = [ol_dry_dis_hirth,ol_wet_dis_hirth,
    ol_dry_dif_hirth,ol_wet_dif_hirth,qz_wet_dis_gleason]

    answers = [7.37e-15,3.80e-25,4.50e-15,3.00e-24,
                1.37e-26]

    for k,law in enumerate(params):
        converted = flow.convert2SI(law)

        A_SI = converted[0]
        n = converted[1]

        scaled = flow.scaleA(A_SI,n)

        assert scaled == approx(answers[k],rel=1e-2,abs=1e-30)