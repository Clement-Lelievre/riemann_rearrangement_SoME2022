import streamlit as st

from utils import (
    feed_plotly_fig,
    raise_count,
    reset_count,
    get_alternating_series_graph,
    make_plotly_fig,
    make_animation,
)

st.set_page_config(
    page_title="Riemann magic",
    page_icon=":heavy_plus_sign:",
    layout="centered",  # wide
    initial_sidebar_state="auto",  # collapsed
    menu_items={
        "About": "# Riemann rearrangement *SoME 2022*",
        "Get help": "https://github.com/Clement-Lelievre/riemann_rearrangement_SoME2022",
    },
)

st.title("♾️ A walk down Rearrangement Street ♾️")

st.markdown(
    """\n

    #### 1 + 2 = 2 + 1, right ? Formally, the addition of real numbers is commutative
    #### What if it's not *always* true?
    #### What if you could alter the sum by changing the order of the numbers you're adding up?
    #### This counter-intuitive fact works for certain series called "*conditionally convergent*" real number series and was discovered by Bernhard Riemann in his [rearrangement theorem](https://en.wikipedia.org/wiki/Riemann_series_theorem)
"""
)

with st.expander("What is a conditionally convergent real number series?"):
    st.write(
        "It is a sequence of real numbers (any number except complex ones) that when added up converge to a single real number, \
             but if you add up the absolute values of the numbers in the sequence, it will not converge to a single real number and\
                 diverge to infinity ♾️ instead. More [here](https://en.wikipedia.org/wiki/Conditional_convergence)"
    )


st.markdown(""" ## A classic illustration: the alternating harmonic series""")

st.latex(
    r"""
    \sum_{k=1}^\infty \frac{(-1)^{k+1}}{k} = 1 - \frac{1}{2} + \frac{1}{3} - \frac{1}{4} + \cdots \xrightarrow{\enskip\\} ln(2)
    """
)

st.markdown(
    """#### In layman's terms, if you take 1, subtract its half, add its third, subtract its fourth, etc., for a \
            *very long time*, you'll get to approximately 0.69 (and arbitrarily close to ln(2), exactly). Basically, the marginal effect of adding up the last term \
                becomes negligible so you end up with an actual number instead of infinity"""
)

with st.expander("What does its graph look like?"):
    st.image("alternating_series.png")

st.markdown("""#### Try it out for yourself below and construct the series:""")

if "riemann_sum" not in st.session_state:
    st.session_state.riemann_sum = 0

if "count" not in st.session_state:
    st.session_state.count = 0

if "series_string" not in st.session_state:
    st.session_state.series_string = ""

col1, col2 = st.columns(2)
increment = col1.button(
    label=f"Add one more term ({-1 if st.session_state.count % 2 else 1}"
    + (f"/{st.session_state.count + 1})" if st.session_state.count else ")"),
    on_click=raise_count,
)
reset = col2.button(label="Reset addition", on_click=reset_count)
col3, col4 = st.columns(2)
col3.write(f"Series = {st.session_state.series_string}")
col4.write(f"Sum = {st.session_state.riemann_sum}")

st.pyplot(get_alternating_series_graph(st.session_state.count))

st.markdown("# Let's change the limit")
st.markdown(
    """#### Now, changing the order of the terms does change the end result! 🤩
#### And there's better: choose any sum you like (including infinity), and there will always exist at least one *rearrangement* of terms such that the new sum if that value you selected"""
)


st.markdown("### Currently the sum converges towards ln(2) ~ 0.69. Let us change that!")

if "new_sum" not in st.session_state:
    st.session_state.new_sum = 2.0

new_sum = st.number_input(
    "Pick a new limit of your choice (incl. a very specific number) 👇",
    0.0,
    3.0,
    2.0,
    step=0.5,
    help="Pick the real number the sum will converge to after rearranging its terms",
    format="%f",
)
series_values, new_sum, cycle_size, *_ = feed_plotly_fig(new_sum)

tab1, tab2 = st.tabs(["Change the sum!", "The series in motion!"])

with tab1:

    st.plotly_chart(make_plotly_fig(series_values, new_sum, cycle_size))
    st.markdown(
        "You can zoom in ☝️ on an area 📈 with the 🖱️. Double-click to zoom back out."
    )
    st.markdown(
        "### Once you're done, you can view the series being built dynamically on the next tab ☝️"
    )
with tab2:
    with st.spinner("Preparing the animation..."):
        st.plotly_chart(make_animation(series_values, new_sum))


with st.expander("What's the trick?"):
    st.markdown(
        "#### Whatever the number you choose (assume it is positive for the sake of the example), you can always add upp positive terms of the series (1, 1/3, 1/5, 1/7 and so on) until the sum becomes bigger than this number."
    )
    st.markdown(
        "#### That is because, remember, the sum of the absolute values of the terms of the series diverges towards infinity and so does the sum of the positive terms"
    )
    st.markdown(
        "#### So once the sum gets just over that number, add up the first negative term (-1/2) (more rigorously, you should likewise add up just enough negative terms to go below your target number, but in practice this will often boil down to a single negative term). Then add up enough positive terms to go just over it again. And so on."
    )
    st.markdown(
        "#### Don't hesitate to zoom in on the above graph with your mouse, to picture that effect better"
    )

with st.expander("💡 Notice any pattern?"):
    st.markdown(
        '#### The number of terms required to offset the previously added negative term converges! This is what I called a "cycle" above in the graph xaxis label'
    )
    st.markdown(
        f"#### e.g. currently, tweaking the series to make it converge towards {new_sum} implies a rearrangement such that after a few iterations, it takes {cycle_size} positive terms to offset one negative term"
    )


st.markdown("#### Thanks for reading this far!")
with st.expander(
    "On a lighter note, do you now feel powerful enough to accomplish prowesses like this?"
):
    st.image(
        "1280px-Feeding_the_multitude,_Daniel_of_Uranc,_1433.jpg",
        caption="The feeding of the multitude, by Daniel of Uranc, c. 1433",
    )
    st.write(
        """DISCLAIMER: The purpose of the above image isn’t to challenge your personal faith or promote/discard any religion. 
             I have no stake in your attitude about God or atheism."""
    )


st.markdown(
    "#### Does it inspire you? Do you foresee any applications of this theorem?"
)
with st.expander("Yes, let me send you an email 📧!"):
    st.write("clement.lelievre91@gmail.com")
