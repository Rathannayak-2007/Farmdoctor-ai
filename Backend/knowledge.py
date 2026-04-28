"""
Knowledge Base Module for FarmDoctor AI
Loads and provides access to disease information, pesticide recommendations, and prevention tips.
"""

import json
import os
from typing import Optional


# Path to disease info JSON
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "pesticide_db.json")
OLD_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "disease_info.json")

# Path to class names JSON
CLASSES_PATH = os.path.join(os.path.dirname(__file__), "data", "class_names.json")

def load_class_names() -> list:
    """Load class names from JSON and return as a sorted list by index."""
    try:
        with open(CLASSES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            # data is a dict like {"0": "Name", "1": "Name"}
            # Return names sorted by their integer keys
            return [data[str(i)] for i in range(len(data))]
    except Exception as e:
        print(f"Error loading class names: {e}")
        return []

CLASS_NAMES = load_class_names()


class KnowledgeBase:
    """Manages disease information and recommendations."""

    def __init__(self):
        self._data = self._load_data()

    def _load_data(self) -> dict:
        """Load disease data from JSON file."""
        try:
            if os.path.exists(DATA_PATH):
                with open(DATA_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            elif os.path.exists(OLD_DATA_PATH):
                with open(OLD_DATA_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading disease info: {e}")
            return {}

    def get_disease_info(self, class_name: str) -> Optional[dict]:
        """
        Retrieve disease information for a given class name.
        Handles both the new pesticide_db schema and the old disease_info schema.
        """
        if class_name in self._data:
            raw_info = self._data[class_name]
            
            # If it's the new schema (pesticide_db.json)
            if "cultural_control" in raw_info:
                pesticide_list = []
                for p in raw_info.get("pesticides", []):
                    if isinstance(p, dict):
                        pesticide_list.append(f"{p['name']} ({p['dosage']})")
                    else:
                        pesticide_list.append(str(p))

                # Extract symptoms from severity_guide if available
                symptoms = list(raw_info.get("severity_guide", {}).values()) if raw_info.get("severity_guide") else ["Check for typical symptoms of " + class_name]

                return {
                    "display_name": class_name.replace("__", " – ").replace("_", " "),
                    "description": raw_info.get("cause", "Plant disease detected."),
                    "symptoms": symptoms,
                    "pesticides": pesticide_list,
                    "prevention": raw_info.get("cultural_control", []),
                    "severity": "Moderate" if "Healthy" not in class_name else "None",
                }
            
            return raw_info

        # Fallback for unknown classes
        is_healthy = "healthy" in class_name.lower()
        parts = class_name.split("__")
        crop = parts[0].replace("_", " ") if parts else "Unknown crop"
        disease = parts[1].replace("_", " ") if len(parts) > 1 else "Unknown condition"

        if is_healthy:
            return {
                "display_name": f"Healthy {crop}",
                "description": f"The {crop} plant appears healthy with no signs of disease.",
                "symptoms": ["No symptoms detected"],
                "pesticides": ["No treatment required"],
                "prevention": [
                    "Monitor regularly for pests and disease",
                    "Maintain proper nutrition and irrigation",
                    "Practice crop rotation",
                ],
                "severity": "None",
            }
        else:
            return {
                "display_name": f"{crop} – {disease}",
                "description": f"Disease detected: {disease} in {crop}.",
                "symptoms": ["Please consult an agricultural expert for detailed symptoms."],
                "pesticides": ["Consult a local agro-dealer for pesticide recommendations."],
                "prevention": [
                    "Practice crop rotation",
                    "Use certified seeds",
                    "Maintain field hygiene",
                ],
                "severity": "Unknown",
            }

    def get_all_disease_names(self) -> list:
        """Return all disease names in the knowledge base."""
        return list(self._data.keys())

    def get_severity_color(self, severity: str) -> str:
        """Return a color code for the severity level."""
        severity_colors = {
            "None": "#28a745",
            "Low": "#90EE90",
            "Moderate": "#FFA500",
            "High": "#FF4500",
            "Very High": "#DC143C",
            "Unknown": "#808080",
        }
        return severity_colors.get(severity, "#808080")


# Singleton instance
knowledge_base = KnowledgeBase()