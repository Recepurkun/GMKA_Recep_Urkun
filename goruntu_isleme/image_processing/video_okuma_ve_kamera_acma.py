"""data klasörümüz altindaki ornek videoyu frame üzerinden oynatmayi ve görüntümüzü kamerayi kullanarak canli olarak frame üzerinde 
gösterdik"""

import cv2

def video_capture(bfr):
    capture = cv2.VideoCapture(bfr)

    while True:
        kontrol,frame = capture.read()
        print(frame)
        cv2.imshow("frame",frame)
        if cv2.waitKey(1) & 0xFF == ord("q"): #q tuşu ile çıkış işlemi gerçekleştirilir
            break

    cv2.destroyAllWindows()

if __name__=="__main__":

    #bfr = 0 #kendi kameramızdan görüntüyü açmak için
    bfr = "data/ornek_video.mp4" #data dosyasında olan örnek videoyu açmak için
    video_capture(bfr)