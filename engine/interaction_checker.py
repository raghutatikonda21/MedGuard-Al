from utils.drug_normalizer import MEDICINES

def check_drug_interactions(drugs):
    alerts = []
    normalized = list(dict.fromkeys(drugs))
    for i, drug_a in enumerate(normalized):
        for drug_b in normalized[i + 1:]:
            if drug_b in MEDICINES.get(drug_a, {}).get("interacts_with", []):
                alerts.append({
                    "type": "Drug-Drug Interaction",
                    "severity": "HIGH",
                    "title": f"{MEDICINES[drug_a]['generic_name']} + {MEDICINES[drug_b]['generic_name']}",
                    "reason": "The demonstration knowledge base flags this medication combination for professional review.",
                    "action": "Review the combination using an authoritative drug-interaction reference."
                })
    return alerts
