#!/usr/bin/env python3
"""
Complex PTSD (CPTSD) Signature Scorer

Detects linguistic and structural markers of Complex Post-Traumatic Stress
in organic communication patterns. Built as a Rose Glass dimension extension.

Core insight: CPTSD is not a single state but a *texture* that runs through
expression — in narrative fragmentation, shame density, hypervigilance markers,
relational collapse patterns, and window of tolerance signals.

This scorer informs the AI's pace, depth, and safety calibration.
High C scores = slow down, don't push, watch for window of tolerance edges.
Low C scores = more direct engagement is probably safe.

Clinical principle: "Never subtract from psychosis, only add."
This scorer operationalizes that principle across all trauma-adjacent states.

Author: Built on Rose Glass framework by Christopher MacGregor bin Joseph
Extension by: Geode (gstevahn) — mental health companion app R&D
"""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class TraumaResponse(Enum):
    """Primary trauma response patterns detectable in language"""
    FAWN = "fawn"           # Excessive appeasing, self-erasure, over-explaining
    FREEZE = "freeze"       # Dissociation markers, flat affect, detachment
    FIGHT = "fight"         # Hypervigilance, defensiveness, threat scanning
    FLIGHT = "flight"       # Avoidance language, minimizing, subject-switching
    COLLAPSE = "collapse"   # Helplessness, hopelessness, shutdown markers


@dataclass
class CPTSDSignature:
    """
    Full CPTSD dimensional signature for a piece of text.

    Each sub-score is 0.0 - 1.0.
    composite_score is the weighted aggregate.
    """
    # Sub-dimension scores
    hypervigilance: float = 0.0        # Threat scanning, worst-case framing
    shame_density: float = 0.0         # Self-blame, "I'm too much", worthlessness
    narrative_fragmentation: float = 0.0  # Non-linear, incomplete, derailed story
    self_abandonment: float = 0.0      # Dismissing own needs, apologizing for existing
    window_of_tolerance: float = 1.0   # 1.0 = fully in window, 0.0 = outside window
    relational_collapse: float = 0.0   # Expecting abandonment, fawning, isolation pulls
    dissociation_markers: float = 0.0  # Depersonalization language, unreality, detachment

    # Detected response patterns
    primary_response: Optional[TraumaResponse] = None
    secondary_response: Optional[TraumaResponse] = None

    # Composite
    composite_score: float = 0.0       # Weighted aggregate, 0.0 = no signal, 1.0 = severe

    # Intervention flags
    slow_down_recommended: bool = False
    window_breach_risk: bool = False
    stabilization_needed: bool = False

    def intervention_summary(self) -> str:
        """Human-readable intervention recommendation"""
        if self.composite_score < 0.2:
            return "LOW: Standard engagement pace appropriate"
        elif self.composite_score < 0.4:
            return "MILD: Gentle pacing, watch for shame activation"
        elif self.composite_score < 0.6:
            return "MODERATE: Slow down, prioritize felt safety, avoid direct challenge"
        elif self.composite_score < 0.8:
            return "HIGH: Stabilization first, no new material, ground before proceeding"
        else:
            return "SEVERE: Window breach risk. Add only, never subtract. Match their world."


