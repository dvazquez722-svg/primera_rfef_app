from dataclasses import dataclass, field

from typing import Any

from typing import Dict

from typing import List

from services.performance_variable import (
    PerformanceVariable
)


# =====================================================
# PERFORMANCE DIMENSION
# =====================================================

@dataclass
class PerformanceDimension:

    # =================================================
    # BASIC INFORMATION
    # =================================================

    name: str

    description: str = ""

    score: float | None = None

    confidence: str = ""

    status: str = ""

    color: str = ""

    icon: str = ""

    priority: int = 0

    # =================================================
    # CONTENT
    # =================================================

    variables: List[PerformanceVariable] = field(

        default_factory=list

    )

    evidence: Dict[str, Any] = field(

        default_factory=dict

    )

    comparisons: Dict[str, Any] = field(

        default_factory=dict

    )

    alerts: List[str] = field(

        default_factory=list

    )

    charts: List[Any] = field(

        default_factory=list

    )

    # =================================================
    # TEXT
    # =================================================

    interpretation: str = ""

    recommendation: str = ""

    summary: str = ""

    notes: str = ""

    # =================================================
    # SCORE
    # =================================================

    def set_score(

        self,

        score

    ):

        self.score = score

    # =================================================
    # CONFIDENCE
    # =================================================

    def set_confidence(

        self,

        confidence

    ):

        self.confidence = confidence

    # =================================================
    # STATUS
    # =================================================

    def set_status(

        self,

        status

    ):

        self.status = status

    # =================================================
    # COLOR
    # =================================================

    def set_color(

        self,

        color

    ):

        self.color = color

    # =================================================
    # ICON
    # =================================================

    def set_icon(

        self,

        icon

    ):

        self.icon = icon

    # =================================================
    # PRIORITY
    # =================================================

    def set_priority(

        self,

        priority

    ):

        self.priority = priority

    # =================================================
    # VARIABLE
    # =================================================

    def add_variable(

        self,

        variable

    ):

        self.variables.append(

            variable

        )

    # =================================================
    # VARIABLES
    # =================================================

    def get_variable(

        self,

        name

    ):

        for variable in self.variables:

            if variable.name == name:

                return variable

        return None

    # =================================================
    # EVIDENCE
    # =================================================

    def add_evidence(

        self,

        name,

        value

    ):

        self.evidence[name] = value

    def get_evidence(

        self,

        name

    ):

        return self.evidence.get(

            name

        )

    # =================================================
    # COMPARISONS
    # =================================================

    def add_comparison(

        self,

        name,

        value

    ):

        self.comparisons[name] = value

    def get_comparison(

        self,

        name

    ):

        return self.comparisons.get(

            name

        )

    # =================================================
    # ALERTS
    # =================================================

    def add_alert(

        self,

        alert

    ):

        self.alerts.append(

            alert

        )

    def clear_alerts(

        self

    ):

        self.alerts = []

    # =================================================
    # CHARTS
    # =================================================

    def add_chart(

        self,

        chart

    ):

        self.charts.append(

            chart

        )

    # =================================================
    # TEXT
    # =================================================

    def set_interpretation(

        self,

        text

    ):

        self.interpretation = text

    def set_recommendation(

        self,

        text

    ):

        self.recommendation = text

    def set_summary(

        self,

        text

    ):

        self.summary = text

    def set_notes(

        self,

        text

    ):

        self.notes = text

    # =================================================
    # EXPORT
    # =================================================

    def to_dict(

        self

    ):

        return {

            "name": self.name,

            "description": self.description,

            "score": self.score,

            "confidence": self.confidence,

            "status": self.status,

            "color": self.color,

            "icon": self.icon,

            "priority": self.priority,

            "variables": [

                variable.to_dict()

                for variable in self.variables

            ],

            "evidence": self.evidence,

            "comparisons": self.comparisons,

            "alerts": self.alerts,

            "charts": self.charts,

            "interpretation": self.interpretation,

            "recommendation": self.recommendation,

            "summary": self.summary,

            "notes": self.notes

        }

    # =================================================
    # RESET
    # =================================================

    def clear(

        self

    ):

        self.variables.clear()

        self.evidence.clear()

        self.comparisons.clear()

        self.alerts.clear()

        self.charts.clear()

        self.interpretation = ""

        self.recommendation = ""

        self.summary = ""

        self.notes = ""

        self.score = None

        self.confidence = ""

        self.status = ""

    # =================================================
    # INFORMATION
    # =================================================

    def has_alerts(

        self

    ):

        return len(

            self.alerts

        ) > 0

    def variable_count(

        self

    ):

        return len(

            self.variables

        )

    def evidence_count(

        self

    ):

        return len(

            self.evidence

        )

    def comparison_count(

        self

    ):

        return len(

            self.comparisons

        )

    # =================================================
    # STRING
    # =================================================

    def __repr__(

        self

    ):

        return (

            f"PerformanceDimension("

            f"name='{self.name}', "

            f"score={self.score}, "

            f"confidence='{self.confidence}')"

        )

    def __str__(

        self

    ):

        return (

            f"{self.name} "

            f"({self.score})"

        )