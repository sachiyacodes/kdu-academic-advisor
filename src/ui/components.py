"""
Reusable UI components for the Streamlit application.

Cards, metrics, charts, disclaimers, navigation, and other visual elements,
themed to the design tokens defined in styles.py.
"""

import streamlit as st
import plotly.graph_objects as go
from typing import Dict, List, Optional

from src.config.settings import (
    DISCLAIMER,
    HYBRID_WEIGHT_DISCLOSURE,
    HIGH_MATCH_THRESHOLD,
    MODERATE_MATCH_THRESHOLD,
    ACADEMIC_WEIGHT,
    INTEREST_WEIGHT,
)
from src.models.schemas import Explanation, SpecializationScore

# Chart palette drawn from the app's design tokens (src/ui/styles.py)
INK = "#1A2333"
BRASS = "#9C7A3C"
BRASS_LIGHT = "#C9AF7C"
GOOD = "#2F6844"
WARN = "#96650F"
BAD = "#A13D3D"
GRID = "#E4E0D6"
FONT_FAMILY = "Inter, sans-serif"


def _base_layout(**overrides) -> dict:
    """Shared Plotly layout so every chart in the app matches the design system."""
    layout = dict(
        font=dict(family=FONT_FAMILY, size=12, color="#4A5468"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=30),
        xaxis=dict(gridcolor=GRID, zerolinecolor=GRID),
        yaxis=dict(gridcolor=GRID, zerolinecolor=GRID),
    )
    layout.update(overrides)
    return layout


def render_page_header(title: str, subtitle: str, kicker: Optional[str] = None) -> None:
    """Render a consistent page header (replaces ad hoc emoji titles + dividers)."""
    if kicker:
        st.markdown(f'<div class="app-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.markdown(f"# {title}")
    st.markdown(f'<div class="app-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def render_score_color(score: float) -> str:
    """Return CSS class name for a score value."""
    if score >= HIGH_MATCH_THRESHOLD:
        return "score-high"
    elif score >= MODERATE_MATCH_THRESHOLD:
        return "score-medium"
    return "score-low"


def render_evidence_badge(evidence_level: str) -> str:
    """Render an evidence level badge as HTML."""
    if "Strong" in evidence_level:
        css_class = "badge-strong"
    elif "Moderate" in evidence_level:
        css_class = "badge-moderate"
    else:
        css_class = "badge-limited"
    return f'<span class="badge {css_class}">{evidence_level}</span>'


def render_category_badge(category: str) -> str:
    """Render a course-recommendation category badge as HTML."""
    css_class = {
        "Recommended Now": "badge-now",
        "Recommended Later": "badge-later",
    }.get(category, "badge-low")
    return f'<span class="badge {css_class}">{category}</span>'


def render_metric_card(title: str, value: str, subtitle: str = "") -> None:
    """Render a styled stat block (replaces the old gradient metric card)."""
    subtitle_html = f'<div class="stat-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div class="stat-block">
            <div class="stat-label">{title}</div>
            <div class="stat-value">{value}</div>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_card(content: str) -> None:
    """Render an info card with left border accent."""
    st.markdown(f'<div class="info-card">{content}</div>', unsafe_allow_html=True)


def render_disclaimer() -> None:
    """Render the application disclaimer (section 42)."""
    st.markdown(f'<div class="disclaimer">{DISCLAIMER}</div>', unsafe_allow_html=True)


def render_weight_disclosure() -> None:
    """Render the 70/30 weight disclosure note (FIX-2)."""
    st.caption(HYBRID_WEIGHT_DISCLOSURE)


def render_step_tracker(current_step: int, completed_steps: List[int]) -> None:
    """Render a sidebar step tracker showing progress through the main flow (§31)."""
    steps = [
        "Academic Profile",
        "Course History",
        "Interests",
        "Recommendations",
        "Course Recommendations",
        "Analysis",
    ]
    lines = []
    for i, label in enumerate(steps, start=1):
        if i == current_step:
            cls = "step-current"
        elif i in completed_steps:
            cls = "step-done"
        else:
            cls = "step-pending"
        lines.append(f'<div class="{cls}">{label}</div>')
    st.markdown(f'<div class="step-track">{"".join(lines)}</div>', unsafe_allow_html=True)


def render_score_breakdown(score: SpecializationScore) -> None:
    """Render the score breakdown showing Academic Fit / Interest / Final (section 7)."""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Academic Fit", f"{score.academic_fit:.1f}")
    with col2:
        st.metric("Interest Alignment", f"{score.interest_alignment:.1f}")
    with col3:
        st.metric("Final Match", f"{score.final_score:.1f}")
    render_weight_disclosure()


def render_specialization_comparison_chart(scores: List[SpecializationScore]) -> go.Figure:
    """
    Create a horizontal bar chart comparing all specializations.
    Shows Academic Fit and Interest Alignment as stacked components.
    """
    names = [s.specialization_name for s in scores]
    academic = [s.academic_fit * ACADEMIC_WEIGHT for s in scores]
    interest = [s.interest_alignment * INTEREST_WEIGHT for s in scores]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=names, x=academic, name=f"Academic Fit ({int(ACADEMIC_WEIGHT*100)}%)",
        orientation="h", marker_color=INK,
    ))
    fig.add_trace(go.Bar(
        y=names, x=interest, name=f"Interest Alignment ({int(INTEREST_WEIGHT*100)}%)",
        orientation="h", marker_color=BRASS,
    ))

    fig.update_layout(_base_layout(
        barmode="stack",
        title="Specialization Compatibility Comparison",
        xaxis_title="Compatibility Score",
        yaxis_title="",
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25),
    ))
    return fig