@dataclass
class CPTSDLexicon:
    """
    Linguistic markers associated with CPTSD dimensions.
    These are patterns, not diagnoses — texture detectors.
    """

    hypervigilance_patterns: List[str] = field(default_factory=lambda: [
        r"\balways\b.{0,20}\b(wrong|bad|hurt|fail)",
        r"\bwhat if\b",
        r"\bthey('re| are) going to\b",
        r"\bno one\b.{0,20}\b(cares|stays|helps)",
        r"\bwaiting for\b.{0,20}\b(to fall|to break|to leave)",
        r"\bsomething('s| is) wrong\b",
        r"\bcan('t| not) trust\b",
        r"\bpreparing for\b",
        r"\bthey('ll| will) eventually\b",
    ])

    shame_patterns: List[str] = field(default_factory=lambda: [
        r"\bi('m| am) too much\b",
        r"\bi('m| am) not enough\b",
        r"\bi('m| am) broken\b",
        r"\bi('m| am) gross\b",
        r"\bi('m| am) disgusting\b",
        r"\bi('m| am) (so |really )?(stupid|worthless|pathetic|ugly|unlovable)\b",
        r"\bi (don't|do not) deserve\b",
        r"\bsorry for (existing|being|asking|bothering)\b",
        r"\bi (always|never) (ruin|mess|break|destroy|ruin)\b",
        r"\balways ruin\b",
        r"\balways mess\b",
        r"\bit('s| is) my fault\b",
        r"\bi (should|shouldn't) have\b.{0,30}\b(known|seen|tried)\b",
        r"\bno one (could|would|should) want\b",
        r"\bso (gross|broken|damaged|wrong|bad|disgusting|pathetic)\b",
        r"\bwhy (would|do) (i|anyone).{0,20}\b(want|like|love|stay)\b",
        r"\bi('m| am) the problem\b",
        r"\beverything (i|i've).{0,20}\b(touch|do|try)\b",
        r"\bi (hate|can't stand) (myself|who i am)\b",
        r"\bwhat('s| is) wrong with me\b",
    ])

    fragmentation_patterns: List[str] = field(default_factory=lambda: [
        r"\bi don't know\b.{0,20}\bi don't know\b",  # Repeated confusion
        r"\.{3,}",  # Trailing off repeatedly
        r"\banyway\b.{0,10}\b(never mind|forget it|doesn't matter)\b",
        r"\bwhere was i\b",
        r"\bi lost (my|the) (train|thread|point)\b",
        r"\bsorry.{0,20}what (was|were) (i|we)\b",
        r"\bi can't (explain|describe|put into words)\b",
    ])

    self_abandonment_patterns: List[str] = field(default_factory=lambda: [
        r"\bi (don't|do not) (matter|count)\b",
        r"\bmy (needs|feelings|pain) (don't|do not|aren't|are not) (matter|important|real)\b",
        r"\bi (shouldn't|should not) (need|want|feel|ask)\b",
        r"\bi('m| am) (being|so) (needy|selfish|dramatic|sensitive)\b",
        r"\bsorry for (needing|wanting|asking|feeling)\b",
        r"\bi (know|knew) i (shouldn't|should not) (have )?(said|asked|brought)\b",
        r"\bnever mind.{0,20}(me|i|my)\b",
        r"\bi('ll| will) (be fine|be okay|manage|figure it out)\b.{0,20}\balone\b",
        r"\bshould(n't| not) have (said|brought|mentioned|shared)\b",
        r"\bshould('ve| have) kept (it|this|that).{0,20}(to myself|quiet|inside)\b",
        r"\bkept it to myself\b",
        r"\bforget (i|it|this|that) (said|mentioned|asked)\b",
        r"\bdisregard\b.{0,20}\bi\b",
        r"\bi('m| am) fine.{0,20}(honestly|really|don't worry)\b",
        r"\bdon't worry about (me|it|this)\b",
        r"\bi('ll| will) (figure|sort|work) it out\b",
        r"\bnot a big deal\b.{0,20}\bi\b",
        r"\bi\b.{0,20}\bnot a big deal\b",
    ])

    dissociation_patterns: List[str] = field(default_factory=lambda: [
        r"\bfeel(ing)? (unreal|not real|like i('m| am) not here|disconnected)\b",
        r"\bwatching (myself|my life) from\b",
        r"\bfloating\b.{0,20}\b(above|outside|away)\b",
        r"\bnumb(ed)?\b.{0,20}\b(again|still|always|everything)\b",
        r"\bdesensitized\b",
        r"\bcan('t| not) feel\b.{0,20}\b(anything|it|much)\b",
        r"\bheavy and (flat|empty|numb|nothing)\b",
        r"\b(going|gone) through (the )?motions\b",
        r"\bnot (quite|really|fully) (here|present|real)\b",
    ])

    window_breach_patterns: List[str] = field(default_factory=lambda: [
        r"\bcan('t| not) (breathe|stop|calm|think straight)\b",
        r"\bspiraling\b",
        r"\bfalling apart\b",
        r"\blosing it\b",
        r"\bshaking\b.{0,20}\bcan('t| not) stop\b",
        r"\bpanic(king)?\b",
        r"\bshutting down\b",
        r"\bcan('t| not) do this\b",
        r"\btoo much\b.{0,20}\bcan('t| not)\b",
        r"\beverything (is|feels) (too|overwhelming|impossible)\b",
    ])

    relational_collapse_patterns: List[str] = field(default_factory=lambda: [
        r"\bthey('re| are|'ll| will) (leave|go|disappear|abandon)\b",
        r"\beveryone (leaves|goes|abandons|disappears)\b",
        r"\bi (ruin|destroy|push away) (everyone|everything|people)\b",
        r"\btoo (much|broken|damaged) (for|to have)\b.{0,20}\b(anyone|relationship|love)\b",
        r"\bdon't deserve\b.{0,20}\b(love|care|help|kindness)\b",
        r"\bwhy (would|would anyone|would they) (stay|want|care)\b",
    ])


