"""Reusable Streamlit UI components."""

from __future__ import annotations

from html import escape
from typing import Any

import plotly.graph_objects as go
import streamlit as st


def render_career_card(career: dict[str, Any], rank: int) -> None:
    with st.container(border=True):
        left, right = st.columns([4, 1])
        with left:
            st.markdown(f"#### {rank}. {career['title']}")
            st.caption(career["category"])
        with right:
            st.metric("Profile similarity", f"{career['similarity_score']:.1f}%")
        st.write(career["description"])
        st.caption(career["explanation"])
        st.markdown("**Relevant skills mentioned**")
        _render_skill_badges(
            career["relevant_skills"],
            "No listed skill was explicitly detected.",
            "relevant",
        )
        st.markdown("**Unconfirmed required skills**")
        _render_skill_badges(
            career["unconfirmed_skills"],
            "All listed required skills were mentioned.",
            "unconfirmed",
        )


def _render_skill_badges(skills: list[str], empty_text: str, kind: str) -> None:
    if not skills:
        st.caption(empty_text)
        return
    badges = "".join(
        f'<span class="skill-badge skill-badge--{kind}">{escape(skill)}</span>'
        for skill in skills
    )
    st.markdown(f'<div class="skill-badges">{badges}</div>', unsafe_allow_html=True)


def render_comparison_chart(careers: list[dict[str, Any]]) -> None:
    if not careers:
        st.info("Share profile details in chat to see a comparison of career matches.")
        return
    chart = go.Figure(
        go.Bar(
            x=[career["similarity_score"] for career in careers],
            y=[career["title"] for career in careers],
            orientation="h",
            marker_color=["#2DD4BF", "#60A5FA", "#A78BFA"][:len(careers)],
            text=[f"{career['similarity_score']:.1f}%" for career in careers],
            textposition="outside",
            hovertemplate="%{y}<br>Text/profile similarity: %{x:.1f}%<extra></extra>",
        )
    )
    chart.update_layout(
        height=max(230, 92 * len(careers)),
        margin=dict(l=8, r=28, t=12, b=12),
        paper_bgcolor="#16243A",
        plot_bgcolor="#16243A",
        font=dict(color="#F1F5F9", family="sans-serif"),
        xaxis=dict(
            range=[0, min(100, max(1, max(c["similarity_score"] for c in careers) * 1.25))],
            title=dict(
                text="Text/profile similarity (not probability)",
                font=dict(color="#B8C5D9"),
            ),
            gridcolor="#2B3B55",
            zerolinecolor="#2B3B55",
            tickfont=dict(color="#B8C5D9"),
        ),
        yaxis=dict(
            autorange="reversed",
            gridcolor="#2B3B55",
            tickfont=dict(color="#F1F5F9"),
        ),
        hoverlabel=dict(
            bgcolor="#111C30",
            bordercolor="#2DD4BF",
            font=dict(color="#F1F5F9"),
        ),
        uniformtext=dict(minsize=11, mode="hide"),
        showlegend=False,
    )
    st.plotly_chart(chart, use_container_width=True)


def render_roadmap(roadmap: list[dict[str, Any]]) -> None:
    for stage in roadmap:
        with st.expander(stage["stage"], expanded=True):
            st.markdown("**Focus:** " + (", ".join(stage["focus"]) if stage["focus"] else "Choose a small practice task."))
            st.write(stage["milestone"])
