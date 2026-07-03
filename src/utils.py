import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_bar_chart(df, x, y, title, text=None, color=None, color_discrete_sequence=None):
    """
    Standardized Bar Chart using Plotly.
    """
    fig = px.bar(
        df, x=x, y=y, color=color, title=title, text=text,
        color_discrete_sequence=color_discrete_sequence or px.colors.qualitative.Pastel
    )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig

def create_pie_chart(df, names, values, title, color_discrete_sequence=None):
    """
    Standardized Pie Chart using Plotly.
    """
    fig = px.pie(
        df, names=names, values=values, title=title, hole=0.4,
        color_discrete_sequence=color_discrete_sequence or px.colors.qualitative.Pastel
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig

def create_scatter_plot(df, x, y, color, title, size=None):
    """
    Standardized Scatter Plot using Plotly.
    """
    fig = px.scatter(
        df, x=x, y=y, color=color, size=size, title=title,
        color_discrete_sequence=px.colors.qualitative.Set2,
        opacity=0.7
    )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig

def create_histogram(df, x, color, title, barmode='group'):
    """
    Standardized Histogram using Plotly.
    """
    fig = px.histogram(
        df, x=x, color=color, title=title, barmode=barmode,
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig

def create_box_plot(df, x, y, color, title):
    """
    Standardized Box Plot using Plotly.
    """
    fig = px.box(
        df, x=x, y=y, color=color, title=title,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig

def create_heatmap(corr_matrix, title):
    """
    Standardized Heatmap using Plotly.
    """
    fig = px.imshow(
        corr_matrix, text_auto=True, aspect="auto",
        title=title, color_continuous_scale="RdBu_r"
    )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig

def format_insight(what, why, impact, strategy):
    """
    Formats the business insight block.
    Returns a markdown string.
    """
    return f"""
**What the visualization shows:** {what}  
**Why the pattern occurs:** {why}  
**Business impact:** {impact}  
**Suggested retention strategy:** {strategy}
"""
