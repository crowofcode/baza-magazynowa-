import streamlit as st
from supabase import create_client, Client

# Konfiguracja połączenia z Supabase
# W produkcji użyj st.secrets["SUPABASE_URL"] oraz st.secrets["SUPABASE_KEY"]
url = st.secrets.get("SUPABASE_URL", "https://huiqprgvgpidcmypcxor.supabase.co")
key = st.secrets.get("SUPABASE_KEY", "sb_publishable_5JeNcPsW0Vq7g5CRIKznUw_lh28Jazg")
supabase: Client = create_client(url, key)

st.title("📦 Zarządzanie Magazynem (Supabase)")

# --- BOCZNY PANEL: NAWIGACJA ---
menu = ["Dodaj Produkt/Kategorię", "Usuń Elementy", "Podgląd Bazy"]
choice = st.sidebar.selectbox("Menu", menu)

# Funkcja pomocnicza do pobierania kategorii
def get_categories():
    response = supabase.table("kategorie").select("id, nazwa").execute()
    return response.data

# --- SEKKCJA 1: DODAWANIE ---
if choice == "Dodaj Produkt/Kategorię":
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Nowa Kategoria")
        kat_nazwa = st.text_input("Nazwa kategorii")
        kat_opis = st.text_area("Opis kategorii")
        if st.button("Dodaj Kategorię"):
            data = {"nazwa": kat_nazwa, "opis": kat_opis}
            supabase.table("kategorie").insert(data).execute()
            st.success(f"Dodano kategorię: {kat_nazwa}")
            st.rerun()

    with col2:
        st.subheader("Nowy Produkt")
        kategorie = get_categories()
        kat_options = {k['nazwa']: k['id'] for k in kategorie}
        
        prod_nazwa = st.text_input("Nazwa produktu")
        prod_liczba = st.number_input("Liczba", min_value=0, step=1)
        prod_cena = st.number_input("Cena", min_value=0.0, format="%.2f")
        prod_kat = st.selectbox("Wybierz kategorię", options=list(kat_options.keys()))

        if st.button("Dodaj Produkt"):
            prod_data = {
                "nazwa": prod_nazwa,
                "liczba": prod_liczba,
                "cena": prod_cena,
                "kategoria_id": kat_options[prod_kat]
            }
            supabase.table("produkty").insert(prod_data).execute()
            st.success(f"Dodano produkt: {prod_nazwa}")
            st.rerun()

# --- SEKCJA 2: USUWANIE ---
elif choice == "Usuń Elementy":
    st.subheader("Usuwanie danych")
    
    tab1, tab2 = st.tabs(["Produkty", "Kategorie"])
    
    with tab1:
        produkty = supabase.table("produkty").select("*").execute().data
        for p in produkty:
            col_p1, col_p2 = st.columns([3, 1])
            col_p1.write(f"ID: {p['id']} | **{p['nazwa']}** (Ilość: {p['liczba']})")
            if col_p2.button("Usuń", key=f"del_prod_{p['id']}"):
                supabase.table("produkty").delete().eq("id", p['id']).execute()
                st.warning("Produkt usunięty!")
                st.rerun()

    with tab2:
        st.info("Uwaga: Usunięcie kategorii może się nie udać, jeśli są do niej przypisane produkty (klucz obcy).")
        kategorie = get_categories()
        for k in kategorie:
            col_k1, col_k2 = st.columns([3, 1])
            col_k1.write(f"ID: {k['id']} | **{k['nazwa']}**")
            if col_k2.button("Usuń", key=f"del_kat_{k['id']}"):
                try:
                    supabase.table("kategorie").delete().eq("id", k['id']).execute()
                    st.warning("Kategoria usunięta!")
                    st.rerun()
                except Exception as e:
                    st.error("Nie można usunąć kategorii, która posiada produkty.")

# --- SEKCJA 3: PODGLĄD ---
elif choice == "Podgląd Bazy":
    st.subheader("Tabela: Produkty")
    res_p = supabase.table("produkty").select("*, kategorie(nazwa)").execute()
    st.table(res_p.data)
    
    st.subheader("Tabela: Kategorie")
    res_k = supabase.table("kategorie").select("*").execute()
    st.table(res_k.data)
