#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def bounding_box(mask, img, n):
    
    gray_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray_mask, 128,255 ,cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    result_img = img.copy()
    contours = contours[0] if len(contours) ==2 else contours[1]
    count = 0
    X = []; Y =[] ; W = []; H = []
    ch = []
    for cntr in contours:
        
        x,y,w,h =  cv2.boundingRect(cntr)
        ch.append([x,y,w,h])
        X.append(x)
        Y.append(y)
        W.append(w)
        H.append(h)
        
        count += 1

    # X = sorted(X, reverse=True)
    # Y = sorted(Y, reverse=True)
    # W = sorted(W, reverse=True)
    # H = sorted(H, reverse=True)
    locs = []
    width = []
    for k in range(len(ch)):
        print(ch[k][2])
        locs.append(k)
        width.append(ch[k][2])

    print(width)
    print(locs)
    dict_ ={width[j]:locs[j] for j in range(len(width))} 
    sorted_width = sorted(width, reverse=True)

    if len(sorted_width) <=n:
        for i in range(len(sorted_width)):
            index = dict_.get(sorted_width[i])
            cv2.rectangle(result_img, (X[index], Y[index]), (X[index]+W[index], Y[index]+H[index]), (255 ,0 ,0 ),1 )
            #print('for box {0} the dimensions x, y, w, h are {1}'.format(count +1 ,(x,y,w,h)))
        return result_img
    else:
        for i in range(len(sorted_width[:n])):
            index = dict_.get(sorted_width[i])
            cv2.rectangle(result_img, (X[index], Y[index]), (X[index]+W[index], Y[index]+H[index]), (255 ,0 ,0 ),1 )
        return result_img

    




    


        

