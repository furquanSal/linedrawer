import streamlit as st
import matplotlib.pyplot as plt
import json

# Streamlit app
st.title("Line Drawing Application")

# Take JSON input from the user
json_input = st.text_area("Paste the JSON response data:", height=300)

# Add a button to trigger the drawing
if st.button("Draw Lines"):
    try:
        # Parse the JSON input
        data = json.loads(json_input)

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(10, 8))

        # Set the background color
        ax.set_facecolor('white')

        # Initialize variables to track min and max coordinates
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')

        # Draw each line and update min/max coordinates
        for line in data["data"]["lines"]:
            color = line["color"]
            startX, startY = line["startX"], line["startY"]
            endX, endY = line["endX"], line["endY"]
            strokeWidth = line["strokeWidth"]
            
            # Update min and max coordinates
            min_x = min(min_x, startX, endX)
            max_x = max(max_x, startX, endX)
            min_y = min(min_y, startY, endY)
            max_y = max(max_y, startY, endY)
            
            # Draw the line
            ax.plot([startX, endX], [startY, endY], color=color, linewidth=strokeWidth)
            
            # Draw labels if they exist
            if "label_coordinates" in line:
                for label in line["label_coordinates"]:
                    label_x, label_y = label["x"], label["y"]
                    ax.text(label_x, label_y, label["label"], fontsize=12, color=color)
                    
                    # Update min and max coordinates for labels
                    min_x = min(min_x, label_x)
                    max_x = max(max_x, label_x)
                    min_y = min(min_y, label_y)
                    max_y = max(max_y, label_y)

        # Add some padding to the plot limits
        padding = 20
        ax.set_xlim(min_x - padding, max_x + padding)
        ax.set_ylim(max_y + padding, min_y - padding)  # Invert y-axis

        # Remove axis
        ax.axis('off')

        # Display the plot in Streamlit
        st.pyplot(fig)

    except json.JSONDecodeError:
        st.error("Invalid JSON input. Please paste a valid JSON response.")
    except KeyError as e:
        st.error(f"Invalid data structure. Missing key: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")