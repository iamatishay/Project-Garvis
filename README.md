# 📞 G.A.R.V.I.S - Geospatial Analysis and Reporting for Visualizing Inefficiencies in Signal

📞 G.A.R.V.I.S - Geospatial Analysis and Reporting for Visualizing Inefficiencies in Signal
G.A.R.V.I.S (Geospatial Analysis and Reporting for Visualizing Inefficiencies in Signal) is a sophisticated web application built with Streamlit, designed to empower telecom analysts and regulators by providing a robust platform for visualizing and analyzing telecom signal quality data. This tool is particularly useful for identifying and reporting drop call rates and other signal inefficiencies across various regions, allowing for targeted improvements and data-driven decision-making.

🌟 Key Features:
🗺️ Interactive Map Visualization
Dynamic Mapping: Utilize Folium to generate interactive maps that display drop call rates and signal inefficiencies with detailed markers and heatmaps.
Clustered Markers: View data points as clustered markers to avoid clutter and enhance readability, with color-coded markers based on technology type (2G, 3G, 4G).
Heatmaps: Visualize the density of drop call rates with heatmaps, providing an at-a-glance view of problematic areas.
🔍 Advanced Filtering Options
Quarterly and TSP Filters: Easily filter data by specific quarters and telecom service providers (TSPs) to focus your analysis on relevant time periods and operators.
LSA Code and Technology Filters: Narrow down the data by LSA Code (License Service Area) and technology (2G, 3G, 4G) to customize the map view according to your needs.
Days DCR Slider: Adjust the range of days with drop call rates (DCR) greater than 2% to analyze the severity and frequency of signal issues.
📊 Dynamic Data Representation
Bar Charts: Visualize the distribution of Cell Q(90) values across different predefined ranges, offering insights into the quality of signal strength over time.
Pie Charts: Analyze the distribution of different technologies (2G, 3G, 4G) with color-coded pie charts, making it easy to compare usage and performance across the network.
💾 Downloadable Map
Offline Accessibility: Save and download the generated interactive map as an HTML file, allowing for offline viewing and sharing with stakeholders.
Customized Legend: A built-in legend makes it easy to interpret the map, with color codes corresponding to different technology types.
🔒 Secure User Authentication
Login System: A secure login feature ensures that only authorized users can access the tool, safeguarding sensitive data and analysis.
🛠️ Technologies and Libraries Used:
Streamlit: Provides a seamless and interactive web interface that is both user-friendly and powerful.
Folium: Enables the creation of rich, interactive maps with features like marker clusters, heatmaps, and custom icons.
Plotly Express: Allows for the generation of dynamic and interactive charts, including bar and pie charts, with customizable color schemes and order.
Pandas: Powers the data manipulation and filtering, enabling the transformation of raw telecom data into actionable insights.
PostgreSQL: Serves as the backend database, storing telecom data and supporting complex queries to fetch relevant information for visualization.
Streamlit-Folium: Integrates Folium maps within the Streamlit app, providing a smooth experience for map-based data analysis.
🚀 How to Get Started
Clone the Repository: Clone this repository to your local machine using git clone.
Set Up the Environment: Install the required Python libraries by running pip install -r requirements.txt.
Database Setup: Ensure you have a PostgreSQL database set up with the necessary tables and data. Update the database connection details in the script.
Run the Application: Start the Streamlit application by running streamlit run app.py.
Login: Use the login credentials to access the application and begin analyzing your telecom data.
🎯 Use Cases
Telecom Regulators: Assess the performance of telecom service providers and enforce regulations based on data-driven insights.
Network Operators: Identify areas of signal inefficiency and prioritize infrastructure upgrades to improve customer experience.
Geospatial Analysts: Utilize the map-based interface to explore regional signal quality and uncover patterns or anomalies in the data.
📝 Future Enhancements
Real-Time Data Integration: Incorporate real-time data feeds for up-to-date analysis.
Enhanced Filtering: Add more granular filtering options, such as by city, district, or specific time ranges.
Performance Optimization: Improve the app’s performance for handling larger datasets and more complex queries.

