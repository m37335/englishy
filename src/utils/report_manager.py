"""
Report management utilities for Englishy.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ReportManager:
    """Manages English learning reports."""
    
    def __init__(self, reports_dir: str = "./data/reports"):
        """Initialize the report manager."""
        self.reports_dir = reports_dir
        self._ensure_reports_directory()
    
    def _ensure_reports_directory(self):
        """Ensure the reports directory exists."""
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def save_report(self, report_data: Dict[str, Any]) -> bool:
        """
        Save a report to disk.
        
        Args:
            report_data: Report data to save
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Generate unique ID and timestamp
            timestamp = datetime.now().isoformat()
            report_id = f"report_{int(datetime.now().timestamp())}"
            
            # Add metadata
            report_data.update({
                "id": report_id,
                "timestamp": timestamp,
                "created_at": timestamp
            })
            
            # Save to file
            filename = f"{report_id}.json"
            filepath = os.path.join(self.reports_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Report saved: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving report: {e}")
            return False
    
    def load_reports(self) -> List[Dict[str, Any]]:
        """
        Load all reports from disk.
        
        Returns:
            List of report data
        """
        try:
            reports = []
            
            if not os.path.exists(self.reports_dir):
                return reports
            
            for filename in os.listdir(self.reports_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.reports_dir, filename)
                    
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            report_data = json.load(f)
                            reports.append(report_data)
                    except Exception as e:
                        logger.error(f"Error loading report {filename}: {e}")
                        continue
            
            # Sort by timestamp (newest first)
            reports.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            return reports
            
        except Exception as e:
            logger.error(f"Error loading reports: {e}")
            return []
    
    def get_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific report by ID.
        
        Args:
            report_id: Report ID
        
        Returns:
            Report data or None if not found
        """
        try:
            filename = f"{report_id}.json"
            filepath = os.path.join(self.reports_dir, filename)
            
            if not os.path.exists(filepath):
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            logger.error(f"Error loading report {report_id}: {e}")
            return None
    
    def delete_report(self, report_id: str) -> bool:
        """
        Delete a report.
        
        Args:
            report_id: Report ID to delete
        
        Returns:
            True if successful, False otherwise
        """
        try:
            filename = f"{report_id}.json"
            filepath = os.path.join(self.reports_dir, filename)
            
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Report deleted: {filepath}")
                return True
            else:
                logger.warning(f"Report not found: {filepath}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting report {report_id}: {e}")
            return False
    
    def search_reports(self, query: str) -> List[Dict[str, Any]]:
        """
        Search reports by query.
        
        Args:
            query: Search query
        
        Returns:
            List of matching reports
        """
        try:
            all_reports = self.load_reports()
            matching_reports = []
            
            query_lower = query.lower()
            
            for report in all_reports:
                # Search in title, query, and content
                title = report.get('title', '').lower()
                report_query = report.get('query', '').lower()
                content = report.get('content', '').lower()
                
                if (query_lower in title or 
                    query_lower in report_query or 
                    query_lower in content):
                    matching_reports.append(report)
            
            return matching_reports
            
        except Exception as e:
            logger.error(f"Error searching reports: {e}")
            return []
    
    def get_report_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about stored reports.
        
        Returns:
            Dictionary with report statistics
        """
        try:
            reports = self.load_reports()
            
            if not reports:
                return {
                    "total_reports": 0,
                    "latest_report": None,
                    "average_report_length": 0
                }
            
            # Calculate statistics
            total_reports = len(reports)
            latest_report = reports[0] if reports else None
            
            # Calculate average content length
            content_lengths = []
            for report in reports:
                content = report.get('content', '')
                content_lengths.append(len(content))
            
            avg_length = sum(content_lengths) / len(content_lengths) if content_lengths else 0
            
            return {
                "total_reports": total_reports,
                "latest_report": latest_report.get('timestamp') if latest_report else None,
                "average_report_length": int(avg_length)
            }
            
        except Exception as e:
            logger.error(f"Error calculating report statistics: {e}")
            return {
                "total_reports": 0,
                "latest_report": None,
                "average_report_length": 0
            } 