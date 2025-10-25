import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

from optim_methods import (
    seccion_aurea, fibonacci, busqueda_secuencial,
    busqueda_dicotomica, biseccion, newton_unidimensional
)


st.set_page_config(page_title="Calculadora de Optimización", page_icon="https://www.iue.edu.co/wp-content/uploads/2025/07/cropped-favicon-1-32x32.png",layout="wide")

logo_url = "https://www.iue.edu.co/wp-content/uploads/2022/05/institucion-universitaria-envigado-iue-logo.svg"
st.markdown(f"""
<div style="display: flex; align-items: center; justify-content: center;">
    <img src="{logo_url}" width="200" style="margin-right: 15px;">
    <h1 style="text-align: center;">Calculadora de Optimización</h1>
</div>
""", unsafe_allow_html=True)


with st.container():
    col_left, col_form, col_right = st.columns([1, 2, 1])  
    with col_form:

        metodo = st.selectbox("Método de optimización:", [
            "Selecciona un método...",
            "Sección Áurea", "Fibonacci", "Búsqueda Secuencial",
            "Búsqueda Dicotómica", "Bisección", "Newton"
        ])

        if metodo != "Selecciona un método...":

            col1, col2, col3 = st.columns(3)
            with col1:
                func_str = st.text_input("Función f(x):", "x**2 + 2*x")
            with col2:
                a = st.number_input("Intervalo inferior (a):", value=-3.0)
            with col3:
                b = st.number_input("Intervalo superior (b):", value=5.0)

            if metodo == "Newton":
                col1n, col2n,col3n = st.columns(3)
                with col1n:
                    x0 = st.number_input("Valor inicial (x0):", value=1.0)
                with col2n:
                    tol = st.number_input("Tolerancia:", value=1e-3, format="%.1e")
                with col3n:
                    max_iter = st.number_input("Número máximo de iteraciones", value=500)
            elif metodo in ["Sección Áurea", "Bisección"]:
                tol = st.number_input("Tolerancia:", value=1e-3, format="%.1e")
            elif metodo =="Búsqueda Dicotómica":
                col1d, col2d = st.columns(2)
                with col1d:
                    max_iter = st.number_input("Número máximo de iteraciones", value=500)
                with col2d:
                    tol = st.number_input("Tolerancia:", value=1e-3, format="%.1e")
               
            elif metodo == "Fibonacci":
                n = st.number_input("Número de iteraciones (n):", min_value=3, max_value=100, value=25)
            elif metodo == "Búsqueda Secuencial":
                paso = st.number_input("Paso de búsqueda (Δx):", value=0.5)
            calcular = st.button("Calcular mínimo")
        else:
            calcular = False

if metodo != "Selecciona un método..." and calcular:
    x = sp.Symbol('x')
    try:
        f_expr = sp.sympify(func_str)
        f = sp.lambdify(x, f_expr, "numpy")
        f_prime = sp.lambdify(x, sp.diff(f_expr, x), "numpy")
        f_double_prime = sp.lambdify(x, sp.diff(f_expr, x, 2), "numpy")
    except Exception as e:
        st.error(f"Error al interpretar la función: {e}")
        st.stop()

    try:
        if metodo == "Sección Áurea":
            res, tabla = seccion_aurea(f, a, b, tol)
        elif metodo == "Fibonacci":
            res, tabla = fibonacci(f, a, b, n)
        elif metodo == "Búsqueda Secuencial":
            res, tabla = busqueda_secuencial(f, a, b, paso)
        elif metodo == "Búsqueda Dicotómica":
            res, tabla = busqueda_dicotomica(f, a, b, tol,max_iter)
        elif metodo == "Bisección":
            res, tabla = biseccion(f_prime, a, b, tol)
        elif metodo == "Newton":
            res, tabla = newton_unidimensional(f_prime,f_double_prime, x0, tol,max_iter)
        else:
            st.error("Método no reconocido")
            st.stop()

        st.markdown("---")
        st.markdown("<h2 style='text-align: center;'>Resultados</h2>", unsafe_allow_html=True)

        col1r, col2r = st.columns(2)
        with col1r:
            st.success(f"Mínimo aproximado en **x = {res:.6f}**")
            st.write(f"f(x) = {f(res):.6f}")
            st.markdown("### Iteraciones del proceso")
            st.dataframe(tabla)
        with col2r:
            xs = np.linspace(a, b, 400)
            ys = f(xs)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(xs, ys, color='royalblue', label='f(x)')
            ax.scatter(res, f(res), color='red', s=80, label='Mínimo encontrado')
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.set_title(f"Función y resultado ({metodo})")
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.5)
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Ocurrió un error al calcular: {e}")
