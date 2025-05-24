#!/bin/bash

# Activate the virtual environment (if used)
if [ -d "venv" ]; then
  source venv/bin/activate
fi

# Launch the Streamlit app
streamlit run hp-vertical-curve-calculator.py
