"""
Research page for Englishy.
"""

import asyncio
import streamlit as st
import sys
import os
from typing import List, Dict, Any
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import dspy
from src.ai.openai_client import OpenAIClient
from src.ai.query_refiner import QueryRefiner
from src.ai.query_expander import QueryExpander
from src.ai.outline_creater import OutlineCreater
from src.ai.report_writer import (
    StreamLeadWriter, StreamSectionWriter, StreamConclusionWriter, 
    WriteLeadEnglish, WriteLeadJapanese, WriteSectionEnglish, WriteSectionJapanese,
    WriteConclusionEnglish, WriteConclusionJapanese, StreamRelatedTopicsWriter,
    StreamReferencesWriter, StreamIntegratedSectionWriter, StreamInlineReferencesWriter
)
from src.ai.mindmap_maker import MindMapMaker
from src.ai.grammar_analyzer import get_grammar_analyzer
from src.ai.llm_grammar_analyzer import LLMGrammarAnalyzer
from src.ai.english_extractor import get_english_extractor
from src.retriever.article_search.faiss import FAISSSearch
# from utils.report_manager import ReportManager
from src.utils.logging import logger
from src.utils.lm import load_lm
from src.utils.web_retriever import load_web_retriever
from utils.mindmap_utils import draw_mindmap


