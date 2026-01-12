import streamlit as st
from supabase import create_client, Client

# 1. Konfiguracja połączenia z Supabase
# W praktyce najlepiej użyć st.secrets, ale tutaj podajemy miejsca na dane:
SUPABASE_URL = "TWOJ_URL_SUPABASE"
SUPABASE_KEY = "TWOJ_KLUCZ_API"

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = init_connection()

st.title("📦 Menadżer Magazynu (Supabase)")

# --- SEKCHJA 1: TWORZENIE (CREATE) ---
st.header("Dodaj nowe dane")
tab1, tab2 = st.tabs(["Nowa Kategoria", "Nowy Produkt"])

with tab1:
    with st.form("form_kat"):
        nowa_kat = st.text_input("Nazwa kategorii")
        if st.form_submit_button("Dodaj kategorię"):
            if nowa_kat:
                supabase.table("kategorie").insert({"nazwa": nowa_kat}).execute()
                st.success(f"Dodano kategorię: {nowa_kat}")
                st.rerun()

with tab2:
    # Pobieramy aktualne kategorie do listy wyboru
    kat_data = supabase.table("kategorie").select("*").execute()
    lista_kat = {k['nazwa']: k['id'] for k in kat_data.data}
    
    with st.form("form_prod"):
        nazwa_prod = st.text_input("Nazwa produktu")
        cena_prod = st.number_input("Cena", min_value=0.0, step=0.01)
        wybrana_kat = st.selectbox("Wybierz kategorię", options=list(lista_kat.keys()))
        
        if st.form_submit_button("Dodaj produkt"):
            if nazwa_prod:
                supabase.table("produkty").insert({
                    "nazwa": nazwa_prod, 
                    "cena": cena_prod, 
                    "kategoria_id": lista_kat[wybrana_kat]
                }).execute()
                st.success(f"Dodano produkt: {nazwa_prod}")
                st.rerun()

---

# --- SEKCJA 2: WYŚWIETLANIE I USUWANIE (READ & DELETE) ---
st.header("Zarządzaj bazą")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Kategorie")
    for k in kat_data.data:
        c1, c2 = st.columns([3, 1])
        c1.write(k['nazwa'])
        if c2.button("Usuń", key=f"del_kat_{k['id']}"):
            supabase.table("kategorie").delete().eq("id", k['id']).execute()
            st.rerun()

with col2:
    st.subheader("Produkty")
    prod_data = supabase.table("produkty").select("*, kategorie(nazwa)").execute()
    for p in prod_data.data:
        c1, c2 = st.columns([3, 1])
        kat_name = p['kategorie']['nazwa'] if p['kategorie'] else "Brak"
        c1.write(f"**{p['nazwa']}** ({p['cena']} zł) \n Kat: {kat_name}")
        if c2.button("Usuń", key=f"del_prod_{p['id']}"):
            supabase.table("produkty").delete().eq("id", p['id']).execute()
            st.rerun()
