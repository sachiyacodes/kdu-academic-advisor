"""
Custom CSS styles for professional UI appearance.

Provides a modern academic analytics look, avoiding default Streamlit styling.
"""


def get_custom_css() -> str:
    """Return custom CSS for the application."""
    return """
    <style>
        /* Main page styling */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        /* Header styling */
        h1 {
            color: #1a1a2e;
            font-weight: 700;
            border-bottom: 3px solid #16213e;
            padding-bottom: 0.5rem;
        }

        h2 {
            color: #16213e;
            font-weight: 600;
            margin-top: 1.5rem;
        }

        h3 {
            color: #0f3460;
            font-weight: 500;
        }

        /* Card container */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            padding: 1.5rem;
            color: white;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }

        .metric-card h3 {
            color: white;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
            opacity: 0.9;
        }

        .metric-card .value {
            font-size: 2rem;
            font-weight: 700;
        }

        /* Info card */
        .info-card {
            background: #f8f9fa;
            border-left: 4px solid #0f3460;
            border-radius: 0 8px 8px 0;
            padding: 1rem 1.5rem;
            margin-bottom: 1rem;
        }

        /* Score display */
        .score-high {
            color: #28a745;
            font-weight: 700;
        }

        .score-medium {
            color: #ffc107;
            font-weight: 700;
        }

        .score-low {
            color: #dc3545;
            font-weight: 700;
        }

        /* Evidence badge */
        .evidence-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }

        .evidence-strong {
            background: #d4edda;
            color: #155724;
        }

        .evidence-moderate {
            background: #fff3cd;
            color: #856404;
        }

        .evidence-limited {
            background: #f8d7da;
            color: #721c24;
        }

        /* Recommendation category badges */
        .rec-now {
            background: #d4edda;
            color: #155724;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-weight: 500;
        }

        .rec-later {
            background: #fff3cd;
            color: #856404;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-weight: 500;
        }

        .rec-low {
            background: #e2e3e5;
            color: #383d41;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-weight: 500;
        }

        /* Disclaimer */
        .disclaimer {
            background: #e8eaf6;
            border-radius: 8px;
            padding: 1rem;
            font-size: 0.85rem;
            color: #283593;
            margin-top: 2rem;
            border: 1px solid #c5cae9;
        }

        /* Table styling */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
        }

        /* Sidebar styling */
        .css-1d391kg {
            padding-top: 2rem;
        }

        /* Streamlit metric override */
        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """
