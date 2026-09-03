"""
Reusable UI components for the Streamlit application.

Cards, metrics, charts, disclaimers, and other visual elements.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
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
        css_class = "evidence-strong"
    elif "Moderate" in evidence_level:
        css_class = "evidence-moderate"
    else:
        css_class = "evidence-limited"
    return f'<span class="evidence-badge {css_class}">{evidence_level}</span>'


def render_metric_card(title: str, value: str, subtitle: str = "") -> None:
    """Render a styled metric card."""
    subtitle_html = f'<div style="font-size: 0.8rem; opacity: 0.8;">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>{title}</h3>
            <div class="value">{value}</div>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_card(content: str) -> None:
    """Render an info card with left border accent."""
    st.markdown(
        f'<div class="info-card">{content}</div>',
        unsafe_allow_html=True,
    )


def render_disclaimer() -> None:
    """Render the application disclaimer (section 42)."""
    st.markdown(
        f'<div class="disclaimer">{DISCLAIMER}</div>',
        unsafe_allow_html=True,
    )


def render_weight_disclosure() -> None:
    """Render the 70/30 weight disclosure note (FIX-2)."""
    st.caption(f"*{HYBRID_WEIGHT_DISCLOSURE}*")


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


def render_specialization_comparison_chart(
    scores: List[SpecializationScore],
) -> go.Figure:
    """
    Create a horizontal bar chart comparing all specializations.
    Shows Academic Fit and Interest Alignment as stacked components.
    """
    names = [s.specialization_name for s in scores]
    academic = [s.academic_fit * ACADEMIC_WEIGHT for s in scores]
    interest = [s.interest_alignment * INTEREST_WEIGHT for s in scores]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=names,
        x=academic,
        name=f"Academic Fit ({int(ACADEMIC_WEIGHT*100)}%)",
        orientation="h",
        marker_color="#667eea",
    ))
    fig.add_trace(go.Bar(
        y=names,
        x=interest,
        name=f"Interest Alignment ({int(INTEREST_WEIGHT*100)}%)",
        orientation="h",
        marker_color="#764ba2",
    ))

    fig.update_layout(
        barmode="stack",
        title="Specialization Compatibility Comparison",
        xaxis_title="Compatibility Score",
        yaxis_title="",
        height=350,
        margin=dict(l=20, r=20, t=50, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25),
        font=dict(size=12),
    )

    return fig


def render_subject_strengths_chart(
    subject_performances: Dict,
) -> go.Figure:
    """Create a radar/bar chart of academic strengths by subject area."""
    if not subject_performances:
        return None

    areas = list(subject_performances.keys())
    marks = [subject_performances[a].average_mark for a in areas]

    fig = go.Figure(go.Bar(
        x=marks,
        y=areas,
        orientation="h",
        marker=dict(
            color=marks,
            colorscale="Viridis",
            showscale=False,
        ),
    ))

    fig.update_layout(
        title="Academic Strengths by Subject Area",
        xaxis_title="Average Mark",
        xaxis=dict(range=[0, 100]),
        height=max(300, len(areas) * 40),
        margin=dict(l=20, r=20, t=50, b=30),
        font=dict(size=12),
    )

    return fig


def render_recommendation_breakdown_chart(
    score: SpecializationScore,
) -> go.Figure:
    """
    Create a chart showing how Academic Fit and Interest Alignment
    combine into the Final Score (section 7 visualization).
    """
    fig = go.Figure()

    categories = ["Academic Fit", "Interest Alignment", "Final Score"]
    values = [score.academic_fit, score.interest_alignment, score.final_score]
    colors = ["#667eea", "#764ba2", "#2d3436"]

    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=[f"{v:.1f}" for v in values],
        textposition="outside",
    ))

    fig.update_layout(
        title=f"Score Breakdown: {score.specialization_name}",
        yaxis_title="Score (0-100)",
        yaxis=dict(range=[0, 110]),
        height=350,
        margin=dict(l=20, r=20, t=50, b=30),
        font=dict(size=12),
        showlegend=False,
    )

    return fig


def render_explanation(explanation: Explanation) -> None:
    """Render a full explanation for a specialization recommendation."""
    st.markdown(f"**{explanation.summary}**")

    if explanation.strengths:
        st.markdown("**Strengths:**")
        for s in explanation.strengths:
            st.markdown(f"- :green[{s}]")

    if explanation.weaknesses:
        st.markdown("**Areas for Improvement:**")
        for w in explanation.weaknesses:
            st.markdown(f"- :orange[{w}]")

    if explanation.interest_matches:
        st.markdown("**Interest Alignment:**")
        for i in explanation.interest_matches:
            st.markdown(f"- {i}")

    st.markdown(f"**{explanation.evidence_note}**")

    if explanation.missing_areas_note:
        st.info(explanation.missing_areas_note)

    if explanation.comparison_notes:
        st.markdown("**Comparison with Higher-Ranked Specializations:**")
        for c in explanation.comparison_notes:
            st.markdown(f"- {c}")


def render_empty_state(message: str, icon: str = "info") -> None:
    """Render a helpful empty state message."""
    icon_map = {
        "info": "information_source",
        "warning": "warning",
        "start": "rocket",
        "data": "bar_chart",
    }
    emoji = icon_map.get(icon, "information_source")
    st.info(f":{emoji}: {message}")
