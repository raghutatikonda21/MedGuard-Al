from utils.drug_normalizer import MEDICINES

def check_dosages(medications):
    alerts = []
    for med in medications:
        drug = med["drug"]
        dose = med["dose"]
        frequency = med["frequency"]
        if dose is None:
            continue
        try:
            daily = float(dose) * max(1, int(frequency))
        except (ValueError, TypeError):
            continue
        limit = MEDICINES.get(drug, {}).get("max_demo_daily_mg")
        if limit and daily > limit:
            alerts.append({
                "type": "Dosage Risk",
                "severity": "HIGH",
                "title": f"{MEDICINES[drug]['generic_name']} daily dose entered: {daily:g} mg",
                "reason": f"The prototype knowledge base has a demonstration daily threshold of {limit:g} mg.",
                "action": "Verify the prescribed dose and frequency against an authoritative clinical dosing reference."
            })
    return alerts
