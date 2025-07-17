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
    StreamReferencesWriter, StreamIntegratedSectionWriter
)
from src.ai.mindmap_maker import MindMapMaker
from src.ai.grammar_analyzer import get_grammar_analyzer
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
        
        submitted = st.form_submit_button("🚀 Start Research")
        
        if submitted and query:
            # Store form data in session state
            st.session_state.research_data = {
                "query": query,
                "include_web_search": include_web_search,
                "include_mindmap": include_mindmap,
                "search_depth": search_depth,
                "report_style": report_style
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
            data["report_style"]
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


async def _start_research(query, include_web_search, include_mindmap, search_depth, report_style):
    """Start the research process."""
    # Initialize AI components
    try:
        # Initialize LM
        logger.info("Initializing LM...")
        lm = load_lm()
        
        # Initialize AI modules with LM
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
        refinement_result = query_refiner.grammar_aware_refiner(query=query)
        refined_query = refinement_result["refined_query"]
        
        st.info(f"Refined query: {refined_query}")
        
        # Display grammar analysis results
        if refinement_result.get("detected_grammar"):
            st.info(f"検出された文法: {', '.join(refinement_result['detected_grammar'])}")
        if refinement_result.get("related_items"):
            st.info(f"関連項目: {len(refinement_result['related_items'])}件の文法項目を検出")
        if refinement_result.get("translation") and refinement_result["translation"] != query:
            st.info(f"英語翻訳: {refinement_result['translation']}")
        
        # Step 2: Web search
        status_text.text("Step 2/7: Searching for resources...")
        progress_bar.progress(30)
        
        web_search_results = []
        if include_web_search:
            web_search = load_web_retriever("DuckDuckGo")
            # 検索結果を12件に増やす（要求された10件程度）
            web_search_results = web_search.search(refined_query, k=12)
        
        # Step 3: Grammar analysis
        status_text.text("Step 3/7: Analyzing grammar structures...")
        progress_bar.progress(45)
        
        grammar_analyzer = get_grammar_analyzer()
        grammar_analysis = grammar_analyzer.analyze_text(refined_query)
        st.info(f"Grammar structures detected: {', '.join(grammar_analysis['grammar_structures'])}")
        
        # Step 4: Query expansion
        status_text.text("Step 4/7: Expanding search topics...")
        progress_bar.progress(55)
        
        # Prepare web search results for expansion
        web_results_text = ""
        for i, result in enumerate(web_search_results):
            web_results_text += f"Result {i+1}:\n"
            web_results_text += f"Title: {result.get('title', '')}\n"
            web_results_text += f"URL: {result.get('url', '')}\n"
            web_results_text += f"Content: {result.get('snippet', '')}\n\n"
        
        # Expand query based on search results
        expanded_result = query_expander(
            query=refined_query,
            web_search_results=web_results_text
        )
        
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
        
        # Step 8: Mind map generation with related topics
        status_text.text("Step 8/8: Creating mind map with related topics...")
        progress_bar.progress(95)
        
        mindmap_content = ""
        if include_mindmap:
            try:
                mindmap_result = mindmap_maker(report=report, related_topics=related_topics)
                mindmap_content = mindmap_result.mindmap
            except Exception as e:
                logger.error(f"Error generating mind map: {e}")
                mindmap_content = "マインドマップの生成中にエラーが発生しました。"
        
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
            "report_style": report_style
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
            async for chunk in integrated_section_writer(
                query=query,
                references="\n".join([f"Title: {ref.get('title', '')}\nURL: {ref.get('url', '')}\nContent: {ref.get('snippet', '')}" for ref in references]),
                section_outline=section_outline.to_text(),
                related_topics=""  # Related topics will be integrated in the section content
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