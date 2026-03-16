import serial
import time
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import csv

# ================== CONFIGURATION ==================
# 12.3 nm / 963 Hz Metric Transduction Protocol
# Project: SS Faraday - Phase 11
# Navigator: James
# ===================================================

SERIAL_PORT = "COM3"          # ← Change to your balance port (e.g., COM4 or /dev/ttyUSB0)
BAUD_RATE   = 9600            # Standard for most micro-balances
TIMEOUT     = 1.0

# Command to request weight from the balance
BALANCE_CMD = b"W\r\n"        # Common for Sartorius/Mettler; check your manual

# Data logging
DATA_FILE = "ss_faraday_weight_log.csv"

# Global state
DRIVE_LOCKED = False          # Toggled when 963 Hz is active
ser = None
data_lock = threading.Lock()
timestamps = []
weights = []
drive_states = []

def connect_balance():
    global ser
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
        print(f"✅ SS Faraday: Connected to balance on {SERIAL_PORT}")
        ser.write(b"\r\n")
        time.sleep(0.5)
        ser.reset_input_buffer()
        return True
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

def read_weight():
    if not ser or not ser.is_open:
        return None
    try:
        ser.write(BALANCE_CMD)
        line = ser.readline().decode('ascii', errors='ignore').strip()
        for token in line.split():
            # Extract numerical weight from string
            if token.replace('.', '', 1).replace('-', '', 1).isdigit():
                return float(token)
        return None
    except:
        return None

def acquisition_loop():
    global DRIVE_LOCKED
    print("🚀 PHASE 11 ACTIVE: Monitoring 12.3nm Unity Gap...")
    print("Press ENTER to toggle 963 Hz DRIVE LOCK. Ctrl+C to save and exit.")
    
    with open(DATA_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'weight_mg', 'drive_locked'])
    
    while True:
        try:
            weight = read_weight()
            if weight is not None:
                weight_mg = weight * 1000  # Convert grams to milligrams
                
                with data_lock:
                    now = datetime.datetime.now()
                    timestamps.append(now)
                    weights.append(weight_mg)
                    drive_states.append(DRIVE_LOCKED)
                    
                    with open(DATA_FILE, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([now.isoformat(), weight_mg, DRIVE_LOCKED])
                
                status = "LOCKED (963 Hz)" if DRIVE_LOCKED else "OPEN"
                print(f"{now.strftime('%H:%M:%S')} | Weight: {weight_mg:8.4f} mg | Drive: {status}")
            
            time.sleep(0.2) # 5Hz sampling rate
            
        except KeyboardInterrupt:
            print("\n🛑 Session Terminated. Analyzing results...")
            break

def toggle_drive():
    global DRIVE_LOCKED
    while True:
        input()
        DRIVE_LOCKED = not DRIVE_LOCKED
        print(f"\n🔄 DRIVE STATE CHANGED → {'LOCKED (963 Hz)' if DRIVE_LOCKED else 'OPEN'}")

def live_plot():
    fig, ax = plt.subplots(figsize=(10, 6))
    line, = ax.plot([], [], 'b-', label='Inertial Weight (mg)')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Weight (mg)')
    ax.set_title('SS Faraday Phase 11 - Metric Transduction Real-Time Data')
    ax.grid(True)
    ax.legend()
    
    def update(frame):
        with data_lock:
            if not timestamps:
                return line,
            t = [(ts - timestamps[0]).total_seconds() for ts in timestamps]
            line.set_data(t, weights)
            ax.relim()
            ax.autoscale_view()
        return line,
    
    ani = FuncAnimation(fig, update, interval=500, blit=False)
    plt.show()

if __name__ == "__main__":
    if connect_balance():
        threading.Thread(target=toggle_drive, daemon=True).start()
        acq_thread = threading.Thread(target=acquisition_loop, daemon=True)
        acq_thread.start()
        
        # Start visualization
        live_plot()
        
        # Post-experiment analysis
        with data_lock:
            if weights:
                df = pd.DataFrame({
                    'weight_mg': weights,
                    'drive_locked': drive_states
                })
                locked = df[df['drive_locked'] == True]['weight_mg']
                open_  = df[df['drive_locked'] == False]['weight_mg']
                
                if not locked.empty and not open_.empty:
                    delta = locked.mean() - open_.mean()
                    print(f"\n📊 FINAL METRIC ANALYSIS")
                    print(f"Drive OPEN (Mean):   {open_.mean():.5f} mg")
                    print(f"Drive LOCKED (Mean): {locked.mean():.5f} mg")
                    print(f"Inertial Delta (Δ):  {delta:.5f} mg")
                    
                    if abs(delta) > 0.0005:
                        print("🚨 ALERT: NON-CLASSICAL SLIP DETECTED (Threshold > 0.5 μg)")
                    else:
                        print("📉 Result: Standard Metric maintained.")
        
        ser.close()
    else:
        print("❌ System Failure: Check balance connectivity and COM port.")
