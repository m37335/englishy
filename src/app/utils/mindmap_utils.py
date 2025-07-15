"""
Mindmap utilities for Englishy.
"""

import streamlit as st


def draw_mindmap(mindmap: str):
    """マインドマップを表示する関数"""
    if not mindmap or not isinstance(mindmap, str):
        return
    
    try:
        from streamlit_markmap import markmap
        
        data = f"""
---
markmap:
  pan: false
  zoom: false
---

{mindmap}
"""
        # ヘッダー数に基づいて高さを調整
        num_headers = len([line for line in mindmap.split("\n") if line.strip().startswith("#")])
        num_subheaders = len([line for line in mindmap.split("\n") if line.strip().startswith("##")])
        height = 15 * (num_subheaders + num_headers) + 200
        return markmap(data, height=height)
    except ImportError:
        st.error("streamlit-markmap is not installed")
        return None 