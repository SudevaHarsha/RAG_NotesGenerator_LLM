from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors

# Slide title style
TITLE_STYLE = ParagraphStyle(
    name="SlideTitle",
    fontSize=18,
    leading=22,
    alignment=TA_CENTER,
    spaceAfter=12,
    textColor=colors.darkblue,
    bold=True
)

# Core explanation style
CORE_STYLE = ParagraphStyle(
    name="CoreExplanation",
    fontSize=12,
    leading=16,
    alignment=TA_LEFT,
    spaceAfter=10
)

# Additional clarification style (enriched mode)
ENRICHED_STYLE = ParagraphStyle(
    name="Enriched",
    fontSize=12,
    leading=16,
    alignment=TA_LEFT,
    textColor=colors.darkgreen,
    spaceAfter=10
)

# Deep explanation / teaching insights style
DEEP_STYLE = ParagraphStyle(
    name="DeepExplanation",
    fontSize=12,
    leading=16,
    alignment=TA_LEFT,
    spaceAfter=10
)

# Heading style for sections in Level 3
SECTION_HEADING = ParagraphStyle(
    name="SectionHeading",
    fontSize=14,
    leading=18,
    alignment=TA_LEFT,
    textColor=colors.darkred,
    spaceAfter=8,
    bold=True
)