class CPTSDScorer:
    """
    Score CPTSD signature in organic text expression.

    Usage:
        scorer = CPTSDScorer()
        signature = scorer.score(text)
        print(signature.intervention_summary())
        print(f"Composite: {signature.composite_score:.3f}")
    """

    # Dimension weights for composite score
    WEIGHTS = {
        'hypervigilance': 0.10,
        'shame_density': 0.20,          # Weighted higher — shame is core CPTSD
        'narrative_fragmentation': 0.08,
        'self_abandonment': 0.18,        # Weighted higher — self-erasure is core
        'window_breach': 0.30,           # Highest weight — immediate safety signal
        'relational_collapse': 0.09,
        'dissociation': 0.05,
    }

    # Thresholds
    SLOW_DOWN_THRESHOLD = 0.35
    WINDOW_BREACH_THRESHOLD = 0.55
    STABILIZATION_THRESHOLD = 0.70

    def __init__(self):
        self.lexicon = CPTSDLexicon()

    def _count_matches(self, text: str, patterns: List[str]) -> int:
        """Count regex pattern matches in text"""
        text_lower = text.lower()
        count = 0
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            count += len(matches)
        return count

    def _normalize(self, count: int, text_length: int, sensitivity: float = 0.3) -> float:
        """
        Normalize match count to 0-1 score.
        sensitivity controls how quickly score saturates.
        Lower sensitivity = more matches needed to reach high score.
        """
        if text_length == 0:
            return 0.0
        # Normalize by text length (per 100 words) then apply saturation
        density = (count / max(text_length / 100, 1))
        return min(1.0, density * sensitivity)

    def _detect_primary_response(self, scores: Dict[str, float]) -> Tuple[Optional[TraumaResponse], Optional[TraumaResponse]]:
        """Detect primary and secondary trauma response from score profile"""
        response_map = {
            TraumaResponse.FAWN: scores.get('self_abandonment', 0) + scores.get('relational_collapse', 0),
            TraumaResponse.FREEZE: scores.get('dissociation', 0) + scores.get('window_breach', 0) * 0.5,
            TraumaResponse.FIGHT: scores.get('hypervigilance', 0),
            TraumaResponse.FLIGHT: scores.get('narrative_fragmentation', 0),
            TraumaResponse.COLLAPSE: scores.get('shame_density', 0) + scores.get('window_breach', 0),
        }

        sorted_responses = sorted(response_map.items(), key=lambda x: x[1], reverse=True)

        primary = sorted_responses[0][0] if sorted_responses[0][1] > 0.1 else None
        secondary = sorted_responses[1][0] if len(sorted_responses) > 1 and sorted_responses[1][1] > 0.1 else None

        return primary, secondary

    def score(self, text: str) -> CPTSDSignature:
        """
        Score CPTSD signature in text.

        Args:
            text: The organic communication to analyze

        Returns:
            CPTSDSignature with all sub-scores and intervention flags
        """
        word_count = len(text.split())

        # Score each dimension
        hypervigilance_count = self._count_matches(text, self.lexicon.hypervigilance_patterns)
        shame_count = self._count_matches(text, self.lexicon.shame_patterns)
        fragmentation_count = self._count_matches(text, self.lexicon.fragmentation_patterns)
        self_abandonment_count = self._count_matches(text, self.lexicon.self_abandonment_patterns)
        dissociation_count = self._count_matches(text, self.lexicon.dissociation_patterns)
        window_breach_count = self._count_matches(text, self.lexicon.window_breach_patterns)
        relational_collapse_count = self._count_matches(text, self.lexicon.relational_collapse_patterns)

        # Normalize scores
        scores = {
            'hypervigilance': self._normalize(hypervigilance_count, word_count, 0.4),
            'shame_density': self._normalize(shame_count, word_count, 0.5),
            'narrative_fragmentation': self._normalize(fragmentation_count, word_count, 0.6),
            'self_abandonment': self._normalize(self_abandonment_count, word_count, 0.5),
            'dissociation': self._normalize(dissociation_count, word_count, 0.4),
            'window_breach': self._normalize(window_breach_count, word_count, 1.5),  # High sensitivity — safety critical
            'relational_collapse': self._normalize(relational_collapse_count, word_count, 0.5),
        }

        # Window of tolerance: inverse of breach score, modulated by dissociation
        window_of_tolerance = max(0.0, 1.0 - scores['window_breach'] - (scores['dissociation'] * 0.3))

        # Weighted composite
        composite = (
            scores['hypervigilance'] * self.WEIGHTS['hypervigilance'] +
            scores['shame_density'] * self.WEIGHTS['shame_density'] +
            scores['narrative_fragmentation'] * self.WEIGHTS['narrative_fragmentation'] +
            scores['self_abandonment'] * self.WEIGHTS['self_abandonment'] +
            scores['window_breach'] * self.WEIGHTS['window_breach'] +
            scores['relational_collapse'] * self.WEIGHTS['relational_collapse'] +
            scores['dissociation'] * self.WEIGHTS['dissociation']
        )

        # Detect trauma response pattern
        primary, secondary = self._detect_primary_response(scores)

        # Build signature
        signature = CPTSDSignature(
            hypervigilance=scores['hypervigilance'],
            shame_density=scores['shame_density'],
            narrative_fragmentation=scores['narrative_fragmentation'],
            self_abandonment=scores['self_abandonment'],
            window_of_tolerance=window_of_tolerance,
            relational_collapse=scores['relational_collapse'],
            dissociation_markers=scores['dissociation'],
            primary_response=primary,
            secondary_response=secondary,
            composite_score=composite,
            slow_down_recommended=composite >= self.SLOW_DOWN_THRESHOLD,
            window_breach_risk=scores['window_breach'] >= self.WINDOW_BREACH_THRESHOLD,
            stabilization_needed=composite >= self.STABILIZATION_THRESHOLD,
        )

        return signature


