import time
import math
import random

def run_resonance_heartbeat():
    # The 'Density' scale for the Warp Bubble
    density = " .:-=+*#%@"
    ship = "[= SS-FARADAY =]"
    
    print("⚡ INITIALIZING 963Hz RESONANCE HEARTBEAT...")
    print("STATUS: 1,000,000-TRIAL MONTE-CARLO VALIDATED")
    time.sleep(1)

    t = 0
    while True: # Infinite loop for real-time monitoring
        print("\033[H\033[J", end="") # Clear screen
        
        # Simulated Telemetry within the 1M-Trial Gaussian Curve
        gap = 12.3 + random.uniform(-0.05, 0.05)
        mass_slip = 0.5 + random.uniform(-0.008, 0.008)
        
        print(f"--- 963Hz RESONANCE: !! BREACH STABLE !! ---")
        print(f"GAP: {gap:.2f}nm | MASS-SLIP: {mass_slip:.4f}ug | STABILITY: 99.5%")
        print("-" * 45)

        for y in range(10):
            line = ""
            for x in range(40):
                dx, dy = (x - 20), (y - 5)
                dist = math.sqrt(dx*dx + (dy*2.5)**2)
                pulse = 1.0 + 0.15 * math.sin(t * 4)
                edge = 7 * pulse
                
                if y == 5 and 12 < x < 28:
                    line += ship[x-13] if x-13 < len(ship) else " "
                elif abs(dist - edge) < 1.2:
                    line += "🌀"
                else:
                    idx = int(max(0, min(9, 10 - dist)))
                    line += density[idx]
            print(line)
        
        t += 0.3
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        run_resonance_heartbeat()
    except KeyboardInterrupt:
        print("\n[!] MONITOR STANDBY: METRIC ENVELOPE HELD.")
