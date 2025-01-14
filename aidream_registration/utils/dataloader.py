from pathlib import Path
import ants

from aidream_registration import constants


class NativeLoader:

    def __init__(self, dir_hard_drive: Path = constants.DIR_DEFAULT_HARD_DRIVE):

        self.dir_hard_drive = dir_hard_drive

    def load_imaging(self, patient: str, stage: str, imaging: str):

        if stage not in ["pre_RT", "Rechute"]:
            raise ValueError(f"Stage {stage} not supported !")

        if imaging not in constants.LIST_MRI_MAPS:
            raise ValueError(f"Imaging {imaging} not supported !")

        path_imaging = (self.dir_hard_drive
                        / "REGISTRATION/NIFTI/NATIVE"
                        / patient / stage
                        / fr"{patient}_{stage}_{imaging}.nii.gz")
        assert path_imaging.exists(), f"Native {stage} {imaging} doesn't exist for {patient} !"

        return ants.image_read(str(path_imaging))

    def load_cercare(self, patient: str, biomarker: str):

        if biomarker not in constants.LIST_CERCARE_MAPS:
            raise ValueError(f"Biomarker {biomarker} not supported !")

        path_biomarker = (self.dir_hard_drive
                          / "REGISTRATION/NIFTI/CERCARE"
                          / patient
                          / fr"{patient}_pre_RT_{biomarker}.nii.gz")
        assert path_biomarker.exists(), f"Cercare {biomarker} doesn't exist for {patient} !"

        return ants.image_read(str(path_biomarker))

    def load_perfusion(self, patient: str, timepoint: str):

        if timepoint not in constants.LIST_PERFUSION_TIMEPOINTS:
            raise ValueError(f"Timepoint {timepoint} not supported !")

        path_perfusion = (self.dir_hard_drive
                          / "REGISTRATION/NIFTI/PERFUSION"
                          / fr"{patient}_pre_RT_{timepoint}_perfusion.nii.gz")

        assert path_perfusion.exists(), f"Perfusion {timepoint} doesn't exist for {patient} !"

        return ants.image_read(str(path_perfusion))
