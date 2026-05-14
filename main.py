import os
import cv2
from dotenv import load_dotenv

from config import *

from core.pdf_parser import PDFParser
from core.image_preprocess import ImagePreprocessor
from core.ocr_engine import OCREngine
from core.text_merger import TextMerger
from core.component_detector import ComponentDetector
from core.noise_filter import NoiseFilter
from core.llm_filter import LLMFilter
from core.deduplicator import Deduplicator
from core.exporter import Exporter
from core.post_filter import PostFilter


load_dotenv(override=True)


# =========================================
# 将大图切块
# =========================================

def split_image_blocks(image_path):

    img = cv2.imread(image_path)

    h, w = img.shape[:2]

    blocks = []

    # 四宫格切分
    blocks.append(img[0:h//2, 0:w//2])
    blocks.append(img[0:h//2, w//2:])
    blocks.append(img[h//2:, 0:w//2])
    blocks.append(img[h//2:, w//2:])

    out_paths = []

    for i, b in enumerate(blocks):

        path = image_path.replace(
            ".png",
            f"_block_{i}.png"
        )

        cv2.imwrite(path, b)

        out_paths.append(path)

    return out_paths


if __name__ == '__main__':

    print("\n===== 电路图BOM解析开始 =====\n")

    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # =========================================
    # 找PDF
    # =========================================

    pdfs = [
        f for f in os.listdir(INPUT_DIR)
        if f.endswith('.pdf')
    ]

    if not pdfs:

        print("input目录下没有PDF")
        exit()

    pdf_path = os.path.join(
        INPUT_DIR,
        pdfs[0]
    )

    print(f"开始处理PDF: {pdf_path}")

    # =========================================
    # PDF -> 图片
    # =========================================

    parser = PDFParser()

    images = parser.pdf_to_images(
        pdf_path,
        TEMP_DIR,
        scale=PDF_SCALE
    )

    # =========================================
    # 只测试前几页
    # =========================================

    images = images[:MAX_PAGES]

    print(f"\n本次处理页数: {len(images)}")

    # =========================================
    # 初始化模块
    # =========================================

    preprocessor = ImagePreprocessor()

    ocr_engine = OCREngine()

    merger = TextMerger()

    detector = ComponentDetector()

    noise_filter = NoiseFilter()

    dedup = Deduplicator()

    post_filter = PostFilter()

    # =========================================
    # 初始化LLM
    # =========================================

    api_key = os.getenv(
        "DASHSCOPE_API_KEY"
    )

    llm = None

    if USE_LLM and api_key:

        print("\n初始化LLM...\n")

        llm = LLMFilter(
            api_key=api_key,
            base_url=BASE_URL,
            model=LLM_MODEL
        )

    else:

        print("\n未启用LLM\n")

    # =========================================
    # 全局候选池
    # =========================================

    all_candidates = []

    # =========================================
    # 遍历PDF页
    # =========================================

    for page_index, image in enumerate(images):

        print(
            f"\n============================"
        )

        print(
            f"处理第 {page_index+1} 页"
        )

        print(
            f"============================"
        )

        # =========================================
        # 图像预处理
        # =========================================

        pre_img = preprocessor.process(image)

        # =========================================
        # 图像切块
        # =========================================

        blocks = split_image_blocks(
            pre_img
        )

        all_ocr = []

        # =========================================
        # OCR
        # =========================================

        for block in blocks:

            print(f"OCR: {block}")

            results = ocr_engine.run(block)

            all_ocr.extend(results)

        print(
            f"\nOCR文本数量: "
            f"{len(all_ocr)}"
        )

        # =========================================
        # 构建上下文块
        # =========================================

        context_blocks = \
            merger.build_context_blocks(
                all_ocr
            )

        print(
            f"上下文块数量: "
            f"{len(context_blocks)}"
        )

        # =========================================
        # 处理文本块
        # =========================================

        for block in context_blocks:

            text = block['text']

            # 去噪
            if noise_filter.is_noise(text):
                continue

            # regex hint
            result = detector.detect(text)

            candidate = {

                "text":
                    result['text'],

                "neighbors":
                    block['neighbors'],

                "bbox":
                    block['bbox'],

                "regex_category":
                    result['regex_category'],

                "regex_score":
                    result['regex_score'],

                "page":
                    page_index + 1
            }

            all_candidates.append(candidate)

    # =========================================
    # 候选统计
    # =========================================

    print(
        f"\n初始候选数量: "
        f"{len(all_candidates)}"
    )

    # =========================================
    # 去重
    # =========================================

    unique = {}

    for item in all_candidates:

        key = dedup.normalize(
            item['text']
        )

        if key not in unique:
            unique[key] = item

    all_candidates = list(unique.values())

    print(
        f"去重后候选数量: "
        f"{len(all_candidates)}"
    )

    # =========================================
    # token限制
    # =========================================

    all_candidates = all_candidates[
        :MAX_TEXTS_FOR_LLM
    ]

    print(
        f"送入LLM数量: "
        f"{len(all_candidates)}"
    )

    # =========================================
    # 调试输出
    # =========================================

    print("\n===== 部分候选 =====\n")

    for i, item in enumerate(
            all_candidates[:50]):

        print(
            f"{i+1}. "
            f"{item['text']} | "
            f"hint={item['regex_category']} | "
            f"page={item['page']}"
        )

    # =========================================
    # LLM分析
    # =========================================

    final_components = []

    if llm:

        print("\n===== 开始LLM分析 =====\n")

        final_components = llm.analyze(
            all_candidates
        )

    # =========================================
    # 后过滤
    # =========================================

    final_components = [

        x for x in final_components

        if post_filter.is_valid_component(x)
    ]

    # =========================================
    # 最终去重
    # =========================================

    final_components = \
        dedup.deduplicate(
            final_components
        )

    # =========================================
    # 输出统计
    # =========================================

    print(
        f"\n最终元器件数量: "
        f"{len(final_components)}"
    )

    # =========================================
    # 导出
    # =========================================

    exporter = Exporter()

    exporter.export(
        final_components,
        OUTPUT_DIR
    )

    print("\n===== 识别完成 =====\n")