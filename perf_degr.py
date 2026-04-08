import datetime
import hashlib
import json
import os
from pathlib import Path

import streamlit as st


# -----------------------------
# UI / BRAND
# -----------------------------
GOLD_SN = "#D4AF37"
APP_TITLE = "Supernova Dopamine Detox Diary"
DB_FILE = Path("dopamine_users_db.json")

st.set_page_config(page_title=APP_TITLE, page_icon="🧠", layout="wide")
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background: linear-gradient(180deg, #FFFFFF 0%, #FFFBEF 75%, #F8EFCF 100%);}
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# STORAGE HELPERS
# -----------------------------
def load_db() -> dict:
    if not DB_FILE.exists():
        return {"users": {}}
    try:
        with DB_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if "users" not in data:
                data["users"] = {}
            return data
    except Exception:
        return {"users": {}}


def save_db(db: dict) -> None:
    with DB_FILE.open("w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_user(db: dict, username: str) -> dict | None:
    return db["users"].get(username)


def ensure_user_record(db: dict, username: str, password_hash: str) -> None:
    if username not in db["users"]:
        db["users"][username] = {
            "password_hash": password_hash,
            "privacy_accepted": False,
            "profile": {},
            "events": [],
            "plans": [],
        }


# -----------------------------
# DETOX ENGINE
# -----------------------------
EVENT_WEIGHTS = {
    "Social media scroll": 30,
    "Gaming compulsivo": 28,
    "Binge video/serie": 25,
    "Snack impulsivo": 15,
    "Porno compulsivo": 35,
    "Altro": 20,
}


def estimate_load(event_type: str, minutes: int, intensity: int) -> int:
    base = EVENT_WEIGHTS.get(event_type, 20)
    load = base + (minutes * 0.4) + (intensity * 4)
    return int(min(max(load, 0), 100))


def hobby_actions(hobbies: str, work_style: str) -> list[str]:
    h = hobbies.lower()
    actions = []
    if "corsa" in h or "run" in h:
        actions.append("20 minuti di corsa leggera a ritmo conversazionale.")
    if "palestra" in h or "gym" in h:
        actions.append("Sessione breve: 3 esercizi base con recuperi lunghi e zero telefono.")
    if "lettura" in h or "libri" in h:
        actions.append("25 minuti di lettura cartacea in ambiente silenzioso.")
    if "musica" in h:
        actions.append("15 minuti di ascolto attivo o pratica strumentale senza notifiche.")
    if "cammin" in h:
        actions.append("Camminata mindfulness di 20 minuti, solo respirazione e postura.")

    if not actions:
        actions.append("20 minuti di attività fisica moderata senza schermi.")
        actions.append("15 minuti di journaling su carta: trigger, emozione, risposta.")

    if "ufficio" in work_style.lower() or "computer" in work_style.lower():
        actions.append("Deep work da 45 minuti con telefono in un'altra stanza.")
    else:
        actions.append("Blocco operativo da 45 minuti su priorità reale della giornata.")
    return actions


def build_plan(profile: dict, event: dict) -> dict:
    load = estimate_load(event["event_type"], event["minutes"], event["intensity"])
    actions = hobby_actions(profile.get("hobbies", ""), profile.get("work_style", ""))

    if load < 35:
        phase = "Reset leggero (2-4 ore)"
        timeline = [
            "0-30 min: idratazione + 10 respiri lenti.",
            "30-90 min: task semplice ma utile (micro-obiettivo).",
            "90-240 min: attività fisica breve + routine serale regolare.",
        ]
    elif load < 65:
        phase = "Reset medio (12-24 ore)"
        timeline = [
            "0-2h: no social/notifiche, acqua, luce naturale.",
            "2-8h: lavoro profondo in blocchi 45/10.",
            "8-24h: allenamento o camminata + sonno anticipato.",
        ]
    else:
        phase = "Reset profondo (24-72 ore)"
        timeline = [
            "0-6h: digital blackout selettivo (solo urgenze).",
            "6-24h: routine minima: lavoro essenziale, movimento, pasti puliti.",
            "24-72h: gradualità: reintroduzione schermi in finestre programmate.",
        ]

    return {
        "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "event_summary": f"{event['event_type']} - {event['minutes']} min - intensita {event['intensity']}/10",
        "dopamine_load": load,
        "phase": phase,
        "timeline": timeline,
        "actions": actions[:5],
    }


# -----------------------------
# SESSION STATE
# -----------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""


# -----------------------------
# HEADER
# -----------------------------
c_logo, c_title = st.columns([1, 4])
with c_logo:
    try:
        st.image("logo.png", width=120)
    except Exception:
        st.markdown(f"<h2 style='color:{GOLD_SN};'>SUPERNOVA</h2>", unsafe_allow_html=True)
with c_title:
    st.title("🧠 Supernova Dopamine Detox Diary")
    st.caption("Reset dopaminico personalizzato: timeline, compiti e progressione reale.")


# -----------------------------
# LOGIN / SIGNUP
# -----------------------------
db = load_db()

if not st.session_state.authenticated:
    st.subheader("🔐 Accesso Utente")
    st.write("Crea o usa il tuo account. Username e password vengono salvati localmente.")
    with st.form("login_form"):
        username = st.text_input("Username", help="Nome univoco dell'account.")
        password = st.text_input("Password", type="password", help="Minimo 6 caratteri consigliato.")
        privacy_ok = st.checkbox(
            "Accetto la Privacy Policy e il trattamento dati personali.",
            help="Necessario per memorizzare profilo, eventi e piani detox.",
        )
        submit = st.form_submit_button("Entra / Registrati", use_container_width=True)

    if submit:
        username = username.strip()
        if not username or not password:
            st.error("Inserisci username e password.")
            st.stop()
        if not privacy_ok:
            st.error("Devi accettare la privacy per continuare.")
            st.stop()

        pwd_hash = hash_password(password)
        user = get_user(db, username)

        if user is None:
            ensure_user_record(db, username, pwd_hash)
            db["users"][username]["privacy_accepted"] = True
            save_db(db)
            st.success("Account creato con successo.")
        else:
            if user["password_hash"] != pwd_hash:
                st.error("Password non corretta.")
                st.stop()
            db["users"][username]["privacy_accepted"] = True
            save_db(db)
            st.success("Login eseguito.")

        st.session_state.authenticated = True
        st.session_state.username = username
        st.rerun()

    st.stop()


# -----------------------------
# APP CONTENT
# -----------------------------
username = st.session_state.username
user_data = db["users"][username]

with st.sidebar:
    st.markdown(f"**Utente attivo:** `{username}`")
    if st.button("Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()

st.markdown("---")


# One-time profile setup
if not user_data.get("profile"):
    st.subheader("👤 Setup Profilo (una volta sola)")
    st.info("Completa il profilo: il software lo ricorderà automaticamente ai prossimi login.")
    with st.form("profile_form"):
        full_name = st.text_input("Nome e Cognome")
        age = st.number_input("Età", min_value=12, max_value=99, value=30)
        work_style = st.text_input("Lavoro / Studio", placeholder="Es: ufficio 8h al computer")
        hobbies = st.text_area("Hobby / Interessi", placeholder="Es: corsa, musica, lettura")
        sleep_hours = st.number_input("Ore medie di sonno", min_value=3.0, max_value=12.0, value=7.0, step=0.5)
        submit_profile = st.form_submit_button("Salva Profilo", use_container_width=True)

    if submit_profile:
        if not full_name.strip() or not work_style.strip():
            st.error("Compila almeno nome e lavoro/studio.")
        else:
            user_data["profile"] = {
                "full_name": full_name.strip(),
                "age": int(age),
                "work_style": work_style.strip(),
                "hobbies": hobbies.strip(),
                "sleep_hours": float(sleep_hours),
                "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
            }
            save_db(db)
            st.success("Profilo salvato. Da ora verra caricato automaticamente.")
            st.rerun()
    st.stop()


profile = user_data["profile"]

c1, c2 = st.columns([2, 1])
with c1:
    st.subheader(f"Benvenuto, {profile.get('full_name', username)}")
    st.caption(f"Stile di vita: {profile.get('work_style', '-')}. Hobby: {profile.get('hobbies', '-')}.")
with c2:
    st.metric("Ore sonno medie", f"{profile.get('sleep_hours', 0):.1f} h")

st.markdown("---")
st.subheader("⚠️ Nuovo Evento Dopamina")

with st.form("event_form"):
    event_type = st.selectbox(
        "Tipo evento",
        list(EVENT_WEIGHTS.keys()),
        help="Evento che ha creato sovrastimolazione dopaminica.",
    )
    minutes = st.slider(
        "Durata evento (minuti)",
        min_value=5,
        max_value=300,
        value=60,
        step=5,
        help="Tempo continuo speso nell'evento.",
    )
    intensity = st.slider(
        "Intensità percepita (1-10)",
        min_value=1,
        max_value=10,
        value=6,
        help="Quanto il trigger ti ha agganciato mentalmente.",
    )
    note = st.text_area("Nota contestuale (opzionale)", placeholder="Es: stanchezza post lavoro, no allenamento.")
    submit_event = st.form_submit_button("Genera Piano Detox", use_container_width=True)

if submit_event:
    event_data = {
        "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "event_type": event_type,
        "minutes": int(minutes),
        "intensity": int(intensity),
        "note": note.strip(),
    }
    plan = build_plan(profile, event_data)
    user_data["events"].append(event_data)
    user_data["plans"].append(plan)
    save_db(db)
    st.success("Piano detox generato e salvato.")


if user_data["plans"]:
    last_plan = user_data["plans"][-1]
    st.markdown("---")
    st.subheader("🧭 Piano Detox Personalizzato")
    m1, m2, m3 = st.columns(3)
    m1.metric("Carico dopaminico", f"{last_plan['dopamine_load']}/100")
    m2.metric("Fase consigliata", last_plan["phase"])
    m3.metric("Piani salvati", str(len(user_data["plans"])))

    st.markdown("**Timeline operativa**")
    for t in last_plan["timeline"]:
        st.write(f"- {t}")

    st.markdown("**Compiti allineati al tuo stile di vita**")
    for a in last_plan["actions"]:
        st.write(f"- {a}")

    st.caption("Nota: questo strumento non sostituisce un percorso medico o psicoterapeutico.")


with st.expander("Storico eventi recenti"):
    if not user_data["events"]:
        st.write("Nessun evento registrato.")
    else:
        recent = user_data["events"][-10:][::-1]
        st.dataframe(recent, use_container_width=True)
