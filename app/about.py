import streamlit as st


def about():
    st.title("DAVIS 2.0")
    st.title("Data visualisation Tool")
    st.markdown("By plants lab")
    st.write("## Features")
    st.write(
        """Davis is an interactive plotting app primarily meant for analysing lab generated datasets.
        The app provides realtime visualisation of data with applied 
        logics of statistics like sum, counts, mean, median, mode and error values to provide better understanding 
        of data generated."""
    )
    st.write("**Experimental data analysis :** This enable realtime " "upload and data analysis using plotly graphs.")
    st.write(
        "**Fetch previous data:** To retro analyse any previous experiment data for a comparative"
        " analysis or download."
    )
    st.write("## Tips: ")
    st.write("1: Its always better to use processed files but the tool also supports non processed files.")
    st.write(
        "2: Make sure the file you use the same template  and it has logical data, if not use the navigation "
        "accordingly."
    )
    st.write(
        "3: To begin using the app, select an appropriate option or "
        "load your google sheet in .csv or .excel format using the file upload option in the sidebar under"
        " experiment data analysis. "
    )
    st.write("\n")

