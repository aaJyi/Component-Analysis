import re


class ComponentDetector:

    SUSPECT_PATTERNS = {

        'fuse': [
            r'\bF\d+\b',
            r'熔断器',
            r'保险丝',
        ],

        'relay': [
            r'\bK\d+\b',
            r'\bJ\d+\b',
            r'继电器'
        ],

        'connector': [
            r'\bX\d+\b',
            r'连接器',
            r'插接器',
        ],

        'sensor': [
            r'\bB\d+\b',
            r'传感器'
        ],

        'switch': [
            r'\bS\d+\b',
            r'开关'
        ],

        'motor': [
            r'\bM\d+\b',
            r'电机'
        ],

        'controller': [
            r'ECU',
            r'VCU',
            r'BCM',
            r'ABS',
            r'控制器',
            r'模块'
        ]
    }

    def detect(self, text):

        text = text.upper().strip()

        best_category = None
        score = 0.0

        for category, patterns in \
                self.SUSPECT_PATTERNS.items():

            for p in patterns:

                if re.search(p, text, re.I):

                    best_category = category
                    score = 0.9
                    break

        return {
            "text": text,
            "regex_category": best_category,
            "regex_score": score
        }