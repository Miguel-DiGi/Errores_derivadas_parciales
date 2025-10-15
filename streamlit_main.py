import streamlit as st
from sympy import symbols, sympify, sqrt, diff, re, im

st.title("Calculadora de Error Propagado (Derivadas Parciales)")

st.markdown("""
Esta app calcula el error propagado de una función de varias variables usando la fórmula de derivadas parciales.
""")

str_funcion = st.text_input("Introduce la función (ej. I*R o V/R o sqrt(L) o mc**2):", value="I*R")
str_variables = st.text_input("Introduce las variables separadas por comas (ej. I, R):", value="I, R")

# Validación de variables
try:
    variables = symbols(str_variables)
except Exception as e:
    st.error(f"Error al interpretar las variables: {e}")
    st.stop()
if not isinstance(variables, (list, tuple)):
    variables = [variables]

valores_medidos = {}
incertidumbres = {}

for var in variables:
    col1, col2 = st.columns(2)
    with col1:
        valor = st.number_input(f"Valor medido de {var}", format="%f", key=f"valor_{var}")
    with col2:
        error = st.number_input(f"Error (incertidumbre) de {var}", format="%f", key=f"error_{var}")
    valores_medidos[var] = valor
    incertidumbres[var] = error

if st.button("Calcular error propagado"):
    try:
        funcion = sympify(str_funcion, locals={str(v): v for v in variables})
    except Exception as e:
        st.error(f"Error: La función introducida no es válida. Detalle: {e}")
        st.stop()

    suma_errores_cuadrado_expr = 0
    for var in variables:
        try:
            derivada_parcial = diff(funcion, var)
            error_termino = (derivada_parcial * incertidumbres[var])**2
            suma_errores_cuadrado_expr += error_termino
        except Exception as e:
            st.error(f"Error al calcular la derivada parcial respecto a {var}: {e}")
            st.stop()

    try:
        suma_errores_cuadrado_val = suma_errores_cuadrado_expr.subs(valores_medidos)
    except Exception as e:
        st.error(f"Error al evaluar la suma de errores al sustituir valores: {e}")
        st.stop()

    try:
        if im(suma_errores_cuadrado_val) != 0 or re(suma_errores_cuadrado_val) < 0:
            st.error("El cálculo del error ha producido un número complejo o negativo.\n"
                     "Causa probable: Uno de los valores medidos está fuera del dominio de la función o la función no es válida para estos valores.\n"
                     f"Valor dentro de la raíz cuadrada: {suma_errores_cuadrado_val}")
            st.stop()
    except Exception as e:
        st.error(f"Error al comprobar la validez del resultado: {e}")
        st.stop()

    try:
        error_final_expr = sqrt(suma_errores_cuadrado_expr)
        error_numerico = error_final_expr.subs(valores_medidos)
        valor_funcion = funcion.subs(valores_medidos)
    except Exception as e:
        st.error(f"Error al calcular el resultado final: {e}")
        st.stop()

    st.success("Cálculo realizado correctamente.")
    st.write(f"**Expresión simbólica del error:** {error_final_expr}")
    try:
        st.write(f"**Valor de la función:** {float(valor_funcion):.4f}")
    except Exception:
        st.write(f"**Valor de la función:** {valor_funcion}")
    try:
        st.write(f"**Error propagado (incertidumbre):** {float(error_numerico):.4f}")
    except Exception:
        st.write(f"**Error propagado (incertidumbre):** {error_numerico}")
