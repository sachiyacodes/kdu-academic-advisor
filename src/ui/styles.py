"""
Custom CSS for the application.

Design direction: a university records/registrar aesthetic rather than a
generic SaaS dashboard — deep ink-navy for structure and authority, a muted
brass accent (the one place color is spent), warm paper background, a serif
display face for headings (academic, transcript-like) paired with a clean
sans for data and body text. No gradients, no pill badges, no emoji chrome.

Targets stable `[data-testid]` hooks rather than Streamlit's internal
auto-generated hash classes (e.g. `.css-xxxxx`), which change between
versions and silently stop working — the previous version of this file did
that and the rules had gone dead.
"""


def get_custom_css() -> str:
    """Return custom CSS for the application."""
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Inter:wght@400;500;600;700&display=swap');

        :root {
            --ink: #1A2333;
            --ink-soft: #4A5468;
            --ink-faint: #7C8598;
            --paper: #FAF9F5;
            --paper-raised: #FFFFFF;
            --line: #E4E0D6;
            --line-soft: #EDEAE1;
            --brass: #9C7A3C;
            --brass-soft: #F1E9D8;
            --brass-strong: #7A5F2C;
            --good: #2F6844;
            --good-bg: #E8F1EA;
            --warn: #96650F;
            --warn-bg: #F7EFDD;
            --bad: #A13D3D;
            --bad-bg: #F6E9E7;
            --radius: 6px;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, sans-serif;
        }

        /* ---------- Layout ---------- */
        .stApp {
            background: var(--paper);
        }

        .main .block-container {
            padding-top: 2.25rem;
            padding-bottom: 3rem;
            max-width: 1120px;
        }

        [data-testid="stSidebar"] {
            background: var(--ink);
            border-right: none;
        }

        [data-testid="stSidebar"] * {
            color: #E7E4DA !important;
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(231, 228, 218, 0.16);
        }

        /* ---------- Typography ---------- */
        h1, h2, h3 {
            font-family: 'Source Serif 4', Georgia, serif;
            color: var(--ink);
            letter-spacing: -0.01em;
        }

        h1 {
            font-weight: 700;
            font-size: 2.1rem;
            margin-bottom: 0.15rem;
        }

        h2 {
            font-weight: 600;
            font-size: 1.4rem;
            margin-top: 2rem;
            padding-top: 1.25rem;
            border-top: 1px solid var(--line);
        }

        h3 {
            font-weight: 600;
            font-size: 1.1rem;
            color: var(--ink-soft);
        }

        p, li, span, label, div {
            color: var(--ink-soft);
        }

        .app-kicker {
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--brass-strong);
            margin-bottom: 0.35rem;
        }

        .app-subtitle {
            font-size: 1.02rem;
            color: var(--ink-faint);
            margin-top: 0.1rem;
            margin-bottom: 1.5rem;
        }

        /* ---------- Buttons ---------- */
        .stButton button, .stFormSubmitButton button {
            border-radius: var(--radius);
            font-weight: 600;
            border: 1px solid var(--line);
            transition: none;
        }

        button[data-testid^="stBaseButton-primary"] {
            background: var(--ink);
            border-color: var(--ink);
            color: var(--paper) !important;
        }

        button[data-testid^="stBaseButton-primary"]:hover {
            background: var(--brass-strong);
            border-color: var(--brass-strong);
        }

        button[data-testid^="stBaseButton-primary"] p {
            color: var(--paper) !important;
        }

        button[data-testid^="stBaseButton-secondary"] {
            background: var(--paper-raised);
            color: var(--bad);
            border-color: var(--line);
        }

        button[data-testid^="stBaseButton-secondary"] p {
            color: var(--bad) !important;
        }

        /* ---------- Inputs & Form Controls ---------- */
        [data-testid="stNumberInput"] div[data-testid="stNumberInputContainer"],
        [data-testid="stNumberInput"] div[data-baseweb="input"],
        [data-testid="stTextInput"] div[data-testid="stTextInputContainer"],
        [data-testid="stTextInput"] div[data-baseweb="input"],
        [data-testid="stTextArea"] div[data-baseweb="textarea"] {
            background-color: var(--paper-raised) !important;
            border: 1px solid var(--line) !important;
            border-radius: var(--radius) !important;
        }

        [data-testid="stNumberInput"] input,
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea {
            background-color: var(--paper-raised) !important;
            color: var(--ink) !important;
            caret-color: var(--ink) !important;
            font-weight: 500 !important;
            border: none !important;
        }

        [data-testid="stNumberInput"] input::placeholder,
        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stTextArea"] textarea::placeholder {
            color: var(--ink-faint) !important;
        }

        /* Number input step buttons (+ / -) */
        [data-testid="stNumberInput"] button,
        [data-testid="stNumberInputStepDown"],
        [data-testid="stNumberInputStepUp"] {
            background: var(--paper-raised) !important;
            color: var(--ink) !important;
            border: none !important;
        }

        [data-testid="stNumberInput"] button:hover,
        [data-testid="stNumberInputStepDown"]:hover,
        [data-testid="stNumberInputStepUp"]:hover {
            background: var(--line-soft) !important;
        }

        [data-testid="stNumberInput"] button svg,
        [data-testid="stNumberInput"] button path {
            fill: var(--ink) !important;
            stroke: var(--ink) !important;
            color: var(--ink) !important;
        }

        /* ---------- Selectbox ---------- */
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        [data-testid="stSelectbox"] div[class*="stSelectbox"] > div,
        [data-testid="stSelectbox"] div[role="combobox"] {
            border-radius: var(--radius) !important;
            border-color: var(--line) !important;
            background: var(--paper-raised) !important;
            color: var(--ink) !important;
        }

        [data-testid="stSelectbox"] div[data-baseweb="select"] *,
        [data-testid="stSelectbox"] [role="combobox"] * {
            color: var(--ink) !important;
        }

        [data-testid="stSelectbox"] svg {
            fill: var(--ink-soft) !important;
            color: var(--ink-soft) !important;
        }

        /* ---------- Dropdown Menus & Popovers ---------- */
        [data-testid="stSelectboxVirtualDropdown"],
        div[data-baseweb="popover"],
        ul[role="listbox"],
        ul[data-baseweb="menu"] {
            background-color: var(--paper-raised) !important;
            border: 1px solid var(--line) !important;
            border-radius: var(--radius) !important;
            box-shadow: 0 4px 16px rgba(26, 35, 51, 0.12) !important;
        }

        /* Individual option items */
        [data-testid="stSelectboxVirtualDropdown"] li,
        [data-testid="stSelectboxVirtualDropdown"] [role="option"],
        ul[role="listbox"] li,
        ul[role="listbox"] [role="option"],
        ul[data-baseweb="menu"] li,
        li[data-baseweb="menu-item"] {
            background-color: var(--paper-raised) !important;
            color: var(--ink) !important;
        }

        [data-testid="stSelectboxVirtualDropdown"] [role="option"] *,
        ul[role="listbox"] [role="option"] *,
        ul[data-baseweb="menu"] li *,
        li[data-baseweb="menu-item"] * {
            color: var(--ink) !important;
        }

        /* Hovered, focused, or selected option state */
        [data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover,
        [data-testid="stSelectboxVirtualDropdown"] [role="option"][aria-selected="true"],
        [data-testid="stSelectboxVirtualDropdown"] [role="option"][data-focused="true"],
        ul[role="listbox"] [role="option"]:hover,
        ul[role="listbox"] [role="option"][aria-selected="true"],
        ul[data-baseweb="menu"] li:hover,
        li[data-baseweb="menu-item"]:hover {
            background-color: var(--brass-soft) !important;
            color: var(--brass-strong) !important;
        }

        [data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover *,
        [data-testid="stSelectboxVirtualDropdown"] [role="option"][aria-selected="true"] *,
        ul[role="listbox"] [role="option"]:hover * {
            color: var(--brass-strong) !important;
        }

        /* ---------- Forms & containers ---------- */
        [data-testid="stForm"] {
            background: var(--paper-raised);
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 1.5rem 1.75rem;
        }

        [data-testid="stExpander"] {
            background: var(--paper-raised);
            border: 1px solid var(--line);
            border-radius: 10px;
        }

        [data-testid="stExpander"] summary {
            font-family: 'Source Serif 4', serif;
            font-weight: 600;
            font-size: 1.05rem;
            color: var(--ink);
        }

        /* ---------- Metrics ---------- */
        [data-testid="stMetric"] {
            background: var(--paper-raised);
            border: 1px solid var(--line);
            border-left: 3px solid var(--brass);
            border-radius: var(--radius);
            padding: 0.85rem 1rem 0.7rem;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.78rem;
            font-weight: 600;
            text-transform: none;
            color: var(--ink-faint) !important;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.4rem;
            font-family: 'Source Serif 4', serif;
            color: var(--ink) !important;
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: unset !important;
            line-height: 1.25;
        }

        /* ---------- Tables ---------- */
        [data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: var(--radius);
            overflow: hidden;
        }

        /* ---------- Alerts ---------- */
        [data-testid="stAlertContentInfo"], [data-testid="stAlertContentSuccess"],
        [data-testid="stAlertContentWarning"], [data-testid="stAlertContentError"] {
            font-size: 0.92rem;
        }

        div[data-testid="stNotification"] {
            border-radius: var(--radius);
            border: 1px solid var(--line);
        }

        /* ---------- Tabs ---------- */
        [data-testid="stTabs"] [role="tablist"] {
            border-bottom: 1px solid var(--line);
            gap: 1.5rem;
        }

        [data-testid="stTab"] {
            color: var(--ink-faint);
        }

        [data-testid="stTab"] p {
            font-weight: 600;
        }

        [data-testid="stTab"][aria-selected="true"] {
            color: var(--ink) !important;
        }

        [data-testid="stTab"] .react-aria-SelectionIndicator {
            background: var(--brass) !important;
        }

        /* ---------- Custom components ---------- */
        .card {
            background: var(--paper-raised);
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 1.1rem 1.3rem;
        }

        .stat-block {
            background: var(--paper-raised);
            border: 1px solid var(--line);
            border-left: 3px solid var(--brass);
            border-radius: var(--radius);
            padding: 0.85rem 1rem 0.7rem;
        }

        .stat-block .stat-label {
            font-size: 0.78rem;
            font-weight: 600;
            color: var(--ink-faint);
        }

        .stat-block .stat-value {
            font-family: 'Source Serif 4', serif;
            font-size: 1.6rem;
            font-weight: 600;
            color: var(--ink);
            line-height: 1.25;
        }

        .stat-block .stat-sub {
            font-size: 0.78rem;
            color: var(--ink-faint);
            margin-top: 0.1rem;
        }

        .info-card {
            background: var(--brass-soft);
            border-left: 3px solid var(--brass);
            border-radius: 0 6px 6px 0;
            padding: 0.85rem 1.1rem;
            font-size: 0.92rem;
            color: var(--brass-strong);
        }

        .score-high { color: var(--good); font-weight: 700; }
        .score-medium { color: var(--warn); font-weight: 700; }
        .score-low { color: var(--bad); font-weight: 700; }

        .badge {
            display: inline-block;
            padding: 0.15rem 0.6rem;
            border-radius: 3px;
            font-size: 0.78rem;
            font-weight: 600;
            border: 1px solid transparent;
        }

        .badge-strong { background: var(--good-bg); color: var(--good); border-color: rgba(47,104,68,0.2); }
        .badge-moderate { background: var(--warn-bg); color: var(--warn); border-color: rgba(150,101,15,0.2); }
        .badge-limited { background: var(--bad-bg); color: var(--bad); border-color: rgba(161,61,61,0.2); }
        .badge-now { background: var(--good-bg); color: var(--good); border-color: rgba(47,104,68,0.2); }
        .badge-later { background: var(--warn-bg); color: var(--warn); border-color: rgba(150,101,15,0.2); }
        .badge-low { background: var(--line-soft); color: var(--ink-faint); border-color: var(--line); }

        .disclaimer {
            background: var(--paper-raised);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 0.95rem 1.2rem;
            font-size: 0.82rem;
            color: var(--ink-faint);
            margin-top: 2.5rem;
            line-height: 1.55;
        }

        .step-track {
            font-size: 0.85rem;
            line-height: 2.1;
        }

        .step-track .step-done { color: #C9C4B4; }
        .step-track .step-done::before { content: "✓  "; color: var(--brass); font-weight: 700; }
        .step-track .step-pending { color: #7C8598; }
        .step-track .step-pending::before { content: "○  "; }
        .step-track .step-current { color: #FFFFFF; font-weight: 600; }
        .step-track .step-current::before { content: "→  "; color: var(--brass); }

        /* Hide default chrome */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """
