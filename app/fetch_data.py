import streamlit as st
import pandas as pd
import plotly_express as px
import pathlib

PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("..\DAVIS2.0\datasets").resolve()
DATA_PATH = PATH.joinpath("../data").resolve()


def convert_df(df):
    return df.to_csv().encode("utf-8")


def fetch_data():
    st.subheader("Fetch Previous Data")
    st.write("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True)
    type_set = st.radio("Select Experiment type: ", ("Environment", "Portfolio", "Hardware"))
    st.write("<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True)
    if type_set == "Environment":
        df1 = pd.read_csv(DATA_PATH.joinpath("source_file.csv"), low_memory=False)
        df_modified1 = df1.loc[df1["Experiment_type"] == type_set]
        exp_list = list(df_modified1[df_modified1["Experiment_name"].notnull()]["Experiment_name"].unique())
        exp_selected = st.selectbox("Select the experiment:", options=exp_list)
        df_modified2 = df1.loc[df1["Experiment_name"] == exp_selected]
        df_dow = df_modified2.copy()
        csv = convert_df(df_dow)
        select_mod = st.radio(
            label="Select:", options=["Fresh weight comparison", "Germination rate"]
        )  # , 'Temperature meta comparison',
        #'EC meta comparison'])
        st.write("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True)
        unique_seedbar_treatments = df_dow["Seedbar_treatment"].unique().tolist()
        unique_treatment_names = df_dow["Treatment_name"].unique().tolist()
        if select_mod == "Fresh weight comparison":
            if (unique_seedbar_treatments == unique_treatment_names) & (len(unique_seedbar_treatments) > 1):
                box_plot = px.box(
                    df_dow, x="Crop", y="FW_g", points="all", color="Seedbar_treatment", height=650, width=850
                )
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
            elif (unique_seedbar_treatments == unique_treatment_names) & (len(unique_seedbar_treatments) <= 1):
                box_plot = px.box(df_dow, x="Crop", y="FW_g", points="all", color="Crop", height=650, width=850)
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
            elif (
                (unique_seedbar_treatments != unique_treatment_names)
                & (len(unique_seedbar_treatments) <= 1)
                & (len(unique_treatment_names) > 1)
            ):
                box_plot = px.box(
                    df_dow, x="Crop", y="FW_g", points="all", color="Treatment_name", height=650, width=850
                )
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
            elif (
                (unique_seedbar_treatments != unique_treatment_names)
                & (len(unique_seedbar_treatments) > 1)
                & (len(unique_treatment_names) <= 1)
            ):
                box_plot = px.box(
                    df_dow, x="Crop", y="FW_g", points="all", color="Seedbar_treatment", height=650, width=850
                )
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
            else:
                box_plot = px.box(
                    df_dow,
                    x="Crop",
                    y="FW_g",
                    points="all",
                    color="Seedbar_treatment",
                    facet_col="Treatment_name",
                    height=650,
                    width=850,
                )
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
        elif select_mod == "Germination rate":
            if (unique_seedbar_treatments == unique_treatment_names) & (len(unique_seedbar_treatments) > 1):
                df_germ = (
                    df_dow[(df_dow["Germination_rate"].notnull()) & (df_dow["DAP"] != 0)]
                    .groupby(["Seedbar_treatment", "Crop", "Position", "Layer"], as_index=False)["Germination_rate"]
                    .last()
                )
                box_plot = px.box(
                    df_germ,
                    x="Crop",
                    y="Germination_rate",
                    points="all",
                    color="Seedbar_treatment",
                    height=650,
                    width=850,
                )
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
            elif (unique_seedbar_treatments == unique_treatment_names) & (len(unique_seedbar_treatments) <= 1):
                df_germ = (
                    df_dow[(df_dow["Germination_rate"].notnull() & (df_dow["DAP"] != 0))]
                    .groupby(["Crop", "Position", "Layer"], as_index=False)["Germination_rate"]
                    .last()
                )
                box_plot = px.box(
                    df_germ, x="Crop", y="Germination_rate", points="all", color="Crop", height=650, width=850
                )
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
            elif (
                (unique_seedbar_treatments != unique_treatment_names)
                & (len(unique_seedbar_treatments) <= 1)
                & (len(unique_treatment_names) > 1)
            ):
                df_germ = (
                    df_dow[(df_dow["Germination_rate"].notnull() & (df_dow["DAP"] != 0))]
                    .groupby(["Crop", "Treatment_name", "Position", "Layer"], as_index=False)["Germination_rate"]
                    .last()
                )
                box_plot = px.box(
                    df_germ, x="Crop", y="Germination_rate", points="all", color="Treatment_name", height=650, width=850
                )
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
            elif (
                (unique_seedbar_treatments != unique_treatment_names)
                & (len(unique_seedbar_treatments) > 1)
                & (len(unique_treatment_names) <= 1)
            ):
                df_germ = (
                    df_dow[(df_dow["Germination_rate"].notnull() & (df_dow["DAP"] != 0))]
                    .groupby(["Crop", "Seedbar_treatment", "Position", "Layer"], as_index=False)["Germination_rate"]
                    .last()
                )
                box_plot = px.box(
                    df_germ,
                    x="Crop",
                    y="Germination_rate",
                    points="all",
                    color="Seedbar_treatment",
                    height=650,
                    width=850,
                )
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
            else:
                df_germ = (
                    df_dow[(df_dow["Germination_rate"].notnull() & (df_dow["DAP"] != 0))]
                    .groupby(["Crop", "Seedbar_treatment", "Treatment_name", "Position", "Layer"], as_index=False)[
                        "Germination_rate"
                    ]
                    .last()
                )
                box_plot = px.box(
                    df_germ,
                    x="Crop",
                    y="Germination_rate",
                    points="all",
                    color="Seedbar_treatment",
                    facet_col="Treatment_name",
                    height=650,
                    width=850,
                )
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
        # elif select_mod == 'Cube Temperature comparison':
        #     df_line = df_dow[(df_dow['Temperature'].notnull())].groupby(['Cube_name', 'DAP', 'Layer'],
        #                                                                         as_index=False)[
        #         'Temperature'].mean()
        #     line_plot = px.line(df_line, x='DAP', y='Temperature', color='Cube_name', height=650, width=850)
        #     line_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
        #     line_plot.update_xaxes(matches=None, showticklabels=True)
        #     st.plotly_chart(line_plot)
        #     st.write('Datatable:')
        #     st.dataframe(df_dow)
        # elif select_mod == 'EC comparison':
        #     df_line = df_dow[(df_dow['EC'].notnull())].groupby(
        #         ['Cube_name', 'DAP'],
        #         as_index=False)['Average_EC_10_days_after_planting', 'Average_EC_10_days_before_harvest'].mean()
        #     line_plot = px.line(df_line, x='DAP', y=['Average_EC_10_days_after_planting'],
        #                         color='Cube_name', height=650, width=850)
        #     line_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
        #     line_plot.update_xaxes(matches=None, showticklabels=True)
        #     st.plotly_chart(line_plot)
        #     st.write('Datatable:')
        #     st.dataframe(df_dow)
        st.download_button(label="Download as .csv file", data=csv, mime="text/csv")
    elif type_set == "Portfolio":
        df1 = pd.read_csv(DATA_PATH.joinpath("source_file.csv"), low_memory=False)
        df_modified1 = df1.loc[df1["Experiment_type"] == type_set]
        exp_list = list(df_modified1[df_modified1["Experiment_name"].notnull()]["Experiment_name"].unique())
        exp_selected = st.selectbox("Select the experiment:", options=exp_list)
        df_modified2 = df1.loc[df1["Experiment_name"] == exp_selected]
        df_dow = df_modified2.copy()
        csv = convert_df(df_dow)
        select_mod = st.radio(label="select:", options=["Fresh weight comparison", "Germination rate"])
        st.write("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True)
        if select_mod == "Fresh weight comparison":
            box_plot = px.box(
                df_dow[df_dow["Crop_name_manually_entered"].notnull()],
                x="Crop_name_manually_entered",
                y="FW_g",
                points="all",
                color="Crop_name_manually_entered",
                height=650,
                width=850,
            )
            box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
            box_plot.update_xaxes(matches=None, showticklabels=True)
            st.plotly_chart(box_plot)
            st.write("Datatable:")
            st.dataframe(df_dow)
        elif select_mod == "Germination rate":
            df_line = (
                df_dow[
                    (
                        (df_dow["Germination_rate"].notnull())
                        & (df_dow["Crop_name_manually_entered"].notnull())
                        & (df_dow["DAP"] != 0)
                    )
                ]
                .groupby(["Layer", "Position", "Crop_name_manually_entered", "Cube_name"], as_index=False)[
                    "Germination_rate"
                ]
                .last()
            )
            box_plot = px.box(
                df_line,
                x="Crop_name_manually_entered",
                y="Germination_rate",
                color="Crop_name_manually_entered",
                height=650,
                width=850,
                points="all",
            )
            box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
            box_plot.update_xaxes(matches=None, showticklabels=True)
            st.plotly_chart(box_plot)
            st.write("Datatable:")
            st.dataframe(df_dow)
        st.download_button(label="Download as .csv file", data=csv, mime="text/csv")
    elif type_set == "Hardware":
        df1 = pd.read_csv(DATA_PATH.joinpath("source_file.csv"), low_memory=False)
        df_modified1 = df1.loc[df1["Experiment_type"] == type_set]
        exp_list = list(df_modified1[df_modified1["Experiment_name"].notnull()]["Experiment_name"].unique())
        exp_selected = st.selectbox("Select the experiment:", options=exp_list)
        df_modified2 = df1.loc[df1["Experiment_name"] == exp_selected]
        df_dow = df_modified2.copy()
        csv = convert_df(df_dow)
        select_mod = st.radio(
            label="Select:", options=["Fresh weight comparison", "Germination rate"]
        )  # , 'Temperature meta comparison',
        #'EC meta comparison'])
        st.write("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True)
        unique_seedbar_treatments = df_dow["Seedbar_treatment"].unique().tolist()
        unique_treatment_names = df_dow["Treatment_name"].unique().tolist()
        if select_mod == "Fresh weight comparison":
            if (unique_seedbar_treatments == unique_treatment_names) & (len(unique_seedbar_treatments) > 1):
                box_plot = px.box(
                    df_dow, x="Crop", y="FW_g", points="all", color="Seedbar_treatment", height=650, width=850
                )
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
            elif (unique_seedbar_treatments == unique_treatment_names) & (len(unique_seedbar_treatments) <= 1):
                box_plot = px.box(df_dow, x="Crop", y="FW_g", points="all", color="Crop", height=650, width=850)
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
            elif (
                (unique_seedbar_treatments != unique_treatment_names)
                & (len(unique_seedbar_treatments) <= 1)
                & (len(unique_treatment_names) > 1)
            ):
                box_plot = px.box(
                    df_dow, x="Crop", y="FW_g", points="all", color="Treatment_name", height=650, width=850
                )
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
            elif (
                (unique_seedbar_treatments != unique_treatment_names)
                & (len(unique_seedbar_treatments) > 1)
                & (len(unique_treatment_names) <= 1)
            ):
                box_plot = px.box(
                    df_dow, x="Crop", y="FW_g", points="all", color="Seedbar_treatment", height=650, width=850
                )
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
            else:
                box_plot = px.box(
                    df_dow,
                    x="Crop",
                    y="FW_g",
                    points="all",
                    color="Seedbar_treatment",
                    facet_col="Treatment_name",
                    height=650,
                    width=850,
                )
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
        elif select_mod == "Germination rate":
            if (unique_seedbar_treatments == unique_treatment_names) & (len(unique_seedbar_treatments) > 1):
                df_germ = (
                    df_dow[(df_dow["Germination_rate"].notnull()) & (df_dow["DAP"] != 0)]
                    .groupby(["Seedbar_treatment", "Crop", "Position", "Layer"], as_index=False)["Germination_rate"]
                    .last()
                )
                box_plot = px.box(
                    df_germ,
                    x="Crop",
                    y="Germination_rate",
                    points="all",
                    color="Seedbar_treatment",
                    height=650,
                    width=850,
                )
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
            elif (unique_seedbar_treatments == unique_treatment_names) & (len(unique_seedbar_treatments) <= 1):
                df_germ = (
                    df_dow[(df_dow["Germination_rate"].notnull() & (df_dow["DAP"] != 0))]
                    .groupby(["Crop", "Position", "Layer"], as_index=False)["Germination_rate"]
                    .last()
                )
                box_plot = px.box(
                    df_germ, x="Crop", y="Germination_rate", points="all", color="Crop", height=650, width=850
                )
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
            elif (
                (unique_seedbar_treatments != unique_treatment_names)
                & (len(unique_seedbar_treatments) <= 1)
                & (len(unique_treatment_names) > 1)
            ):
                df_germ = (
                    df_dow[(df_dow["Germination_rate"].notnull() & (df_dow["DAP"] != 0))]
                    .groupby(["Crop", "Treatment_name", "Position", "Layer"], as_index=False)["Germination_rate"]
                    .last()
                )
                box_plot = px.box(
                    df_germ, x="Crop", y="Germination_rate", points="all", color="Treatment_name", height=650, width=850
                )
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
            elif (
                (unique_seedbar_treatments != unique_treatment_names)
                & (len(unique_seedbar_treatments) > 1)
                & (len(unique_treatment_names) <= 1)
            ):
                df_germ = (
                    df_dow[(df_dow["Germination_rate"].notnull() & (df_dow["DAP"] != 0))]
                    .groupby(["Crop", "Seedbar_treatment", "Position", "Layer"], as_index=False)["Germination_rate"]
                    .last()
                )
                box_plot = px.box(
                    df_germ,
                    x="Crop",
                    y="Germination_rate",
                    points="all",
                    color="Seedbar_treatment",
                    height=650,
                    width=850,
                )
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
            else:
                df_germ = (
                    df_dow[(df_dow["Germination_rate"].notnull() & (df_dow["DAP"] != 0))]
                    .groupby(["Crop", "Seedbar_treatment", "Treatment_name", "Position", "Layer"], as_index=False)[
                        "Germination_rate"
                    ]
                    .last()
                )
                box_plot = px.box(
                    df_germ,
                    x="Crop",
                    y="Germination_rate",
                    points="all",
                    color="Seedbar_treatment",
                    facet_col="Treatment_name",
                    height=650,
                    width=850,
                )
                box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                box_plot.update_xaxes(matches=None, showticklabels=True)
                st.plotly_chart(box_plot)
                st.write("Datatable:")
                st.dataframe(df_dow)
        st.write("Datatable:")
        st.dataframe(df_dow)
        st.download_button(label="Download as .csv file", data=csv, mime="text/csv")

