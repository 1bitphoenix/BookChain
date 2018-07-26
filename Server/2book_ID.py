
#Scans the pwd for smallest n books<n> and checks uploads within that, against all books stored in db
from skimage.measure import compare_ssim as ssim
import numpy as np
import cv2
import os
import sys
import shutil
def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	return err
 
def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)		# Basic Euclidean Algorithm for image similarity
	s = ssim(imageA, imageB)	# Advanced Structural Similarity method
	# print 'basic : %f' % (m)
	return (s)
ccn=0
while os.path.isdir('books'+str(ccn)) == 0:
    ccn+=1  	
for up_book in os.listdir("books"+str(ccn)):
	print ("\n\n"+"Checking "+str(up_book))

	if up_book.endswith(".jpg") or up_book.endswith(".jpeg"):
		new_book=True
		for db_book in os.listdir("db"):
			if db_book.endswith(".jpg") or db_book.endswith(".jpeg"):
				check=cv2.imread("books"+str(ccn)+"//"+up_book,0)
				ideal= cv2.imread("db//"+db_book,0)					
				# compare the images
				factor = compare_images(ideal, check, "Original vs. Check")
				if factor > 0.7:
					print ('SAME BOOK AS '+str(db_book))
					new_book=False
				else:
					continue
		if new_book == True:
			print ("New Book !!!")
			ss=raw_input("Enter the Book Title : ")
			shutil.copy("books"+str(ccn)+"//"+str(up_book),"db//"+ss+".jpg")
	else:
		print ("INVALID FILE UPLOADED, NOT CHECKING\n")
shutil.rmtree("books"+str(ccn))