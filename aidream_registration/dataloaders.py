from pathlib import Path
import ants

from aidream_registration import constants


class NativeImagingNiftiLoader:

    def __init__(self, dir_hard_drive: Path = constants.DIR_DEFAULT_HARD_DRIVE):

        self.dir_hard_drive = dir_hard_drive

    def load_mri(self, patient: str, stage: str, imaging: str):

        if stage not in ["pre_RT", "Rechute"]:
            raise ValueError(f"Stage {stage} not supported !")

        if imaging not in constants.LIST_MRI_MAPS:
            raise ValueError(f"Imaging {imaging} not supported !")

        path_imaging = (self.dir_hard_drive
                        / "AIDREAM DATA"
                        / "MRI DATA"
                        / "NIFTI"
                        / patient
                        / stage
                        / fr"{patient}_{stage}_{imaging}.nii.gz")
        assert path_imaging.exists(), f"Native {stage} {imaging} doesn't exist for {patient} !"

        return ants.image_read(str(path_imaging))

    def load_biomarker(self, patient: str, biomarker: str):

        if biomarker not in constants.LIST_CERCARE_MAPS:
            raise ValueError(f"Biomarker {biomarker} not supported !")

        path_biomarker = (self.dir_hard_drive
                          / "AIDREAM DATA"
                          / "CERCARE DATA"
                          / "NIFTI"
                          / patient
                          / fr"{patient}_{biomarker}.nii.gz")
        assert path_biomarker.exists(), f"Cercare {biomarker} doesn't exist for {patient} !"

        return ants.image_read(str(path_biomarker))
