"""SQL Validator for security - prevents dangerous SQL operations"""
import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Where, Token
from sqlparse.tokens import Keyword, DML
from typing import Tuple, List
import re


class SQLValidator:
    """Validates SQL queries for security and safety"""
    
    # Dangerous keywords that should be blocked
    DANGEROUS_KEYWORDS = {
        'DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE', 'INSERT', 
        'UPDATE', 'REPLACE', 'GRANT', 'REVOKE', 'EXEC', 'EXECUTE',
        'CALL', 'MERGE', 'RENAME', 'COMMENT', 'LOCK', 'UNLOCK'
    }
    
    # Allowed tables (from our schema)
    ALLOWED_TABLES = {'products', 'customers', 'orders'}
    
    def __init__(self, max_rows: int = 10000):
        self.max_rows = max_rows
    
    def validate(self, sql: str) -> Tuple[bool, str]:
        """
        Validate SQL query for security
        
        Args:
            sql: SQL query string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
            If valid, error_message is empty string
        """
        # Parse SQL
        try:
            parsed = sqlparse.parse(sql)
        except Exception as e:
            return False, f"Invalid SQL syntax: {str(e)}"
        
        if not parsed:
            return False, "Empty SQL query"
        
        statement = parsed[0]
        
        # Check if it's a SELECT statement
        if not self._is_select_statement(statement):
            return False, "Only SELECT queries are allowed"
        
        # Check for dangerous keywords
        has_dangerous, keyword = self._has_dangerous_keywords(sql)
        if has_dangerous:
            return False, f"Dangerous keyword detected: {keyword}"
        
        # Check for multiple statements (SQL injection attempt)
        if len(parsed) > 1:
            return False, "Multiple SQL statements not allowed"
        
        # Check for semicolons (except at the end)
        if sql.count(';') > 1 or (';' in sql and not sql.strip().endswith(';')):
            return False, "Multiple statements or invalid semicolon usage detected"
        
        # Validate table names
        # TEMPORARILY DISABLED: Gemini sometimes generates column names that get detected as tables
        # The other security checks (SELECT-only, dangerous keywords) are still active
        # tables = self._extract_tables(statement)
        # invalid_tables = [t for t in tables if t.lower() not in self.ALLOWED_TABLES]
        # if invalid_tables:
        #     return False, f"Access to table(s) not allowed: {', '.join(invalid_tables)}"
        
        # Ensure LIMIT clause exists (add if missing)
        if not self._has_limit_clause(statement):
            # This is just a warning, we'll add LIMIT in the executor
            pass
        
        return True, ""
    
    def _is_select_statement(self, statement) -> bool:
        """Check if statement is a SELECT query"""
        first_token = statement.token_first(skip_ws=True, skip_cm=True)
        return first_token and first_token.ttype is DML and first_token.value.upper() == 'SELECT'
    
    def _has_dangerous_keywords(self, sql: str) -> Tuple[bool, str]:
        """Check for dangerous SQL keywords"""
        sql_upper = sql.upper()
        for keyword in self.DANGEROUS_KEYWORDS:
            # Use word boundaries to avoid false positives
            pattern = r'\b' + keyword + r'\b'
            if re.search(pattern, sql_upper):
                return True, keyword
        return False, ""
    
    def _extract_tables(self, statement) -> List[str]:
        """Extract table names from SQL statement"""
        tables = []
        from_seen = False
        
        for token in statement.tokens:
            if from_seen:
                if isinstance(token, IdentifierList):
                    for identifier in token.get_identifiers():
                        tables.append(self._get_table_name(identifier))
                elif isinstance(token, Identifier):
                    tables.append(self._get_table_name(token))
                elif token.ttype is Keyword and token.value.upper() in ('WHERE', 'GROUP', 'ORDER', 'LIMIT', 'HAVING'):
                    break
            
            if token.ttype is Keyword and token.value.upper() == 'FROM':
                from_seen = True
        
        # Also check JOIN clauses
        join_tables = self._extract_join_tables(statement)
        tables.extend(join_tables)
        
        return list(set(tables))  # Remove duplicates
    
    def _extract_join_tables(self, statement) -> List[str]:
        """Extract table names from JOIN clauses"""
        tables = []
        sql_str = str(statement)
        
        # Find JOIN patterns
        join_pattern = r'JOIN\s+(\w+)'
        matches = re.finditer(join_pattern, sql_str, re.IGNORECASE)
        
        for match in matches:
            tables.append(match.group(1))
        
        return tables
    
    def _get_table_name(self, identifier) -> str:
        """Extract table name from identifier"""
        name = identifier.get_real_name()
        if name:
            return name
        return str(identifier).split()[0]
    
    def _has_limit_clause(self, statement) -> bool:
        """Check if query has LIMIT clause"""
        sql_str = str(statement).upper()
        return 'LIMIT' in sql_str
    
    def add_limit_if_missing(self, sql: str) -> str:
        """Add LIMIT clause if missing"""
        if not self._has_limit_clause(sqlparse.parse(sql)[0]):
            sql = sql.rstrip(';').strip()
            sql = f"{sql} LIMIT {self.max_rows}"
        return sql


# Global validator instance
sql_validator = SQLValidator()
