from pathlib import Path


DIR_DEFAULT_HARD_DRIVE = Path("/media/maichi/T7")
LIST_MRI_MAPS = ["T1", "T1CE", "FLAIR"]
LIST_CERCARE_MAPS = ["CTH", "rCBV", "OEF", "rCMRO2", "Delay", "rLeakage", "COV", "brainmask"]
LIST_PERFUSION_TIMEPOINTS = ["first", "last", "avg"]

DIR_DATA = Path(__file__).parent.parent / "data"

PATH_PERFUSION_PATIENTS = DIR_DATA / "perfusion_patients.txt"
PATH_REFERENTIAL_TABLE = DIR_DATA / "referential_table.xlsx"