def render_subject_strengths_chart(subject_performances: Dict):
    """Create a bar chart of academic strengths by subject area."""
    if not subject_performances:
        return None

    areas = list(subject_performances.keys())
    marks = [subject_performances[a].average_mark for a in areas]

    paired = sorted(zip(marks, areas))
    marks = [m for m, _ in paired]
    areas = [a for _, a in paired]

    fig = go.Figure(go.Bar(
        x=marks, y=areas, orientation="h",
        marker_color=[GOOD if m >= 75 else WARN if m >= 50 else BAD for m in marks],
    ))
    fig.update_layout(_base_layout(
        title="Academic Strengths by Subject Area",
        xaxis_title="Average Mark",
        xaxis=dict(range=[0, 100], gridcolor=GRID),
        height=max(300, len(areas) * 38),
    ))
    return fig


def render_recommendation_breakdown_chart(score: SpecializationScore) -> go.Figure:
    """Chart showing how Academic Fit and Interest Alignment combine into Final Score."""
    categories = ["Academic Fit", "Interest Alignment", "Final Score"]
    values = [score.academic_fit, score.interest_alignment, score.final_score]
    colors = [INK, BRASS, GOOD if score.final_score >= HIGH_MATCH_THRESHOLD else WARN]

    fig = go.Figure(go.Bar(
        x=categories, y=values, marker_color=colors,
        text=[f"{v:.1f}" for v in values], textposition="outside",
    ))
    fig.update_layout(_base_layout(
        title=f"Score Breakdown: {score.specialization_name}",
        yaxis_title="Score (0-100)",
        yaxis=dict(range=[0, 110], gridcolor=GRID),
        height=320,
        showlegend=False,
    ))
    return fig


def render_explanation(explanation: Explanation) -> None:
    """Render a full explanation for a specialization recommendation."""
    st.markdown(f"**{explanation.summary}**")

    if explanation.strengths:
        st.markdown("**Strengths**")
        for s in explanation.strengths:
            st.markdown(f"- {s}")

    if explanation.weaknesses:
        st.markdown("**Areas for improvement**")
        for w in explanation.weaknesses:
            st.markdown(f"- {w}")

    if explanation.interest_matches:
        st.markdown("**Interest alignment**")
        for i in explanation.interest_matches:
            st.markdown(f"- {i}")

    st.caption(explanation.evidence_note)

    if explanation.missing_areas_note:
        render_info_card(explanation.missing_areas_note)

    if explanation.comparison_notes:
        st.markdown("**Compared with higher-ranked specializations**")
        for c in explanation.comparison_notes:
            st.markdown(f"- {c}")


def render_empty_state(message: str, icon: str = "info") -> None:
    """Render a helpful empty state message."""
    st.info(message)
