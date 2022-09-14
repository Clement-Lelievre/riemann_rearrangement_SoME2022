from functools import lru_cache
from math import log
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np


@st.experimental_memo
@lru_cache
def riemann_sum(n: int) -> float:
    """Takes an integer representing the index up to which the sum of the alternate harmonic series is computed\n
    Args
    n: int the max index of the sum\n
    Returns:
    The sum of the alternate harmonic series up to index n"""
    return sum((-1) ** k / (k + 1) for k in range(n))


def _get_alternating_series_graph_image(n: int = 100):
    """Used just once to generate an image for the Streamlit app"""
    x = [_ for _ in range(n)]  # the indices
    y = [riemann_sum(i) for i in x]  # the sum values up to indice i_
    plt.figure()
    plt.plot(x, y, label="Our strange addition")
    plt.plot(x, [log(2)] * n, c="r", label="ln(2)")
    plt.title("""Alternating harmonic series""", fontdict={
                #"family": "serif",
                "color": "blue",
                "weight": "bold",
                "size": 12,
            })
    plt.xlabel("Number of terms added up")
    plt.ylabel("Sum")
    plt.legend()
    plt.savefig("alternating_series.png")


def get_alternating_series_graph(n: int = 100):
    """Used for the user to construct the graph step by step in the app"""
    x = [_ for _ in range(n + 1)]  # the indices
    y = [riemann_sum(i) for i in x]  # the sum values up to indice i_
    fig_ = plt.figure()
    plt.plot(x, y, label=f"Our strange addition ({n} terms)")
    plt.plot(x, [log(2)] * (n + 1), c="r", label="y = ln(2)")
    plt.title("""Alternating harmonic series""", fontdict={
                #"family": "serif",
                "color": "blue",
                "weight": "bold",
                "size": 12,
            })
    plt.xlabel("Number of terms added up")
    plt.xticks(range(n + 1))
    plt.ylabel("Sum")
    plt.legend()
    return fig_


def raise_count():
    """Alters the session state by raising the count by 1 and updating the sum"""
    st.session_state.count += 1
    st.session_state.riemann_sum = riemann_sum(st.session_state.count)
    st.session_state.series_string += (
        " + " if st.session_state.count % 2 else " - "
    ) + f"1/{st.session_state.count}"


def reset_count():
    """resets the session state count to 0 and updates the sum to 0"""
    st.session_state.count = 0
    st.session_state.riemann_sum = 0
    st.session_state.series_string = ""


@st.experimental_memo
@lru_cache
def feed_plotly_fig(new_sum: float, /, nb_cycles: int = 80) -> tuple:
    """Updates the plotly graph with the new sum"""
    # TO DO: enhance performance by improving the algorithm
    pos = np.ones(shape=(50_000,)) / np.linspace(1, 100_000, 50_000)
    neg = -1 * np.ones(shape=(50_000,)) / np.linspace(2, 100_000, 50_000)
    s = 0
    index_pos = 0
    index_neg = 0
    series_values = []
    cycle_size = []
    for _ in range(nb_cycles):
        while s < new_sum:
            # s = np.cumsum(pos[:index_pos])
            s += pos[index_pos]
            index_pos += 1
            series_values.append(s)
        cycle_size.append(index_pos)
        s += neg[index_neg]
        index_neg += 1
        series_values.append(s)
    cycle_size = [cycle_size[i + 1] - cycle_size[i] for i in range(len(cycle_size) - 1)]
    cycle_size = int(sum(cycle_size) / len(cycle_size))
    return series_values, new_sum, cycle_size


def make_plotly_fig(*args):
    series_values, new_sum, cycle_size, *_ = args
    fig = go.Figure()
    x = list(range(len(series_values)))
    fig.add_trace(go.Scatter(x=x, y=series_values, name="The series rearranged"))
    fig.add_trace(
        go.Scatter(
            x=np.arange(len(x)),
            y=np.tile(new_sum, len(x)),
            name=f"y = {new_sum}",
            line=dict(color="red"),
        )
    )
    fig.update_layout(
        title=f"Alternating harmonic series rearranged (sum -> {new_sum})",
        xaxis_title=f"Number of terms added up (cycle size: {cycle_size})",
        yaxis_title="Sum",
    )
    return fig


@st.experimental_memo
def make_animation(series_values, new_sum):
    """Prepares the data for the Plotly animation that shows the rearranged series in motion

    Args:
        series_values (list): the values taken by the series, in order
        new_sum (float): the limit of the rearranged series

    Returns:
        fig: the Plotly figure object
    """
    series_values = series_values[:100]
    x = list(range(len(series_values)))
    fig = go.Figure(
        data=[
            go.Scatter(
                x=np.arange(len(x)),
                y=np.tile(new_sum, len(x)),
                name=f"y = {new_sum}",
                line=dict(color="red"),
            )
        ],
        layout=go.Layout(
            xaxis_title=f"Number of terms added up",
            yaxis_title="Sum",
            title=f"The series in motion (limit = {new_sum})",
            updatemenus=[
                dict(
                    type="buttons",
                    buttons=[dict(label="&#931;", method="animate", args=[None])],
                    font={'color':'red'},
                )
            ],
        ),
        frames=[
            go.Frame(
                data=[
                    go.Scatter(
                        x=x[:i],
                        y=series_values[:i],
                        name=f"rearranged series (sum -> {new_sum})",
                        line=dict(color="blue"),
                    )
                ],
                layout=go.Layout(
                    title_text=f"The series in motion (limit = {new_sum})"
                ),
            )
            for i in range(len(series_values))
        ],
    )
    return fig


if __name__ == "__main__":
    # get_alternating_series_graph()
    # a = np.ones(shape=3)
    # print(a)
    # print(np.cumsum(a))
    _get_alternating_series_graph_image()
