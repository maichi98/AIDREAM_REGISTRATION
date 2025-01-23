from pathlib import Path


DIR_DEFAULT_HARD_DRIVE = Path("D:")
LIST_MRI_MAPS = ["T1", "T1CE", "FLAIR"]
LIST_CERCARE_MAPS = ["CTH", "rCBV", "OEF", "rCMRO2", "Delay", "rLeakage", "COV", "brainmask"]
LIST_PERFUSION_TIMEPOINTS = ["first", "last", "avg"]
LIST_INTERPOLATORS = ["linear", "bSpline", "lanczosWindowedSinc", "nearestNeighbor", "genericLabel"]

DIR_DATA = Path(__file__).parent.parent / "data"

PATH_PERFUSION_PATIENTS = DIR_DATA / "perfusion_patients.txt"
PATH_REFERENTIAL_TABLE = DIR_DATA / "referential_table.csv"
PATH_IDENTITY_TRANSFORM = DIR_DATA / "identity_transform.mat"

LIST_ATLAS_MRI_POSSIBLE_SOURCES = ["PIPELINE", "PIPELINE_SS"]
LIST_ATLAS_CERCARE_POSSIBLE_SOURCES = ["PADDING"]

DICT_CERCARE_P = {
    "CTH": 2,
    "OEF": 3,
    "rCBV": 2,
    "rCMRO2": 2,
    "Delay": 2,
    "COV": 2,
    "rLeakage": 1
}
