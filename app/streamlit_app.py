import streamlit as st
import pandas as pd

from config import EXPORT_DIR
from storage import load_all, add_entry, update_familiarity, update_familiarity_entries, set_familiarity, set_familiarity_entries, delete_entry, delete_entries,  export_excel, import_csv_df
from models import Entry

st.set_page_config(page_title="个人英语语料库", page_icon="📚", layout="wide")

# ---- Helpers ----
def get_data():
    rows = load_all()
    df = pd.DataFrame(rows)
    if not df.empty and "phrases" in df.columns:
        df["phrases_text"] = df["phrases"].apply(lambda v: "; ".join(v) if isinstance(v, list) else (v or ""))
    else:
        if not df.empty:
            df["phrases_text"] = ""
    return rows, df

st.title("📚 个人英语语料库")
st.caption("按主题管理词汇 · 支持音标/释义/例句/实用短语 · 熟悉度 1-5")

tab_browse, tab_add, tab_import = st.tabs(["🔍 浏览&复习", "➕ 添加/编辑", "📥 导入 / 📤 导出"])

# ---- Browse Tab ----
with tab_browse:
    rows, df = get_data()
    if df.empty:
        st.info("当前词库为空，请在“添加/编辑”页添加一些词条。")
    else:
        # Filters
        topics = sorted([t for t in df["topic"].dropna().unique() if t])
        sel_topics = st.multiselect("按主题筛选", options=topics, default=[])
        fam_min, fam_max = st.slider("熟悉度范围", 1, 5, (1, 5))
        keyword = st.text_input("关键词搜索（匹配 word/meaning/example/phrases）")

        fdf = df.copy()
        if sel_topics:
            fdf = fdf[fdf["topic"].isin(sel_topics)]
        fdf = fdf[(fdf["familiarity"] >= fam_min) & (fdf["familiarity"] <= fam_max)]
        if keyword.strip():
            kw = keyword.strip().lower()
            def row_match(s):
                s = str(s or "").lower()
                return kw in s
            mask = (
                fdf["word"].apply(row_match) |
                fdf["meaning"].apply(row_match) |
                fdf["example"].apply(row_match) |
                fdf["phrases_text"].apply(row_match)
            )
            fdf = fdf[mask]

        st.subheader("词库列表")
        show_cols = ["id","word","phonetic","meaning","topic","example","phrases_text","familiarity","notes","updated_at"]
        st.dataframe(
            fdf[show_cols].rename(columns={"phrases_text":"phrases"}),
            use_container_width=True,
            hide_index=True,
        )

        # ---- Batch and Single Operations ----
        st.markdown("---")
        st.subheader("批量操作")
        selected_ids = st.multiselect(
            "选择要批量操作的词条",
            options=fdf["id"].tolist(),
            format_func=lambda x: f"{fdf.loc[fdf['id']==x, 'word'].values[0]} ({fdf.loc[fdf['id']==x, 'topic'].values[0]})"
        )
        if "refresh_batch" not in st.session_state:
            st.session_state.refresh_batch = False
        if selected_ids:
            st.info(f"已选择 {len(selected_ids)} 个词条")

        # 批量操作卡片
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):
                st.markdown("**熟悉度调整**")
                if st.button("📈 熟悉度 +1", use_container_width=True, key="batch_inc"):
                    updated = update_familiarity_entries(selected_ids, +1)
                    st.success(f"成功更新 {updated} 个词条")
                    st.session_state.refresh_batch = True
                if st.button("📉 熟悉度 -1", use_container_width=True, key="batch_dec"):
                    updated = update_familiarity_entries(selected_ids, -1)
                    st.success(f"成功更新 {updated} 个词条")
                    st.session_state.refresh_batch = True
        with col2:
            with st.container(border=True):
                st.markdown("**设定熟悉度**")
                batch_val = st.number_input("设定值 (1~5)", min_value=1, max_value=5, value=3, 
                                        key="batch_set_val", label_visibility="collapsed")
                if st.button("🎯 设定熟悉度", use_container_width=True, key="batch_set"):
                    updated = set_familiarity_entries(selected_ids, batch_val)
                    st.success(f"成功设定 {updated} 个词条为 {batch_val}")
                    st.session_state.refresh_batch = True
        with col3:
            with st.container(border=True):
                st.markdown("**删除操作**")
                if st.button("🗑️ 批量删除", use_container_width=True, type="secondary", key="batch_del"):
                    deleted_count = delete_entries(selected_ids)
                    st.success(f"成功删除 {deleted_count} 个词条")
                    st.session_state.refresh_batch = True

        st.markdown("---")
        st.subheader("单条操作")
        if "refresh_single" not in st.session_state:
            st.session_state.refresh_single = False
        sel_id = st.text_input("输入要操作的词条 ID", placeholder="从表格复制 ID", key="single_id_input")
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):
                st.markdown("**熟悉度调整**")
                if st.button("📈 熟悉度 +1", use_container_width=True, key="single_inc"):
                    if sel_id and update_familiarity(sel_id, +1):
                        st.success("已提升熟悉度 +1")
                        st.session_state.refresh_single = True
                    else:
                        st.warning("找不到该 ID")
                if st.button("📉 熟悉度 -1", use_container_width=True, key="single_dec"):
                    if sel_id and update_familiarity(sel_id, -1):
                        st.success("已降低熟悉度 -1")
                        st.session_state.refresh_single = True
                    else:
                        st.warning("找不到该 ID")
        with col2:
            with st.container(border=True):
                st.markdown("**设定熟悉度**")
                single_val = st.number_input("设定值 (1~5)", min_value=1, max_value=5, value=3, 
                                        key="single_val", label_visibility="collapsed")
                if st.button("🎯 设定熟悉度", use_container_width=True, key="single_set"):
                    if sel_id and set_familiarity(sel_id, single_val):
                        st.success(f"已设置熟悉度为 {single_val}")
                        st.session_state.refresh_single = True
                    else:
                        st.warning("找不到该 ID")
        with col3:
            with st.container(border=True):
                st.markdown("**删除操作**")
                if st.button("🗑️ 删除词条", use_container_width=True, type="secondary", key="single_del"):
                    if sel_id and delete_entry(sel_id):
                        st.success("已删除该词条")
                        st.session_state.refresh_single = True
                    else:
                        st.warning("找不到该 ID")

        # 页面刷新
        if st.session_state.refresh_batch or st.session_state.refresh_single:
            st.session_state.refresh_batch = False
            st.session_state.refresh_single = False
            st.rerun()

        # ---- 导出excel ----
        st.markdown("---")
        if st.button("📤 导出到 Excel"):
            path = export_excel()
            st.success(f"已导出到：{path}")
            st.caption("文件保存在项目的 exports/ 文件夹内。")

