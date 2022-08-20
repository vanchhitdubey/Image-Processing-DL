#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def bounding_box(mask, img):
    gray_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray_mask, 128,255 ,cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    result_img = img.copy()
    contours = contours[0] if len(contours) ==2 else contours[1]
    count = 0
#     for cntr in contours:
       
#         x,y,w,h =  cv2.boundingRect(cntr)
#         cv2.rectangle(result_img, (x, y), (x+w, y+h), (255 ,0 ,0 ),1 )
#         print('for box {0} the dimensions x, y, w, h are {1}'.format(count +1 ,(x,y,w,h)))
        
#         count += 1
#     return result_img
    if len(contours) != 0:
        area = []
        for cnt in contours:

            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(result_img, [box],0,(255 ,0 ,0),1)
        return result_img
        

