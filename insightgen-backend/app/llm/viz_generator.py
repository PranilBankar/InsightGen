"""Visualization configuration generator using Google Gemini"""
import google.generativeai as genai
from app.config import settings
from app.llm.prompt_templates import VISUALIZATION_GENERATION_PROMPT
import json
from typing import Dict, Any, List

# Configure Google AI
genai.configure(api_key=settings.GOOGLE_API_KEY)


class VizGenerator:
    """Generate visualization configurations using Google Gemini"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def generate_viz_config(
        self, 
        sql_query: str, 
        data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate visualization configuration based on query and data
        
        Args:
            sql_query: The SQL query that was executed
            data: Query results (list of dictionaries)
            
        Returns:
            Visualization configuration dictionary
        """
        if not data:
            return self._default_config()
        
        # Get column names
        column_names = list(data[0].keys())
        
        # Create data preview (first 5 rows)
        data_preview = json.dumps(data[:5], indent=2, default=str)
        
        # Format prompt
        prompt = VISUALIZATION_GENERATION_PROMPT.format(
            sql_query=sql_query,
            data_preview=data_preview,
            column_names=", ".join(column_names)
        )
        
        # Generate visualization config
        response = self.model.generate_content(prompt)
        config_text = response.text.strip()
        
        # Parse JSON response
        try:
            config = self._parse_config(config_text)
            return config
        except Exception as e:
            print(f"Error parsing viz config: {e}")
            return self._default_config(column_names)
    
    def _parse_config(self, config_text: str) -> Dict[str, Any]:
        """Parse and validate visualization config from LLM response"""
        # Remove markdown formatting if present
        config_text = config_text.replace('```json', '').replace('```', '').strip()
        
        # Parse JSON
        config = json.loads(config_text)
        
        # Validate required fields
        required_fields = ['chart_type', 'title', 'x_axis', 'y_axis']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field: {field}")
        
        return config
    
    def _default_config(self, column_names: List[str] = None) -> Dict[str, Any]:
        """Return default visualization config when generation fails"""
        if column_names and len(column_names) >= 2:
            return {
                "chart_type": "bar",
                "title": "Data Visualization",
                "x_axis": column_names[0],
                "y_axis": column_names[1],
                "group_by": None,
                "aggregation": "none"
            }
        
        return {
            "chart_type": "bar",
            "title": "Data Visualization",
            "x_axis": "category",
            "y_axis": "value",
            "group_by": None,
            "aggregation": "none"
        }


# Global instance
viz_generator = VizGenerator()
