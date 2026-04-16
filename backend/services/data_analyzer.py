import pandas as pd
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings

class DataAnalyzer:
    """
    Analyzes CSV/Excel data using pandas and LLM.
    Performs computations and generates natural language explanations.
    """
    
    def __init__(self):
        """Initialize LLM for generating explanations"""
        self.llm = ChatGoogleGenerativeAI(
            model=f"models/{settings.model_name}",
            temperature=settings.temperature,
            google_api_key=settings.google_api_key
        )
        self.dataframes = {}  # Store loaded dataframes by filename
    
    def load_data(self, file_path: str, filename: str):
        """
        Load data file into memory.
        
        Args:
            file_path: Path to CSV/Excel file
            filename: Original filename for reference
        """
        ext = file_path.lower().split('.')[-1]
        
        if ext == 'csv':
            df = pd.read_csv(file_path)
        elif ext in ['xlsx', 'xls']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        
        self.dataframes[filename] = df
    
    def analyze(self, question: str, filename: str = None) -> Dict[str, Any]:
        """
        Analyze data based on user question.
        
        Args:
            question: User's analytical question
            filename: Specific file to analyze (if None, uses most recent)
            
        Returns:
            Dict with analysis results and explanation
        """
        # Get dataframe
        if filename and filename in self.dataframes:
            df = self.dataframes[filename]
        elif self.dataframes:
            df = list(self.dataframes.values())[-1]  # Most recent
            filename = list(self.dataframes.keys())[-1]
        else:
            return {
                "answer": "No data files have been uploaded yet.",
                "analysis": None
            }
        
        # Perform analysis based on question keywords
        analysis_result = self._perform_analysis(df, question)
        
        # Generate natural language explanation
        explanation = self._generate_explanation(df, question, analysis_result)
        
        return {
            "answer": explanation,
            "analysis": analysis_result,
            "source": filename
        }
    
    def _perform_analysis(self, df: pd.DataFrame, question: str) -> Dict[str, Any]:
        """
        Execute pandas operations based on question.
        Uses keyword detection for simplicity.
        """
        question_lower = question.lower()
        result = {}
        
        # Basic statistics
        result["shape"] = {"rows": len(df), "columns": len(df.columns)}
        result["columns"] = df.columns.tolist()
        
        # Detect numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        # Total/Sum operations
        if any(word in question_lower for word in ['total', 'sum', 'add']):
            if numeric_cols:
                result["totals"] = df[numeric_cols].sum().to_dict()
        
        # Average/Mean operations
        if any(word in question_lower for word in ['average', 'mean', 'avg']):
            if numeric_cols:
                result["averages"] = df[numeric_cols].mean().to_dict()
        
        # Count operations
        if 'count' in question_lower or 'how many' in question_lower:
            result["counts"] = len(df)
        
        # Max/Min operations
        if 'max' in question_lower or 'highest' in question_lower:
            if numeric_cols:
                result["max_values"] = df[numeric_cols].max().to_dict()
        
        if 'min' in question_lower or 'lowest' in question_lower:
            if numeric_cols:
                result["min_values"] = df[numeric_cols].min().to_dict()
        
        # Anomaly detection (simple: values > 2 std devs)
        if 'anomal' in question_lower or 'outlier' in question_lower:
            anomalies = {}
            for col in numeric_cols:
                mean = df[col].mean()
                std = df[col].std()
                outliers = df[abs(df[col] - mean) > 2 * std]
                if len(outliers) > 0:
                    anomalies[col] = len(outliers)
            result["anomalies"] = anomalies
        
        # Sample data
        result["sample_data"] = df.head(5).to_dict('records')
        
        return result
    
    def _generate_explanation(self, df: pd.DataFrame, question: str, analysis: Dict[str, Any]) -> str:
        """
        Use LLM to generate natural language explanation of analysis.
        """
        prompt = f"""You are a data analyst. Based on the following data analysis results, 
provide a clear, concise answer to the user's question.

User Question: {question}

Dataset Info:
- Rows: {analysis['shape']['rows']}
- Columns: {analysis['shape']['columns']}
- Column names: {', '.join(analysis['columns'])}

Analysis Results:
{self._format_analysis(analysis)}

Provide a natural language answer that directly addresses the question."""

        response = self.llm.invoke(prompt)
        return response.content
    
    def _format_analysis(self, analysis: Dict[str, Any]) -> str:
        """Format analysis results for LLM prompt"""
        formatted = []
        
        if "totals" in analysis:
            formatted.append(f"Totals: {analysis['totals']}")
        if "averages" in analysis:
            formatted.append(f"Averages: {analysis['averages']}")
        if "max_values" in analysis:
            formatted.append(f"Maximum values: {analysis['max_values']}")
        if "min_values" in analysis:
            formatted.append(f"Minimum values: {analysis['min_values']}")
        if "anomalies" in analysis:
            formatted.append(f"Anomalies detected: {analysis['anomalies']}")
        
        return "\n".join(formatted) if formatted else "No specific computations performed."
