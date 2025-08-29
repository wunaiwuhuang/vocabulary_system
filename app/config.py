from pathlib import Path

# 项目根目录：app/ 的上一级
ROOT_DIR = Path(__file__).resolve().parents[1]

# 子目录
DATA_DIR = ROOT_DIR / "data"
BACKUP_DIR = ROOT_DIR / "backups"
EXPORT_DIR = ROOT_DIR / "exports"

# 文件路径
VOCAB_JSON = DATA_DIR / "vocab.json"

# 确保目录存在
for d in [DATA_DIR, BACKUP_DIR, EXPORT_DIR]:
    d.mkdir(parents=True, exist_ok=True)
