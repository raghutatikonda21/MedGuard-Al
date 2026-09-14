from utils.drug_normalizer import MEDICINES

def check_allergies(drugs, allergies):
    alerts = []
    allergy_text = {a.strip().lower() for a in allergies if a.strip()}
    for drug in drugs:
        data = MEDICINES.get(drug, {})
        group = data.get("allergy_group", "").lower()
        if group and (group in allergy_text or any(group in a or a in group for a in allergy_text)):
            alerts.append({
                "type": "Allergy Conflict",
                "severity": "HIGH",
                "title": data["generic_name"],
                "reason": f"The entered allergy information appears to match the drug's demonstration allergy group: {group}.",
                "action": "Do not treat this prototype warning as a prescribing decision; verify the allergy and medication with a qualified professional."
            })
    return alerts
