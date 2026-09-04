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


def render_ml_prediction_card(
    prediction: str,
    probabilities: Dict[str, float],
    top_rule_spec: str,
    consensus_info: Optional[Dict[str, Any]] = None,
) -> None:
    """Render the machine learning prediction with multi-model consensus, confidence, and probability distribution."""
    prediction_str = str(prediction)
    confidence = float(probabilities.get(prediction, 0.0)) * 100
    is_agreement = (prediction_str == str(top_rule_spec))

    # Details from consensus if available
    dt_pred = consensus_info.get("dt_prediction", "") if consensus_info else ""
    is_consensus = consensus_info.get("consensus", False) if consensus_info else False
    is_preliminary = consensus_info.get("is_preliminary", False) if consensus_info else False
    confidence_label = consensus_info.get("confidence_label", "Standard") if consensus_info else "Standard"

    consensus_text = ""
    if consensus_info:
        if is_consensus:
            consensus_text = f"<br>🎯 <b>Ensemble Consensus:</b> Both Random Forest and Decision Tree independently predict <b>{prediction_str}</b>."
        else:
            consensus_text = f"<br>📊 <b>Model Comparison:</b> Primary Random Forest predicts <b>{prediction_str}</b>, while Decision Tree highlights <b>{dt_pred}</b>."

    preliminary_badge = ""
    if is_preliminary:
        preliminary_badge = '<span style="background: var(--warn-bg); color: var(--warn); padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600; margin-left: 0.5rem;">⚠️ Preliminary / Early-Stage</span>'

    st.markdown(f"""
    <div style="background: var(--paper-raised); border: 1px solid var(--line); border-left: 4px solid var(--brass); border-radius: var(--radius); padding: 1.1rem 1.3rem; margin-top: 1.5rem; margin-bottom: 1.2rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
            <span style="font-size: 0.78rem; font-weight: 600; color: var(--brass-strong); text-transform: uppercase; letter-spacing: 0.05em;">
                🤖 Machine Learning Cross-Check (Random Forest & Decision Tree Benchmark)
            </span>
            {preliminary_badge}
        </div>
        <div style="display: flex; align-items: baseline; gap: 1rem; margin-bottom: 0.5rem;">
            <span style="font-family: 'Source Serif 4', serif; font-size: 1.35rem; font-weight: 700; color: var(--ink);">{prediction_str}</span>
            <span style="font-size: 0.92rem; font-weight: 600; color: var(--brass);">{confidence:.1f}% confidence ({confidence_label})</span>
        </div>
        <div style="font-size: 0.88rem; color: var(--ink-soft); line-height: 1.5;">
            {"✅ <b>Model Agreement:</b> The Machine Learning benchmark independently concurs with the Knowledge-Based Recommender's top choice." if is_agreement else f"ℹ️ <b>Divergent Insight:</b> The ML benchmark indicates high statistical affinity with <b>{prediction_str}</b> based on non-linear curriculum patterns."}
            {consensus_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

    sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
    specs = [str(p[0]) for p in sorted_probs]
    probs = [float(p[1]) * 100 for p in sorted_probs]

    fig = go.Figure(go.Bar(
        x=probs,
        y=specs,
        orientation="h",
        marker=dict(color=[BRASS if s == prediction_str else INK for s in specs]),
        text=[f"{v:.1f}%" for v in probs],
        textposition="outside",
    ))
    fig.update_layout(
        _base_layout(
            title="Class Probability Distribution",
            xaxis=dict(title="Probability (%)", range=[0, 110], gridcolor=GRID),
            yaxis=dict(autorange="reversed"),
            height=280,
            margin=dict(l=20, r=20, t=35, b=20),
        )
    )
    st.plotly_chart(fig, width="stretch")


def render_sensitivity_chart(sensitivity_data: Dict[str, Any]) -> go.Figure:
    """Render interactive sensitivity curves showing how recommendations vary with Academic Weight."""
    weights = sensitivity_data["academic_weights"]
    trajectories = sensitivity_data["trajectories"]

    fig = go.Figure()
    colors = [BRASS, "#2F6844", "#2B5C8F", "#8C3B68", "#96650F", INK]

    for i, (spec_name, scores) in enumerate(trajectories.items()):
        color = colors[i % len(colors)]
        fig.add_trace(go.Scatter(
            x=[round(w * 100) for w in weights],
            y=scores,
            mode="lines+markers",
            name=spec_name,
            line=dict(color=color, width=2.5 if spec_name == sensitivity_data.get("baseline_top") else 1.5),
            marker=dict(size=5),
        ))

    # Add reference line at current default (70% Academic / 30% Interest)
    fig.add_vline(
        x=70,
        line_dash="dash",
        line_color=BRASS_LIGHT,
        annotation_text="Default 70/30 Split",
        annotation_position="top right",
    )

    fig.update_layout(
        _base_layout(
            title="Recommendation Stability vs. Academic Weight Ratio",
            xaxis=dict(title="Academic Weight (%) [Interest Weight = 100 - Academic]", range=[-5, 105], gridcolor=GRID),
            yaxis=dict(title="Final Compatibility Score (0-100)", range=[0, 105], gridcolor=GRID),
            height=360,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=40, b=20),
        )
    )
    return fig


def render_feature_importance_chart(feature_importance: Dict[str, float]) -> go.Figure:
    """Render Decision Tree feature importance horizontal bar chart."""
    sorted_items = sorted(feature_importance.items(), key=lambda x: x[1], reverse=False)
    features = [str(k) for k, v in sorted_items]
    scores = [float(v) * 100 for k, v in sorted_items]

    fig = go.Figure(go.Bar(
        x=scores,
        y=features,
        orientation="h",
        marker_color=BRASS,
        text=[f"{v:.1f}%" for v in scores],
        textposition="outside",
    ))
    fig.update_layout(
        _base_layout(
            xaxis=dict(title="Importance Weight (%)", gridcolor=GRID),
            margin=dict(l=20, r=30, t=20, b=20),
            height=360,
        )
    )
    return fig


def render_confusion_matrix_heatmap(conf_matrix: List[List[int]], class_labels: List[str]) -> go.Figure:
    """Render confusion matrix heatmap."""
    short_labels = [
        str(label)
        .replace("Artificial Intelligence / Machine Learning", "AI/ML")
        .replace("Networking & Cloud Computing", "Networks/Cloud")
        .replace("Database & Data Engineering", "Database")
        .replace("Software Engineering", "SE")
        for label in class_labels
    ]

    fig = go.Figure(data=go.Heatmap(
        z=conf_matrix,
        x=short_labels,
        y=short_labels,
        colorscale=[[0, "#FAF9F5"], [0.5, "#F1E9D8"], [1.0, "#9C7A3C"]],
        text=[[str(val) for val in row] for row in conf_matrix],
        texttemplate="%{text}",
        textfont=dict(family=FONT_FAMILY, size=12, color=INK),
        showscale=False,
    ))
    fig.update_layout(
        _base_layout(
            xaxis=dict(title="Predicted Class"),
            yaxis=dict(title="Actual Class", autorange="reversed"),
            height=360,
            margin=dict(l=20, r=20, t=20, b=20),
        )
    )
    return fig

