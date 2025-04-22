import pandas as pd
import subprocess
import os
import numpy as np


def run_command(command: str):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False
    return True


if __name__ == "__main__":

    os.environ["FS_ALLOW_DEEP"] = "1"

    # path_ref = "/home/maichi/work/my_projects/AIDREAM/AIDREAM_REGISTRATION/data/referential_table.csv"
    # df_ref = pd.read_csv(path_ref)
    #
    # aseg_patients = df_ref.loc[df_ref["FREESURFER STATUS"] == "ASEG", "AIDREAM_ID"].tolist()
    #
    # aseg_auto_patients = df_ref.loc[df_ref["FREESURFER STATUS"] == "ASEG_AUTO", "AIDREAM_ID"].tolist()

    aseg_patients = ["AIDREAM_120", "AIDREAM_306", "AIDREAM_358"]

    for patient in aseg_patients:

        print(fr" --------------------- {patient} --------------------- ")

        # convert the aseg.mgz to nii.gz using mri_convert :
        path_src = f"/media/maichi/T7/AIDREAM DATA/VENTRICLES SEGMENTATION/FREESURFER SEGMENTATION ON PRE_RT T1/{patient}/mri/aseg.mgz"
        path_dst = f"/media/maichi/T7/AIDREAM DATA/VENTRICLES SEGMENTATION/NIFTI FREESURFER SEGMENTATION ON PRE_RT T1/{patient}_pre_RT_T1_seg.nii.gz"

        command = f'mri_convert "{path_src}" "{path_dst}"'

        if not run_command(command):
            print(fr"Error converting {patient}")
            continue

        else:
            print(fr"Converted {patient}")

    # for patient in aseg_auto_patients:
    #
    #     print(fr" --------------------- {patient} --------------------- ")
    #
    #     # convert the aseg.auto.mgz to nii.gz using mri_convert :
    #     path_src = f"/media/maichi/T7/AIDREAM DATA/FREESURFER RESULTS/PRE_RT T1 SEGMENTATION/{patient}/mri/aseg.auto.mgz"
    #     path_dst = f"/media/maichi/T7/AIDREAM DATA/FREESURFER RESULTS/PRE_RT T1 SEGMENTATION NIFTI/{patient}_pre_RT_T1_seg.nii.gz"
    #
    #     command = f'mri_convert --ctab /home/maichi/freesurfer/FreeSurferColorLUT.txt "{path_src}" "{path_dst}"'
    #
    #     if not run_command(command):
    #         print(fr"Error converting {patient}")
    #         continue
    #
    #     else:
    #         print(fr"Converted {patient}")
