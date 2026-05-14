from paddleocr import PaddleOCR


class OCREngine:

    def __init__(self):

        print("初始化 PaddleOCR...")

        self.paddle = PaddleOCR(
            use_angle_cls=True,
            lang='ch',
            show_log=False
        )

    def run(self, image_path):

        results = []

        p_res = self.paddle.ocr(image_path)

        if p_res and p_res[0]:

            for line in p_res[0]:

                text = line[1][0]

                conf = float(line[1][1])

                if conf < 0.45:
                    continue

                results.append({

                    "text": text,

                    "confidence": conf,

                    "bbox": line[0],

                    "source": "paddle"
                })

        return results