from dataclasses import dataclass

from typing import Any

# =====================================================
# PERFORMANCE VARIABLE
# =====================================================

@dataclass
class PerformanceVariable:

    # =================================================
    # BASIC
    # =================================================

    name: str

    value: Any = None

    unit: str = ""

    description: str = ""

    category: str = ""

    # =================================================
    # COMPARISON
    # =================================================

    percentile: float | None = None

    ranking: float | None = None

    zscore: float | None = None

    baseline: float | None = None

    deviation: float | None = None

    deviation_percent: float | None = None

    # =================================================
    # TREND
    # =================================================

    acute: float | None = None

    chronic: float | None = None

    ewma7: float | None = None

    ewma28: float | None = None

    acwr: float | None = None

    trend: float | None = None

    # =================================================
    # STATUS
    # =================================================

    status: str = ""

    color: str = ""

    icon: str = ""

    confidence: str = ""

    # =================================================
    # TEXT
    # =================================================

    interpretation: str = ""

    recommendation: str = ""

    notes: str = ""

    # =================================================
    # SCORE
    # =================================================

    score: float | None = None

    weight: float = 1.0

    enabled: bool = True

    # =================================================
    # SETTERS
    # =================================================

    def set_value(

        self,

        value

    ):

        self.value = value

    def set_score(

        self,

        score

    ):

        self.score = score

    def set_status(

        self,

        status

    ):

        self.status = status

    def set_color(

        self,

        color

    ):

        self.color = color

    def set_icon(

        self,

        icon

    ):

        self.icon = icon

    def set_confidence(

        self,

        confidence

    ):

        self.confidence = confidence

    # =================================================
    # COMPARISON
    # =================================================

    def set_percentile(

        self,

        value

    ):

        self.percentile = value

    def set_ranking(

        self,

        value

    ):

        self.ranking = value

    def set_zscore(

        self,

        value

    ):

        self.zscore = value

    def set_baseline(

        self,

        value

    ):

        self.baseline = value

    def set_deviation(

        self,

        value

    ):

        self.deviation = value

    def set_deviation_percent(

        self,

        value

    ):

        self.deviation_percent = value

    # =================================================
    # TREND
    # =================================================

    def set_acute(

        self,

        value

    ):

        self.acute = value

    def set_chronic(

        self,

        value

    ):

        self.chronic = value

    def set_ewma7(

        self,

        value

    ):

        self.ewma7 = value

    def set_ewma28(

        self,

        value

    ):

        self.ewma28 = value

    def set_acwr(

        self,

        value

    ):

        self.acwr = value

    def set_trend(

        self,

        value

    ):

        self.trend = value

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

            "value": self.value,

            "unit": self.unit,

            "description": self.description,

            "category": self.category,

            "percentile": self.percentile,

            "ranking": self.ranking,

            "zscore": self.zscore,

            "baseline": self.baseline,

            "deviation": self.deviation,

            "deviation_percent": self.deviation_percent,

            "acute": self.acute,

            "chronic": self.chronic,

            "ewma7": self.ewma7,

            "ewma28": self.ewma28,

            "acwr": self.acwr,

            "trend": self.trend,

            "status": self.status,

            "color": self.color,

            "icon": self.icon,

            "confidence": self.confidence,

            "interpretation": self.interpretation,

            "recommendation": self.recommendation,

            "notes": self.notes,

            "score": self.score,

            "weight": self.weight,

            "enabled": self.enabled

        }
    
    # =================================================
    # HELPERS
    # =================================================

    def is_available(

        self

    ):

        return self.value is not None

    def is_missing(

        self

    ):

        return self.value is None

    def is_enabled(

        self

    ):

        return self.enabled

    def enable(

        self

    ):

        self.enabled = True

    def disable(

        self

    ):

        self.enabled = False

    # =================================================
    # RESET
    # =================================================

    def clear(

        self

    ):

        self.value = None

        self.percentile = None

        self.ranking = None

        self.zscore = None

        self.baseline = None

        self.deviation = None

        self.deviation_percent = None

        self.acute = None

        self.chronic = None

        self.ewma7 = None

        self.ewma28 = None

        self.acwr = None

        self.trend = None

        self.status = ""

        self.color = ""

        self.icon = ""

        self.confidence = ""

        self.interpretation = ""

        self.recommendation = ""

        self.notes = ""

        self.score = None

    # =================================================
    # STRING
    # =================================================

    def __repr__(

        self

    ):

        return (

            f"PerformanceVariable("

            f"name='{self.name}', "

            f"value={self.value})"

        )

    def __str__(

        self

    ):

        return (

            f"{self.name}: "

            f"{self.value}"

        )