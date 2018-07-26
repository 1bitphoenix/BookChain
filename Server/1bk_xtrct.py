#!/usr/bin/python
#// DETECTS THE BOOKS in image : upload.jpeg
#// saves THE DETECTED BOOKS IN books FOLDER WITHIN pwd 
# import the necessary packages
from flask import Flask, jsonify

# print(os.getcwd())

app = Flask(__name__)


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
            cv2.imwrite("books"+str(ccn)+"//DETECTED BOOK"+str(total)+".jpg",im_out)
            total-=1
            # Show corners of the identified images
        # print ("ID: "+str(ccn))
        return jsonify({'ID': ccn}), 201
    else:
        return jsonify({'Error': 'No Image Found'}), 404



# OUT OF BOUNDS FROM HERE !!!!

from flask import make_response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
