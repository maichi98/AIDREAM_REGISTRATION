import pandas as pd
import numpy as np

from aidream_registration import constants


def get_perfusion_patients():

    list_patients = constants.PATH_PERFUSION_PATIENTS.read_text().splitlines()
    list_patients = [list_patients[i]
                     for i in np.argsort([int(p.strip("AIDREAM_"))
                                          for p in list_patients
                                          if p.startswith("AIDREAM_")
                                          ])
                     ]

    return list_patients


def get_referential_table(list_patients: list = None):

    df_ref = pd.read_excel(constants.PATH_REFERENTIAL_TABLE)

    if list_patients is not None:
        df_ref = df_ref.loc[df_ref["AIDREAM_ID"].isin(list_patients)].reset_index(drop=True)

    return df_ref