# ---- Add/Edit Tab ----
with tab_add:
    st.subheader("添加新词条")
    with st.form("add_form", clear_on_submit=True):
        c1, c2 = st.columns([2,1])
        with c1:
            word = st.text_input("单词/短语 *", placeholder="例如：appetite / set off")
            meaning = st.text_area("中文释义 *", placeholder="简洁明了，必要时可分条")
            example = st.text_area("例句", placeholder="可选")
        with c2:
            phonetic = st.text_input("音标", placeholder="[ˈæpɪtaɪt]")
            topic = st.text_input("主题 *", placeholder="Food / Travel / Health ...")
            familiarity = st.number_input("熟悉度（1~5）", min_value=1, max_value=5, value=1, step=1)
            notes = st.text_area("备注", height=80)

        phrases_text = st.text_area("实用短语（分号或换行分隔）", placeholder="have a good appetite; lose one's appetite")

        submitted = st.form_submit_button("添加")
        if submitted:
            phrases = [p.strip() for p in phrases_text.replace("\n", ";").split(";") if p.strip()]
            if not word.strip() or not topic.strip():
                st.error("请至少填写：单词/短语、主题")
            else:
                e = Entry.create(
                    word=word,
                    phonetic=phonetic,
                    meaning=meaning,
                    topic=topic,
                    example=example,
                    phrases=phrases,
                    familiarity=int(familiarity),
                    notes=notes,
                )
                add_entry(e)
                st.success(f"已添加：{word}（主题：{topic}）")

    st.caption("提示：同一主题下重复添加同名词条会**合并**释义/短语，并保留更高的熟悉度。")

# ---- Import/Export Tab ----
with tab_import:
    st.subheader("导入 CSV")
    st.caption("CSV 需包含列：word, topic（必填）；可选：phonetic, meaning, example, phrases, familiarity, notes。phrases 多条用分号 ';' 分隔。")
    up = st.file_uploader("选择 CSV 文件", type=["csv"])
    if up is not None:
        try:
            df = pd.read_csv(up)
            cnt = import_csv_df(df)
            st.success(f"导入完成，合并新增 {cnt} 条。")
        except Exception as e:
            st.error(f"导入失败：{e}")

    st.markdown("---")
    st.subheader("导出 Excel")
    if st.button("立即导出"):
        path = export_excel()
        st.success(f"已导出到：{path}")
        st.caption("文件保存在项目的 exports/ 文件夹内。")
