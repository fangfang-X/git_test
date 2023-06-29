# -*- coding: utf-8 -*-
import pickle
import os
file_path = 'Existing_documents_jh1.pkl'  # pickle文件的路径
gz_path = '/data/img_gz'
with open(file_path, 'rb') as file:
    my_list = pickle.load(file)

for i in my_list:

    dirPath = os.path.join(gz_path,i)
    print(dirPath)
    if (os.path.exists(dirPath)):
        os.remove(dirPath)
    else:
        print("要删除的文件不存在！")
