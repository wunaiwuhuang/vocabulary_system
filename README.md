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

### 工作流程

#### 1. 启动
浏览器会打开一个本地页面（若未自动打开，把终端里显示的本地地址复制到浏览器）。

#### 2. 网页端功能

**🔍 浏览 & 复习**  
- 按主题和熟悉度筛选  
- 关键字搜索（匹配单词、释义、例句、短语）  
- 支持快速操作：  
  - 「熟悉度 +1 / −1」  
  - 「直接设定熟悉度」  
  - 「删除」词条  

**➕ 添加 / 编辑**  
- 填写「单词/短语」「主题」「释义」等  
- 实用短语支持多条（分号或换行分隔）  
- 系统会在同主题下自动合并重名词条（合并释义/短语，并保留更高熟悉度）  

**📥 导入 / 📤 导出**  
- **导入**：上传 CSV 文件  
  - 至少包含列：`word, topic`  
  - 可选列：`phonetic, meaning, example, phrases, familiarity, notes`  
  - `phrases` 多条用分号分隔  
- **导出**：一键导出到 `exports/vocab_export.xlsx`，可直接用 Excel 打开或打印  

#### 3. 数据与备份

- **主数据**：`G:\corpus\data\vocab.json`（UTF-8 JSON）  
- **备份**：每次写入前自动备份到 `G:\corpus\backups\`（时间戳文件名）  
- **导出文件**：保存在 `G:\corpus\exports\`  

#### 4. 小贴士与扩展

- **主题命名**：尽量稳定（如 `Food`、`Travel`、`Health`），后期检索更方便  
- **熟悉度建议**：1 = 陌生，3 = 一般，5 = 非常熟  
- **批量导入**：已有 Excel/表格时另存为 CSV，确保表头符合： word, phonetic, meaning, topic, example, phrases, familiarity, notes（至少包含 `word, topic`）

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
