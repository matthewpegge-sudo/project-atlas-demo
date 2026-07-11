"""
Topic Catalogue — GCSE Higher Maths syllabus topics.

Each topic has a stable `topic_id` used as keys in LearnerDNA (e.g. mastery,
confidence, knowledge). IDs use the form "strand.topic_name".
"""

from __future__ import annotations

from dataclasses import dataclass

from ben_maths_coach.learner_dna import ExamTier


@dataclass(frozen=True)
class Topic:
    """One teachable topic on the GCSE Higher Maths syllabus."""

    topic_id: str
    name: str
    strand: str
    description: str = ""


@dataclass(frozen=True)
class TopicCatalogue:
    """A named collection of topics for a given qualification tier."""

    name: str
    tier: ExamTier
    topics: tuple[Topic, ...]

    def get(self, topic_id: str) -> Topic | None:
        """Return a topic by id, or None if it is not in this catalogue."""
        for topic in self.topics:
            if topic.topic_id == topic_id:
                return topic
        return None

    def topic_ids(self) -> list[str]:
        """All topic ids in catalogue order."""
        return [topic.topic_id for topic in self.topics]

    def strands(self) -> list[str]:
        """Unique strand names in the order they first appear."""
        seen: list[str] = []
        for topic in self.topics:
            if topic.strand not in seen:
                seen.append(topic.strand)
        return seen

    def topics_in_strand(self, strand: str) -> list[Topic]:
        """All topics belonging to one strand."""
        return [topic for topic in self.topics if topic.strand == strand]


# ---------------------------------------------------------------------------
# GCSE Higher Maths topics
# Aligned to common UK exam board content (AQA, Edexcel, OCR).
# ---------------------------------------------------------------------------

