import os

BASE_DIR = os.path.dirname(__file__)

INPUT_DIR = "input"
OUTPUT_DIR = "output"
TEMP_DIR = "temp"

OCR_CONFIDENCE = 0.45

PDF_SCALE = 3

USE_LLM = True

LLM_MODEL = "qwen-plus"

BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

MAX_PAGES = 14

MAX_TEXTS_FOR_LLM = 3000