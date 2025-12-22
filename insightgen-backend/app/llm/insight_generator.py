"""Insight generator using Google Gemini"""
import google.generativeai as genai
from app.config import settings
from app.llm.prompt_templates import INSIGHT_GENERATION_PROMPT
import json
from typing import List, Dict, Any

# Configure Google AI
genai.configure(api_key=settings.GOOGLE_API_KEY)


class InsightGenerator:
    """Generate business insights from query results using Google Gemini"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def generate_insights(
        self,
        user_question: str,
        sql_query: str,
        data: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Generate actionable business insights from data
        
        Args:
            user_question: Original user question
            sql_query: SQL query that was executed
            data: Query results
            
        Returns:
            List of insight strings
        """
        if not data:
            return ["No data available to generate insights."]
        
        # Create data summary
        data_summary = self._create_data_summary(data)
        
        # Format prompt
        prompt = INSIGHT_GENERATION_PROMPT.format(
            user_question=user_question,
            sql_query=sql_query,
            data_summary=data_summary
        )
        
        # Generate insights
        response = self.model.generate_content(prompt)
        insights_text = response.text.strip()
        
        # Parse insights
        try:
            insights = self._parse_insights(insights_text)
            return insights
        except Exception as e:
            print(f"Error parsing insights: {e}")
            return self._default_insights(data)
    
    def _create_data_summary(self, data: List[Dict[str, Any]]) -> str:
        """Create a summary of the data for the LLM"""
        summary_parts = []
        
        # Number of rows
        summary_parts.append(f"Total rows: {len(data)}")
        
        # Show first few rows
        preview = json.dumps(data[:10], indent=2, default=str)
        summary_parts.append(f"Data preview:\n{preview}")
        
        # Column statistics (if numeric columns exist)
        if data:
            numeric_stats = self._calculate_numeric_stats(data)
            if numeric_stats:
                summary_parts.append(f"Numeric statistics:\n{json.dumps(numeric_stats, indent=2)}")
        
        return "\n\n".join(summary_parts)
    
    def _calculate_numeric_stats(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate basic statistics for numeric columns"""
        stats = {}
        
        if not data:
            return stats
        
        # Get numeric columns
        first_row = data[0]
        numeric_cols = [
            col for col, val in first_row.items()
            if isinstance(val, (int, float))
        ]
        
        # Calculate stats for each numeric column
        for col in numeric_cols:
            values = [row[col] for row in data if col in row and row[col] is not None]
            if values:
                stats[col] = {
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                    "total": sum(values)
                }
        
        return stats
    
    def _parse_insights(self, insights_text: str) -> List[str]:
        """Parse insights from LLM response"""
        # Remove markdown formatting
        insights_text = insights_text.replace('```json', '').replace('```', '').strip()
        
        # Parse JSON array
        insights = json.loads(insights_text)
        
        # Ensure it's a list
        if not isinstance(insights, list):
            raise ValueError("Insights must be a list")
        
        return insights
    
    def _default_insights(self, data: List[Dict[str, Any]]) -> List[str]:
        """Generate basic insights when AI generation fails"""
        insights = []
        
        insights.append(f"Query returned {len(data)} rows of data.")
        
        # Try to find numeric columns and report totals
        if data:
            first_row = data[0]
            numeric_cols = [
                col for col, val in first_row.items()
                if isinstance(val, (int, float))
            ]
            
            for col in numeric_cols[:2]:  # Limit to first 2 numeric columns
                values = [row[col] for row in data if col in row and row[col] is not None]
                if values:
                    total = sum(values)
                    insights.append(f"Total {col}: {total:,.2f}")
        
        return insights


# Global instance
insight_generator = InsightGenerator()
