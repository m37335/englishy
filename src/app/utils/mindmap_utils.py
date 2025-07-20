"""
Mindmap utilities for Englishy.
"""

import streamlit as st


def draw_mindmap(mindmap: str):
    """マインドマップを表示する関数"""
    if not mindmap or not isinstance(mindmap, str):
        st.info("マインドマップの内容がありません")
        return
    
    # デバッグ: 元のマインドマップ内容を表示
    with st.expander("🔍 マインドマップ生成内容の確認", expanded=False):
        st.text("元のマインドマップ内容:")
        st.code(mindmap, language="markdown")
    
    # マインドマップの内容をクリーンアップ
    cleaned_mindmap = _clean_mindmap_content(mindmap)
    
    # クリーンアップ後の内容が空でないかチェック
    if not cleaned_mindmap.strip():
        st.info("マインドマップの内容が空です")
        return
    
    # デバッグ: クリーンアップ後の内容を表示
    with st.expander("🔧 クリーンアップ後のマインドマップ内容", expanded=False):
        st.text("クリーンアップ後の内容:")
        st.code(cleaned_mindmap, language="markdown")
    
    try:
        from streamlit_markmap import markmap
        
        data = f"""
---
markmap:
  pan: false
  zoom: false
  colorFreezeLevel: 2
  initialExpandLevel: 1
  maxWidth: 800
---

{cleaned_mindmap}
"""
        # ヘッダー数に基づいて高さを調整
        num_headers = len([line for line in cleaned_mindmap.split("\n") if line.strip().startswith("#")])
        num_subheaders = len([line for line in cleaned_mindmap.split("\n") if line.strip().startswith("##")])
        height = max(400, 20 * (num_subheaders + num_headers) + 200)
        
        # デバッグ: 最終的なmarkmapデータを表示
        with st.expander("📊 最終的なmarkmapデータ", expanded=False):
            st.text("最終的なmarkmapデータ:")
            st.code(data, language="yaml")
        
        # マインドマップを表示
        st.info("マインドマップを表示中...")
        markmap(data, height=height)
        
    except ImportError:
        st.error("streamlit-markmap is not installed. Please install it with: pip install streamlit-markmap")
        st.info("マインドマップの内容（Markdown形式）:")
        st.code(cleaned_mindmap, language="markdown")
        return None
    except Exception as e:
        st.error(f"マインドマップの表示中にエラーが発生しました: {str(e)}")
        st.info("マインドマップの内容（Markdown形式）:")
        st.code(cleaned_mindmap, language="markdown")
        return None


def _clean_mindmap_content(mindmap: str) -> str:
    """マインドマップの内容をクリーンアップする"""
    lines = mindmap.split("\n")
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 深すぎる階層（####以上）を###に変換
        if line.startswith("####"):
            line = "###" + line[4:]
        elif line.startswith("#####"):
            line = "###" + line[5:]
        elif line.startswith("######"):
            line = "###" + line[6:]
        
        cleaned_lines.append(line)
    
    return "\n".join(cleaned_lines) 