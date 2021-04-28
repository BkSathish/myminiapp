import cv2
import imutils
import numpy as np
import streamlit as st


st.title("ATM SKIMMER ENQUIRER")


original = cv2.imread("Resources/skimmer1a.jpg")

uploaded_file=st.sidebar.file_uploader(label="Upload Image",type=["jpg","jpeg","png"],key="i",help="upload image of atm slot")

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()),dtype=np.uint8)
    new = cv2.imdecode(file_bytes, 1)
    #Grab the images you want to compare.

    #new = cv2.imread("Resources/skimmer1b.jpg")
    new=new[0:505,0:590]
    #cv2.imshow("ss",new)
    #resize the images to make them smaller. Bigger image may take a significantly
    #more computing power and time
    original = imutils.resize(original, height = 600)
    new = imutils.resize(new, height = 600)


    #make a copy of original image so that we can store the
    #difference of 2 images in the same
    diff = original.copy()
    cv2.subtract(original, new, diff)
    result= not np.any(diff)

    # converting the difference into grascale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # increasing the size of differences so we can capture them all


    for i in range(0, 3):
        dilated = cv2.dilate(gray.copy(), None, iterations=i + 1)

        # threshold the gray image to binarise it. Anything pixel that has
        # value more than 3 we are converting to white
        # the image is called binarised as any value less than 3 will be 0 and
        # all values equal to and more than 3 will be 255
    (T, thresh) = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY)

    # now we need to find contours in the binarised image
    cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    area=[]
    i=[]
    if result is True:
        st.warning("NO SKIMMER DETECTED")
        st.warning("NOW YOU CAN USE YOUR CARD SAFELY")
    else:
        for c in cnts:
            # fit a bounding box to the contour
            (x, y, w, h) = cv2.boundingRect(c)

            area=int(cv2.contourArea(c))
            if area>11000 and area<15000:
                #
                print(area)
                cv2.rectangle(new, (x, y), (x + w, y + h), (255,0,0), 2)
                cv2.putText(new,"skimmer detected",((w//2)+x-200,(h//2)+y-200),cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,0,0),1 )
                st.error("ALERT")

                st.image(new, caption=None, width=590)
    # uncomment below 2 lines if you want to
    # view the image press any key to continue
    # write the identified changes to disk
    #cv2.imshow("changes", new)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


else:
    st.warning("please upload image")
