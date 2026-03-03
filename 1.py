
class Patient:
    def __init__(self, name, age, diagnosis_severity=1, smoker=False, heart_rate=100):
        self.name = name
        self.age = age
        self.heart_rate = heart_rate #number
        self.diagnosis_severity = diagnosis_severity #number from 1 to 5

class Rule:
    def __init__(self, 
                 min_heart_rate=None, 
                 max_heart_rate=None, 
                 min_age=None, 
                 max_age=None, 
                 diagnosis_severity=None, 
                 group_class=None):
        self.min_heart_rate = min_heart_rate
        self.max_heart_rate = max_heart_rate
        self.min_age = min_age
        self.max_age = max_age
        self.diagnosis_severity = diagnosis_severity
        self.group_class = group_class  # classification group label ("Critical", "Moderate", or "Stable")

    def classify(self, patient):
        """Return the rule's label if patient matches, else None."""
        if self.min_heart_rate is not None and patient.heart_rate < self.min_heart_rate:
            return None
        if self.max_heart_rate is not None and patient.heart_rate > self.max_heart_rate:
            return None
        if self.min_age is not None and patient.age < self.min_age:
            return None
        if self.max_age is not None and patient.age > self.max_age:
            return None
        if self.diagnosis_severity is not None and patient.diagnosis_severity != self.diagnosis_severity:
            return None
        return self.group_class

    def __repr__(self):
        return f"Rule(label={self.label})"