def create_research_page():
    """Create the research page function."""
    
    st.title("🔍 New Research")
    st.markdown("Start a new English learning research project")
    
    # Query input
    with st.form("research_form"):
        query = st.text_area(
            "What would you like to learn about?",
            placeholder="e.g., English grammar rules, vocabulary for business, pronunciation tips...",
            height=100,
            help="Describe what you want to learn or research"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            include_web_search = st.checkbox(
                "Include web search",
                value=True,
                help="Search the web for additional resources"
            )
            
            include_mindmap = st.checkbox(
                "Generate mind map",
                value=True,
                help="Create a visual mind map of the content"
            )
        
        with col2:
            search_depth = st.selectbox(
                "Search depth",
                ["Basic", "Comprehensive", "Deep"],
                index=1,
                help="How thorough should the search be?"
            )
            
            report_style = st.selectbox(
                "Report style",
                ["Beginner-friendly", "Intermediate", "Advanced"],
                index=0,
                help="Choose the complexity level of the report"
            )
        
        # LLM-based grammar analysis option
        use_llm_analysis = st.checkbox(
            "Use LLM-based grammar analysis (Recommended)",
            value=True,
            help="Use advanced AI for more accurate grammar structure analysis"
            )
        
        submitted = st.form_submit_button("🚀 Start Research")
        
        if submitted and query:
            # Store form data in session state
            st.session_state.research_data = {
                "query": query,
                "include_web_search": include_web_search,
                "include_mindmap": include_mindmap,
                "search_depth": search_depth,
                "report_style": report_style,
                "use_llm_analysis": use_llm_analysis
            }
            st.session_state.start_research = True

    # Handle research execution outside of form
    if hasattr(st.session_state, 'start_research') and st.session_state.start_research:
        data = st.session_state.research_data
        asyncio.run(_start_research(
            data["query"], 
            data["include_web_search"], 
            data["include_mindmap"], 
            data["search_depth"], 
            data["report_style"],
            data["use_llm_analysis"]
        ))
        st.session_state.start_research = False
    
    # Action buttons for completed research
    if hasattr(st.session_state, 'current_report'):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Save to Reports", key="save_reports"):
                st.success("Report already saved!")
        
        with col2:
            if st.button("🔄 Start New Research", key="new_research"):
                # Clear session state and rerun
                if hasattr(st.session_state, 'current_report'):
                    del st.session_state.current_report
                if hasattr(st.session_state, 'research_data'):
                    del st.session_state.research_data
                st.rerun()


async def _start_research(query, include_web_search, include_mindmap, search_depth, report_style, use_llm_analysis):
    """Start the research process."""
    # Initialize AI components
    try:
        # Initialize LM
        logger.info("Initializing LM...")
        lm = load_lm()
        
        # Remove dspy.settings.configure to avoid thread conflicts
        # All modules will use dspy.settings.context instead
        
        # Initialize AI modules with LM (without individual dspy.settings.configure calls)
        logger.info("Initializing QueryRefiner...")
        query_refiner = QueryRefiner(lm=lm)
        
        logger.info("Initializing QueryExpander...")
        query_expander = QueryExpander(lm=lm)
        
        logger.info("Initializing OutlineCreater...")
        outline_creater = OutlineCreater(lm=lm)
        
        logger.info("Initializing MindMapMaker...")
        mindmap_maker = MindMapMaker(lm=lm)
        
        # Initialize stream writers for English and Japanese
        logger.info("Initializing StreamLeadWriter...")
        lead_writer = StreamLeadWriter(lm=lm)
        
        logger.info("Initializing StreamSectionWriter...")
        section_writer = StreamSectionWriter(lm=lm)
        
        logger.info("Initializing StreamConclusionWriter...")
        conclusion_writer = StreamConclusionWriter(lm=lm)
        
        logger.info("Initializing StreamRelatedTopicsWriter...")
        related_topics_writer = StreamRelatedTopicsWriter(lm=lm)
        
        logger.info("Initializing StreamReferencesWriter...")
        references_writer = StreamReferencesWriter(lm=lm)
        
        logger.info("Initializing StreamIntegratedSectionWriter...")
        integrated_section_writer = StreamIntegratedSectionWriter(lm=lm)
        
        ai_initialized = True
        logger.info("AI components initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize AI components: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        ai_initialized = False
        st.error(f"AI initialization failed: {e}")
        return
    
    if not ai_initialized:
        st.error("❌ AI components not initialized. Please check your configuration.")
        return
    
    st.info("🚀 Starting research... This may take a few minutes.")
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Query refinement with grammar awareness
        status_text.text("Step 1/7: Refining query with grammar analysis...")
        progress_bar.progress(15)
        
        # Query refinement with grammar analysis
        refinement_result = query_refiner.grammar_aware_refiner(text=query)
        refined_query = refinement_result["refined_query"]
        
        st.info(f"Refined query: {refined_query}")
        
        # Display grammar analysis results
        if refinement_result.get("detected_grammar"):
            st.info(f"検出された文法: {', '.join(refinement_result['detected_grammar'])}")
        if refinement_result.get("related_items"):
            st.info(f"関連項目: {len(refinement_result['related_items'])}件の文法項目を検出")
        if refinement_result.get("translation") and refinement_result["translation"] != query:
            st.info(f"英語翻訳: {refinement_result['translation']}")
        
        # Step 2: Query expansion (before web search for better search optimization)
        status_text.text("Step 2/7: Expanding search topics for optimized web search...")
        progress_bar.progress(30)
        
        # Expand query to generate optimized search topics
        expanded_result = query_expander(
            query=refined_query,
            web_search_results=""  # No web search results yet
        )
        
        st.info(f"Generated {len(expanded_result.topics)} search topics for web search")
        if expanded_result.topics:
            st.info(f"Search topics: {', '.join(expanded_result.topics[:5])}{'...' if len(expanded_result.topics) > 5 else ''}")
        
        # Step 3: Web search with expanded topics
        status_text.text("Step 3/7: Searching for resources with expanded topics...")
        progress_bar.progress(45)
        
        web_search_results = []
        if include_web_search:
            web_search = load_web_retriever("DuckDuckGo")
            
            # Search with refined query and expanded topics
            all_search_queries = [refined_query] + expanded_result.topics[:3]  # Use top 3 topics
            logger.info(f"Starting web search with {len(all_search_queries)} queries: {all_search_queries}")
            
            for i, search_query in enumerate(all_search_queries):
                try:
                    logger.info(f"Search {i+1}: Searching for '{search_query}'")
                    results = web_search.search(search_query, k=4)  # 4 results per query
                    logger.info(f"Search {i+1}: Raw results count: {len(results)}")
                    web_search_results.extend(results)
                    st.info(f"Search {i+1}: Found {len(results)} results for '{search_query}'")
                except Exception as e:
                    logger.warning(f"Search failed for query '{search_query}': {e}")
                    import traceback
                    logger.warning(f"Search traceback: {traceback.format_exc()}")
            
            logger.info(f"Before deduplication: {len(web_search_results)} total results")
            
            # Remove duplicates and limit to 12 results
            seen_urls = set()
            unique_results = []
            for result in web_search_results:
                url = result.get('url', '')
                if url not in seen_urls and len(unique_results) < 12:
                    unique_results.append(result)
                    seen_urls.add(url)
                    logger.info(f"Added unique result: {result.get('title', 'No title')} - {url}")
                else:
                    logger.info(f"Skipped duplicate result: {result.get('title', 'No title')} - {url}")
            
            web_search_results = unique_results
            logger.info(f"After deduplication: {len(web_search_results)} unique results")
            
            st.info(f"Total unique search results: {len(web_search_results)}")
        
        # Step 4: Grammar analysis of search results
        status_text.text("Step 4/7: Analyzing grammar structures in search results...")
        progress_bar.progress(55)
        
        # Choose grammar analyzer based on user preference
        if use_llm_analysis:
            try:
                # Use LLM-based grammar analyzer
                llm_analyzer = LLMGrammarAnalyzer()
                grammar_analysis = llm_analyzer.analyze_text(refined_query)
                st.info("🤖 Using LLM-based grammar analysis for higher accuracy")
            except Exception as e:
                logger.warning(f"LLM analysis failed, falling back to rule-based: {e}")
                st.warning("⚠️ LLM analysis failed, using rule-based analysis instead")
                grammar_analyzer = get_grammar_analyzer()
                grammar_analysis = grammar_analyzer.analyze_text(refined_query)
        else:
            # Use traditional rule-based grammar analyzer
            grammar_analyzer = get_grammar_analyzer()
            grammar_analysis = grammar_analyzer.analyze_text(refined_query)
            st.info("📋 Using rule-based grammar analysis")
        
        # Display grammar analysis results with enhanced information
        if grammar_analysis.get('grammar_structures'):
            st.success(f"🔍 Grammar structures detected: {', '.join(grammar_analysis['grammar_structures'])}")
        
        if grammar_analysis.get('related_topics'):
            st.info(f"📚 Related topics: {', '.join(grammar_analysis['related_topics'])}")
        
        if grammar_analysis.get('key_points'):
            st.info("💡 Key learning points:")
            for point in grammar_analysis['key_points']:
                st.write(f"  • {point}")
        
        if grammar_analysis.get('error'):
            st.warning(f"⚠️ Grammar analysis warning: {grammar_analysis['error']}")
        
        # Step 5: Outline creation
        status_text.text("Step 5/7: Creating report outline...")
        progress_bar.progress(65)
        
        outline_result = outline_creater(
            query=refined_query,
            topics=expanded_result.topics,
            references=web_search_results
        )
        
        # Step 6: Report generation with integrated related topics
        status_text.text("Step 6/7: Generating report with integrated related topics...")
        progress_bar.progress(75)
        
        report = await _generate_report_with_integration(
            query=refined_query,
            outline=outline_result.outline,
            references=web_search_results,
            lead_writer=lead_writer,
            integrated_section_writer=integrated_section_writer,
            conclusion_writer=conclusion_writer
        )
        
        # Step 7: Related topics generation
        status_text.text("Step 7/7: Generating related topics...")
        progress_bar.progress(85)
        
        related_topics = ""
        try:
            async for chunk in related_topics_writer(query=query):
                related_topics += chunk
        except Exception as e:
            logger.error(f"Error generating related topics: {e}")
            related_topics = "関連文法事項の生成中にエラーが発生しました。"
        
        # Step 7.5: Generate references
        status_text.text("Step 7.5/7: Generating references...")
        progress_bar.progress(90)
        
        references_content = ""
        try:
            async for chunk in references_writer(
                query=query,
                report_content=report,
                search_results="\n".join([f"Title: {ref.get('title', '')}\nURL: {ref.get('url', '')}\nContent: {ref.get('snippet', '')}" for ref in web_search_results])
            ):
                references_content += chunk
        except Exception as e:
            logger.error(f"Error generating references: {e}")
            references_content = "参考文献の生成中にエラーが発生しました。"
        
        # Step 7.6: Generate inline references and append to report
        status_text.text("Step 7.6/7: Generating inline references...")
        progress_bar.progress(92)
        
        # 本文に引用番号と対応した参考文献リストを追加
        try:
            inline_references_writer = StreamInlineReferencesWriter()
            
            inline_references_content = ""
            async for chunk in inline_references_writer(
                report_content=report,
                search_results="\n".join([f"Title: {ref.get('title', '')}\nURL: {ref.get('url', '')}\nContent: {ref.get('snippet', '')}" for ref in web_search_results])
            ):
                inline_references_content += chunk
            
            # デバッグ: 生成されたインライン参考文献の内容をログ出力
            logger.info(f"Generated inline references content: {inline_references_content}")
            logger.info(f"Inline references content length: {len(inline_references_content)}")
            
            # 本文の最後に参考文献リストを追加
            if inline_references_content.strip():
                original_report_length = len(report)
                report += f"\n\n{inline_references_content}"
                logger.info(f"Inline references added to report. Original length: {original_report_length}, New length: {len(report)}")
                logger.info(f"Added content: {inline_references_content}")
            else:
                logger.info("No inline references generated - content was empty")
                
        except Exception as e:
            logger.error(f"Error generating inline references: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            # エラーが発生してもレポート生成は継続
        
        # Step 8: Mind map generation with related topics
        status_text.text("Step 8/8: Creating mind map with related topics...")
        progress_bar.progress(95)
        
        mindmap_content = ""
        if include_mindmap:
            try:
                # アウトライン構造からキーワードを抽出
                outline_keywords = []
                if hasattr(outline_result, 'outline') and outline_result.outline:
                    for section in outline_result.outline.section_outlines:
                        for subsection in section.subsection_outlines:
                            if hasattr(subsection, 'keywords') and subsection.keywords:
                                outline_keywords.extend(subsection.keywords)
                
                # 重複を除去
                unique_keywords = list(dict.fromkeys(outline_keywords))
                
                # デバッグ情報をログ出力
                logger.info(f"Generating mindmap with {len(unique_keywords)} keywords")
                logger.info(f"Report length: {len(report)} characters")
                logger.info(f"Related topics length: {len(related_topics)} characters")
                
                mindmap_result = mindmap_maker(
                    report=report,
                    outline_structure=outline_result.outline,
                    keywords=unique_keywords,
                    related_topics=related_topics
                )
                mindmap_content = mindmap_result.mindmap
                logger.info(f"Mindmap generated successfully with {len(unique_keywords)} keywords")
                logger.info(f"Generated mindmap content length: {len(mindmap_content)} characters")
                
                # マインドマップ内容の検証
                if not mindmap_content or mindmap_content.strip() == "":
                    logger.warning("Generated mindmap content is empty")
                    mindmap_content = "# マインドマップ\n## 内容\n### マインドマップの生成に失敗しました"
                elif "#" not in mindmap_content:
                    logger.warning("Generated mindmap content does not contain headers")
                    mindmap_content = "# マインドマップ\n## 内容\n### マインドマップの形式が正しくありません"
                    
            except Exception as e:
                logger.error(f"Error generating mind map: {e}")
                import traceback
                logger.error(f"Mindmap error traceback: {traceback.format_exc()}")
                mindmap_content = "# マインドマップ\n## エラー\n### マインドマップの生成中にエラーが発生しました"
        
        # Complete
        progress_bar.progress(100)
        status_text.text("✅ Research completed!")
        
        # Store results in session state
        st.session_state.current_report = {
            "query": query,
            "refined_query": refined_query,
            "grammar_analysis": grammar_analysis,
            "report": report,
            "mindmap": mindmap_content,
            "related_topics": related_topics,
            "references": references_content,
            "search_results": web_search_results,
            "processing_time": datetime.now().timestamp(),
            "search_depth": search_depth,
            "report_style": report_style,
            "use_llm_analysis": use_llm_analysis
        }
        
        # Display results
        _display_results(st.session_state.current_report)
        
    except Exception as e:
        logger.error(f"Research failed: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        st.error(f"❌ Research failed: {e}")
        progress_bar.progress(0)
        status_text.text("❌ Research failed")


async def _generate_report_with_integration(query: str, outline, references: List[str], lead_writer, integrated_section_writer, conclusion_writer) -> str:
    """Generate the final report with integrated related topics."""
    try:
        # Generate lead
        lead_content = ""
        async for chunk in lead_writer(query=query, title=outline.title, draft=outline.to_text()):
            lead_content += chunk
        
        # Generate sections with integrated related topics
        sections_content = ""
        for section_outline in outline.section_outlines:
            section_content = ""
            
            # セクション内のサブセクションからキーワードを収集
            section_keywords = []
            for subsection in section_outline.subsection_outlines:
                if hasattr(subsection, 'keywords') and subsection.keywords:
                    section_keywords.extend(subsection.keywords)
            
            # 重複を除去してキーワード文字列を作成
            unique_keywords = list(dict.fromkeys(section_keywords))
            keywords_text = ", ".join(unique_keywords) if unique_keywords else ""
            
            async for chunk in integrated_section_writer(
                query=query,
                references="\n".join([f"Title: {ref.get('title', '')}\nURL: {ref.get('url', '')}\nContent: {ref.get('snippet', '')}" for ref in references]),
                section_outline=section_outline.to_text(),
                related_topics="",  # Related topics will be integrated in the section content
                keywords=keywords_text  # 新規追加: キーワードを渡す
            ):
                section_content += chunk
            sections_content += section_content + "\n\n"
        
        # Generate conclusion
        conclusion_content = ""
        draft = f"{outline.title}\n\n{lead_content}\n\n{sections_content}"
        async for chunk in conclusion_writer(query=query, report_draft=draft):
            conclusion_content += chunk
        
        # Combine all parts
        final_report = f"{outline.title}\n\n{lead_content}\n\n{sections_content}## 結論\n{conclusion_content}"
        
        return final_report
        
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return f"レポート生成中にエラーが発生しました: {e}"


async def _generate_report(query: str, outline, references: List[str], lead_writer, section_writer, conclusion_writer) -> str:
    """Generate the final report."""
    try:
        # Generate lead
        lead_content = ""
        async for chunk in lead_writer(query=query, title=outline.title, draft=outline.to_text()):
            lead_content += chunk
        
        # Generate sections
        sections_content = ""
        for section_outline in outline.section_outlines:
            section_content = ""
            async for chunk in section_writer(
                query=query,
                references="\n".join([f"Title: {ref.get('title', '')}\nURL: {ref.get('url', '')}\nContent: {ref.get('snippet', '')}" for ref in references]),
                section_outline=section_outline.to_text()
            ):
                section_content += chunk
            sections_content += section_content + "\n\n"
        
        # Generate conclusion
        conclusion_content = ""
        draft = f"{outline.title}\n\n{lead_content}\n\n{sections_content}"
        async for chunk in conclusion_writer(query=query, report_draft=draft):
            conclusion_content += chunk
        
        # Combine all parts
        final_report = f"{outline.title}\n\n{lead_content}\n\n{sections_content}## 結論\n{conclusion_content}"
        
        return final_report
        
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return f"レポート生成中にエラーが発生しました: {e}"


def _display_results(report_data: Dict[str, Any]):
    """Display research results."""
    st.success("✅ Research completed successfully!")
    
    # Debug information
    st.write("Debug: Report data keys:", list(report_data.keys()))
    st.write("Debug: Report content length:", len(report_data.get('report', '')))
    st.write("Debug: Mindmap content length:", len(report_data.get('mindmap', '')))
    
    # Results summary
    st.subheader("📊 Research Results")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Processing Time", f"{report_data.get('processing_time', 0):.2f}s")
    with col2:
        st.metric("Search Results", len(report_data.get('search_results', [])))
    with col3:
        st.metric("Report Length", f"{len(report_data.get('report', ''))} chars")
    
    # Report preview
    st.subheader("📝 Report Preview")
    
    # Show first 1000 characters of report
    report_text = report_data.get('report', '')
    if len(report_text) > 1000:
        st.text_area("Report (first 1000 characters)", report_text[:1000] + "...", height=300, disabled=True)
        st.info("📄 View the full report below!")
    else:
        st.text_area("Report", report_text, height=300, disabled=True)
    
    # Display full report
    st.subheader("📄 Full Report")
    st.markdown(report_text)
    
    # Download report
    if st.button("📥 Download Report (Markdown)"):
        st.download_button(
            label="Download Report",
            data=report_text,
            file_name=f"english_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
    
    # Mind map display
    if report_data.get('mindmap'):
        st.subheader("🗺️ Mind Map")
        try:
            draw_mindmap(report_data['mindmap'])
            st.success("✅ Mind map generated successfully!")
            
            # Download mind map
            if st.button("📥 Download Mind Map"):
                st.download_button(
                    label="Download Mind Map",
                    data=report_data['mindmap'],
                    file_name=f"mindmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )
        except Exception as e:
            st.error(f"❌ Error displaying mind map: {e}")
            st.text_area("Mind Map Content (Text)", report_data['mindmap'], height=200, disabled=True)
    
    # English extraction display
    if report_data.get('extraction_result'):
        st.subheader("🔤 English Extraction")
        extraction_result = report_data['extraction_result']
        
        if extraction_result.get('has_english'):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**抽出された英文:**")
                for text in extraction_result.get('english_texts', []):
                    st.write(f"- {text}")
            
            with col2:
                st.write("**検出された文法構造:**")
                for structure in extraction_result.get('grammar_structures', []):
                    st.write(f"- {structure}")
            
            if extraction_result.get('grammar_details'):
                st.write("**文法詳細:**")
                for detail in extraction_result['grammar_details']:
                    st.write(f"- **{detail['text']}**: {detail['structure']}")
                    if detail.get('details', {}).get('summary'):
                        st.write(f"  - {detail['details']['summary']}")
        else:
            st.info("英文が検出されませんでした。元のクエリを使用しました。")
    
    # Grammar analysis display
    if report_data.get('grammar_analysis'):
        st.subheader("🔍 Grammar Analysis")
        
        # Show analysis method used
        analysis_method = "🤖 LLM-based" if report_data.get('use_llm_analysis') else "📋 Rule-based"
        st.info(f"Analysis method: {analysis_method}")
        
        grammar_analysis = report_data['grammar_analysis']
        
        col1, col2 = st.columns(2)
        with col1:
            if grammar_analysis.get('grammar_structures'):
                st.write("**検出された文法構造:**")
                for structure in grammar_analysis['grammar_structures']:
                    st.write(f"- {structure}")
        
        with col2:
            if grammar_analysis.get('key_points'):
                st.write("**学習ポイント:**")
                for point in grammar_analysis['key_points']:
                    st.write(f"- {point}")
        
        if grammar_analysis.get('related_topics'):
            st.write("**関連文法項目:**")
            for topic in grammar_analysis['related_topics']:
                st.write(f"- {topic}")
        
        # Show error if any
        if grammar_analysis.get('error'):
            st.warning(f"⚠️ Analysis warning: {grammar_analysis['error']}")
    
    # Related topics display
    if report_data.get('related_topics'):
        st.subheader("📚 Related Topics")
        st.markdown(report_data['related_topics'])
    
    # References display
    if report_data.get('references'):
        st.subheader("📖 References")
        st.markdown(report_data['references'])
    
    # Search results summary (showing 10 results as requested)
    if report_data.get('search_results'):
        st.subheader("🔍 Search Results Summary")
        with st.expander("View search results"):
            for i, result in enumerate(report_data['search_results'][:10]):  # Show 10 results
                st.write(f"**{i+1}. {result.get('title', 'No title')}**")
                st.write(f"URL: {result.get('url', 'No URL')}")
                st.write(f"Content: {result.get('snippet', 'No content')[:200]}...")
                st.write("---") 