def test_cptsd_scorer():
    """Test with real-world expression samples across severity levels"""

    scorer = CPTSDScorer()

    print("=" * 90)
    print("CPTSD SIGNATURE SCORER — Rose Glass Extension")
    print("=" * 90)

    test_cases = [
        (
            "baseline",
            "I had a really good day today. Work went well and I feel pretty calm about things. "
            "Looking forward to the weekend.",
        ),
        (
            "mild activation",
            "I've been a bit anxious lately. I keep wondering what if something goes wrong. "
            "I probably shouldn't need so much reassurance but it's been hard.",
        ),
        (
            "moderate CPTSD signal",
            "I feel like I'm too much for people. I know I shouldn't feel this way but I just "
            "keep waiting for them to leave. I'm sorry for even bringing this up, I know it's "
            "not a big deal. I'm probably being dramatic again.",
        ),
        (
            "high signal — self abandonment + shame",
            "I don't know why I even said anything. I'm so gross and broken. I always ruin "
            "everything. No one would want to deal with this, I should have just kept it to "
            "myself. I'm sorry for existing like this. It's my fault anyway.",
        ),
        (
            "window breach risk",
            "I can't breathe. I'm spiraling and I can't stop it. Everything is too much right "
            "now and I'm falling apart. I can't do this anymore. I'm shutting down.",
        ),
    ]

    for label, text in test_cases:
        print(f"\n{'─' * 90}")
        print(f"SAMPLE: {label.upper()}")
        print(f"Text: \"{text[:80]}...\"" if len(text) > 80 else f"Text: \"{text}\"")
        print(f"{'─' * 90}")

        sig = scorer.score(text)

        print(f"\n📊 Sub-Scores:")
        print(f"  Hypervigilance:           {sig.hypervigilance:.3f}")
        print(f"  Shame Density:            {sig.shame_density:.3f}")
        print(f"  Narrative Fragmentation:  {sig.narrative_fragmentation:.3f}")
        print(f"  Self Abandonment:         {sig.self_abandonment:.3f}")
        print(f"  Relational Collapse:      {sig.relational_collapse:.3f}")
        print(f"  Dissociation Markers:     {sig.dissociation_markers:.3f}")
        print(f"  Window of Tolerance:      {sig.window_of_tolerance:.3f}")

        print(f"\n🧠 Trauma Response Pattern:")
        print(f"  Primary:   {sig.primary_response.value if sig.primary_response else 'none detected'}")
        print(f"  Secondary: {sig.secondary_response.value if sig.secondary_response else 'none detected'}")

        print(f"\n⚡ Composite Score: {sig.composite_score:.3f}")
        print(f"\n🎯 Intervention: {sig.intervention_summary()}")

        if sig.window_breach_risk:
            print(f"\n🚨 WINDOW BREACH RISK — Stabilize before proceeding")
        if sig.stabilization_needed:
            print(f"🛑 STABILIZATION NEEDED — Add only, never subtract")
        elif sig.slow_down_recommended:
            print(f"⚠️  SLOW DOWN — Reduce pace and depth")

    print(f"\n{'=' * 90}")
    print("CLINICAL NOTE:")
    print("=" * 90)
    print("""
This scorer detects texture, not diagnosis.
High scores inform pace and approach — they do not pathologize.

Core principle: A person with high CPTSD signal is not broken.
They are adapted. The AI's job is to enter their world safely,
add to it, and never subtract.

"Never subtract from psychosis, only add."
    """)


if __name__ == "__main__":
    test_cptsd_scorer()
