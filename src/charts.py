# -*- coding: utf-8 -*-
"""
Plotly figure builders. Palette and mark rules follow the project's
validated chart-mark palette (src.design_tokens): sequential single-hue for
magnitude/ranking, the validated <=3-slot categorical set only where series
identity genuinely matters, and status green/red reserved exclusively for
profit/loss polarity. No dual-axis charts, no 3D, no decorative pies.
"""
import plotly.graph_objects as go

from src import design_tokens as tok
from src.translations import t

FONT_FAMILY = "Inter, system-ui, -apple-system, 'Segoe UI', sans-serif"


def _base_layout(title: str, lang: str, height: int = 360, show_legend: bool = False, show_title: bool = True):
    """show_title=False omits the in-plot Plotly title entirely (text and
    reserved space) -- used wherever the page already renders a
    title_with_info() section heading with the same meaning immediately
    above the chart, so the title isn't shown twice. The top margin still
    reserves just enough room for the legend row when one is shown."""
    if show_title:
        top_margin = 46
    elif show_legend:
        top_margin = 34
    else:
        top_margin = 14
    layout = dict(
        font=dict(family=FONT_FAMILY, size=12, color=tok.INK_PRIMARY),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=10, r=10, t=top_margin, b=10),
        showlegend=show_legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="left", x=0, font=dict(size=11)),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family=FONT_FAMILY, bordercolor=tok.BORDER),
        xaxis=dict(showgrid=False, linecolor=tok.GRIDLINE, tickfont=dict(color=tok.INK_MUTED)),
        yaxis=dict(showgrid=True, gridcolor=tok.GRIDLINE, zeroline=True, zerolinecolor=tok.GRIDLINE,
                    tickfont=dict(color=tok.INK_MUTED)),
    )
    if show_title:
        layout["title"] = dict(text=title, font=dict(size=15, color=tok.BRAND_NAVY, family=FONT_FAMILY), x=0, xanchor="left")
    return layout


def _hover_amount(lang: str) -> str:
    return "%{customdata:,.2f} " + ("ر.س" if lang == "ar" else "SAR")


def revenue_vs_expenses_chart(years, revenue_vals, expense_vals, lang: str, show_title: bool = True) -> go.Figure:
    fig = go.Figure()
    fig.add_bar(
        x=years, y=revenue_vals, name=t("legend.revenue", lang),
        marker_color=tok.CHART_NAVY, customdata=revenue_vals,
        hovertemplate=t("legend.revenue", lang) + " %{x}: " + _hover_amount(lang) + "<extra></extra>",
    )
    fig.add_bar(
        x=years, y=expense_vals, name=t("legend.expenses", lang),
        marker_color=tok.CHART_TEAL, customdata=expense_vals,
        hovertemplate=t("legend.expenses", lang) + " %{x}: " + _hover_amount(lang) + "<extra></extra>",
    )
    layout = _base_layout(t("chart.revenue_vs_expenses", lang), lang, show_legend=True, show_title=show_title)
    layout["barmode"] = "group"
    layout["xaxis"]["type"] = "category"
    fig.update_layout(**layout)
    return fig


def pl_trend_chart(years, pl_vals, lang: str, show_title: bool = True) -> go.Figure:
    colors = [tok.STATUS_GOOD if v >= 0 else tok.STATUS_CRITICAL for v in pl_vals]
    fig = go.Figure()
    fig.add_bar(
        x=years, y=pl_vals, marker_color=colors, customdata=pl_vals,
        hovertemplate=t("legend.profit_loss", lang) + " %{x}: " + _hover_amount(lang) + "<extra></extra>",
    )
    fig.add_hline(y=0, line_width=1, line_color=tok.INK_MUTED)
    layout = _base_layout(t("chart.pl_trend", lang), lang, show_legend=False, show_title=show_title)
    layout["xaxis"]["type"] = "category"
    fig.update_layout(**layout)
    return fig


def break_even_gap_trend_chart(years, gap_vals, lang: str, show_title: bool = True) -> go.Figure:
    fig = go.Figure()
    fig.add_scatter(
        x=years, y=gap_vals, mode="lines+markers",
        line=dict(color=tok.CHART_TEAL, width=2.5),
        marker=dict(size=8, color=tok.CHART_TEAL),
        customdata=gap_vals,
        hovertemplate=t("kpi.break_even_gap", lang) + " %{x}: " + _hover_amount(lang) + "<extra></extra>",
        fill="tozeroy", fillcolor="rgba(14,140,114,0.10)",
    )
    layout = _base_layout(t("chart.break_even_trend", lang), lang, show_legend=False, show_title=show_title)
    layout["xaxis"]["type"] = "category"
    fig.update_layout(**layout)
    return fig


