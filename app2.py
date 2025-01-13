import streamlit as st
import numpy as np
from scipy.fft import fft, ifft
import plotly.graph_objects as go

# Function to generate signals based on the type
def generate_signal(signal_type, frequency, signal_length):
    t = np.linspace(0, 1, signal_length)
    if signal_type == "Sine":
        return np.sin(2 * np.pi * frequency * t)
    elif signal_type == "Square":
        return np.sign(np.sin(2 * np.pi * frequency * t))
    elif signal_type == "Sawtooth":
        return 2 * (t * frequency - np.floor(t * frequency + 0.5))

# Function to add noise to the signal
def add_noise(signal, noise_level):
    noise = noise_level * np.random.randn(len(signal))
    return signal + noise

# Function to calculate Signal-to-Noise Ratio (SNR)
def calculate_snr(original_signal, noisy_signal, filtered_signal):
    noise_before = original_signal - noisy_signal
    noise_after = original_signal - filtered_signal
    
    # SNR formula
    snr_before = np.mean(original_signal**2) / np.std(noise_before)**2
    snr_after = np.mean(original_signal**2) / np.std(noise_after)**2
    return snr_before, snr_after

# Streamlit UI Setup
st.title("Interactive Noise Reduction using FFT")
st.sidebar.header("Settings")

# Explanation of FFT
st.write("### What is FFT?")
st.write("""
The **Fast Fourier Transform (FFT)** is an algorithm used to compute the Discrete Fourier Transform (DFT) and its inverse. 
FFT transforms a signal from its original time domain into the frequency domain. This allows us to analyze the frequency 
components of the signal, making it possible to filter out unwanted noise or extract specific frequency bands. In this app, 
we use FFT to reduce noise from a signal by filtering out high-frequency components.
""")


# Add user-friendly tooltips for sliders
st.write("### Insights")
st.write("Open arrow on top left to use the sliders to adjust signal properties and FFT filtering threshold.")
st.write("SNR (Signal-to-Noise Ratio) quantifies noise reduction. Higher values indicate less noise.")

# User Inputs
signal_length = st.sidebar.slider("Signal Length", min_value=128, max_value=2048, step=128, value=512, help="Adjust the length of the signal")
noise_level = st.sidebar.slider("Noise Level", min_value=0.1, max_value=1.0, step=0.1, value=0.5, help="Increase to add more noise to the signal")
frequency = st.sidebar.slider("Signal Frequency", min_value=1, max_value=50, step=1, value=10, help="Frequency of the signal (Hz)")
signal_type = st.sidebar.selectbox("Signal Type", ["Sine", "Square", "Sawtooth"], help="Choose the type of signal to generate")

# Signal Generation and Noise Addition
original_signal = generate_signal(signal_type, frequency, signal_length)
noisy_signal = add_noise(original_signal, noise_level)

# FFT of the noisy signal
fft_signal = fft(noisy_signal)
frequencies = np.fft.fftfreq(signal_length, d=1 / signal_length)

# Thresholding and Filtering
threshold = st.sidebar.slider("FFT Threshold (Hz)", min_value=0.01, max_value=0.5, step=0.01, value=0.1, help="Threshold for filtering higher frequencies in the FFT spectrum")
fft_signal_filtered = np.copy(fft_signal)
fft_signal_filtered[np.abs(frequencies) > threshold] = 0
filtered_signal = np.real(ifft(fft_signal_filtered))

# Calculate Signal-to-Noise Ratio (SNR)
snr_before, snr_after = calculate_snr(original_signal, noisy_signal, filtered_signal)

# Display SNR values
st.write(f"**SNR Before Filtering**: {snr_before:.2f}")
st.write(f"**SNR After Filtering**: {snr_after:.2f}")

# Plot the signals
fig = go.Figure()

# Plot Noisy Signal
fig.add_trace(go.Scatter(x=np.linspace(0, 1, signal_length), y=noisy_signal, mode='lines', name='Noisy Signal', line=dict(color='red')))

# Plot Original Signal
fig.add_trace(go.Scatter(x=np.linspace(0, 1, signal_length), y=original_signal, mode='lines', name='Original Signal', line=dict(color='green')))

# Plot Filtered Signal
fig.add_trace(go.Scatter(x=np.linspace(0, 1, signal_length), y=filtered_signal, mode='lines', name='Filtered Signal', line=dict(color='blue')))

# Layout adjustments
fig.update_layout(title="Original, Noisy, and Filtered Signal",
                  xaxis_title="Time (s)",
                  yaxis_title="Amplitude",
                  legend_title="Legend",
                  template="plotly_dark")

# Show the plot
st.plotly_chart(fig, use_container_width=True)

# Display FFT Spectrum
fft_magnitude = np.abs(fft_signal)
fft_magnitude_filtered = np.abs(fft_signal_filtered)

fig_fft = go.Figure()
fig_fft.add_trace(go.Scatter(x=frequencies[:signal_length // 2], y=fft_magnitude[:signal_length // 2],
                             mode='lines', name='Original FFT', line=dict(color='purple')))
fig_fft.add_trace(go.Scatter(x=frequencies[:signal_length // 2], y=fft_magnitude_filtered[:signal_length // 2],
                             mode='lines', name='Filtered FFT', line=dict(color='orange')))

fig_fft.update_layout(title="FFT Spectrum",
                      xaxis_title="Frequency (Hz)",
                      yaxis_title="Magnitude",
                      legend_title="Legend",
                      template="plotly_dark")

st.plotly_chart(fig_fft, use_container_width=True)
