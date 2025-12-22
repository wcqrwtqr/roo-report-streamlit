import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Tuple
import time
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Variabels
# known
poro = 0.28
rw = 0.4  # in ft
h = 86  # in ft
ct = 9e-06  # in psi^-1
pi = 3700  # initial pressure in psia
mu_oil = 1  # in cP
Bo = 1.121  # in RB/STB
re = np.inf  # reservoir is infinity in size
q = 3000  # RB/D
pwf = 3462.4  # in psia, flowing pressure
# the well is flowed for 24 hours, then shut-in for another 24 hours (24-hour buildup)
tp = 12


def regression(x, y):
    # number of observations/points
    n = np.size(x)

    # mean of x and y vector
    m_x, m_y = np.mean(x), np.mean(y)

    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y*x) - n*m_y*m_x
    SS_xx = np.sum(x*x) - n*m_x*m_x

    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1*m_x

    return(b_0, b_1)


@st.cache_data
def load_df_horner(source_file: str) -> Tuple[pd.DataFrame, List[int]]:
    """
    Load the csv file data in elapse time and pressure only and output the \
    dataframe and a list.

    Return data is a tuple of dataframe and list.
    """
    try:
        df = pd.read_csv(source_file, sep=",")
    except Exception as e:
        st.write("Error loading the file - ensure using the correct file\n" + str(e))
    range_data = df.index.tolist()
    return df, range_data


def Horner_plot_data(source_file):
    """
    Load the dataframe from the previous function and draw the horner\
    plot in the streamlit.

    Accept the csv file and generate the plots.
    """
    # Load data to df
    df, range_data = load_df_horner(source_file)
    range_data_selection = st.slider(
        "Range:",
        min_value=min(range_data),
        max_value=max(range_data),
        value=(min(range_data), max(range_data)),
    )
    df_lst = df[range_data_selection[0] : range_data_selection[1]]
    with st.expander(label="Table of Data"):
        NN = st.selectbox("Interval", [1, 2, 5, 10, 25, 50, 100])
        if NN is None:  # This code is to address int|None condition
            NN = 1
        st.dataframe(df_lst.loc[:: int(NN)])
        st.markdown(f"*Available Data: {df_lst.loc[::int(NN)].shape[0]}")
        st.download_button(
            label="Download data", data=df_lst.loc[:: int(NN)].to_csv(), mime="csv"
        )

    with st.expander(label="Pressure plot"):
        graph = graphing_horner_1v(
            df_lst,
            "Hours",
            "Pressure",
            title="Pressure Buildup Profile Over Time",
            x_lable="Time(Hourse)",
            y_label="Pressure(psi)",
        )
        st.plotly_chart(graph)

    with st.expander(label="Horner Plot"):
        # graph = graphing_horner_1v(df_lst, "Hours", "Pressure")
        # st.plotly_chart(graph)
        delta_t = df_lst.Hours - df_lst.Hours[0]
        x_horner = np.log10((24 + delta_t) / delta_t)
        horner = pd.DataFrame(
            {
                "Time(hour)": df_lst.Hours,
                "logtime": x_horner,
                "Shut-in pressure(psia)": df.Pressure,
            }
        )
        # Graph the new horner plot after update dataframe
        index5 = 15_000
        # cut dataframe from index 0 to index of end of straight line
        dfhorner = horner.iloc[index5:, :]
        # linear regression to find slope and intercept of a straight line
        x5 = dfhorner.iloc[:, 1]
        y5 = dfhorner.iloc[:, 2]
        c5, m5 = regression(x5,y5)
        pi = c5 # initial pressure equals to intercept c5
        graph = graphing_horner_1v(
            horner,
            "logtime",
            "Shut-in pressure(psia)",
            title="Complete Horner Build Plot",
            x_lable="Log((tp+delta_t)/delte_t)",
            y_label="Shut-in pressure, pws (psi)",
        )
        st.plotly_chart(graph)
        st.write("Slope of linear-region Horner plot:", m5)
        st.write("Intercept of linear-region Horner plot:", c5, "psia")
        st.write("The initial reservoir pressure equals to the intercept:", pi, "psia")
        # Calculate the skin below
        # calculate permeability
        k = - (162.6 * q * Bo * mu_oil) / (m5 * h)
        # calculate skin factor
        # determine b1hr: pressure value at t = 1 hour, in psia
        b1hr = c5 + m5 * np.log10(tp + 1)
        s = 1.1513 * (((pwf - b1hr) / m5) - np.log10(k / (poro * mu_oil * ct * (rw**2))) + 3.2275)
        st.write("Skin factor:", s)
        # Calculate pressure drop due to well damage
        delta_ps = ((141.2 * q * Bo * mu_oil) / (k * h)) * s
        st.write("Pressure drop due to well skin:", delta_ps, "psia")
        delta_p_shutin = pi - df.Pressure[0]
        st.write("Pressure drop before shut-in:", delta_p_shutin, "psia")
        wellskin_contribution = (delta_ps / delta_p_shutin) * 100
        st.write("Well damage contribute to:", wellskin_contribution, "% of total pressure drop")
        formation_drop = delta_p_shutin - delta_ps
        formation_contribution = 100 - wellskin_contribution
        st.write("Reservoir formation contribute to:", formation_drop, "psia of the total pressure drop,\nor in percent:", formation_contribution, "% of total pressure drop")


def graphing_horner_1v(
    df: pd.DataFrame, x: str, ym: str, title: str, x_lable: str, y_label: str
):
    """Graphing code that can graph the values from the DataFrame\
    for two axes only and can by used and called serveral time as\
    much as you need.

    This function is only for the Horner plot only.
    """
    xt = df[x]
    yp = df[ym]
    # Making the graph for the values
    fig_n = make_subplots(specs=[[{"secondary_y": True}]])
    # Added below update_layout to see if I can add the hover in the graph
    # It worked nicely :)
    fig_n.update_layout(
        title_text=f"{ym}",
        hovermode="x unified",  # Enables crosshair line for hover
    )
    fig_n.update_layout(title_text=title)
    fig_n.update_xaxes(title_text=x_lable)
    fig_n.update_yaxes(title_text=y_label)
    fig_n.add_trace(go.Scatter(x=xt, y=yp, mode="lines", name=ym))
    return fig_n
