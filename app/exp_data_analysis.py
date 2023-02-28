import streamlit as st
import pandas as pd
import plotly_express as px
import numpy as np


# this function is referenced from main.py


def exp_data_analysis():
    st.subheader("Experiment Data Analysis")
    uploaded_file = st.sidebar.file_uploader(label="Upload :", type=["csv", "xlsx"])

    global df
    # this if loop toggles between different statuses of the uploaded file and also
    # let to read between csv anv xlsx files unless it prints the no file markdown
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, low_memory=False)
        except Exception as e:
            df = pd.read_excel(uploaded_file)
            print(e)
    elif uploaded_file is None:
        st.warning("Please upload a file to analyse or confirm your file extension(.csv/.xlsx only) and try again!")

    # all global variables are declared here which is later used in the graphing functions
    global xdata_list, ydata_list, crop_list, facet_var_list, color_var_list, default_x, default_y, default_cr, std_h, std_w, default_clr, default_fac, norm_h, norm_w, facet_col_wrap, color_var, facet_num, facet_var, facet_col_wrap, facet_col_spacing, facet_row_spacing
    try:
        # this if statement throughout the code bypasses the requirement of having crops in dataframe.
        if "Crop" in df.columns:
            xdata_list = list(
                [
                    i
                    for i in df.columns
                    if i
                    not in [
                        "Experiment_ID",
                        "Experiment_name",
                        "Start_date",
                        "Substrate",
                        "Variant",
                        "NP",
                        "Germination_rate",
                        "FW_g",
                        "PW_g",
                        "DW_g",
                        "DW_content",
                        "Observations",
                        "Cover_sheet",
                        "Substrate_type",
                        "Plantcube_ID",
                        "Experiment_type",
                        "EC",
                        "pH",
                        "NO3",
                        "K",
                        "Ca2",
                        "Water_level",
                        "Nutrients_added",
                        "max_water_level",
                        "EC_normalized_by_water_level",
                        "Temperature",
                    ]
                ]
            )
            ydata_list = list(
                [
                    i
                    for i in df.columns
                    if i
                    not in [
                        "Experiment_ID",
                        "Experiment_name",
                        "Start_date",
                        "Measurement_date",
                        "Treatment_name",
                        "Cube_name",
                        "Layer",
                        "Position",
                        "Plant_ID",
                        "Substrate",
                        "Variant",
                        "Crop",
                        "Seed_density",
                        "Seedbar_treatment",
                        "NP",
                        "Crop_name_manually_entered",
                        "Plantcube_version",
                        "Production_type",
                        "Substrate",
                        "Variant",
                        "Observations",
                        "Cover_sheet",
                        "Substrate_type",
                        "Plantcube_ID",
                        "Experiment_type",
                        "Nutrients_added",
                        "max_water_level",
                    ]
                ]
            )
            color_var_list = list(
                [
                    i
                    for i in df.columns
                    if i
                    not in [
                        "Experiment_ID",
                        "Experiment_name",
                        "Start_date",
                        "Substrate",
                        "Variant",
                        "NP",
                        "Germination_rate",
                        "FW_g",
                        "PW_g",
                        "DW_g",
                        "DW_content",
                        "Observations",
                        "Cover_sheet",
                        "Substrate_type",
                        "Plantcube_ID",
                        "Experiment_type",
                        "EC",
                        "pH",
                        "NO3",
                        "K",
                        "Ca2",
                        "Water_level",
                        "Nutrients_added",
                        "max_water_level",
                        "EC_normalized_by_water_level",
                        "Temperature",
                        "Average_temperature",
                        "Average_EC_10_days_before_harvest",
                        "Average_EC_10_days_after_planting",
                        "GDD",
                    ]
                ]
                + ["None"]
            )
            facet_var_list = list(
                [
                    i
                    for i in df.columns
                    if i
                    not in [
                        "Experiment_ID",
                        "Experiment_name",
                        "Start_date",
                        "Substrate",
                        "Variant",
                        "NP",
                        "Germination_rate",
                        "FW_g",
                        "PW_g",
                        "DW_g",
                        "DW_content",
                        "Observations",
                        "Cover_sheet",
                        "Substrate_type",
                        "Plantcube_ID",
                        "Experiment_type",
                        "EC",
                        "pH",
                        "NO3",
                        "K",
                        "Ca2",
                        "Water_level",
                        "Nutrients_added",
                        "max_water_level",
                        "EC_normalized_by_water_level",
                        "Temperature",
                        "Average_temperature",
                        "Average_EC_10_days_before_harvest",
                        "Average_EC_10_days_after_planting",
                        "GDD",
                    ]
                ]
                + ["None"]
            )
            crop_list = list(df[df["Crop"].notnull()]["Crop"].unique())
            default_cr = list(df[df["Crop"].notnull()]["Crop"].unique())
            default_x = xdata_list.index("Crop")
            default_y = ydata_list.index("FW_g")
            default_fac = facet_var_list.index("None")
            default_clr = color_var_list.index("None")
            std_h = 650
            std_w = 850
        else:
            # if there is no crop data in the dataframe
            xdata_list = df.columns.unique()
            ydata_list = df.columns.unique()
            color_var_list = list([i for i in df.columns] + ["None"])
            facet_var_list = list([i for i in df.columns] + ["None"])
            default_x = 0
            default_y = 1
            default_fac = facet_var_list.index("None")
            default_clr = color_var_list.index("None")
            std_h = 650
            std_w = 850
            crop_list = ["No crops in data"]

    except Exception as e:
        print(e)
    # this if loop only activates and prints the radio items if the upload status turn 1
    # and also prevents dynamic caching to avoid multi-user interference
    if uploaded_file is not None:
        if "Crop" not in df:
            df["Crop"] = "No crops in data"
        select_graph = st.sidebar.radio(label="Select plot type:", options=["Box", "Scatter", "line"])
        st.write("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True)
        if select_graph == "Box":
            try:
                # plot parameters including crop filter
                if "Crop" in df.columns:
                    st.sidebar.subheader("Box plot settings")
                    x_data = st.sidebar.selectbox("X axis:", options=xdata_list, index = default_x)
                    y_data = st.sidebar.selectbox("Y axis:", options=ydata_list, index = default_y)
                    color_var = st.sidebar.selectbox("Colour:", options=color_var_list, index = default_fac)
                    facet_var = st.sidebar.selectbox("Facet:", options=facet_var_list, index = default_clr)
                    if facet_var != "None":
                        facet_num = df[facet_var].nunique()
                        if (facet_num % 2) == 0:
                            facet_col_wrap = 2
                        else:
                            facet_col_wrap = 3
                        norm_h = std_h * (int(facet_num / facet_col_wrap) + (facet_num % facet_col_wrap > 0))
                        norm_w = (std_w - 200) * facet_col_wrap
                        facet_row_spacing = 0.05
                        facet_col_spacing = 0.05
                    crop_data = st.sidebar.multiselect("Crops:", options=crop_list, default = crop_list)
                    crop_filter = (df["Crop"].isin(crop_data)) | (df["Crop"].isnull())
                    f_df = df[crop_filter].copy()
                    grouping_var = [x_data, "Layer", "Position", "Experiment_ID", "Start_date", color_var, facet_var]
                    grouping_var = list(filter(lambda a: a != "None", grouping_var))
                    grouping_var = list(set(grouping_var))
                    if y_data == "FW_g":
                        df_box = f_df[(f_df[y_data].notnull())].groupby(grouping_var, as_index=False)[y_data].sum()
                    elif y_data == "Germination_rate":
                        df_box = f_df[(f_df[y_data].notnull())].groupby(grouping_var, as_index=False)[y_data].last()
                    else:
                        df_box = f_df.copy()
                    if color_var == "None" and facet_var == "None":
                        ordered_df_box = df_box.sort_values(
                            by = x_data,
                            ascending = True
                        )
                        box_plot = px.box(
                            ordered_df_box[ordered_df_box[y_data].notnull()],
                            x=x_data,
                            y=y_data,
                            points="all",
                            height=std_h,
                            width=std_w
                        )
                        box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                        st.plotly_chart(box_plot)
                    elif color_var != "None" and facet_var == "None":
                        ordered_df_box = df_box.sort_values(
                            by = color_var,
                            ascending = True
                        )
                        box_plot = px.box(
                            ordered_df_box[ordered_df_box[y_data].notnull()],
                            x=x_data,
                            y=y_data,
                            points="all",
                            color=color_var,
                            height=std_h,
                            width=std_w,
                        )
                        box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                        st.plotly_chart(box_plot)
                    elif color_var == "None" and facet_var != "None":
                        ordered_df_box = df_box.sort_values(
                            by = facet_var,
                            ascending = True
                        )
                        box_plot = px.box(
                            ordered_df_box[ordered_df_box[y_data].notnull()],
                            x=x_data,
                            y=y_data,
                            points="all",
                            facet_col=facet_var,
                            facet_col_wrap=facet_col_wrap,
                            facet_row_spacing=facet_row_spacing,
                            facet_col_spacing=facet_col_spacing,
                            height=norm_h,
                            width=norm_w,
                        )
                        box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                        box_plot.update_xaxes(matches=None, showticklabels=True)
                        st.plotly_chart(box_plot)
                    elif color_var != "None" and facet_var != "None":
                        ordered_df_box = df_box.sort_values(
                            by = [facet_var,color_var],
                            ascending = [True, True]
                        )
                        box_plot = px.box(
                            ordered_df_box[ordered_df_box[y_data].notnull()],
                            x=x_data,
                            y=y_data,
                            points="all",
                            color=color_var,
                            facet_col=facet_var,
                            facet_col_wrap=facet_col_wrap,
                            facet_row_spacing=facet_row_spacing,
                            facet_col_spacing=facet_col_spacing,
                            height=norm_h,
                            width=norm_w,
                        )
                        box_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                        box_plot.update_xaxes(matches=None, showticklabels=True)
                        st.plotly_chart(box_plot)
                # else:
                #     # general plot settings excluding crop filter
                #     x_data = st.sidebar.selectbox("X axis:", options=xdata_list)
                #     y_data = st.sidebar.selectbox("Y axis:", options=ydata_list)
                #     color_var = st.sidebar.selectbox("Colour:", options=color_var_list)
                #     facet_var = st.sidebar.selectbox("Facet:", options=facet_var_list)
                #     if facet_var != "None":
                #         facet_num = df[facet_var].nunique()
                #         if (facet_num % 2) == 0:
                #             facet_col_wrap = 2
                #         else:
                #             facet_col_wrap = 3
                #         norm_h = std_h * (int(facet_num / facet_col_wrap) + (facet_num % facet_col_wrap > 0))
                #         norm_w = (std_w - 200) * facet_col_wrap
                #         facet_row_spacing = 0.05
                #         facet_col_spacing = 0.05

                #     nocr_box_plot = px.box(
                #         df,
                #         x=x_data,
                #         y=y_data,
                #         points="all",
                #         color=color_var,
                #         facet_col=facet_var,
                #         facet_col_wrap=facet_col_wrap,
                #         facet_row_spacing=facet_row_spacing,
                #         facet_col_spacing=facet_col_spacing,
                #         height=norm_h,
                #         width=norm_w,
                #     )
                #     st.plotly_chart(nocr_box_plot)
            except Exception as e:
                st.warning("Error processing the graph :- *Impossible graph settings*")
                st.warning("Please recheck the logic behind the parameters from the navigation")
                print(e)

        elif select_graph == "Scatter":
            try:
                # plot parameters including crop filter
                if "Crop" in df.columns:
                    st.sidebar.subheader("Scatter plot settings")
                    x_data = st.sidebar.selectbox("X axis:", options=df.select_dtypes([np.number]).columns)
                    y_data = st.sidebar.selectbox("Y axis:", options=df.select_dtypes([np.number]).columns)
                    color_var = st.sidebar.selectbox("Colour:", options=color_var_list, index=default_clr)
                    facet_var = st.sidebar.selectbox("Facet:", options=facet_var_list, index=default_fac)
                    if facet_var != "None":
                        facet_num = df[facet_var].nunique()
                        if (facet_num % 2) == 0:
                            facet_col_wrap = 2
                        else:
                            facet_col_wrap = 3
                        norm_h = std_h * (int(facet_num / facet_col_wrap) + (facet_num % facet_col_wrap > 0))
                        norm_w = (std_w - 200) * facet_col_wrap
                        facet_row_spacing = 0.05
                        facet_col_spacing = 0.05
                    crop_data = st.sidebar.multiselect("Crops:", options=crop_list, default = crop_list)
                    crop_filter = (df["Crop"].isin(crop_data)) | (df["Crop"].isnull())
                    f_df = df[crop_filter].copy()
                    df_scatter = f_df.copy()
                    if color_var == "None" and facet_var == "None":
                        ordered_df_scatter = df_scatter.sort_values(
                            by = x_data,
                            ascending = True
                        )
                        scatter_plot = px.scatter(
                            ordered_df_scatter[ordered_df_scatter[y_data].notnull()], 
                            x=x_data, 
                            y=y_data, 
                            height=std_h, 
                            width=std_w,
                            trendline="ols",
                        )
                        scatter_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                        st.plotly_chart(scatter_plot)
                    elif color_var != "None" and facet_var == "None":
                        ordered_df_scatter = df_scatter.sort_values(
                            by = color_var,
                            ascending = True
                        )
                        scatter_plot = px.scatter(
                            ordered_df_scatter[ordered_df_scatter[y_data].notnull()],
                            x=x_data,
                            y=y_data,
                            color=color_var,
                            trendline="ols",
                            height=std_h,
                            width=std_w,
                        )
                        scatter_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                        st.plotly_chart(scatter_plot)
                    elif color_var == "None" and facet_var != "None":
                        ordered_df_scatter = df_scatter.sort_values(
                            by = facet_var,
                            ascending = True
                        )
                        scatter_plot = px.scatter(
                            ordered_df_scatter[ordered_df_scatter[y_data].notnull()],
                            x=x_data,
                            y=y_data,
                            trendline="ols",
                            facet_col=facet_var,
                            facet_col_wrap=facet_col_wrap,
                            facet_row_spacing=facet_row_spacing,
                            facet_col_spacing=facet_col_spacing,
                            height=norm_h,
                            width=norm_w,
                        )
                        scatter_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                        scatter_plot.update_xaxes(matches=None, showticklabels=True)
                        st.plotly_chart(scatter_plot)
                    elif color_var != "None" and facet_var != "None":
                        ordered_df_scatter = df_scatter.sort_values(
                            by = [color_var, facet_var],
                            ascending = True
                        )
                        scatter_plot = px.scatter(
                            ordered_df_scatter[ordered_df_scatter[y_data].notnull()],
                            x=x_data,
                            y=y_data,
                            trendline="ols",
                            color=color_var,
                            facet_col=facet_var,
                            facet_col_wrap=facet_col_wrap,
                            facet_row_spacing=facet_row_spacing,
                            facet_col_spacing=facet_col_spacing,
                            height=norm_h,
                            width=norm_w,
                        )
                        scatter_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                        scatter_plot.update_xaxes(matches=None, showticklabels=True)
                        st.plotly_chart(scatter_plot)
                # else:
                #     # general plot settings excluding crop filter
                #     x_data = st.sidebar.selectbox("X axis:", options=xdata_list)
                #     y_data = st.sidebar.selectbox("Y axis:", options=ydata_list)
                #     color_var = st.sidebar.selectbox("Colour:", options=color_var_list)
                #     facet_var = st.sidebar.selectbox("Facet:", options=facet_var_list)
                #     if facet_var != "None":
                #         facet_num = df[facet_var].nunique()
                #         if (facet_num % 2) == 0:
                #             facet_col_wrap = 2
                #         else:
                #             facet_col_wrap = 3
                #         norm_h = std_h * (int(facet_num / facet_col_wrap) + (facet_num % facet_col_wrap > 0))
                #         norm_w = (std_w - 200) * facet_col_wrap
                #         facet_row_spacing = 0.05
                #         facet_col_spacing = 0.05
                        
                #     nocr_scatter_plot = px.scatter(
                #         df[df[y_data].notnull()],
                #         x=x_data,
                #         y=y_data,
                #         trendline="lowess",
                #         color=color_var,
                #         facet_col=facet_var,
                #         facet_col_wrap=facet_col_wrap,
                #         facet_row_spacing=facet_row_spacing,
                #         facet_col_spacing=facet_col_spacing,
                #         height=norm_h,
                #         width=norm_w,
                #     )
                #     nocr_scatter_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                #     nocr_scatter_plot.update_xaxes(matches=None, showticklabels=True)
                #     st.plotly_chart(nocr_scatter_plot)
            except Exception as e:
                st.warning("Error processing the graph :-*Impossible graph settings*")
                st.warning("Please recheck the logic behind the parameters from the navigation")
                print(e)
        elif select_graph == "line":
            try:
                # plot parameters including crop filter
                if "Crop" in df.columns:
                    st.sidebar.subheader("Line plot settings")
                    x_data = st.sidebar.selectbox("X axis:", options=xdata_list, index=default_x)
                    y_data = st.sidebar.selectbox("Y axis:", options=ydata_list, index=default_y)
                    color_var = st.sidebar.selectbox("Colour:", options=color_var_list, index=default_clr)
                    facet_var = st.sidebar.selectbox("Facet:", options=facet_var_list, index=default_fac)
                    if facet_var != "None":
                        facet_num = df[facet_var].nunique()
                        if (facet_num % 2) == 0:
                            facet_col_wrap = 2
                        else:
                            facet_col_wrap = 3
                        norm_h = std_h * (int(facet_num / facet_col_wrap) + (facet_num % facet_col_wrap > 0))
                        norm_w = (std_w - 200) * facet_col_wrap
                        facet_row_spacing = 0.05
                        facet_col_spacing = 0.05
                    crop_data = st.sidebar.multiselect("Crops:", options=crop_list, default=crop_list)
                    crop_filter = (df["Crop"].isin(crop_data)) | (df["Crop"].isnull())
                    f_df = df[crop_filter].copy()
                    grouping_var = [x_data, color_var, facet_var]
                    grouping_var = list(filter(lambda a: a != "None", grouping_var))
                    grouping_var = list(set(grouping_var))
                    df_line = f_df[(f_df[y_data].notnull())].groupby(grouping_var, as_index=False)[y_data].mean()
                    if color_var == "None" and facet_var == "None":
                        ordered_df_line = df_line.sort_values(
                            by = x_data,
                            ascending = True
                        )
                        line_plot = px.line(ordered_df_line, x=x_data, y=y_data, height=std_h, width=std_w)
                        line_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                        st.plotly_chart(line_plot)
                    elif color_var != "None" and facet_var == "None":
                        ordered_df_line = df_line.sort_values(
                            by = color_var,
                            ascending = True
                        )
                        line_plot = px.line(ordered_df_line, x=x_data, y=y_data, height=std_h, width=std_w, color=color_var)
                        line_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                        st.plotly_chart(line_plot)
                    elif color_var == "None" and facet_var != "None":
                        ordered_df_line = df_line.sort_values(
                            by = facet_var,
                            ascending = True
                        )
                        line_plot = px.line(
                            ordered_df_line,
                            x=x_data,
                            y=y_data,
                            facet_col=facet_var,
                            facet_col_wrap=facet_col_wrap,
                            facet_row_spacing=facet_row_spacing,
                            facet_col_spacing=facet_col_spacing,
                            height=norm_h,
                            width=norm_w,
                        )
                        line_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                        line_plot.update_xaxes(matches=None, showticklabels=True)
                        st.plotly_chart(line_plot)
                    elif color_var != "None" and facet_var != "None":
                        ordered_df_line = df_line.sort_values(
                            by = [color_var, facet_var],
                            ascending = True
                        )
                        line_plot = px.line(
                            ordered_df_line,
                            x=x_data,
                            y=y_data,
                            facet_col=facet_var,
                            facet_col_wrap=facet_col_wrap,
                            facet_row_spacing=facet_row_spacing,
                            facet_col_spacing=facet_col_spacing,
                            height=norm_h,
                            width=norm_w,
                            color=color_var,
                        )
                        line_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                        line_plot.update_xaxes(matches=None, showticklabels=True)
                        st.plotly_chart(line_plot)
                #                    elif x_data == 'DAP' and y_data == 'EC':
                #                        df_line_ec = df_line[(df_line['Average_EC_10_days_after_planting'].notnull())].groupby(
                #                            ['Cube_name', 'DAP', 'Average_EC_10_days_after_planting',
                #                             'Average_EC_10_days_before_harvest'],
                #                            as_index=False)['Average_EC_10_days_after_planting',
                #                                            'Average_EC_10_days_before_harvest'].mean()
                #                        line_plot = px.line(df_line_ec, x='DAP', y=['Average_EC_10_days_after_planting'],
                #                                            color='Cube_name', height=650, width=850)
                #                        line_plot.update_yaxes(rangemode="tozero", matches=None, showticklabels=True)
                #                        line_plot.update_xaxes(matches=None, showticklabels=True)
                #                        st.plotly_chart(line_plot)
                # else:
                #     # general plot settings excluding crop filter
                #     x_data = st.sidebar.selectbox("X axis:", options=xdata_list)
                #     y_data = st.sidebar.selectbox("Y axis:", options=ydata_list)
                #     color_var = st.sidebar.selectbox("Colour:", options=color_var_list)
                #     facet_var = st.sidebar.selectbox("Facet:", options=facet_var_list)
                #     if facet_var != "None":
                #         facet_num = df[facet_var].nunique()
                #         if (facet_num % 2) == 0:
                #             facet_col_wrap = 2
                #         else:
                #             facet_col_wrap = 3
                #         norm_h = std_h * (int(facet_num / facet_col_wrap) + (facet_num % facet_col_wrap > 0))
                #         norm_w = (std_w - 200) * facet_col_wrap
                #         facet_row_spacing = 0.05
                #         facet_col_spacing = 0.05
                #     nocr_line_plot = px.line(
                #         df,
                #         x=x_data,
                #         y=y_data,
                #         color=color_var,
                #         facet_col=facet_var,
                #         facet_col_wrap=facet_col_wrap,
                #         facet_row_spacing=facet_row_spacing,
                #         facet_col_spacing=facet_col_spacing,
                #         height=norm_h,
                #         width=norm_w,
                #     )
                #     st.plotly_chart(nocr_line_plot)
            except Exception as e:
                st.warning("Error processing the graph :- *Impossible graph settings*")
                st.warning("Please recheck the logic behind the parameters from the navigation")
                print(e)
        table_show = st.button("Show data table")
        if table_show:
            st.dataframe(df, width=1200, height=500)
