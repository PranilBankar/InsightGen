"""Dashboard builder service - orchestrates the entire dashboard generation pipeline"""
from sqlalchemy.orm import Session
from app.llm import sql_generator, viz_generator, insight_generator
from app.services.query_executor import query_executor
from typing import Dict, Any
import uuid


class DashboardBuilder:
    """Orchestrates dashboard generation from natural language query"""
    
    def build_dashboard(
        self, 
        db: Session, 
        user_question: str
    ) -> Dict[str, Any]:
        """
        Build complete dashboard from natural language question
        
        Pipeline:
        1. Generate SQL from natural language
        2. Validate and execute SQL
        3. Generate visualization config
        4. Generate insights
        5. Return complete dashboard JSON
        
        Args:
            db: Database session
            user_question: Natural language question from user
            
        Returns:
            Complete dashboard configuration dictionary
        """
        # Step 1: Generate SQL
        sql_query = sql_generator.generate_sql(user_question)
        
        # Step 2: Execute query
        data, metadata = query_executor.execute_query(db, sql_query)
        
        # Step 3: Generate visualization config
        viz_config = viz_generator.generate_viz_config(sql_query, data)
        
        # Step 4: Generate insights
        insights = insight_generator.generate_insights(
            user_question, 
            sql_query, 
            data
        )
        
        # Step 5: Build dashboard response
        dashboard = {
            "dashboard_id": str(uuid.uuid4()),
            "query": user_question,
            "sql": sql_query,
            "charts": [
                {
                    "id": "chart_1",
                    "type": viz_config.get("chart_type", "bar"),
                    "title": viz_config.get("title", "Data Visualization"),
                    "data": data,
                    "config": {
                        "x_axis": viz_config.get("x_axis"),
                        "y_axis": viz_config.get("y_axis"),
                        "group_by": viz_config.get("group_by"),
                        "aggregation": viz_config.get("aggregation", "none")
                    }
                }
            ],
            "insights": insights,
            "metadata": metadata
        }
        
        return dashboard


# Global instance
dashboard_builder = DashboardBuilder()
