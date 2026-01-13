import streamlit as st
import pandas as pd
import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def autenticar(email, senha):
    xls = pd.ExcelFile(BASE_DIR / "data" / "aplicativo_sare.xlsx")
    usuarios = xls.parse("gestores")

    usuarios["LOGIN"] = usuarios["LOGIN"].astype(str).str.strip()
    usuarios["SENHA"] = usuarios["SENHA"].astype(str).str.strip()

    senha_hash = hash_senha(senha)

    user = usuarios[
        (usuarios["LOGIN"] == email.strip()) &
        (usuarios["SENHA"] == senha_hash)
    ]

    if user.empty:
        return None

    return {
        "perfil": user.iloc[0]["PERFIL"],
        "escola": user.iloc[0]["ESCOLA"]
    }

def tela_login():
    st.subheader("🔐 Acesso ao Painel SARE")

    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        auth = autenticar(email, senha)
        if auth:
            st.session_state.logado = True
            st.session_state.perfil = auth["perfil"]
            st.session_state.escola = auth["escola"]
            st.rerun()
        else:
            st.error("Credenciais inválidas")
