import os
import requests
from io import StringIO
import math

import pandas as pd
import numpy as np

print('pandas version ',pd.__version__)

def gitlab_raw_data(prj_id,prj_file,branch):
    '''
    read remote raw file from gitlab using api
    GET /projects/:id/repository/files/:file_path/raw
    file_path (required) - URL encoded full path to new file, such as lib%2Fclass%2Erb.
    ref (optional) - The name of branch, tag or commit. Default is the HEAD of the project.
    '''
    prj_id_q = requests.utils.quote(prj_id,safe='')
    prj_file_q = requests.utils.quote(prj_file,safe='')
    #data_url = "https://gitlab.advr.iit.it/api/v4/projects/hhmc-firmware%2Fmsp432-ft6/repository/files/calib%2Fsens_2%2Etxt/raw?ref=calib"
    data_url = f"https://gitlab.advr.iit.it/api/v4/projects/{prj_id_q}/repository/files/{prj_file_q}/raw?ref={branch}"
    print(data_url)
    headers = {"PRIVATE-TOKEN": "MCBxyjeT61Bngox7Ktas"}
    return StringIO(requests.get(data_url,headers=headers).text)


def write_bin(np_mat, filename):
    (name,ext) = os.path.splitext(filename)
    orig_shape = np_mat.shape

    # write txt file
    dfMat = pd.DataFrame(data=np_mat.astype(float))
    dfMat.to_csv(name+'.txt', sep=',', header=False, float_format='%.6f', index=False)
    #np_mat.tofile(name+'.txt', sep=',', format='%.6f')
    
    with open(filename, "wb") as f:
        f.write(bytearray([0xFE,0xCA,0x00,0x00])+np_mat.astype('float32').tobytes())
        #f.write(bytearray([0xFE,0xCA,0x00,0x00]))
        #np_mat.astype('float32').tofile(f)
    # read back 
    with open(filename, "rb") as f:
        np_back = np.fromfile(f,dtype='float32',offset=4).reshape(orig_shape)

    print( np.array_equiv(np_mat,np_back) )
    print(np_back)
    print(f"m shape {orig_shape} {np_back.shape}")
    print(f"m bytes {len(np_back.tobytes())}")

    return np_back  