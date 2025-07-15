"""
Configuration page for Englishy.
"""

import streamlit as st
import os
import json
import sys

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def create_config_page():
    """Create the config page function."""
    
    st.title("⚙️ Configuration")
    st.markdown("Configure Englishy settings")
    
    config_file = "./data/config.json"
    _ensure_config_directory()
    config = _load_config(config_file)
    
    # Create tabs for different settings
    tab1, tab2, tab3, tab4 = st.tabs(["API Settings", "Search Settings", "Data Settings", "Advanced"])
    
    with tab1:
        _render_api_settings(tab1, config, config_file)
    
    with tab2:
        _render_search_settings(tab2, config, config_file)
    
    with tab3:
        _render_data_settings(tab3, config, config_file)
    
    with tab4:
        _render_advanced_settings(tab4, config, config_file)


def _ensure_config_directory():
    """Ensure the config directory exists."""
    os.makedirs("./data", exist_ok=True)


def _load_config(config_file):
    """Load configuration from file."""
    default_config = {
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
        "web_search_engine": "DuckDuckGo",
        "language_model": "openai/gpt-4o-mini",
        "data_directory": "./data",
        "cache_directory": "./cache",
        "max_search_results": 10,
        "default_report_style": "Beginner-friendly",
        "enable_logging": True,
        "log_level": "INFO"
    }
    
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                saved_config = json.load(f)
                # Merge with defaults
                default_config.update(saved_config)
    except Exception as e:
        st.warning(f"Failed to load config: {e}")
    
    return default_config


def _save_config(config, config_file):
    """Save configuration to file."""
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Failed to save config: {e}")
        return False


def _render_api_settings(tab, config, config_file):
    """Render API settings tab."""
    st.subheader("🔑 API Configuration")
    
    with st.form("api_config_form"):
        openai_key = st.text_input(
            "OpenAI API Key",
            value=config.get("openai_api_key", ""),
            type="password",
            help="Your OpenAI API key for GPT models"
        )
        
        language_model = st.selectbox(
            "Language Model",
            ["openai/gpt-4o-mini", "openai/gpt-4o", "anthropic/claude-3-sonnet"],
            index=0 if config.get("language_model") == "openai/gpt-4o-mini" else
                  1 if config.get("language_model") == "openai/gpt-4o" else 2,
            help="Choose the language model for analysis"
        )
        
        if st.form_submit_button("Save API Settings"):
            config["openai_api_key"] = openai_key
            config["language_model"] = language_model
            
            if _save_config(config, config_file):
                st.success("✅ API settings saved!")
                # Update environment variable
                os.environ["OPENAI_API_KEY"] = openai_key
            else:
                st.error("❌ Failed to save API settings")


def _render_search_settings(tab, config, config_file):
    """Render search settings tab."""
    st.subheader("🔍 Search Configuration")
    
    with st.form("search_config_form"):
        web_search_engine = st.selectbox(
            "Web Search Engine",
            ["DuckDuckGo", "Google", "Tavily"],
            index=0 if config.get("web_search_engine") == "DuckDuckGo" else
                  1 if config.get("web_search_engine") == "Google" else 2,
            help="Choose your preferred web search engine"
        )
        
        max_search_results = st.slider(
            "Maximum Search Results",
            min_value=5,
            max_value=20,
            value=config.get("max_search_results", 10),
            help="Maximum number of search results to retrieve"
        )
        
        default_report_style = st.selectbox(
            "Default Report Style",
            ["Beginner-friendly", "Intermediate", "Advanced"],
            index=0 if config.get("default_report_style") == "Beginner-friendly" else
                  1 if config.get("default_report_style") == "Intermediate" else 2,
            help="Default style for generated reports"
        )
        
        if st.form_submit_button("Save Search Settings"):
            config["web_search_engine"] = web_search_engine
            config["max_search_results"] = max_search_results
            config["default_report_style"] = default_report_style
            
            if _save_config(config, config_file):
                st.success("✅ Search settings saved!")
            else:
                st.error("❌ Failed to save search settings")


def _render_data_settings(tab, config, config_file):
    """Render data settings tab."""
    st.subheader("💾 Data Configuration")
    
    with st.form("data_config_form"):
        data_directory = st.text_input(
            "Data Directory",
            value=config.get("data_directory", "./data"),
            help="Directory for storing English learning materials and reports"
        )
        
        cache_directory = st.text_input(
            "Cache Directory",
            value=config.get("cache_directory", "./cache"),
            help="Directory for caching embeddings and models"
        )
        
        # Show current data statistics
        st.markdown("**Current Data Statistics:**")
        
        # Count reports
        reports_dir = os.path.join(data_directory, "reports")
        report_count = 0
        if os.path.exists(reports_dir):
            report_count = len([f for f in os.listdir(reports_dir) if f.endswith('.json')])
        
        st.metric("Saved Reports", report_count)
        
        # Cache size
        cache_size = 0
        if os.path.exists(cache_directory):
            for root, dirs, files in os.walk(cache_directory):
                cache_size += sum(os.path.getsize(os.path.join(root, name)) for name in files)
        
        st.metric("Cache Size", f"{cache_size / 1024 / 1024:.1f} MB")
        
        if st.form_submit_button("Save Data Settings"):
            config["data_directory"] = data_directory
            config["cache_directory"] = cache_directory
            
            # Create directories if they don't exist
            os.makedirs(data_directory, exist_ok=True)
            os.makedirs(cache_directory, exist_ok=True)
            
            if _save_config(config, config_file):
                st.success("✅ Data settings saved!")
            else:
                st.error("❌ Failed to save data settings")


def _render_advanced_settings(tab, config, config_file):
    """Render advanced settings tab."""
    st.subheader("🔧 Advanced Configuration")
    
    with st.form("advanced_config_form"):
        enable_logging = st.checkbox(
            "Enable Logging",
            value=config.get("enable_logging", True),
            help="Enable detailed logging for debugging"
        )
        
        log_level = st.selectbox(
            "Log Level",
            ["DEBUG", "INFO", "WARNING", "ERROR"],
            index=1 if config.get("log_level") == "INFO" else
                  0 if config.get("log_level") == "DEBUG" else
                  2 if config.get("log_level") == "WARNING" else 3,
            help="Set the logging level"
        )
        
        # System information
        st.markdown("**System Information:**")
        st.code(f"""
Python Version: {sys.version}
Streamlit Version: {st.__version__}
Working Directory: {os.getcwd()}
Data Directory: {config.get('data_directory', './data')}
Cache Directory: {config.get('cache_directory', './cache')}
        """)
        
        if st.form_submit_button("Save Advanced Settings"):
            config["enable_logging"] = enable_logging
            config["log_level"] = log_level
            
            if _save_config(config, config_file):
                st.success("✅ Advanced settings saved!")
            else:
                st.error("❌ Failed to save advanced settings")
    
    # Additional tools
    st.subheader("🛠️ Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Clear Cache"):
            cache_dir = config.get("cache_directory", "./cache")
            if os.path.exists(cache_dir):
                import shutil
                shutil.rmtree(cache_dir)
                os.makedirs(cache_dir)
                st.success("✅ Cache cleared!")
            else:
                st.info("No cache directory found.")
    
    with col2:
        if st.button("Export Configuration"):
            config_json = json.dumps(config, ensure_ascii=False, indent=2)
            st.download_button(
                label="Download Config",
                data=config_json,
                file_name="englishy_config.json",
                mime="application/json"
            ) 