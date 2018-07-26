#!/usr/bin/python
#// DETECTS THE BOOKS in image : upload.jpeg
#// saves THE DETECTED BOOKS IN books FOLDER WITHIN pwd 
# import the necessary packages
from flask import Flask, jsonify

# print(os.getcwd())

app = Flask(__name__)

book_db=[
    {
        'fname' : 1,
        'title' : 'Being Peace',
        'author' :'Author1'
    },
    {
        'fname' : 2,
        'title' : 'Computer Vision',
        'author' :'OpenCV'
    },
    {
        'fname' : 3,
        'title' : 'Congo',
        'author' :'Michael C.'
    },
    {
        'fname' : 4,
        'title' : 'Post Office',
        'author' :'Charles B.'
    }
    # ,
    # {
    #     'fname' : 5,
    #     'title' : 'Prey',
    #     'author' :'Michael C.'
    # }
]
from flask import abort
from flask import request

# there must be an 'image' in json blob that is incoming
# @app.route('/bookchain/api/detect', methods=['POST'])
# def extract_books():
#     if not request.json or not 'image' in request.json:
#         abort(400)
    
@app.route("/bookchain/api/detect", methods=["POST"])
def extract_books():
    import numpy as np
    import cv2
    import os
    from PIL import Image

    pil_image = Image.open(request.files['image']).convert('RGB')
    open_cv_image = np.array(pil_image) 
    # Convert RGB to BGR 
    image = open_cv_image[:, :, ::-1].copy() 
    # load the image, convert it to grayscale, and blur it
    # image = cv2.imread("upload.jpeg")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    (height,width,_) = image.shape
    # detect edges in the image
    edged = cv2.Canny(gray, 10, 250)
    # cv2.imshow("Edged", edged)
    # cv2.waitKey(0)
    # construct and apply a closing kernel to 'close' gaps between 'white'
    # pixels
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow("Closed", closed)
    # cv2.waitKey(0)

    # find contours (i.e. the 'outlines') in the image and initialize the
    # total number of X found
    (_,cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total = 0
    # loop over the contours and record book contours
    books=[]
    for c in cnts:
    # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    # if the approximated contour has four points, then assume that the
    # contour is a book -- a book is a rectangle and thus has four vertices
        if len(approx) == 4:    
            corn=[]
            for corner in approx:
                corn.append(corner[0])
            books.append(corn)
            total += 1 
        ccn=0           # The ID given to every API user !   
    if total>0 :
        while os.path.isdir('books'+str(ccn)) == 1:
            ccn+=1   
        os.mkdir('books'+str(ccn))    
        for book in books:
            im_src = image
            pts_src = np.array(book)
            # Read destination image.
            im_dst = np.zeros((501,501, 3), np.uint8)
            # Four corners of the book in destination image.
            pts_dst = np.array([[0, 0],[500, 0],[500, 500],[0, 500]])
            
            # Calculate Homography
            h, status = cv2.findHomography(pts_src, pts_dst)
                
            # Warp source image to destination based on homography
            im_out = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]))
            cv2.imwrite("books"+str(ccn)+"//"+str(total)+".jpg",im_out)
            total-=1
            # Show corners of the identified images
        # print ("ID: "+str(ccn))
    else:
        return jsonify({'Error': 'No Image Found'}), 404
    from skimage.measure import compare_ssim as ssim
    import sys
    import shutil

    # def mse(imageA, imageB):
    #     # the 'Mean Squared Error' between the two images is the
    #     # sum of the squared difference between the two images;
    #     # NOTE: the two images must have the same dimension
    #     err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    #     err /= float(imageA.shape[0] * imageA.shape[1])	
    #     return err

    # def compare_images(imageA, imageB, title):
    #     # compute the mean squared error and structural similarity
    #     # index for the images
    #     # m = mse(imageA, imageB)		# Basic Euclidean Algorithm for image similarity
    #     # m = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    #     # m /= float(imageA.shape[0] * imageA.shape[1])
    #     s = ssim(imageA, imageB)	# Advanced Structural Similarity method
    #     # print 'basic : %f' % (m)
    #     return (s)
    ccn=0
    while os.path.isdir('books'+str(ccn)) == 0:
        ccn+=1  	
    list_found=[]
    for up_book in os.listdir("books"+str(ccn)):
        # print ("\n\n"+"Checking "+str(up_book))
        new_book = True
        for every in book_db:    # for every book in database 
            check=cv2.imread("books"+str(ccn)+"//"+up_book,0)
            ideal= cv2.imread("db//"+str(every['fname'])+'.jpg',0)					
            # compare the images
            factor = ssim(ideal, check) # compare uploaded book to every book in db folder
            if factor > 0.7 :   # if match found
                list_found.append(every)
                new_book=False
                                   
            else:
                continue
        if new_book == True:
            shutil.copy("books"+str(ccn)+"//"+str(up_book),"db//"+str(book_db[-1]['fname']+1)+".jpg")
            newbook={
                u'fname' : book_db[-1]['fname']+1,
                u'title' : u'NewBook'+str(book_db[-1]['fname']+1),
                u'author' :u'NewAuthor'+str(book_db[-1]['fname']+1)
            }
            book_db.append(newbook)
    
    shutil.rmtree("books"+str(ccn))
    return make_response(jsonify({ u'success': u'Operation Completed', u'old_books_found' : list_found , u'all_books' : book_db}), 200)
    


# OUT OF BOUNDS FROM HERE !!!!

from flask import make_response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
