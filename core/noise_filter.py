import re


class NoiseFilter:

    def is_noise(self, text):

        text = text.strip()

        if not text:
            return True

        # 太短
        if len(text) <= 1:
            return True

        # 纯数字
        if re.fullmatch(r'[\d\.\-]+', text):
            return True

        # 单字母
        if re.fullmatch(r'[A-Z]', text):
            return True

        # 电线颜色
        if text in [
            'B', 'W', 'R', 'G',
            'L', 'BR', 'GR'
        ]:
            return True

        return False