def employee_vs_revenue_chart(years, revenue_vals, employee_vals, lang: str, show_title: bool = True) -> go.Figure:
    fig = go.Figure()
    fig.add_scatter(
        x=years, y=revenue_vals, name=t("legend.revenue", lang), mode="lines+markers",
        line=dict(color=tok.CHART_NAVY, width=2.5), marker=dict(size=7),
        customdata=revenue_vals, hovertemplate=t("legend.revenue", lang) + " %{x}: " + _hover_amount(lang) + "<extra></extra>",
    )
    fig.add_scatter(
        x=years, y=employee_vals, name=t("legend.employee_costs", lang), mode="lines+markers",
        line=dict(color=tok.CHART_TEAL, width=2.5), marker=dict(size=7),
        customdata=employee_vals, hovertemplate=t("legend.employee_costs", lang) + " %{x}: " + _hover_amount(lang) + "<extra></extra>",
    )
    layout = _base_layout(t("chart.employee_vs_revenue", lang), lang, show_legend=True, show_title=show_title)
    layout["xaxis"]["type"] = "category"
    fig.update_layout(**layout)
    return fig


def sorted_magnitude_bar_chart(labels, values, title: str, lang: str, height: int = 380, top_hue=None, show_title: bool = True) -> go.Figure:
    """Single-hue horizontal bar for ranking (management groups, top expenses,
    employee subgroups). Magnitude, not identity -> one hue, per dataviz skill."""
    color = top_hue or tok.SEQUENTIAL_DEFAULT_MARK
    order = sorted(range(len(values)), key=lambda i: values[i])
    labels_sorted = [labels[i] for i in order]
    values_sorted = [values[i] for i in order]
    fig = go.Figure()
    fig.add_bar(
        y=labels_sorted, x=values_sorted, orientation="h",
        marker_color=color, customdata=values_sorted,
        hovertemplate="%{y}: " + _hover_amount(lang) + "<extra></extra>",
        text=[f"{v:,.0f}" for v in values_sorted], textposition="outside",
        textfont=dict(size=11, color=tok.INK_SECONDARY),
    )
    layout = _base_layout(title, lang, height=height, show_legend=False, show_title=show_title)
    layout["yaxis"]["showgrid"] = False
    layout["xaxis"]["showgrid"] = True
    layout["xaxis"]["gridcolor"] = tok.GRIDLINE
    # The longest bar's outside data-label needs headroom past the bar's own
    # end, or it gets clipped by the plot area at narrower viewport widths.
    # An explicit axis range with ~22% headroom keeps every label fully
    # inside the plot area regardless of container width.
    max_val = max(values_sorted) if values_sorted else 0
    layout["xaxis"]["range"] = [0, max_val * 1.22 if max_val > 0 else 1]
    fig.update_layout(**layout)
    return fig


def expense_heatmap_chart(years, account_labels, z_matrix, lang: str, value_suffix: str = "", show_title: bool = True) -> go.Figure:
    fig = go.Figure(
        data=go.Heatmap(
            z=z_matrix, x=years, y=account_labels,
            colorscale=[[i / 12, tok.SEQUENTIAL_BLUE[step]] for i, step in enumerate(sorted(tok.SEQUENTIAL_BLUE))],
            hovertemplate="%{y} - %{x}: %{z:,.2f}" + value_suffix + "<extra></extra>",
            colorbar=dict(thickness=12, outlinewidth=0),
            hoverongaps=False,
        )
    )
    layout = _base_layout(t("chart.expense_heatmap", lang), lang, height=max(360, 22 * len(account_labels)), show_title=show_title)
    layout["xaxis"]["type"] = "category"
    layout["yaxis"]["showgrid"] = False
    fig.update_layout(**layout)
    return fig


def revenue_composition_chart(years, series_dict, lang: str, show_title: bool = True) -> go.Figure:
    """series_dict: {label: [values per year]} with at most 3 entries."""
    palette = [tok.CHART_NAVY, tok.CHART_TEAL, tok.CHART_TERRACOTTA]
    fig = go.Figure()
    for i, (label, values) in enumerate(series_dict.items()):
        fig.add_bar(
            x=years, y=values, name=label, marker_color=palette[i % len(palette)],
            customdata=values, hovertemplate=label + " %{x}: " + _hover_amount(lang) + "<extra></extra>",
        )
    layout = _base_layout(t("chart.revenue_composition", lang), lang, show_legend=True, show_title=show_title)
    layout["barmode"] = "stack"
    layout["xaxis"]["type"] = "category"
    fig.update_layout(**layout)
    return fig


