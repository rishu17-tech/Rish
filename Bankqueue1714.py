import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# ---------------- Simulation Function ----------------
def queue_simulation(arrival_rate, service_rate, tellers, simulation_time=60):
    arrivals = np.random.poisson(arrival_rate, simulation_time)
    service_capacity = tellers * service_rate

    queue = 0
    wait_times = []

    for customers in arrivals:
        queue += customers
        
        served = min(queue, service_capacity)
        queue -= served

        if service_capacity > 0:
            wait_times.append(queue / service_capacity)
        else:
            wait_times.append(0)

    avg_wait = np.mean(wait_times)
    return avg_wait, queue


# ---------------- Streamlit UI ----------------
st.title("🏦 Bank Teller Queue Simulation")

st.markdown("Simulate customer waiting time using queuing theory.")

# Inputs
arrival_rate = st.slider("Arrival Rate (customers/min)", 1, 20, 5)
service_rate = st.slider("Service Rate per Teller", 1, 10, 3)
tellers = st.slider("Number of Tellers", 1, 5, 2)
simulation_time = st.slider("Simulation Time (minutes)", 10, 120, 60)


# Run Simulation Button
if st.button("Run Simulation"):

    avg_wait, remaining_queue = queue_simulation(
        arrival_rate, service_rate, tellers, simulation_time
    )

    st.subheader("📊 Results")
    st.write(f"Average Waiting Time: **{round(avg_wait, 3)}**")
    st.write(f"Remaining Queue Length: **{remaining_queue}**")

    # Peak Hour Detection
    utilization = arrival_rate / (tellers * service_rate)

    if utilization > 1:
        st.error("⚠️ Peak Hour Detected! System is overloaded.")
    elif utilization > 0.8:
        st.warning("⚠️ High Load! Approaching peak conditions.")
    else:
        st.success("✅ System is stable.")


    # -------- Graph --------
    st.subheader("📈 Waiting Time vs Arrival Rate")

    arrival_rates = list(range(1, 21))
    avg_waits = []

    for rate in arrival_rates:
        avg_w, _ = queue_simulation(rate, service_rate, tellers, simulation_time)
        avg_waits.append(avg_w)

    fig, ax = plt.subplots()
    ax.plot(arrival_rates, avg_waits)
    ax.set_xlabel("Arrival Rate")
    ax.set_ylabel("Average Waiting Time")
    ax.set_title("Queue Performance")

    st.pyplot(fig)
