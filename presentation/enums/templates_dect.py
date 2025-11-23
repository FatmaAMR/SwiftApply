from enum import Enum

class TemplateID(str, Enum):
    CLASSIC = "cv_classic.html"
    SIDEBAR = "cv_sidebar.html"
    MINIMAL = "cv_minimal.html"
    FUUL_PAGE = "cv_fullpage.html"
    TWO_COL = "cv_two_columns.html"