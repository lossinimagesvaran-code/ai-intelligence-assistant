"""
Script to generate synthetic sample datasets for testing the AI Project Intelligence Assistant.
Generates both PDF documents and CSV data files.
"""

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import random
from datetime import datetime, timedelta

def generate_project_report_pdf():
    """Generate a sample project report PDF"""
    filename = "sample_project_report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title = Paragraph("AI Project Intelligence Assistant - Project Report", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.3*inch))
    
    sections = [
        ("Executive Summary", 
         "This project aims to develop an AI-powered intelligence assistant capable of analyzing both "
         "structured and unstructured data. The system leverages Retrieval-Augmented Generation (RAG) "
         "to provide accurate answers to user queries based on uploaded documents and datasets. "
         "The total project budget is $250,000 with an expected completion timeline of 6 months."),
        
        ("Project Objectives",
         "1. Develop a robust document processing pipeline supporting PDF, CSV, and Excel formats. "
         "2. Implement a multi-agent architecture with specialized agents for document Q&A and data analysis. "
         "3. Create an intuitive user interface for seamless interaction. "
         "4. Ensure scalability and production-ready deployment capabilities. "
         "5. Maintain comprehensive documentation and testing coverage."),
        
        ("Technical Architecture",
         "The system is built using a modern tech stack including Python FastAPI for the backend, "
         "React for the frontend, and LangChain for orchestrating LLM interactions. "
         "The RAG pipeline uses OpenAI embeddings stored in a Chroma vector database. "
         "A router agent intelligently directs queries to either the Document Q&A Agent or "
         "Data Analysis Agent based on query content and available data sources."),
        
        ("Budget Breakdown",
         "Development costs: $150,000 including backend ($60,000), frontend ($40,000), "
         "and AI/ML components ($50,000). Infrastructure and cloud services: $30,000. "
         "Testing and QA: $25,000. Documentation and training: $20,000. "
         "Contingency reserve: $25,000. Total project budget: $250,000."),
        
        ("Risk Assessment",
         "Key risks include potential API rate limiting from OpenAI, data privacy concerns "
         "with sensitive documents, and scalability challenges with large document volumes. "
         "Mitigation strategies include implementing caching mechanisms, ensuring GDPR compliance, "
         "and designing for horizontal scalability from the outset."),
        
        ("Timeline and Milestones",
         "Month 1-2: Core backend development and RAG pipeline implementation. "
         "Month 3: Agent system development and integration. "
         "Month 4: Frontend development and UI/UX refinement. "
         "Month 5: Testing, optimization, and security hardening. "
         "Month 6: Deployment, documentation, and knowledge transfer."),
        
        ("Success Metrics",
         "The project will be evaluated based on query accuracy (>90%), response time (<3 seconds), "
         "system uptime (99.9%), user satisfaction scores (>4.5/5), and successful handling of "
         "diverse document types and query patterns. Regular performance monitoring and user "
         "feedback will guide continuous improvement efforts.")
    ]
    
    for section_title, content in sections:
        heading = Paragraph(section_title, styles['Heading2'])
        story.append(heading)
        story.append(Spacer(1, 0.1*inch))
        
        para = Paragraph(content, styles['BodyText'])
        story.append(para)
        story.append(Spacer(1, 0.2*inch))
    
    doc.build(story)
    print(f"✓ Generated {filename}")

def generate_budget_csv():
    """Generate a sample budget CSV file"""
    filename = "sample_project_budget.csv"
    
    categories = [
        "Backend Development",
        "Frontend Development",
        "AI/ML Components",
        "Cloud Infrastructure",
        "Database Services",
        "API Costs",
        "Testing & QA",
        "Documentation",
        "Training Materials",
        "Security Audit",
        "Performance Optimization",
        "Deployment",
        "Contingency Reserve"
    ]
    
    data = []
    for i, category in enumerate(categories):
        allocated = random.randint(10000, 60000)
        spent = int(allocated * random.uniform(0.3, 0.9))
        remaining = allocated - spent
        
        data.append({
            "Category": category,
            "Budget_Allocated": allocated,
            "Amount_Spent": spent,
            "Remaining": remaining,
            "Percentage_Used": round((spent / allocated) * 100, 2),
            "Status": "On Track" if spent < allocated * 0.8 else "Needs Review"
        })
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"✓ Generated {filename}")
    print(f"  Total Budget: ${df['Budget_Allocated'].sum():,}")
    print(f"  Total Spent: ${df['Amount_Spent'].sum():,}")
    print(f"  Total Remaining: ${df['Remaining'].sum():,}")

def generate_performance_metrics_excel():
    """Generate a sample performance metrics Excel file"""
    filename = "sample_performance_metrics.xlsx"
    
    dates = [(datetime.now() - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(30, 0, -1)]
    
    data = {
        "Date": dates,
        "Queries_Processed": [random.randint(100, 500) for _ in range(30)],
        "Average_Response_Time_Sec": [round(random.uniform(1.5, 4.0), 2) for _ in range(30)],
        "Success_Rate_Percent": [round(random.uniform(88, 99), 2) for _ in range(30)],
        "Documents_Uploaded": [random.randint(5, 25) for _ in range(30)],
        "Active_Users": [random.randint(20, 80) for _ in range(30)],
        "Error_Count": [random.randint(0, 10) for _ in range(30)]
    }
    
    df = pd.DataFrame(data)
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Daily Metrics', index=False)
        
        summary_data = {
            "Metric": [
                "Total Queries",
                "Average Response Time",
                "Overall Success Rate",
                "Total Documents",
                "Average Active Users"
            ],
            "Value": [
                df['Queries_Processed'].sum(),
                round(df['Average_Response_Time_Sec'].mean(), 2),
                round(df['Success_Rate_Percent'].mean(), 2),
                df['Documents_Uploaded'].sum(),
                round(df['Active_Users'].mean(), 0)
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    print(f"✓ Generated {filename}")
    print(f"  Total Queries: {df['Queries_Processed'].sum():,}")
    print(f"  Avg Response Time: {df['Average_Response_Time_Sec'].mean():.2f}s")

if __name__ == "__main__":
    print("Generating synthetic sample datasets...\n")
    
    try:
        generate_project_report_pdf()
    except Exception as e:
        print(f"✗ Error generating PDF: {e}")
        print("  Note: Install reportlab with: pip install reportlab")
    
    generate_budget_csv()
    generate_performance_metrics_excel()
    
    print("\n✓ Sample data generation complete!")
    print("\nGenerated files:")
    print("  - sample_project_report.pdf (Document for Q&A)")
    print("  - sample_project_budget.csv (Budget data)")
    print("  - sample_performance_metrics.xlsx (Performance metrics)")
