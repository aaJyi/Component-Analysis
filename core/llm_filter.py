import json
import re

from openai import OpenAI


class LLMFilter:

    def __init__(self,
                 api_key,
                 base_url,
                 model):

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

        self.model = model

    def extract_json(self, content):

        # 去 markdown
        content = content.replace(
            "```json",
            ""
        )

        content = content.replace(
            "```",
            ""
        )

        # 提取 JSON 数组
        match = re.search(
            r'\[.*\]',
            content,
            re.S
        )

        if match:

            return match.group(0)

        return None

    def analyze(self, texts):

        if not texts:
            return []

        prompt = f"""
        你是汽车电路图解析专家。

        下面是OCR识别出的文本。

        任务：

        从中提取：

        所有“电气相关对象”。

        注意：

        不是仅仅识别传统电子元器件。

        而是：

        只要属于以下任何一种，
        都必须保留：

        1. ECU
        2. 控制器
        3. 仪表
        4. 指示灯
        5. 报警器
        6. 蜂鸣器
        7. 传感器
        8. 电机
        9. 电磁阀
        10. 继电器
        11. 保险丝
        12. 接插件
        13. CAN节点
        14. 模块
        15. 开关
        16. 功能总成
        17. 组合仪表
        18. 电气设备
        19. 通讯节点
        20. 电路功能名称

        非常重要：

        宁可多输出，
        绝对不要漏。

        即使你不确定，
        也输出。

        尤其：

        像：

        - 车速表
        - 水温表
        - 燃油表
        - 转速表
        - ABS报警
        - 发动机故障报警
        - 指示灯
        - 蜂鸣器
        - CAN
        - 仪表总成

        这些都必须保留。

        不要过度过滤。

        输出：

        JSON数组：

        [
          {{
            "name": "xxx",
            "category": "xxx",
            "confidence": 0.95,
            "page": 1
          }}
        ]

        OCR文本：

        {json.dumps(texts, ensure_ascii=False, indent=2)}
        """

        try:

            response = self.client.chat.completions.create(

                model=self.model,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.1
            )

            content = \
                response.choices[0].message.content

            print("\n===== LLM原始输出 =====\n")
            print(content)

            json_str = self.extract_json(content)

            if not json_str:

                print("未找到JSON")

                return []

            return json.loads(json_str)

        except Exception as e:

            print("LLM分析失败:", e)

            return []