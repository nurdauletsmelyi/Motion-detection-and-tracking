import numpy as np
import cv2



start = 1
duration = 10
fps = '30'
capture = cv2.VideoCapture('vtest.avi')
outfile = 'heatmap.avi'

while True:
    try:
        _, f = capture.read()
        f = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        f = cv2.GaussianBlur(f, (11, 11), 2, 2)
        cnt = 0
        res = 0.05 * f
        res = res.astype(np.float64)
        break
    except:
        print('s')

fgbg = cv2.createBackgroundSubtractorMOG2(history=1, varThreshold=100,
                                          detectShadows=True)



kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
cnt = 0
sec = 0
while True:
    # if sec == duration: break
    cnt += 1
    if cnt % int(fps) == 0:
        print(sec)
        sec += 1
    ret, frame = capture.read()
    if not ret: break
    fgmask = fgbg.apply(frame, None, 0.01)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # if cnt == 30: res
    gray = cv2.GaussianBlur(gray, (11, 11), 2, 2)
    gray = gray.astype(np.float64)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    fgmask = fgmask.astype(np.float64)
    res += (40 * fgmask + gray) * 0.01
    res_show = res / res.max()
    res_show = np.floor(res_show * 255)
    res_show = res_show.astype(np.uint8)
    res_show = cv2.applyColorMap(res_show, cv2.COLORMAP_JET)
    cv2.imshow('s', res_show)


    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


capture.release()
cv2.destroyAllWindows()