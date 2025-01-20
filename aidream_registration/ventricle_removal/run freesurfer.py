from pathlib import Path
import subprocess
import os
import numpy as np

dir_hard_drive = Path("/media/maichi/T7")


def get_perfusion_patients():

    list_patients = Path("/home/maichi/work/my_projects/AIDREAM/AIDREAM_REGISTRATION/data/perfusion_patients.txt").read_text().splitlines()
    list_patients = [list_patients[i]
                     for i in np.argsort([int(p.strip("AIDREAM_"))
                                          for p in list_patients
                                          if p.startswith("AIDREAM_")
                                          ])
                     ]

    return list_patients


def run_command(command: str):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False
    return True


if __name__ == "__main__":

    FREESURFER_HOME = "/home/maichi/freesurfer"
    SETUP_SCRIPT = os.path.join(FREESURFER_HOME, "SetUpFreeSurfer.sh")

    os.environ["FS_ALLOW_DEEP"] = "1"

    list_patients = get_perfusion_patients()[:5]
    dir_hd = Path("/media/maichi/T7")

    for patient in list_patients:

        print(fr"Processing patient {patient} ----------- ")

        dir_t1 = str(dir_hd / "freesurfer" / fr"{patient}_t1.nii.gz")

        autorecon = f"recon-all -i {dir_t1} -subjid {patient} -all -openmp 25"
        print("Running autorecon")
        if not run_command(autorecon):
            print(fr"Error in autorecon, for patient {patient}, skipping")

        else:
            print(fr'Successfully processed patient {patient}')
