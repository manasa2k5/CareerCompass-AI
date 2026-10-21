"""Static, local-only Midnight Blue and Teal theme for Streamlit."""

APP_CSS = """
<style>
  :root {
    color-scheme: dark;
    --cc-bg: #0B1120;
    --cc-sidebar: #111C30;
    --cc-panel: #16243A;
    --cc-border: #2B3B55;
    --cc-text: #F1F5F9;
    --cc-secondary: #B8C5D9;
    --cc-muted: #94A3B8;
    --cc-accent: #2DD4BF;
    --cc-accent-hover: #5EEAD4;
    --cc-input: #1B2A42;
    --cc-input-text: #F1F5F9;
    --cc-placeholder: #94A3B8;
    --cc-focus: #5EEAD4;
  }

  html, body, [class*="stApp"] {
    background-color: var(--cc-bg);
    color: var(--cc-text);
  }
  [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: var(--cc-bg);
    color: var(--cc-text);
  }
  [data-testid="stHeader"] {
    background: rgba(11, 17, 32, .96);
    color: var(--cc-text);
  }
  [data-testid="stToolbar"], [data-testid="stDecoration"] {
    background: transparent;
  }
  [data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {
    background-color: var(--cc-sidebar);
    border-right: 1px solid var(--cc-border);
    color: var(--cc-text);
  }
  [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    color: var(--cc-text);
  }

  h1, h2, h3, h4, h5, h6,
  [data-testid="stMarkdownContainer"] p,
  [data-testid="stMarkdownContainer"] li,
  [data-testid="stMarkdownContainer"] strong,
  [data-testid="stMarkdownContainer"] em,
  [data-testid="stText"],
  [data-testid="stCaptionContainer"] {
    color: var(--cc-text);
  }
  .hero {
    padding: 1.4rem 1.55rem;
    border: 1px solid var(--cc-border);
    border-radius: 16px;
    background: linear-gradient(120deg, #182A43, #132238);
    margin-bottom: 1.1rem;
  }
  .hero h1 { margin: .2rem 0 .35rem; color: var(--cc-text); }
  .hero p { margin-bottom: .15rem; }
  .eyebrow {
    color: var(--cc-accent);
    font-size: .78rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
  }
  .muted { color: var(--cc-secondary) !important; }
  hr { border-color: var(--cc-border); }

  /* Sidebar, form labels, help buttons, captions, and slider annotations. */
  [data-testid="stWidgetLabel"],
  [data-testid="stWidgetLabel"] p,
  [data-testid="stWidgetLabel"] label,
  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] label p,
  [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
  [data-testid="stCaptionContainer"],
  [data-testid="stSlider"] [data-testid="stMarkdownContainer"] p {
    color: var(--cc-secondary) !important;
  }
  [data-testid="stTooltipIcon"],
  [data-testid="stTooltipIcon"] svg,
  button[data-testid="stTooltipIcon"],
  [data-testid="stHelp"], [data-testid="stHelp"] svg {
    color: var(--cc-muted) !important;
    fill: currentColor;
  }
  [data-testid="stTooltipIcon"]:hover,
  [data-testid="stTooltipIcon"]:focus-visible {
    color: var(--cc-accent-hover) !important;
  }
  [data-testid="stTooltipContent"], [role="tooltip"] {
    color: var(--cc-text);
    background: var(--cc-panel);
    border: 1px solid var(--cc-border);
  }

  /* Tabs: readable in all states, with a teal selected indicator. */
  [data-testid="stTabs"] [role="tablist"] {
    gap: .35rem;
    border-bottom: 1px solid var(--cc-border);
  }
  [data-testid="stTabs"] button[role="tab"] {
    color: var(--cc-secondary) !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 8px 8px 0 0;
    background: transparent;
    transition: color .15s ease, background-color .15s ease, border-color .15s ease;
  }
  [data-testid="stTabs"] button[role="tab"]:hover {
    color: var(--cc-accent-hover) !important;
    background: rgba(45, 212, 191, .08);
  }
  [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: var(--cc-accent) !important;
    border-bottom-color: var(--cc-accent) !important;
    font-weight: 650;
  }
  [data-testid="stTabs"] button[role="tab"]:focus-visible {
    outline: 2px solid var(--cc-focus);
    outline-offset: 2px;
  }

  /* Text inputs, text areas, select controls, chat input, and dropdown menus. */
  [data-baseweb="input"] > div,
  [data-baseweb="textarea"] > div,
  [data-baseweb="select"] > div,
  [data-testid="stChatInput"] textarea,
  [data-testid="stTextInput"] input,
  [data-testid="stNumberInput"] input {
    color: var(--cc-input-text) !important;
    background-color: var(--cc-input) !important;
    border-color: var(--cc-border) !important;
    caret-color: var(--cc-accent);
  }
  [data-baseweb="input"] input,
  [data-baseweb="textarea"] textarea,
  [data-baseweb="select"] input,
  [data-testid="stChatInput"] textarea {
    color: var(--cc-input-text) !important;
    -webkit-text-fill-color: var(--cc-input-text);
  }
  input::placeholder, textarea::placeholder,
  [data-testid="stChatInput"] textarea::placeholder {
    color: var(--cc-placeholder) !important;
    -webkit-text-fill-color: var(--cc-placeholder);
    opacity: 1;
  }
  [data-baseweb="select"] [role="combobox"],
  [data-baseweb="select"] [data-testid="stMarkdownContainer"],
  [data-baseweb="select"] div {
    color: var(--cc-input-text);
  }
  [data-baseweb="popover"], [data-baseweb="menu"],
  [data-baseweb="popover"] ul, [data-baseweb="menu"] ul {
    color: var(--cc-text) !important;
    background-color: var(--cc-panel) !important;
    border: 1px solid var(--cc-border);
  }
  [data-baseweb="popover"] li, [data-baseweb="menu"] li,
  [role="option"] {
    color: var(--cc-text) !important;
    background-color: var(--cc-panel) !important;
  }
  [data-baseweb="popover"] li:hover, [data-baseweb="menu"] li:hover,
  [role="option"]:hover, [role="option"][aria-selected="true"] {
    color: var(--cc-text) !important;
    background-color: #223650 !important;
  }
  [data-baseweb="input"] > div:focus-within,
  [data-baseweb="textarea"] > div:focus-within,
  [data-baseweb="select"] > div:focus-within,
  [data-testid="stChatInput"] textarea:focus {
    border-color: var(--cc-focus) !important;
    box-shadow: 0 0 0 2px rgba(45, 212, 191, .22) !important;
    outline: none;
  }
  [data-testid="stSlider"] [role="slider"] {
    background-color: var(--cc-accent) !important;
    border-color: var(--cc-accent) !important;
    box-shadow: 0 0 0 2px var(--cc-bg);
  }
  [data-testid="stSlider"] [data-baseweb="slider"] > div > div {
    background-color: var(--cc-accent);
  }
  [data-testid="stCheckbox"] label, [data-testid="stRadio"] label {
    color: var(--cc-secondary);
  }

  /* Buttons, including disabled and keyboard-focus states. */
  [data-testid="stButton"] button,
  [data-testid="stDownloadButton"] button,
  [data-testid="stFormSubmitButton"] button {
    color: var(--cc-text);
    background: #1B2A42;
    border: 1px solid var(--cc-border);
    border-radius: 9px;
    transition: color .15s ease, background-color .15s ease, border-color .15s ease;
  }
  [data-testid="stButton"] button:hover,
  [data-testid="stDownloadButton"] button:hover,
  [data-testid="stFormSubmitButton"] button:hover {
    color: #07131F;
    background: var(--cc-accent-hover);
    border-color: var(--cc-accent-hover);
  }
  [data-testid="stButton"] button:focus-visible,
  [data-testid="stDownloadButton"] button:focus-visible,
  [data-testid="stFormSubmitButton"] button:focus-visible {
    outline: 2px solid var(--cc-focus);
    outline-offset: 2px;
    box-shadow: 0 0 0 3px rgba(45, 212, 191, .2);
  }
  [data-testid="stButton"] button:disabled,
  [data-testid="stDownloadButton"] button:disabled,
  [data-testid="stFormSubmitButton"] button:disabled {
    color: #A6B2C5 !important;
    background: #202D42 !important;
    border-color: #3A4A62 !important;
    opacity: 1;
  }

  /* Cards, metrics, expanders, chat bubbles, and comparison panels. */
  [data-testid="stVerticalBlockBorderWrapper"],
  [data-testid="stMetric"],
  [data-testid="stExpander"] details,
  [data-testid="stChatMessage"] {
    background: var(--cc-panel);
    border-color: var(--cc-border);
    border-radius: 12px;
  }
  [data-testid="stMetric"] {
    padding: .9rem;
  }
  [data-testid="stMetricLabel"],
  [data-testid="stMetricLabel"] p {
    color: var(--cc-secondary) !important;
  }
  [data-testid="stMetricValue"], [data-testid="stMetricValue"] div {
    color: var(--cc-accent) !important;
  }
  .skill-badges {
    display: flex;
    flex-wrap: wrap;
    gap: .45rem;
    margin: .25rem 0 .7rem;
  }
  .skill-badge {
    display: inline-block;
    padding: .25rem .6rem;
    border: 1px solid var(--cc-border);
    border-radius: 999px;
    color: var(--cc-text);
    background: #1B2A42;
    font-size: .84rem;
    line-height: 1.4;
  }
  .skill-badge--relevant {
    color: #99F6E4;
    border-color: #23685F;
    background: #123A3A;
  }
  .skill-badge--unconfirmed {
    color: var(--cc-secondary);
    border-color: var(--cc-border);
    background: #1B2A42;
  }
  [data-testid="stExpander"] summary,
  [data-testid="stExpander"] summary p {
    color: var(--cc-text);
  }
  [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
    color: var(--cc-text);
  }

  /* Alerts and status messages remain distinct without losing contrast. */
  [data-testid="stAlert"] {
    color: var(--cc-text);
    background: var(--cc-panel);
    border: 1px solid var(--cc-border);
    border-radius: 10px;
  }
  [data-testid="stAlert"] [data-testid="stMarkdownContainer"],
  [data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {
    color: var(--cc-text);
  }
  [data-testid="stSpinner"] { color: var(--cc-accent); }

  @media (max-width: 720px) {
    .hero { padding: 1.05rem; }
    [data-testid="stTabs"] [role="tablist"] { gap: .1rem; }
    [data-testid="stTabs"] button[role="tab"] { padding-inline: .45rem; }
  }
</style>
"""
