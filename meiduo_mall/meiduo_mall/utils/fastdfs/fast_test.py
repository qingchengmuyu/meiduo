from fdfs_client.client import Fdfs_client


client = Fdfs_client('./client.conf')

ret = client.upload_by_filename('/home/python/Desktop/upload_Images/kk01.jpeg')
print(ret)


# {'Group name': 'group1',
#  'Remote file_id': 'group1/M00/00/00/wKhAjl0LVoCADDmLAACJkifT0n004.jpeg',
#  'Status': 'Upload successed.',
#  'Local file name': '/home/python/Desktop/upload_Images/kk01.jpeg',
#  'Uploaded size': '34.00KB', 'Storage IP': '192.168.64.142'}
