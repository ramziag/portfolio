from io import StringIO
from time import sleep

import pandas as pd
import streamlit as st

from src import helpers as h
from src.bar_charts import DatawrapperBarChart
from src.create_chart import create_chart
from src.line_charts import DatawrapperLineChart
from src.locator_maps import DatawrapperLocatorMap
from src.table_charts import DatawrapperTableChart

# Try to limit package usage to snowflake conda channel packages here: https://repo.anaconda.com/pkgs/snowflake/

# Global variable declarations
coords_list = []
locations = []
df = None
state = st.session_state
if "form_submitted" not in state:
    state.form_submitted = False
if "result" not in state:
    state.result = None
if "df" not in state:
    state.df = False
print(f"State on page initialization:\n{state}")

# Config controlling published dimensions
PUBLISHED_DIMENSION_CONFIG: dict = {
    "locator-map": {
        "embed-width": 600,
        "chart-height": 450,
        "embed-height": 554,
    },
    "column-chart": {
        "embed-width": 600,
        "chart-height": 450,
        "embed-height": 600,
    },
    "d3-bars": {
        "embed-width": 600,
        "chart-height": 482,
        "embed-height": 554,
    },
    "d3-lines": {
        "embed-width": 600,
        "chart-height": 482,
        "embed-height": 554,
    },
    "tables": {
        "embed-width": 600,
        "chart-height": 482,
        "embed-height": 554,
    },
}

# Begin page
# Title & description
st.title("Create a Datawrapper chart")
st.markdown(
    "###### Please fill out the form below. Fields marked with an asterisk (*) are required."
)

# Begin form
with st.form("datawrapper_form"):
    # Fields handling the type of graphic that will be created
    chart_type = None  # Placeholder variable that will be populated by the user's selection in the item below:
    chart_selection = st.selectbox(
        "What kind of chart would you like?",
        ["Point Map", "Bar Chart", "Column Chart", "Line Chart", "Table Chart"],
        help="### I'm a helpful piece of text! :partying:",
    )

    # Chart metadata (headline, subhead, author, source, source url, zoom for maps [Note: zoom needs to be conditionally rendered in the future])
    st.subheader("Information about chart")
    hed = st.text_input("Headline*", key="hed")
    subhed = st.text_input("Subhead*", key="intro")
    byline = st.text_input("Byline*", key="byline")
    source = st.text_input("Source", key="source")
    source_url = st.text_input("Source URL", key="url")
    zoom_level = st.slider(
        "Zoom",
        min_value=5.0,
        max_value=15.0,
        value=9.0,
        step=0.5,
        help="**This is only used for locator maps.**",
    )

    # Chart data
    st.subheader("Chart data")
    st.caption(
        "Please use comma separated values only, following the format of the templates provided for each chart type."
    )
    # File upload element
    file_upload = st.file_uploader(
        "Upload data", max_upload_size=2, type=".csv", label_visibility="hidden"
    )
    # Text blob in case user doesn't want to upload
    chart_data: str = st.text_area(
        "Chart Data",
        placeholder="Enter your chart data here if you don't want to upload.",
        label_visibility="hidden",
    )

    # Submit button, switches to "Update" after first submission
    button_label = "Update" if state.form_submitted else "Submit"
    submitted = st.form_submit_button(button_label)

### END FORM

