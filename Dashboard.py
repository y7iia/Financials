# Custom CSS for visual enhancements
st.markdown("""
    <style>
        .title {
            font-size: 2.5em;
            color: #4CAF50;
            text-align: center;
            margin-bottom: 10px;
        }
        .description {
            font-size: 1.25em;
            color: #666;
            text-align: center;
            margin-bottom: 20px;
        }
        .new-badge {
            background-color: #FFC107;
            color: white;
            padding: 3px 8px;
            border-radius: 5px;
            font-size: 0.75em;
            margin-left: 5px;
        }
        .button {
            width: 100%;
            padding: 15px;
            font-size: 1.1em;
            border-radius: 10px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="title">My Financial Market Apps</div>', unsafe_allow_html=True)
st.markdown('<div class="description">Welcome to the dashboard! Click on any button below to access one of our apps.</div>', unsafe_allow_html=True)

# Button grid
app_links = [
    ("App 1", "https://dummy-link1.com"),
    ("App 2", "https://dummy-link2.com"),
    ("App 3", "https://dummy-link3.com"),
    ("App 4", "https://dummy-link4.com"),
    ("App 5", "https://dummy-link5.com"),
    ("App 6", "https://dummy-link6.com"),
    ("App 7", "https://dummy-link7.com"),
    ("App 8", "https://dummy-link8.com"),
    ("App 9", "https://dummy-link9.com"),
    ("App 10", "https://dummy-link10.com"),
]

# Indicate new apps (example: App 4 and App 9 are new)
new_apps = ["App 4", "App 9"]

# Create a 2x5 grid using Streamlit's columns
columns = st.columns(2)
for i, (app_name, link) in enumerate(app_links):
    col = columns[i % 2]  # Alternate between left and right columns
    with col:
        if app_name in new_apps:
            st.markdown(
                f'<a href="{link}" target="_blank">'
                f'<button class="button">{app_name} <span class="new-badge">NEW</span></button>'
                f'</a>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<a href="{link}" target="_blank">'
                f'<button class="button">{app_name}</button>'
                f'</a>',
                unsafe_allow_html=True,
            )