_HIGHER_TOPICS: tuple[Topic, ...] = (
    # Number
    Topic(
        "number.structure_and_calculation",
        "Structure and Calculation",
        "Number",
        "Types of number, order of operations, and standard calculation methods.",
    ),
    Topic(
        "number.fractions_decimals_percentages",
        "Fractions, Decimals and Percentages",
        "Number",
        "Converting between forms and calculating with fractions and percentages.",
    ),
    Topic(
        "number.standard_form",
        "Standard Form",
        "Number",
        "Writing numbers as a × 10ⁿ and calculating with standard form.",
    ),
    Topic(
        "number.surds_and_indices",
        "Surds and Indices",
        "Number",
        "Index laws, simplifying surds, and rationalising denominators.",
    ),
    Topic(
        "number.bounds_and_accuracy",
        "Bounds and Accuracy",
        "Number",
        "Upper and lower bounds, error intervals, and limits of accuracy.",
    ),
    Topic(
        "number.estimation",
        "Estimation",
        "Number",
        "Rounding, significant figures, and checking calculations.",
    ),
    # Algebra
    Topic(
        "algebra.expressions_and_formulae",
        "Expressions and Formulae",
        "Algebra",
        "Simplifying expressions, expanding brackets, and factorising.",
    ),
    Topic(
        "algebra.linear_equations",
        "Linear Equations",
        "Algebra",
        "Solving linear equations and forming equations from context.",
    ),
    Topic(
        "algebra.simultaneous_equations",
        "Simultaneous Equations",
        "Algebra",
        "Solving pairs of linear simultaneous equations algebraically and graphically.",
    ),
    Topic(
        "algebra.quadratics",
        "Quadratic Equations",
        "Algebra",
        "Factorising, completing the square, quadratic formula, and solving quadratics.",
    ),
    Topic(
        "algebra.inequalities",
        "Inequalities",
        "Algebra",
        "Linear and quadratic inequalities, number lines, and graphical regions.",
    ),
    Topic(
        "algebra.sequences",
        "Sequences",
        "Algebra",
        "nth terms of linear and quadratic sequences, and special sequences.",
    ),
    Topic(
        "algebra.graphs",
        "Graphs",
        "Algebra",
        "Plotting and interpreting linear, quadratic, cubic, reciprocal, and exponential graphs.",
    ),
    Topic(
        "algebra.algebraic_fractions",
        "Algebraic Fractions",
        "Algebra",
        "Simplifying and solving equations involving algebraic fractions.",
    ),
    Topic(
        "algebra.rearranging_formulae",
        "Rearranging Formulae",
        "Algebra",
        "Changing the subject of a formula, including with squares and fractions.",
    ),
    Topic(
        "algebra.functions",
        "Functions",
        "Algebra",
        "Function notation, composite and inverse functions, and graph transformations.",
    ),
    Topic(
        "algebra.iteration",
        "Iteration",
        "Algebra",
        "Using iterative formulae to find approximate solutions.",
    ),
    # Ratio, proportion and rates of change
    Topic(
        "ratio.direct_and_inverse_proportion",
        "Direct and Inverse Proportion",
        "Ratio, Proportion and Rates of Change",
        "Recognising and solving problems involving direct and inverse proportion.",
    ),
    Topic(
        "ratio.percentages",
        "Percentage Change",
        "Ratio, Proportion and Rates of Change",
        "Repeated percentage change, reverse percentages, and multipliers.",
    ),
    Topic(
        "ratio.compound_measures",
        "Compound Measures",
        "Ratio, Proportion and Rates of Change",
        "Speed, density, pressure, and other compound measures.",
    ),
    Topic(
        "ratio.growth_and_decay",
        "Growth and Decay",
        "Ratio, Proportion and Rates of Change",
        "Exponential growth and decay, including compound interest.",
    ),
    Topic(
        "ratio.gradients_and_rates",
        "Gradients and Rates of Change",
        "Ratio, Proportion and Rates of Change",
        "Interpreting gradients as rates of change, including real-life graphs.",
    ),
    # Geometry and measures
    Topic(
        "geometry.angles_and_polygons",
        "Angles and Polygons",
        "Geometry and Measures",
        "Angle facts, parallel lines, and interior and exterior angles of polygons.",
    ),
    Topic(
        "geometry.circle_theorems",
        "Circle Theorems",
        "Geometry and Measures",
        "Applying circle theorems to find unknown angles and lengths.",
    ),
    Topic(
        "geometry.area_and_volume",
        "Area and Volume",
        "Geometry and Measures",
        "Areas and volumes of 2D and 3D shapes, including cones, spheres, and frustums.",
    ),
    Topic(
        "geometry.pythagoras",
        "Pythagoras' Theorem",
        "Geometry and Measures",
        "Using Pythagoras' theorem in 2D and 3D problems.",
    ),
    Topic(
        "geometry.trigonometry",
        "Trigonometry",
        "Geometry and Measures",
        "SOHCAHTOA in right-angled triangles, including 3D problems.",
    ),
    Topic(
        "geometry.trigonometry_non_right",
        "Sine and Cosine Rules",
        "Geometry and Measures",
        "Using the sine rule, cosine rule, and area formula ½ab sin C.",
    ),
    Topic(
        "geometry.vectors",
        "Vectors",
        "Geometry and Measures",
        "Vector notation, addition, subtraction, and geometric proofs with vectors.",
    ),
    Topic(
        "geometry.transformations",
        "Transformations",
        "Geometry and Measures",
        "Translations, reflections, rotations, enlargements, and combined transformations.",
    ),
    Topic(
        "geometry.constructions_and_loci",
        "Constructions and Loci",
        "Geometry and Measures",
        "Accurate constructions with compass and ruler, and loci problems.",
    ),
    Topic(
        "geometry.similarity_and_congruence",
        "Similarity and Congruence",
        "Geometry and Measures",
        "Similar shapes, scale factors, and congruence criteria.",
    ),
    # Probability
    Topic(
        "probability.basic",
        "Basic Probability",
        "Probability",
        "Calculating probabilities, sample spaces, and the probability scale.",
    ),
    Topic(
        "probability.tree_diagrams",
        "Tree Diagrams",
        "Probability",
        "Combined events using tree diagrams and the AND/OR rules.",
    ),
    Topic(
        "probability.conditional",
        "Conditional Probability",
        "Probability",
        "Calculating and interpreting conditional probabilities.",
    ),
    Topic(
        "probability.venn_diagrams",
        "Venn Diagrams",
        "Probability",
        "Using Venn diagrams and set notation for probability problems.",
    ),
    # Statistics
    Topic(
        "statistics.data_handling",
        "Data Handling",
        "Statistics",
        "Collecting, organising, and interpreting statistical data.",
    ),
    Topic(
        "statistics.averages_and_spread",
        "Averages and Spread",
        "Statistics",
        "Mean, median, mode, range, and interquartile range.",
    ),
    Topic(
        "statistics.histograms",
        "Histograms",
        "Statistics",
        "Drawing and interpreting histograms with unequal class widths.",
    ),
    Topic(
        "statistics.cumulative_frequency",
        "Cumulative Frequency",
        "Statistics",
        "Cumulative frequency graphs, quartiles, and interquartile range.",
    ),
    Topic(
        "statistics.scatter_graphs",
        "Scatter Graphs",
        "Statistics",
        "Correlation, lines of best fit, and interpolation/extrapolation.",
    ),
)

HIGHER_MATHS_CATALOGUE = TopicCatalogue(
    name="GCSE Higher Maths",
    tier=ExamTier.HIGHER,
    topics=_HIGHER_TOPICS,
)
