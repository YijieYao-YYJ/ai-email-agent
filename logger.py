import logging
from pathlib import Path


# 创建 logs 文件夹
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# 日志文件路径
LOG_FILE = LOG_DIR / "agent.log"


# 创建我们自己的 Logger
logger = logging.getLogger("ai_email_agent")
logger.setLevel(logging.INFO)

# 防止日志继续传递给 root logger
logger.propagate = False


# 避免重复添加 Handler
if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # 写入 agent.log
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # 同时显示在 PyCharm Console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)