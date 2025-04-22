
import numpy as np
import matplotlib.pyplot as plt

functions_dict = {
    "sin(x)": (lambda x: np.sin(x)),
    "sin(x^2)": (lambda x: np.sin(np.power(x, 2))),
    "x^2": (lambda x: x**2),
    "x^3": (lambda x: x**3),
    "x^4": (lambda x: x**4),
    "e^x": (lambda x: np.exp(x)),
    "ln(x)": (lambda x: np.log(x)),
    "|x|": (lambda x: np.abs(x)),
    "1 / (1 + x^2)": (lambda x: 1 / (1 + x**2)),
    "cos(x)": (lambda x: np.cos(x)),
    "tan(x)": (lambda x: np.tan(x)),
    "sqrt(x)": (lambda x: np.sqrt(x)),
    "x^3": (lambda x: x**3),
    "sign(x)": (lambda x: np.sign(x)),
    "sin(1/x)": (lambda x: np.sin(1/x)),
}


def get_function_graph(f, x_min, x_max, x_vals=None, interpolant=None, name=None, mse=None):
    x_dense = np.linspace(x_min, x_max, 300)
    y_dense = f(x_dense)

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(x_dense, y_dense, label="Функція", linestyle='--')

    if x_vals is not None and interpolant is not None:
        ax.plot(x_dense, interpolant(x_dense), label="Інтерполяція")
        ax.scatter(x_vals, f(x_vals), color='red', label="Точки")
        ax.set_title(f"{name} (MSE = {mse:.5f})")

    ax.legend()
    ax.grid(True)
    return fig

# Середньоквадратична похибка
def get_mse(interpolant, f, x_min, x_max):
    x_dense = np.linspace(x_min, x_max, 300)
    y_true = f(x_dense)
    y_interp = interpolant(x_dense)
    return np.mean((y_true - y_interp) ** 2)
