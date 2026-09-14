import streamlit as st
from utils.drug_normalizer import normalize_drug, MEDICINES
from engine.interaction_checker import check_drug_interactions
from engine.allergy_checker import check_allergies
from engine.disease_checker import check_diseases
from engine.dosage_checker import check_dosages
from engine.risk_engine import calculate_score

st.set_page_config(page_title="MedGuard AI", page_icon="🛡️", layout="wide")

st.title("🛡️ MedGuard AI")
st.subheader("Explainable Medication Safety & Prescription Risk Detection")

st.info(
    "Prototype / hackathon decision-support system. It is not a substitute for "
    "a qualified healthcare professional or an authoritative clinical reference."
)

with st.sidebar:
    st.header("Patient Information")
    patient_name = st.text_input("Patient name", "Demo Patient")
    age = st.number_input("Age", min_value=0, max_value=120, value=35)
    allergies_raw = st.text_area("Allergies (comma separated)", "penicillin")
    diseases_raw = st.text_area("Diagnoses (comma separated)", "none")

st.header("Current / New Medications")
st.caption("Enter one medicine per line: medicine, dose in mg, times per day")

default = "warfarin, 5, 1\nibuprofen, 400, 2"
med_text = st.text_area("Medication list", default, height=140)

if st.button("🔍 ANALYZE MEDICATION SAFETY", type="primary"):
    medications = []
    unknown = []

    for line in med_text.splitlines():
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        name = parts[0]
        canonical = normalize_drug(name)
        if not canonical:
            unknown.append(name)
            continue

        dose = None
        frequency = 1
        if len(parts) > 1:
            try:
                dose = float(parts[1])
            except ValueError:
                dose = None
        if len(parts) > 2:
            try:
                frequency = int(parts[2])
            except ValueError:
                frequency = 1

        medications.append({
            "drug": canonical,
            "dose": dose,
            "frequency": frequency
        })

    if unknown:
        st.warning("Unknown medicines were skipped: " + ", ".join(unknown))

    drugs = [m["drug"] for m in medications]
    allergies = [x.strip() for x in allergies_raw.split(",") if x.strip()]
    diseases = [x.strip() for x in diseases_raw.split(",") if x.strip() and x.strip().lower() != "none"]

    alerts = []
    alerts += check_drug_interactions(drugs)
    alerts += check_allergies(drugs, allergies)
    alerts += check_diseases(drugs, diseases)
    alerts += check_dosages(medications)

    # Duplicate active medication check using canonical names.
    if len(drugs) != len(set(drugs)):
        alerts.append({
            "type": "Duplicate Medication",
            "severity": "MEDIUM",
            "title": "Duplicate medication detected",
            "reason": "The same normalized medicine appears more than once in the entered list.",
            "action": "Review the prescription for duplicate therapy before administration."
        })

    score, level = calculate_score(alerts)

    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Safety Score", f"{score}/100")
    c2.metric("Risk Level", level)
    c3.metric("Warnings", len(alerts))

    st.header("Safety Report")

    if not alerts:
        st.success("No issues were detected by the current demonstration knowledge base.")
    else:
        for a in alerts:
            if a["severity"] == "HIGH":
                st.error(f"🔴 {a['type']} — {a['title']}")
            elif a["severity"] == "MEDIUM":
                st.warning(f"🟠 {a['type']} — {a['title']}")
            else:
                st.info(f"🟡 {a['type']} — {a['title']}")

            with st.expander("Why was this flagged?"):
                st.write(a["reason"])
                st.write("**Recommended review:**", a["action"])

    with st.expander("Normalized medication data"):
        st.json(medications)

    with st.expander("Prototype knowledge-base note"):
        st.write(
            "The bundled medicine data is intentionally small and is for software "
            "demonstration only. Before any real clinical use, replace it with "
            "validated, current, authoritative medication data and clinical rules."
        )
