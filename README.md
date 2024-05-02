# Interactive Time Series Model Inspection Tool

InteractiveCharts with counterfactuals

## Overview

This project provides an interactive web-based tool for inspecting time series classification models. It allows users to upload a Keras model and an associated binary dataset of univariate time series. With this tool, you can:

1. **Select Individual Time Series:** Choose specific time series from your dataset.
2. **Real-Time Modification:** Modify the selected time series in real time.
3. **Model Prediction Updates:** Observe how the model's predictions change based on the modified time series.
4. **Display Counterfactuals:** View counterfactual explanations that update dynamically as you interact with the data.

## Associated Paper

The tool is based on the research paper titled "XAI for Time Series Classification: Evaluating the Benefits of Model Inspection for End-Users." The authors of the paper are:

- Brigt Håvardstun
- Cèsar Ferri
- Kristian Flikka
- Jan Arne Telle

## Implementation Details

- **Frontend:** The tool is built using React.
- **Backend:** Python (for model inference and data handling).

## Dataset Requirements

- The dataset should be in CSV format.
- Each row represents a single time series.
- The dataset should not contain any labels; instead, the model's predictions serve as labels for each data instance.

## Usage

1. Clone this repository.
2. Install the necessary dependencies.
3. Upload your Keras model and associated dataset.
4. Interact with the tool to explore model behavior and counterfactuals.
