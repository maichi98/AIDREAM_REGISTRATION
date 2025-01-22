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
        assert path_imaging.exists(), f"NATIVE {stage} {imaging} doesn't exist for {patient} !"

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

        ants_biomarker = ants.image_read(str(path_biomarker))

        if biomarker == "brainmask":
            ants_biomarker = ants_biomarker / ants_biomarker.max()

        return ants_biomarker


class AtlasImagingNiftiLoader:

    def __init__(self,
                 dir_hard_drive: Path = constants.DIR_DEFAULT_HARD_DRIVE,
                 source_mri: str = "PIPELINE",
                 source_cercare: str = "PADDING"):

        self.dir_hard_drive = dir_hard_drive

        self.source_mri = source_mri.upper()
        if source_mri not in constants.LIST_ATLAS_MRI_POSSIBLE_SOURCES:
            raise ValueError(f"Source MRI {source_mri} not supported !,"
                             f" supported sources are {constants.LIST_ATLAS_MRI_POSSIBLE_SOURCES}")

        self.source_cercare = source_cercare.upper()
        if source_cercare not in constants.LIST_ATLAS_CERCARE_POSSIBLE_SOURCES:
            raise ValueError(f"Source Cercare {source_cercare} not supported !"
                             f" supported sources are {constants.LIST_ATLAS_CERCARE_POSSIBLE_SOURCES}")

    def get_path_mri(self, patient: str, stage: str, imaging: str):

        if stage not in ["pre_RT", "Rechute"]:
            raise ValueError(f"Stage {stage} not supported !")

        if imaging not in constants.LIST_MRI_MAPS:
            raise ValueError(f"Imaging {imaging} not supported !")

        dict_imaging_paths = {
            "PIPELINE": f"AIDREAM DATA"
                        f"/MRI DATA"
                        f"/REGISTERED MRI BY PIPELINE"
                        f"/{stage}"
                        f"/OUTPUT_DIR"
                        f"/{patient}"
                        f"/coregistration"
                        f"/image_n4_register_{imaging.lower()}.nii.gz",
            "PIPELINE_SS": f"AIDREAM DATA"
                           f"/MRI DATA"
                           f"/REGISTERED MRI BY PIPELINE"
                           f"/{stage}"
                           f"/OUTPUT_DIR"
                           f"/{patient}"
                           f"/skullstripping"
                           f"/image_n4_register_ss_{imaging.lower()}.nii.gz"
        }

        path_imaging = (self.dir_hard_drive
                        / dict_imaging_paths[self.source_mri])
        assert path_imaging.exists(), f"ATLAS {stage} {imaging} doesn't exist for {patient} !"

        return path_imaging

    def load_mri(self, patient: str, stage: str, imaging: str):

        path_imaging = self.get_path_mri(patient, stage, imaging)
        return ants.image_read(str(path_imaging))

    def load_cercare(self, patient: str, biomarker: str, interpolator: str):

        if biomarker not in constants.LIST_CERCARE_MAPS:
            raise ValueError(f"Biomarker {biomarker} not supported !")

        if interpolator not in constants.LIST_INTERPOLATORS:
            raise ValueError(f"Interpolator {interpolator} not supported !"
                             f" supported interpolators are {constants.LIST_INTERPOLATORS}")

        dict_cercare_paths = {
            "PADDING": f"AIDREAM DATA"
                       f"/CERCARE DATA"
                       f"/REGISTERED CERCARE BY PADDING"
                       f"/{patient}"
                       f"/{interpolator}"
                       f"/{patient}_{biomarker}_registered_by_padding.nii.gz"
        }

        path_biomarker = (self.dir_hard_drive
                          / dict_cercare_paths[self.source_cercare])
        assert path_biomarker.exists(), f"ATLAS {biomarker} {interpolator} doesn't exist for {patient} !"

        return ants.image_read(str(path_biomarker))

    def get_mri_transform(self, patient: str, stage: str, imaging: str):

        if stage not in ["pre_RT", "Rechute"]:
            raise ValueError(f"Stage {stage} not supported !")

        if imaging not in constants.LIST_MRI_MAPS:
            raise ValueError(f"Imaging {imaging} not supported !")

        dict_transform_paths = {
            "PIPELINE": f"AIDREAM DATA"
                        f"/MRI DATA"
                        f"/REGISTERED MRI BY PIPELINE"
                        f"/{stage}"
                        f"/OUTPUT_DIR"
                        f"/{patient}"
                        f"/affine_transform"
                        f"/image_n4_fwdtransforms_{imaging.lower()}.mat",
        }
        dict_transform_paths["PIPELINE_SS"] = dict_transform_paths["PIPELINE"]

        path_transform = (self.dir_hard_drive
                          / dict_transform_paths[self.source_mri])
        assert path_transform.exists(), f"ATLAS {stage} {imaging} transform doesn't exist for {patient} !"

        return str(path_transform)
