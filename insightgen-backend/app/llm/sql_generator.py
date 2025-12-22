"""SQL Generator using Google Gemini AI"""
import google.generativeai as genai
from app.config import settings
from app.db.schema_loader import get_schema_context
from app.llm.prompt_templates import SQL_GENERATION_PROMPT
import re

# Configure Google AI
genai.configure(api_key=settings.GOOGLE_API_KEY)


class SQLGenerator:
    """Generate SQL queries from natural language using Google Gemini"""
    
    def __init__(self):
        # Use Gemini 2.5 Flash - stable model with good rate limits
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def generate_sql(self, user_question: str) -> str:
        """
        Generate SQL query from natural language question
        
        Args:
            user_question: Natural language question from user
            
        Returns:
            Generated SQL query string
        """
        # Get database schema context
        schema_context = get_schema_context()
        
        # Format prompt
        prompt = SQL_GENERATION_PROMPT.format(
            schema_context=schema_context,
            user_question=user_question
        )
        
        # Generate SQL using Gemini
        response = self.model.generate_content(prompt)
        sql_query = response.text.strip()
        
        # Clean up the response (remove markdown formatting if present)
        sql_query = self._clean_sql(sql_query)
        
        return sql_query
    
    def _clean_sql(self, sql: str) -> str:
        """
        Clean SQL query by removing markdown formatting and extra whitespace
        
        Args:
            sql: Raw SQL string from LLM
            
        Returns:
            Cleaned SQL query
        """
        # Remove markdown code blocks
        sql = re.sub(r'```sql\s*', '', sql)
        sql = re.sub(r'```\s*', '', sql)
        
        # Remove extra whitespace
        sql = ' '.join(sql.split())
        
        # Remove trailing semicolon if present
        sql = sql.rstrip(';')
        
        return sql.strip()


# Global instance
sql_generator = SQLGenerator()
