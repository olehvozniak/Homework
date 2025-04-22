
import streamlit as st
import numpy as np
from scipy.interpolate import BarycentricInterpolator
import matplotlib.pyplot as plt

from utils import functions_dict, get_function_graph, get_mse

st.set_page_config(page_title="Змагання", layout="wide")

pair_index = st.session_state.get("pair_index", 0)

if pair_index >= len(st.session_state.get("matches", [])):
    st.info("✅ Раунд завершено. Переходимо до наступного.")
    st.switch_page("pages/Учасники.py")
    st.stop()

match = st.session_state.matches[pair_index]

name_a, name_b = match[0], match[1]
name_c = match[2] if len(match) == 3 else None

st.title(f"Раунд {st.session_state.get('round', 1)}")

round_name = st.selectbox("Оберіть функцію", list(functions_dict.keys()))
f = functions_dict[round_name]

st.markdown("### Інтервал інтерполяції")
x_min = st.number_input("Мінімум x", value=float(0), key="x_min")
x_max = st.number_input("Максимум x", value=float(1), key="x_max")

num_points = st.slider("Кількість точок", 3, 10, 5)

st.pyplot(get_function_graph(f, x_min, x_max))

def get_x_input(name, key_prefix):
    x_vals = []
    st.subheader(name)
    for i in range(num_points):
        x = st.number_input(f"{name} - x[{i}]", float(x_min), float(x_max),
                            value=float(x_min + i*(x_max - x_min)/(num_points-1)),
                            key=f"{key_prefix}_x_{i}")
        x_vals.append(x)
    return np.array(x_vals)

cols = st.columns(3 if name_c else 2)
with cols[0]:
    x_a = get_x_input(name_a, "a")
with cols[1]:
    x_b = get_x_input(name_b, "b")
if name_c:
    with cols[2]:
        x_c = get_x_input(name_c, "c")

if st.button("Побудувати поліноми"):
    st.session_state.run_battle = True

    if st.session_state.get("run_battle"):
        y_dense = f(np.linspace(x_min, x_max, 300))

        y_a = f(x_a)
        y_b = f(x_b)

        interp_a = BarycentricInterpolator(x_a, y_a)
        interp_b = BarycentricInterpolator(x_b, y_b)

        mse_list = [
            (name_a, get_mse(interp_a, f, x_min, x_max))
        ]

        col_plot_idx = 0
        cols[col_plot_idx].pyplot(get_function_graph(f, x_min, x_max, x_a, interp_a, name_a, mse_list[-1][1]))
        col_plot_idx += 1

        mse_list.append((name_b, get_mse(interp_b, f, x_min, x_max)))
        cols[col_plot_idx].pyplot(get_function_graph(f, x_min, x_max, x_b, interp_b, name_b, mse_list[-1][1]))
        col_plot_idx += 1

        if name_c:
            y_c = f(x_c)
            interp_c = BarycentricInterpolator(x_c, y_c)
            mse_list.append((name_c, get_mse(interp_c, f, x_min, x_max)))
            cols[col_plot_idx].pyplot(get_function_graph(f, x_min, x_max, x_c, interp_c, name_c, mse_list[-1][1]))

        mse_list.sort(key=lambda tup: tup[1])
        winner, best_mse = mse_list[0]

        st.success(f"🏅 Переможець: {winner}")
        st.session_state.winners.append(winner)

        # Перехід до наступної пари або нового раунду
        st.session_state.pair_index += 1

        if st.session_state.pair_index >= len(st.session_state.matches):
            players = st.session_state.winners.copy()
            st.session_state.winners = []

            if len(players) == 1:
                st.success(f"🏆 Переможець турніру: {players[0]}")
                st.session_state.matches = []
            elif len(players) == 3:
                st.session_state.matches = [(players[0], players[1], players[2])]
            else:
                st.session_state.matches = []
                for i in range(0, len(players), 2):
                    if i+1 < len(players):
                        st.session_state.matches.append((players[i], players[i+1]))
                    else:
                        st.session_state.matches.append((players[i], "Автоматичне проходження"))

            st.session_state.round += 1
            st.session_state.pair_index = 0
            
    st.session_state.run_battle = False
    if st.button("➡️ Продовжити"):
        st.switch_page("pages/Учасники.py")
    
