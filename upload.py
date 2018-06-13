# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
from qiniu import BucketManager
from optparse import OptionParser

def watermark_add(filename):
	#要上传的空间
	bucket_name = 'bl-bucket'

	#上传到七牛后保存的文件名
	arr = filename.split("/")
	
	key = arr[len(arr)-1]
	# 设置图片缩略参数
	fops = 'imageView2/0/q/75|watermark/2/text/5YWs5LyX5Y-377yaYW9ob-axgue0og==/font/5b6u6L2v6ZuF6buR/fontsize/400/fill/IzAwMDAwMA==/dissolve/50/gravity/SouthEast/dx/10/dy/10'

	# 通过添加'|saveas'参数，指定处理后的文件保存的bucket和key，不指定默认保存在当前空间，bucket_saved为目标bucket，key_saved为目标key
	encode_str = bucket_name + ":" + key

	saveas_key = urlsafe_base64_encode(encode_str)

	fops = fops+'|saveas/'+saveas_key

	access_key = '93lqZSG8ooeOgpUYdQIUDlTthFZV-BjYlUWhy7yM'
	secret_key = 'Y-1vg2rvQYiwFDMGvgnkP3jmn-0UfJ-dGZBWwe_-'

	#构建鉴权对象
	q = Auth(access_key, secret_key)

	#生成上传 Token，可以指定过期时间等
	# 在上传策略中指定fobs和pipeline
	policy={
	  'persistentOps':fops
	 }

	token = q.upload_token(bucket_name, key, 3600, policy)

	#要上传文件的本地路径
	localfile = filename

	ret, info = put_file(token, key, localfile)
	print("http://image.blueskykong.com/" + key)
	assert ret['key'] == key
	assert ret['hash'] == etag(localfile)
	pass

def upload_pic(filename):
	# parser = OptionParser()
	# parser.add_option("", "--filename", dest="filename", help="filename")
	# (opts, args) = parser.parse_args()

	#需要填写你的 Access Key 和 Secret Key
	access_key = '93lqZSG8ooeOgpUYdQIUDlTthFZV-BjYlUWhy7yM'
	secret_key = 'Y-1vg2rvQYiwFDMGvgnkP3jmn-0UfJ-dGZBWwe_-'

	#构建鉴权对象
	q = Auth(access_key, secret_key)

	#要上传的空间
	bucket_name = 'bl-bucket'

	#上传到七牛后保存的文件名
	arr = filename.split("/")

	key = arr[len(arr)-1]

	#生成上传 Token，可以指定过期时间等
	token = q.upload_token(bucket_name, key, 3600)

	#要上传文件的本地路径

	localfile = filename

	ret, info = put_file(token, key, localfile)
	bucket = BucketManager(q)

	print("http://image.blueskykong.com/" + key)
	assert ret['key'] == key
	assert ret['hash'] == etag(localfile)
	return info

def get_sign_policy(fname):
  with open(fname, 'r') as f:  #打开文件
    lines = f.readlines() #读取所有行
    first_line = lines[0] #取第一行
    last_line = lines[-1] #取最后一行
    return last_line

fname='nohup.out'
if __name__ == '__main__':
  l = get_sign_policy(fname)
  l=l.replace("\n", "")
#  print (l)
  watermark_add(l)
#  print (upload_pic(l))




