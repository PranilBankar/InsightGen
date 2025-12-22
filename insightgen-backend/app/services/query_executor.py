"""Query executor service - safely executes SQL queries"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.config import settings
from app.security import sql_validator
from typing import List, Dict, Any, Tuple
import time


class QueryExecutor:
    """Execute SQL queries safely with timeout and row limits"""
    
    def __init__(self):
        self.timeout = settings.QUERY_TIMEOUT_SECONDS
        self.max_rows = settings.MAX_QUERY_ROWS
    
    def execute_query(
        self, 
        db: Session, 
        sql: str
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Execute SQL query and return results with metadata
        
        Args:
            db: Database session
            sql: SQL query to execute
            
        Returns:
            Tuple of (results, metadata)
            - results: List of dictionaries (rows)
            - metadata: Dict with execution info
        """
        # Validate SQL
        is_valid, error_msg = sql_validator.validate(sql)
        if not is_valid:
            raise ValueError(f"SQL validation failed: {error_msg}")
        
        # Add LIMIT if missing
        sql = sql_validator.add_limit_if_missing(sql)
        
        # Execute query with timing
        start_time = time.time()
        
        try:
            # Set statement timeout
            db.execute(text(f"SET statement_timeout = {self.timeout * 1000}"))
            
            # Execute query
            result = db.execute(text(sql))
            
            # Fetch results
            rows = result.fetchall()
            
            # Convert to list of dictionaries
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in rows]
            
            # Calculate execution time
            execution_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Create metadata
            metadata = {
                "rows_returned": len(data),
                "execution_time_ms": round(execution_time, 2),
                "columns": list(columns)
            }
            
            return data, metadata
            
        except Exception as e:
            raise RuntimeError(f"Query execution failed: {str(e)}")


# Global instance
query_executor = QueryExecutor()
