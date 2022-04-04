import cv2
import ImageProcessor as Model


def VideoDetection(CVid, Detection, LabelList):
    if not CVid.isOpened:
        CVid = CVid.open()
        if not CVid.isOpened():
            print("Cam Fail, closing")
            exit()

    while True:
        Stream_Check, RGB_Frame = CVid.read()
        Height, Width, Channels = RGB_Frame.shape[:3]
        RGB_RESIZE = cv2.resize(RGB_Frame, (512, 512), interpolation=cv2.INTER_AREA)
        DetectedImages = Model.IntializeDetection(RGB_RESIZE, Detection)

        Boxes = DetectedImages["detection_boxes"].numpy().astype('float32')[0]
        Labels = DetectedImages["detection_classes"].numpy()[0].astype('int')
        Scores = DetectedImages["detection_scores"].numpy().astype('float32')[0]
        ZippedData = zip(Boxes, Labels, Scores)
        for (ymin, xmin, ymax, xmax), ULabels, UScores in ZippedData:
            if UScores < .50:
                continue

            ymin = round(ymin * Height)
            xmin = round(xmin * Width)
            ymax = round(ymax * Height)
            xmax = round(xmax * Width)

            BoundryColor = (int(ULabels * 100), int(ULabels * 50), int(ULabels * 25))

            pboundries = cv2.rectangle(RGB_Frame, (xmin, ymax), (xmax, ymin), BoundryColor, 3)
            cv2.putText(pboundries, "Confidence: " + str(int(UScores * 100)), (xmin + 10, ymin + 65),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(pboundries, "Object: " + LabelList[ULabels - 1], (xmin + 10, ymin + 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
        return RGB_Frame



def ImageDetection(InputImage, Detector, LabelList):
    img = cv2.imread(filename=InputImage)
    Height, Width, Channels = img.shape[:3]

    img_resize = cv2.resize(img, (1024, 1024), interpolation=cv2.INTER_AREA)

    DetectedImages = Model.IntializeDetection(img_resize, Detector)

    Boxes = DetectedImages["detection_boxes"].numpy().astype('float32')[0]
    Labels = DetectedImages["detection_classes"].numpy()[0].astype('int')
    Scores = DetectedImages["detection_scores"].numpy().astype('float32')[0]
    ZippedData = zip(Boxes, Labels, Scores)

    for (ymin, xmin, ymax, xmax), ULabels, UScores in ZippedData:
        if UScores < .6:
            continue

        ymin = round(ymin * Height)
        ymax = round(ymax * Height)
        xmin = round(xmin * Width)
        xmax = round(xmax * Width)

        BoundryColor = (int(ULabels * 100), int(ULabels * 150), int(ULabels * 125))

        pboundries = cv2.rectangle(img, (xmin, ymax), (xmax, ymin), BoundryColor, 3)
        cv2.putText(pboundries, str(int(UScores * 100)), (xmin + 10, ymin + 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.putText(pboundries, LabelList[ULabels - 1], (xmin + 10, ymin + 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 3, cv2.LINE_AA)
    return img

def PrepareSystem(UseVideo):
    Labels = open("Labels.txt", "r")
    Lists = Labels.readlines()
    Labels.close()

    if UseVideo:
        ImageProcessor = Model.LoadModel(True)
        return ImageProcessor, Lists
    else:
        ImageProcessor = Model.LoadModel(False)

    return ImageProcessor, Lists