def account_trend_chart(years, values, account_label: str, lang: str, show_title: bool = True) -> go.Figure:
    fig = go.Figure()
    fig.add_scatter(
        x=years, y=values, mode="lines+markers", line=dict(color=tok.CHART_NAVY, width=2.5),
        marker=dict(size=8), customdata=values,
        hovertemplate="%{x}: " + _hover_amount(lang) + "<extra></extra>",
        connectgaps=False,
    )
    layout = _base_layout(f"{t('chart.expense_trend', lang)} — {account_label}", lang, show_legend=False, show_title=show_title)
    layout["xaxis"]["type"] = "category"
    fig.update_layout(**layout)
    return fig


def cost_driver_waterfall_chart(base_year, comparison_year, base_total, top_movers, other_delta, comparison_total, lang: str, show_title: bool = True) -> go.Figure:
    """top_movers: list of (label, delta, status) sorted by |delta| desc.

    Built with go.Bar (base + height per segment) rather than go.Waterfall,
    because Waterfall has no per-point color override -- it can only color
    a whole trace by increasing/decreasing/totals. That matters here: a
    segment whose status is "Not Present" (the account is missing from the
    comparison year's dataset, not actually reduced) must render in a
    neutral gray, never the normal decrease-green, so it never reads as a
    confirmed saving.
    """
    from src.expense_analysis import STATUS_NOT_PRESENT

    currency = "ر.س" if lang == "ar" else "SAR"

    def fmt_val(v):
        return f"{v:,.2f} {currency}"

    x_labels = [str(base_year)]
    bases = [0.0]
    heights = [base_total]
    colors = [tok.CHART_NAVY]
    hover = [f"{base_year}: {fmt_val(base_total)}"]

    running = base_total
    for label, delta, status in top_movers:
        is_not_present = status == STATUS_NOT_PRESENT
        if delta >= 0:
            b, h = running, delta
        else:
            b, h = running + delta, -delta
        running += delta
        x_labels.append(label)
        bases.append(b)
        heights.append(h)
        if is_not_present:
            colors.append(tok.STATUS_NOT_PRESENT)
            hover.append(f"{label}: {t('loss.not_present_tooltip', lang)} ({fmt_val(delta)})")
        else:
            colors.append(tok.STATUS_CRITICAL if delta >= 0 else tok.STATUS_GOOD)
            hover.append(f"{label}: {fmt_val(delta)}")

    if abs(other_delta) > 0.01:
        if other_delta >= 0:
            b, h = running, other_delta
        else:
            b, h = running + other_delta, -other_delta
        running += other_delta
        x_labels.append(t("common.other", lang))
        bases.append(b)
        heights.append(h)
        colors.append(tok.STATUS_CRITICAL if other_delta >= 0 else tok.STATUS_GOOD)
        hover.append(f"{t('common.other', lang)}: {fmt_val(other_delta)}")

    x_labels.append(str(comparison_year))
    bases.append(0.0)
    heights.append(comparison_total)
    colors.append(tok.CHART_NAVY)
    hover.append(f"{comparison_year}: {fmt_val(comparison_total)}")

    fig = go.Figure()
    fig.add_bar(
        x=x_labels, y=heights, base=bases,
        marker_color=colors,
        hovertext=hover, hovertemplate="%{hovertext}<extra></extra>",
    )
    layout = _base_layout(t("chart.cost_driver_waterfall", lang), lang, height=420, show_title=show_title)
    layout["xaxis"]["type"] = "category"
    fig.update_layout(**layout)
    return fig


def actual_vs_scenario_chart(labels, actual_vals, scenario_vals, lang: str, show_title: bool = True) -> go.Figure:
    fig = go.Figure()
    fig.add_bar(x=labels, y=actual_vals, name=t("legend.actual", lang), marker_color=tok.CHART_NAVY,
                customdata=actual_vals, hovertemplate="%{x} " + t("legend.actual", lang) + ": " + _hover_amount(lang) + "<extra></extra>")
    fig.add_bar(x=labels, y=scenario_vals, name=t("legend.scenario", lang), marker_color=tok.CHART_TEAL,
                customdata=scenario_vals, hovertemplate="%{x} " + t("legend.scenario", lang) + ": " + _hover_amount(lang) + "<extra></extra>")
    layout = _base_layout(t("chart.actual_vs_scenario", lang), lang, show_legend=True, show_title=show_title)
    layout["barmode"] = "group"
    layout["xaxis"]["type"] = "category"
    fig.update_layout(**layout)
    return fig
