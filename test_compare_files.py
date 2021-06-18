from compare import ComparisonService

TXT_FILES = \
    ['https://dl.dropboxusercontent.com/s/vjerymizfqnetz8/bigger-out-1.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/e52pq4wzgrgtc1w/bigger-out-2.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/i4byp7xvxomtx7d/bigger-out-3.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/5lhikw7sa3aurml/bigger-out-4.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/eazw4ecmh0ztk3c/bigger-out-5.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/ebgwriv8jz07qs4/bigger-out-6.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/wscvfunnv1yikzf/bigger-out-7.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/lgi446rwijmyl0a/bigger-out-8.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/l97dj4xctdtbzjh/bigger-out-9.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/nn9jyeggq0g1pjq/bigger-out-10.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/zpogqecauh75zum/out-1.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/mdmtqyoe8mi5hmg/out-2.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/45vsmdhqkklbnd4/out-3.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/ec5v4v5ejspyzou/out-4.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/i92kocs02vl1844/out-5.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/k2tapuwdk2u3g4g/out-6.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/if0ri79oja6m5xa/out-7.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/c7iq66ybqfpy70k/out-8.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/ituyz6bmkek6e5c/out-9.txt?dl=0'
     ,'https://dl.dropboxusercontent.com/s/2bdjx1h32ru5iy3/out-10.txt?dl=0']


def test_comparison_files():
    txt_file = TXT_FILES
    yml_file = 'services_versions.yml'
    compare = ComparisonService(yml_file)
    compare.make_comparison(txt_file)