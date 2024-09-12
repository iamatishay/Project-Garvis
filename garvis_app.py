import streamlit as st
import pandas as pd
import os
import folium
from folium.plugins import MarkerCluster, HeatMap
import tempfile
import psycopg2
from sqlalchemy import create_engine
from streamlit_folium import folium_static
import plotly.express as px
from login_page import login

def categorize_cell_q_90(df):
    bins = [2, 4, 10, 20, 50, float('inf')]
    labels = ['Above 2 to 4', 'Above 4 to 10', 'Above 10 to 20', 'Above 20 to 50', 'Above 50']
    df['Cell_Q_90_Range'] = pd.cut(df['Cell_Q_90'], bins=bins, labels=labels, right=False)
    return df

if 'logged_in' in st.session_state and st.session_state['logged_in']:
    
    st.set_page_config(
        page_title="G.A.R.V.I.S",
        page_icon="📞",
        layout="wide"
    )

    title_container = st.container()

    with title_container:
        col1, col2, col3 = st.columns([1, 7, 1])
        with col1:
            st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRAi94_JCgttBmlH-VwW3tc7ma68MOLn2Wy0A&s", width=140)  

        with col2:
            st.markdown(
                '<h1 style="color: darkblue;">G.A.R.V.I.S</h1>',
                unsafe_allow_html=True
            )
            st.markdown(
                '<h3 style="color: grey;">Geospatial Analysis and Reporting for Visualizing Inefficiencies in Signal</h3>',
                unsafe_allow_html=True
            )

        with col3:
            if st.button("Logout"):
                st.session_state['logged_in'] = False
                st.success("Logged out successfully!")
                st.rerun()

    favicon = "https://upload.wikimedia.org/wikipedia/en/thumb/5/5c/TRAI.svg/800px-TRAI.svg.png"
    st.markdown(f'<link rel="shortcut icon" href="{favicon}">', unsafe_allow_html=True)

    background_image = "https://upload.wikimedia.org/wikipedia/en/thumb/5/5c/TRAI.svg/800px-TRAI.svg.png"
    st.markdown(
        f"""
        <style>
        .reportview-container {{
            background: url("{background_image}") center center;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    engine = create_engine('postgresql+psycopg2://trai@bccms:B5*m6$p5aS427Ed@bccms.postgres.database.azure.com:5432/dcr')

    conn = None
    
    try:
        conn = engine.connect()
        query = """
        SELECT "CGI", "Latitude", "Longitude", "Cell_Q_90", "LSA Code", "State/ UT", "Quarter", "Technology", "TSP", "Days" 
        FROM public.map_data;
        """
        df = pd.read_sql_query(query, conn)

        df = df.dropna(subset=['Latitude', 'Longitude'])

        df['Quarter'] = df['Quarter'].str.strip()
        df['TSP'] = df['TSP'].str.strip()
        df['LSA Code'] = df['LSA Code'].str.strip()

        quarter_options = sorted(df['Quarter'].drop_duplicates().tolist())
        tsp_options = sorted(df['TSP'].drop_duplicates().tolist())
        tsp_options.insert(0, "All")
        lsa_code_options = sorted(df['LSA Code'].drop_duplicates().tolist())
        technology_options = sorted(df['Technology'].drop_duplicates().tolist())

        quarter_selected = st.selectbox("Select Quarter", [""] + quarter_options, index=0)
        tsp_selected = st.selectbox("Select TSP", ["All"] + tsp_options, index=0)
        lsa_code_selected = st.selectbox("Select LSA Code", [""] + lsa_code_options, index=0)

        st.sidebar.markdown(
                '<div style="text-align: center; font-size: 1.0em; color: #007BFF;">Filter Technology</div>',
                unsafe_allow_html=True
            )


        tech_selected = st.sidebar.multiselect("", technology_options, default=technology_options)

        show_map = quarter_selected or tsp_selected != "All" or lsa_code_selected

        if show_map:
            filtered_df = df[
                (df['Quarter'] == quarter_selected if quarter_selected else True) &
                ((df['TSP'] == tsp_selected) if tsp_selected != "All" else True) &
                (df['LSA Code'] == lsa_code_selected if lsa_code_selected else True) &
                (df['Technology'].isin(tech_selected))
            ]

            st.sidebar.markdown(
                '<div style="text-align: center; font-size: 1.0em; color: #007BFF;">Days Cell Q(90) Value > 2% [Select Range]</div>',
                unsafe_allow_html=True
            )

            days_selected = st.sidebar.slider(
                "",
                min_value=int(df['Days'].min()),
                max_value=int(df['Days'].max()),
                value=(int(df['Days'].min()), int(df['Days'].max()))
            )

            filtered_df = filtered_df[
                (filtered_df['Days'] >= days_selected[0]) &
                (filtered_df['Days'] <= days_selected[1])
            ]

            categorized_df = categorize_cell_q_90(filtered_df)
            cell_q_90_counts = categorized_df['Cell_Q_90_Range'].value_counts().reset_index()
            cell_q_90_counts.columns = ['Range', 'Count']

            st.sidebar.markdown(
                '<div style="text-align: center; font-size: 1.0em; color: #007BFF;">Cell Q(90) Value Range [Select Range]</div>',
                unsafe_allow_html=True
            )

            cell_q_90_selected = st.sidebar.slider(
                "",
                min_value=float(df['Cell_Q_90'].min()),
                max_value=float(df['Cell_Q_90'].max()),
                value=(float(df['Cell_Q_90'].min()), float(df['Cell_Q_90'].max()))
            )

            filtered_df = filtered_df[
                (filtered_df['Cell_Q_90'] >= cell_q_90_selected[0]) &
                (filtered_df['Cell_Q_90'] <= cell_q_90_selected[1])
            ]

            if filtered_df['Latitude'].isna().all() or filtered_df['Longitude'].isna().all():
                st.write("No data available for the selected filters.")
            else:
                category_order = ['Above 2 to 4', 'Above 4 to 10', 'Above 10 to 20', 'Above 20 to 50', 'Above 50']

                fig_bar = px.bar(
                    cell_q_90_counts,
                    x='Range',
                    y='Count',
                    category_orders={'Range': category_order}
                )

                tech_counts = filtered_df['Technology'].value_counts().reset_index()
                tech_counts.columns = ['Technology', 'Count']

                tech_colors = {
                    '2G': 'black',
                    '3G': 'dodgerblue',
                    '4G': 'red'
                }

                fig_pie = px.pie(
                    tech_counts,
                    names='Technology',
                    values='Count',
                    color='Technology',
                    color_discrete_map=tech_colors,
                    category_orders={'Technology': ['2G', '3G', '4G']}
                )

                tsp_counts = filtered_df['TSP'].value_counts().reset_index()
                tsp_counts.columns = ['TSP', 'Count']

                fig_tsp_pie = px.pie(
                    tsp_counts,
                    names='TSP',
                    values='Count',
                    color='TSP'
                )

                with st.sidebar:
                    st.markdown(
                        '<div style="text-align: center; font-size: 1.0em; color: #007BFF;">Technology Distribution Analysis</div>',
                        unsafe_allow_html=True
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                    st.markdown(
                        '<div style="text-align: center; font-size: 1.0em; color: #007BFF;">Service Provider (TSP) Distribution Analysis</div>',
                        unsafe_allow_html=True
                    )
                    st.plotly_chart(fig_tsp_pie, use_container_width=True)
                    st.markdown(
                        '<div style="text-align: center; font-size: 1.0em; color: #007BFF;">Cell Q(90) Distribution Analysis</div>',
                        unsafe_allow_html=True
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)

                map_center = (filtered_df['Latitude'].mean(), filtered_df['Longitude'].mean())
                my_map = folium.Map(location=map_center, zoom_start=7, width='100%', height='100%')

                disable_clustering_at_zoom = 20
                all_markers_cluster = MarkerCluster(name='Markers 📍 ', disableClusteringAtZoom=disable_clustering_at_zoom).add_to(my_map)

                dcr_density = filtered_df[['Latitude', 'Longitude']].groupby(['Latitude', 'Longitude']).size().reset_index(name='count').values.tolist()
                heatmap = HeatMap(dcr_density, radius=15)
                heatmap_fg = folium.FeatureGroup(name='Heat Map 🌡️ ', show=False)
                heatmap_fg.add_child(heatmap)
                my_map.add_child(heatmap_fg)

                technology_colors = {
                    '2G': 'black',
                    '3G': 'dodgerblue',
                    '4G': 'red'
                }

                for index, row in filtered_df.iterrows():
                    tooltip_text = (
                        f"<div style='font-size: 16px;'>"
                        f"<b>CGI:</b> {row['CGI']}<br>"
                        f"<b>Days DCR > 2%:</b> {int(row['Days'])}<br>"
                        f"<b>Latitude:</b> {row['Latitude']}<br>"
                        f"<b>Longitude:</b> {row['Longitude']}<br>"
                        f"<b>LSA Code:</b> {row['LSA Code']}<br>"
                        f"<b>TSP:</b> {row['TSP']}<br>"
                        f"<b>State/ UT:</b> {row['State/ UT']}<br>"
                        f"<b>Cell_Q_90:</b> {row['Cell_Q_90']}<br>"
                        f"<b>Quarter:</b> {row['Quarter']}<br>"
                        f"<b>Technology:</b> {row['Technology']}</div>"
                    )

                    icon_html = (
                        f"<div style='font-size: 15px; color: {technology_colors.get(row['Technology'], 'blue')}'>"
                        f"<i class='fa fa-map-marker fa-1x'></i>"
                        f"</div>"
                    )

                    marker_icon = folium.DivIcon(html=icon_html)

                    folium.Marker(
                        location=[row['Latitude'], row['Longitude']],
                        popup=f"CGI: {row['CGI']}, Cell_Q_90: {row['Cell_Q_90']}",
                        tooltip=tooltip_text,
                        icon=marker_icon
                    ).add_to(all_markers_cluster)

                folium.LayerControl().add_to(my_map)
                legend_html = """
                <div style="
                position: fixed; 
                bottom: 50px; left: 50px; width: 180px; height: 150px; 
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color:white;
                opacity: 0.85;
                ">
                &nbsp;<b>Legend</b> <br>
                &nbsp;<i class="fa fa-map-marker fa-2x" style="color:black"></i>&nbsp; 2G<br>
                &nbsp;<i class="fa fa-map-marker fa-2x" style="color:dodgerblue"></i>&nbsp; 3G<br>
                &nbsp;<i class="fa fa-map-marker fa-2x" style="color:red"></i>&nbsp; 4G<br>
                </div>
                """

                my_map.get_root().html.add_child(folium.Element(legend_html))

                folium_static(my_map, width=1550, height=1000)

                legend_html = """
                <div style="
                position: fixed; 
                bottom: 50px; left: 50px; width: 100px; height: 120px; 
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color:white;
                opacity: 0.85;
                ">
                &nbsp;<b>Legend</b> <br>
                &nbsp;<i class="fa fa-map-marker fa-2x" style="color:black"></i>&nbsp; 2G<br>
                &nbsp;<i class="fa fa-map-marker fa-2x" style="color:dodgerblue"></i>&nbsp; 3G<br>
                &nbsp;<i class="fa fa-map-marker fa-2x" style="color:red"></i>&nbsp; 4G<br>
                </div>
                """

                my_map.get_root().html.add_child(folium.Element(legend_html))

                with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp_file:
                    temp_file_path = temp_file.name
                    my_map.save(temp_file_path)

                st.markdown(
                    "<h3 style='font-size:16px;'>Download map for Offline View</h3>",
                    unsafe_allow_html=True
                )

                with open(temp_file_path, "rb") as file:
                    st.download_button(
                        label="Download Map",
                        data=file,
                        file_name=os.path.basename(temp_file_path),
                        mime="text/html",
                        key='download_map_button'
                    )

        else:
            st.write("No filters selected. Please select options to display the map and analysis.")

    except psycopg2.Error as e:
        st.error(f"Error connecting to database: {e}")
        st.stop()

    finally:
        if conn is not None:
            conn.close()

else:
    login()
