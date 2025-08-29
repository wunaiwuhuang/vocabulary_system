# 📚 Personal English Corpus

这是一个基于 **Python + Json + Streamlit** 搭建的简易英语学习语料库管理工具。
灵感来自《English Vocabulary in Use》的主题单元化设计，可以帮助你将单词、短语按照 **主题分类**，并记录释义、音标、熟悉程度等信息。

---

## ✨ 功能介绍

- 📝 **单词管理**

  - 按主题归类记录单词、短语
  - 支持添加中文释义、音标、例句、熟悉程度
- 📂 **数据库存储**

  - 所有数据存储在 `corpus.db`（SQLite 格式）中，轻量且可扩展
- 📊 **可视化与检索**

  - 通过 Streamlit 网页界面进行浏览、检索、过滤
  - 支持按主题、熟悉程度快速筛选
- 📤 **数据导出**

  - 支持导出为 Excel (`.xlsx`)
  - 便于备份或进一步加工使用

---

## 📦 部署方法

### 1. 克隆/下载项目

假设你把项目放在 `G:\corpus` 下：

```powershell
cd G:\corpus
```

目录结构示例：

```
corpus/
│── app/
│   ├── __init__.py
│   ├── streamlit_app.py
│   ├── config.py
│   ├── storage.py
│   └── models.py
│── data/
│   └── vocab.json
│── backups/
│── exports/
│── run_app.bat
│── README.md
│── requirements.txt
```

---

### 2. 创建 Conda 环境

```powershell
conda create -n corpus python=3.10
conda activate corpus
```

---

### 3. 安装依赖

```powershell
pip install -r requirements.txt
```

（若没有 `requirements.txt`，可手动安装：）

```powershell
pip install streamlit pandas sqlalchemy openpyxl
```

---

## 🚀 使用方法

### 方法 1：直接运行（命令行）

在项目根目录下执行：

```powershell
$env:PYTHONPATH="G:\corpus"
streamlit run app/streamlit_app.py
```

### 方法 2：使用批处理文件（推荐 ✅）

双击运行 `run_app.bat`，它会自动：

1. 激活 conda 环境
2. 设置 `PYTHONPATH`
3. 启动 Streamlit 服务

运行后，在浏览器中访问：

```
http://localhost:8501
```

即可使用你的英语语料库。

---

## 📖 示例工作流

1. 打开应用 → 选择主题（如 *Food & Drink*）
2. 添加单词（输入 `word, phonetic, meaning, phrase, familiarity`）
3. 数据实时保存到 `corpus.db`
4. 使用检索/过滤功能快速复习
5. 定期导出 Excel 进行备份

---

## 🛠️ 后续扩展计划

- [ ] 熟悉度学习曲线统计（类似 Anki 的复习曲线）
- [ ] 支持音频文件（单词发音）
- [ ] 增加 Markdown 笔记字段
- [ ] 移动端优化

---

## 📝 作者

- **Wu Guojia**
  Tianjin Medical University
  📧 wuguojia@tmu.edu.cn

---
