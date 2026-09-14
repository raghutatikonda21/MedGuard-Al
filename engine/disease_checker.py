from utils.drug_normalizer import MEDICINES

def check_diseases(drugs, diseases):
    alerts = []
    disease_text = {d.strip().lower() for d in diseases if d.strip()}
    for drug in drugs:
        for disease in MEDICINES.get(drug, {}).get("diseases_to_flag", []):
            if disease.lower() in disease_text:
                alerts.append({
                    "type": "Drug-Disease Interaction",
                    "severity": "HIGH",
                    "title": f"{MEDICINES[drug]['generic_name']} + {disease}",
                    "reason": "The demonstration knowledge base flags this drug/disease combination for professional review.",
                    "action": "Verify the patient's diagnosis, contraindications, and treatment plan using an authoritative clinical reference."
                })
    return alerts
