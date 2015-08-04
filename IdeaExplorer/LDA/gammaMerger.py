import os,sys

if __name__=="__main__":
	f=open("../../data/LDAResult/gamma.dat","w+")

	for cnt in range(0,50):
		#print cnt
		f1=open("../../data/LDAResult/gamma"+str(cnt)+".dat","r+")
		buf=f1.read()
		f.write(buf)


	f.close()
