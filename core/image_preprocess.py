import cv2


class ImagePreprocessor:

    def process(self, image_path):

        img = cv2.imread(image_path)

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        # 直方图增强
        gray = cv2.equalizeHist(gray)

        # 自适应二值化
        thresh = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            2
        )

        # 放大提升 OCR
        thresh = cv2.resize(
            thresh,
            None,
            fx=2,
            fy=2,
            interpolation=cv2.INTER_CUBIC
        )

        # 降噪
        thresh = cv2.fastNlMeansDenoising(thresh)

        out_path = image_path.replace(
            ".png",
            "_pre.png"
        )

        cv2.imwrite(out_path, thresh)

        return out_path