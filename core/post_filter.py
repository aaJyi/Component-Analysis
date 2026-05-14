import re


class PostFilter:

    def is_valid_component(self, item):

        name = item['name'].upper()

        # 删除 connector pin
        if re.fullmatch(
                r'X\d+:\d+',
                name):

            return False

        # 删除 CAN
        if "CAN-H" in name:
            return False

        if "CAN-L" in name:
            return False

        # 删除明显信号
        signal_keywords = [

            "信号",
            "电平",
            "电压",
            "数据",
            "误差",
            "频率",
            "速度",
            "转速",
            "波形"
        ]

        for k in signal_keywords:

            if k in name:
                return False

        return True