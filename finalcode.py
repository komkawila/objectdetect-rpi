import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
if not (cap.isOpened()):
    print("Could not open video device")


def load_image(path_img):
    return cv2.imread(path_img)


def bgr2hsv(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


def setRangeColor(hsv, lower_color, upper_color):
    return cv2.inRange(hsv, lower_color, upper_color)


def contours_img(mask):
    contours, _ = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def filter_contours_img(contours, img_draw, color_bbox):
    count = 0
    for c in contours:
        rect = cv2.boundingRect(c)
        x, y, w, h = rect
        area = w * h

        if area > 2000:
            count = count + 1
            cv2.rectangle(img_draw, (x, y), (x+w, y+h), color_bbox, 5)
    return img_draw, count


def draw_text_on_image(img_draw, count_yellow, count_orange, count_blue):
    cv2.rectangle(img_draw, (0, 0), (300, 120), (0, 0, 0), -1)
    cv2.putText(img_draw, 'Red Count : ' + str(count_orange),
                (10, 30),                  # bottomLeftCornerOfText
                cv2.FONT_HERSHEY_SIMPLEX,  # font
                1.0,                      # fontScale
                (0, 255, 255),            # fontColor
                2)                        # lineType

    cv2.putText(img_draw, 'Yellow Count : ' + str(count_yellow),
                (10, 70),                  # bottomLeftCornerOfText
                cv2.FONT_HERSHEY_SIMPLEX,  # font
                1.0,                      # fontScale
                (0, 255, 255),            # fontColor
                2)                        # lineType

    cv2.putText(img_draw, 'Blue Count : ' + str(count_blue),
                (10, 110),                  # bottomLeftCornerOfText
                cv2.FONT_HERSHEY_SIMPLEX,  # font
                1.0,                      # fontScale
                (0, 255, 255),            # fontColor
                2)                        # lineType
    return img_draw


# def main():
while(True):
    ret, frame = cap.read()
    # path_img = 'C:/Users/phanuwat_ka61/Desktop/DOLAB_Blog4-master/images/IMG_2686.jpg'
    path_img = 'C:/Users/phanuwat_ka61/Desktop/DOLAB_Blog4-master/images/obj/yellow2.jpg'
    # path_img = 'C:/Users/phanuwat_ka61/Desktop/DOLAB_Blog4-master/images/obj/red1.jpg'
    # path_img = 'C:/Users/phanuwat_ka61/Desktop/DOLAB_Blog4-master/images/obj/blue2.jpg'
    # img = load_image(frame)
    img = frame
    img = cv2.resize(img, None, fx=1, fy=1)
    hsv = bgr2hsv(img)
    img_draw = img

    # define range of Yellow color in HSV
    # lower_Yellow = np.array([20,100,100])
    lower_Yellow = np.array([20, 100, 100])
    upper_Yellow = np.array([45, 255, 255])
    mask = setRangeColor(hsv, lower_Yellow, upper_Yellow)
    contours = contours_img(mask)
    color_bbox = (0, 0, 255)
    img_draw, count_yellow = filter_contours_img(
        contours, img_draw, color_bbox)

    # define range of Orange color in HSV RED
    # lower_Orange = np.array([0, 150, 100]) # BGR // ถูกใช้งานได้
    # upper_Orange = np.array([255, 230, 180]) # BGR// ถูกใช้งานได้
    lower_Orange = np.array([0, 50, 120])  # BGR
    upper_Orange = np.array([255, 230, 180])  # BGR
    mask = setRangeColor(hsv, lower_Orange, upper_Orange)
    contours = contours_img(mask)
    color_bbox = (0, 255, 0)
    img_draw, count_red = filter_contours_img(
        contours, img_draw, color_bbox)

    # define range of Orange color in HSV
    lower_Blue = np.array([100, 36, 50])  # BGR | Work
    upper_Blue = np.array([255, 187, 200])  # BGR | Work
    mask = setRangeColor(hsv, lower_Blue, upper_Blue)
    contours = contours_img(mask)
    color_bbox = (255, 0, 0)  # BGR
    img_draw, count_blue = filter_contours_img(
        contours, img_draw, color_bbox)
    if(count_yellow > 0 or count_red > 0 or count_blue > 0):
        print('Yellow Count:', count_yellow)
        print('Red Count:', count_red)
        print('Blue Count:', count_blue)
        if(count_red != 0):
            if(count_red > 3):
                print('Red Hold')
            elif(count_red == count_blue or count_red > count_blue):
                print('Red')
        if(count_yellow != 0):
            if(count_yellow > 3):
                print('Yellow Hold')
            elif(count_yellow > 1):
                print('Yellow')
        if(count_blue != 0):
            if(count_blue > 3):
                print('Blue Hold')
            elif(count_blue > 1):
                print('Blue')

    cv2.imshow("preview", img_draw)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    # img_draw = draw_text_on_image(img_draw, count_yellow, count_orange, count_blue)

    # cv2.imwrite(
    #     'C:/Users/phanuwat_ka61/Desktop/DOLAB_Blog4-master/output/output.png', img_draw)
    time.sleep(0.5)

cap.release()
cv2.destroyAllWindows()

# if __name__ == '__main__':
#     main()