### BEGIN BACKEND LOGIC AFTER FORM SUBMISSION
if submitted:
    # Switch toggling form submission state value from False to True
    state.form_submitted = True
    # Control flow - this section controls which datawrapper chart is rendered to the end user
    with st.spinner("Creating...", show_time=True):
        print("Form submitted.")

        # Match case logic to determine type of chart requested
        match chart_selection:
            # Point map logic including automatic geocoding
            case "Point Map":
                print("The user is making a locator map.")
                chart_type = "locator-map"
                if file_upload is not None:
                    df = pd.read_csv(file_upload)
                    print("CSV file uploaded, passed as dataframe object.")
                else:
                    df = pd.read_csv(StringIO(chart_data))
                    print("CSV text entered, passed as dataframe object.")
                # Explode empty indices from dataframe, return in place
                df.dropna(axis=1, how="all", inplace=True)
                # Logic to check if marker coordinates are provided as addresses or coordinates:
                try:
                    if "address" in df.columns:
                        print("User uploaded data with addresses. Now geocoding.")
                        for index, row in df.iterrows():
                            print(f"Processing address: {row['address']}")
                            coords = h.geocode_address(str(row["address"]))
                            print(f"Coordinates: {coords}")
                            print(
                                "Now attempting to add coordinates to designated columns..."
                            )
                            df.loc[index, "x_coord"] = coords[0]
                            df.loc[index, "y_coord"] = coords[1]
                            # print(coords_list)
                            sleep(1)
                    else:
                        pass
                except KeyError as e:
                    print("There was an error trying to process this address.")
                    print(e)
                    st.warning("Incorrectly formatted document.")
                # Append dataframe items to coordinates list {coords_list} for computing map views & to a list of dicts {locations} to populate coordinate points
                try:
                    for index, row in df.iterrows():
                        coords_list.append([row["x_coord"], row["y_coord"]])
                        # print(
                        #     f"{row['x_coord']} passed as X value, {row['y_coord']} passed as Y value for {row['title'],""}. Now adding to 'locations' variable."
                        # )
                        locations.append(
                            {
                                "coords": [row["x_coord"], row["y_coord"]],
                                "title": row.get("title", ""),
                                "tooltip": row.get("tooltip", ""),
                            }
                        )
                        # print(
                        #     f"Title: {row['title']}\nCoords: {row['x_coord']}, {row['y_coord']}\nTooltip: {row['tooltip']}\nadded to locations variable."
                        # )
                except TypeError as e:
                    print("Couldn't add coordinates to list.")
                    print(e)
                # Add locations to a list of dicts
                print("Computing views.")
                computed_views = h.compute_view(coords_list)
                print("Views computed.")
                # Call factory function to create a locator map
                if "chartId" not in state:
                    print("Creating a new chart.")
                    locator_map_base = create_chart(hed, chart_type)
                    state["chartId"] = locator_map_base
                    # Initialize DatawrapperLocatorMap object and populate with data
                    locator_map_meta = DatawrapperLocatorMap(locator_map_base)
                    locator_map_meta.write_metadata(
                        locator_map_meta.mapId,
                        computed_views,
                        byline,
                        PUBLISHED_DIMENSION_CONFIG,
                        hed,
                        source,
                        source_url,
                        subhed,
                        zoom=9,
                    )
                    locator_map_meta.create_points(locator_map_meta.mapId, locations)
                    published_chart = locator_map_meta.publish_map(
                        locator_map_meta.mapId
                    )
                    state.result = published_chart["data"]["metadata"]["publish"][
                        "embed-codes"
                    ]["embed-method-iframe"]
                else:  # Conditional will update an existing chart found in state
                    print("Updating chart.")
                    locator_map_meta = DatawrapperLocatorMap(state["chartId"])
                    locator_map_meta.write_metadata(
                        state["chartId"],
                        computed_views,
                        byline,
                        PUBLISHED_DIMENSION_CONFIG,
                        hed,
                        source,
                        source_url,
                        subhed,
                        zoom_level,
                    )
                    locator_map_meta.create_points(locator_map_meta.mapId, locations)
                    published_chart = locator_map_meta.publish_map(
                        locator_map_meta.mapId
                    )
                    state.result = published_chart["data"]["metadata"]["publish"][
                        "embed-codes"
                    ]["embed-method-iframe"]
            # Bar & Column Graphs
            case "Bar Chart" | "Column Chart":
                if chart_selection == "Bar Chart":
                    chart_type = "d3-bars"
                    print("The user is making a bar chart.")
                else:
                    chart_type = "column-chart"
                    print("The user is making a column chart.")
                if file_upload is not None:
                    df = pd.read_csv(file_upload)
                    print("CSV file uploaded, passed as dataframe object.")
                else:
                    df = pd.read_csv(StringIO(chart_data))
                    print("CSV text entered, passed as dataframe object.")
                df = df.to_csv(index=False)
                print("Trying to create graph.")
                if "chartId" not in state:
                    chart_base = create_chart(hed, chart_type)
                    state["chartId"] = chart_base
                    print("Graph creation successful.")
                    chart_meta = DatawrapperBarChart(chart_base)
                    chart_metadata = chart_meta.write_metadata(
                        chart_meta.graphId,
                        byline,
                        PUBLISHED_DIMENSION_CONFIG[chart_type],
                        hed,
                        source,
                        source_url,
                        subhed,
                    )
                    write_data = chart_meta.write_data(chart_meta.graphId, df)
                    publish_chart = chart_meta.publish_chart(chart_meta.graphId)
                    state.result = publish_chart["data"]["metadata"]["publish"][
                        "embed-codes"
                    ]["embed-method-iframe"]
                else:
                    chart_meta = DatawrapperBarChart(state["chartId"])
                    chart_metadata = chart_meta.write_metadata(
                        chart_meta.graphId,
                        byline,
                        PUBLISHED_DIMENSION_CONFIG[chart_type],
                        hed,
                        source,
                        source_url,
                        subhed,
                    )
                    write_data = chart_meta.write_data(chart_meta.graphId, df)
                    publish_chart = chart_meta.publish_chart(chart_meta.graphId)
                    state.result = publish_chart["data"]["metadata"]["publish"][
                        "embed-codes"
                    ]["embed-method-iframe"]
            # Line chart
            case "Line Chart":
                chart_type = "d3-lines"
                print("The user is making a line chart.")
                if file_upload is not None:
                    df = pd.read_csv(file_upload)
                    print("CSV file uploaded, passed as dataframe object.")
                else:
                    df = pd.read_csv(StringIO(chart_data))
                    print("CSV text entered, passed as dataframe object.")
                df = df.to_csv(index=False)
                print("Trying to create chart.")
                if "chartId" not in state:
                    chart_base = create_chart(hed, chart_type)
                    state["chartId"] = chart_base
                    print("Graph creation successful.")
                    chart_meta = DatawrapperLineChart(chart_base)
                    chart_metadata = chart_meta.write_metadata(
                        chart_meta.graphId,
                        byline,
                        PUBLISHED_DIMENSION_CONFIG[chart_type],
                        hed,
                        source,
                        source_url,
                        subhed,
                    )
                    write_data = chart_meta.write_data(chart_meta.graphId, df)
                    publish_chart = chart_meta.publish_chart(chart_meta.graphId)
                    state.result = publish_chart["data"]["metadata"]["publish"][
                        "embed-codes"
                    ]["embed-method-iframe"]
                else:
                    chart_meta = DatawrapperLineChart(state["chartId"])
                    chart_metadata = chart_meta.write_metadata(
                        chart_meta.graphId,
                        byline,
                        PUBLISHED_DIMENSION_CONFIG[chart_type],
                        hed,
                        source,
                        source_url,
                        subhed,
                    )
                    write_data = chart_meta.write_data(chart_meta.graphId, df)
                    publish_chart = chart_meta.publish_chart(chart_meta.graphId)
                    state.result = publish_chart["data"]["metadata"]["publish"][
                        "embed-codes"
                    ]["embed-method-iframe"]
            # Table chart
            case "Table Chart":
                chart_type = "tables"
                print("The user is making a line chart.")
                if file_upload is not None:
                    df = pd.read_csv(file_upload)
                    print("CSV file uploaded, passed as dataframe object.")
                else:
                    df = pd.read_csv(StringIO(chart_data))
                    print("CSV text entered, passed as dataframe object.")
                df = df.to_csv(index=False)
                print("Trying to create chart.")
                if "chartId" not in state:
                    chart_base = create_chart(hed, chart_type)
                    state["chartId"] = chart_base
                    print("Graph creation successful.")
                    chart_meta = DatawrapperTableChart(chart_base)
                    chart_metadata = chart_meta.write_metadata(
                        chart_meta.graphId,
                        byline,
                        PUBLISHED_DIMENSION_CONFIG[chart_type],
                        hed,
                        source,
                        source_url,
                        subhed,
                    )
                    write_data = chart_meta.write_data(chart_meta.graphId, df)
                    publish_chart = chart_meta.publish_chart(chart_meta.graphId)
                    state.result = publish_chart["data"]["metadata"]["publish"][
                        "embed-codes"
                    ]["embed-method-iframe"]
                else:
                    chart_meta = DatawrapperTableChart(state["chartId"])
                    chart_metadata = chart_meta.write_metadata(
                        chart_meta.graphId,
                        byline,
                        PUBLISHED_DIMENSION_CONFIG[chart_type],
                        hed,
                        source,
                        source_url,
                        subhed,
                    )
                    write_data = chart_meta.write_data(chart_meta.graphId, df)
                    publish_chart = chart_meta.publish_chart(chart_meta.graphId)
                    state.result = publish_chart["data"]["metadata"]["publish"][
                        "embed-codes"
                    ]["embed-method-iframe"]
    st.rerun()
if state.result is not None:
    print("Rendering chart to user.")
    st.code(state.result, language="html")
    render_result = st.iframe(state.result)

st.markdown("**For assistance, please contact the Research Division.**")
