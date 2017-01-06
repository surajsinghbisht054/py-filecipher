#!/usr/bin/python

# ---------------- READ ME ---------------------------------------------
# This Script is Created Only For Practise And Educational Purpose Only
# This Script Is Created For http://bitforestinfo.blogspot.in
# This Script is Written By
__author__='''

######################################################
                By S.S.B Group                          
######################################################

    Suraj Singh
    Admin
    S.S.B Group
    surajsinghbisht054@gmail.com
    http://bitforestinfo.blogspot.in/

    Note: We Feel Proud To Be Indian
######################################################
'''
# 
# ===============================================
# ++++++++++x Importing Module x+++++++++++++++++
# ===============================================
import base64, os
import hashlib, fileinput
from Crypto import Random
from Crypto.Cipher import AES

# ============= Encryption and Decryption Handler =======================================
class AESCipher(object):

    def __init__(self, key): 
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))#.decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

class FileCipher:
	def __init__(self,inputpath, outputpath,password,function):
		self.inputpath=inputpath
		self.outputpath=outputpath
		self.password=password
		self.function=function
		self.cipher_process_started()

	def cipher_process_started(self):
		self.opening_files()
		if self.function=='E':
			self.start_encryption()
		else:
			self.start_decryption()
		self.closing_files()
		return

	def start_decryption(self):
		print "[+] Please Wait... Reading File "
		lines=self.inputfiles.readlines()
		md5sum=lines[0].strip('\n')
		base=lines[1].strip('\n')
		self.outputfiles=open(base64.b64decode(base),'wb')
		lines=lines[2:]
		cipher=AESCipher(self.password)
		print "[+] Please Wait... Decrypting File."
		try:
			for i in lines:
				k=i.strip('\n')
				self.outputfiles.write(cipher.decrypt(k))
		except Exception as e:
			print "[Error] Wrong Password or Something Not Right"
			print e
		self.outputfiles.close()
		print "[+] Decryption Complete. \n[+] Please Wait.. \n[+] Check File MD5SUM"
		cmd5sum=self.what_is_hash(base64.b64decode(base))
		print "[+] Before Encryption : [{}]\n[+]  After Decryption : [{}]\n".format(cmd5sum,md5sum)
		if str(cmd5sum)==str(md5sum):
			print "[+] File is Verified."
			print "[+] Thanks For Using My Program."
			exit(0)

		else:
			print "[+] File Is Corrupted"
		return

	def start_encryption(self):
		print "[+] Please Wait... Calculating MD5 SUM"
		md5sum=self.what_is_hash(self.inputpath)
		print " [+] Input File MD5 Sum : ",md5sum
		self.outputfiles.write(md5sum+'\n')
		base=base64.b64encode(os.path.basename(self.inputpath))
		self.outputfiles.write(base+'\n')
		cipher=AESCipher(self.password)
		print "[+] Please Wait.. Encrypting File.."
		for i in self.inputfiles.readlines():
			self.outputfiles.write(cipher.encrypt(i)+'\n')
		print "[+] Encryption Done!."
		print "[+] Thanks For Using My Program."
		return

	def what_is_hash(self, filename):
		h=hashlib.md5()
		with open(filename,'rb') as file:
			# loop till the end of the file
			chunk = 0
			while chunk != b'':
				# read only 1024 bytes at a time
				chunk = file.read(1024)
				h.update(chunk)
		file.close()
		data=h.hexdigest()
		return data

	def opening_files(self):
		self.inputfiles=open(self.inputpath,'rb')
		if self.function=="E":
			self.outputfiles=open(self.outputpath,'wb')

	def closing_files(self):
		self.inputfiles.close()
		if self.function=='E':
			self.outputfiles.close()
		return
