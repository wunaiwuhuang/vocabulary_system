import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import pandas as pd

from config import VOCAB_JSON, BACKUP_DIR, EXPORT_DIR, DATA_DIR
from models import Entry

# ---------- 基础 I/O ----------
def _read_raw() -> List[Dict[str, Any]]:
    if VOCAB_JSON.exists():
        with open(VOCAB_JSON, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return data
            except json.JSONDecodeError:
                pass
    return []

def _backup():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"vocab_{ts}.json"
    if VOCAB_JSON.exists():
        backup_file.write_text(VOCAB_JSON.read_text(encoding="utf-8"), encoding="utf-8")

def _write_raw(rows: List[Dict[str, Any]]):
    _backup()
    with open(VOCAB_JSON, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

# ---------- 高层 API ----------
def load_all() -> List[Dict[str, Any]]:
    '''按更新时间倒序返回'''
    rows = _read_raw()
    rows.sort(key=lambda r: r.get("updated_at", ""), reverse=True)
    return rows

def add_entry(entry: Entry) -> None:
    rows = _read_raw()
    # 简单去重：同 topic 下 word 重名则视为重复
    for r in rows:
        if r.get("word", "").lower() == entry.word.lower() and r.get("topic", "").lower() == entry.topic.lower():
            # 合并：更新释义/音标/例句/短语/备注，保留熟悉度较高的
            r["phonetic"] = entry.phonetic or r.get("phonetic", "")
            r["meaning"] = entry.meaning or r.get("meaning", "")
            r["example"] = entry.example or r.get("example", "")
            # 合并 phrases 去重
            phrases = set([*(r.get("phrases", []) or []), *entry.phrases])
            r["phrases"] = sorted([p for p in phrases if p])
            r["notes"] = entry.notes or r.get("notes", "")
            r["familiarity"] = max(int(r.get("familiarity", 1) or 1), int(entry.familiarity or 1))
            r["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _write_raw(rows)
            return
    # 新增
    rows.append(entry.to_dict())
    _write_raw(rows)

def update_familiarity(entry_id: str, delta: int = 1) -> bool:
    rows = _read_raw()
    for r in rows:
        if r.get("id") == entry_id:
            fam = int(r.get("familiarity", 1) or 1) + delta
            fam = max(1, min(5, fam))
            r["familiarity"] = fam
            r["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _write_raw(rows)
            return True
    return False

def update_familiarity_entries(entry_ids: list[str], delta: int = 1) -> int:
    """批量修改熟悉度，返回成功修改的数量"""
    rows = _read_raw()
    count = 0
    for r in rows:
        if r.get("id") in entry_ids:
            fam = int(r.get("familiarity", 1) or 1) + delta
            fam = max(1, min(5, fam))
            r["familiarity"] = fam
            r["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            count += 1
    if count > 0:
        _write_raw(rows)
    return count

def set_familiarity(entry_id: str, value: int) -> bool:
    rows = _read_raw()
    for r in rows:
        if r.get("id") == entry_id:
            r["familiarity"] = max(1, min(5, int(value)))
            r["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _write_raw(rows)
            return True
    return False

def set_familiarity_entries(entry_ids: list[str], value: int) -> int:
    """批量设置熟悉度，返回成功修改的数量"""
    rows = _read_raw()
    count = 0
    for r in rows:
        if r.get("id") in entry_ids:
            r["familiarity"] = max(1, min(5, int(value)))
            r["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            count += 1
    if count > 0:
        _write_raw(rows)
    return count

def delete_entry(entry_id: str) -> bool:
    rows = _read_raw()
    new_rows = [r for r in rows if r.get("id") != entry_id]
    if len(new_rows) != len(rows):
        _write_raw(new_rows)
        return True
    return False

def delete_entries(entry_ids: list[str]) -> int:
    """批量删除多个 ID 的词条，返回删除数量"""
    rows = _read_raw()
    new_rows = [r for r in rows if r.get("id") not in entry_ids]
    deleted = len(rows) - len(new_rows)
    if deleted > 0:
        _write_raw(new_rows)
    return deleted

# ---------- 导入/导出 ----------
#def export_excel(filepath: Optional[Path] = None) -> Path:
#    filepath = filepath or (EXPORT_DIR / "vocab_export.xlsx")
#    rows = load_all()
#    if not rows:
#        # 也导出空结构，方便后续填充
#        rows = []
#    df = pd.DataFrame(rows)
#    # phrases 列转字符串以便 Excel 显示
#    if "phrases" in df.columns:
#        df["phrases"] = df["phrases"].apply(lambda v: "; ".join(v) if isinstance(v, list) else (v or ""))
#    df.to_excel(filepath, index=False)
#    return filepath

def export_csv(filepath: Optional[Path] = None, return_df: bool = False):
    """导出词库为 CSV 文件或 DataFrame"""
    filepath = filepath or (EXPORT_DIR / "vocab_export.csv")
    rows = load_all()
    if not rows:
        rows = []
    df = pd.DataFrame(rows)
    # phrases 列转字符串以便 CSV 显示
    if "phrases" in df.columns:
        df["phrases"] = df["phrases"].apply(
            lambda v: "; ".join(v) if isinstance(v, list) else (v or "")
        )

    if return_df:
        return df  # 提供给 Streamlit download_button 使用
    else:
        df.to_csv(filepath, index=False, encoding="utf-8-sig")
        return filepath

# 如果直接调用add_entry的话，会频繁调用_write_raw进而导致频繁调用_back_up，会产生非常多的备份信息。故import_csv_df只能完全重构
def import_csv_df(df: "pd.DataFrame") -> int:
    '''从 DataFrame 导入，要求列名至少包含：word, topic。
    可选字段：phonetic, meaning, example, phrases, familiarity, notes。
    phrases 可用分号 ';' 分隔。
    返回导入条数（合并后）。
    '''
    required = {"word", "topic"}
    if not required.issubset(set(c.lower() for c in df.columns)):
        raise ValueError("导入需要至少包含列：word, topic")

    # 统一小写列名 -> 原名映射
    cols_map = {c.lower(): c for c in df.columns}
    count = 0
    
    # 先读取当前数据
    rows = _read_raw()
    modified = False
    
    for _, row in df.iterrows():
        def get(name, default=""):
            return row.get(cols_map.get(name, name), default) if cols_map.get(name, name) in row else default

        phrases_cell = str(get("phrases", "") or "").strip()
        phrases = [p.strip() for p in phrases_cell.replace("\n", ";").split(";")] if phrases_cell else []

        try:
            familiarity = int(get("familiarity", 1) or 1)
        except Exception:
            familiarity = 1

        # 创建词条对象（使用Entry.create确保ID正确生成）
        entry = Entry.create(
            word=str(get("word", "")).strip(),
            phonetic=str(get("phonetic", "")).strip(),
            meaning=str(get("meaning", "")).strip(),
            topic=str(get("topic", "")).strip(),
            example=str(get("example", "")).strip(),
            phrases=phrases,
            familiarity=familiarity,
            notes=str(get("notes", "")).strip(),
        )
        
        if not entry.word or not entry.topic:
            continue  # 跳过无效数据
            
        # 使用与add_entry完全相同的去重和合并逻辑
        found = False
        for r in rows:
            if (r.get("word", "").lower() == entry.word.lower() and 
                r.get("topic", "").lower() == entry.topic.lower()):
                # 合并：更新释义/音标/例句/短语/备注，保留熟悉度较高的
                r["phonetic"] = entry.phonetic or r.get("phonetic", "")
                r["meaning"] = entry.meaning or r.get("meaning", "")
                r["example"] = entry.example or r.get("example", "")
                # 合并 phrases 去重
                existing_phrases = set(r.get("phrases", []) or [])
                new_phrases = set(entry.phrases)
                r["phrases"] = sorted(list(existing_phrases | new_phrases))
                r["notes"] = entry.notes or r.get("notes", "")
                r["familiarity"] = max(int(r.get("familiarity", 1) or 1), int(entry.familiarity or 1))
                r["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                found = True
                modified = True
                break
        
        if not found:
            # 新增词条
            rows.append(entry.to_dict())
            modified = True
        
        count += 1
    
    # 所有操作完成后，一次性写入和备份
    if modified:
        _write_raw(rows)
    
    return count