#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def bounding_box(mask, img):
    gray_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    contours,_ = cv2.findContours(gray_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) != 0:
        area = []
        for cnt in contours:
            area.append(cv2.contourArea(cnt))
        area = np.array(area)
        cnt = contours[np.argmax(area)]
        area = cv2.contourArea(cnt)
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img, [box],0,(255,0,0),1)
        return img
        

