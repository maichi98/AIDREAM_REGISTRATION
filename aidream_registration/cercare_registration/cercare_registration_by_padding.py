from aidream_registration.dataloaders import NativeImagingNiftiLoader, AtlasImagingNiftiLoader
from aidream_registration.utils.ants_utils import get_id_transform

from aidream_registration import constants

from pathlib import Path
import ants


class CercareRegByPadding:

    def __init__(self,
                 dir_hard_drive: Path = constants.DIR_DEFAULT_HARD_DRIVE):

        self.dir_hard_drive = dir_hard_drive
        assert self.dir_hard_drive.exists(), f"Missing {str(self.dir_hard_drive)} !"

        self.native_loader = NativeImagingNiftiLoader(dir_hard_drive=dir_hard_drive)
        self.atlas_loader = AtlasImagingNiftiLoader(dir_hard_drive=dir_hard_drive)

    def round_cercare(self, patient: str, biomarker: str, overwrite: bool = False):

        if biomarker not in constants.DICT_CERCARE_P.keys():
            raise ValueError(f"Biomarker {biomarker} not supported to be rounded ! "
                             f"Supported biomarkers are {constants.DICT_CERCARE_P.keys()} !")

        p = constants.DICT_CERCARE_P[biomarker]
        path_rounded_biomarker = (self.dir_hard_drive
                                  / "AIDREAM DATA"
                                  / "CERCARE DATA"
                                  / "ROUNDED CERCARE"
                                  / patient
                                  / fr"{patient}_{biomarker}_rounded_p{p}.nii.gz")

        if not path_rounded_biomarker.exists() or overwrite:

            # Load the CERCARE biomarker :
            ants_biomarker = self.native_loader.load_biomarker(patient, biomarker)

            # Round the CERCARE biomarker :
            ants_rounded_biomarker = ants.from_numpy(ants_biomarker.numpy().round(p),
                                                     origin=ants_biomarker.origin, spacing=ants_biomarker.spacing,
                                                     direction=ants_biomarker.direction)
            ants.image_write(ants_rounded_biomarker, str(path_rounded_biomarker))
            print(f"Rounding {biomarker} for {patient} successful !")

        else:
            print(f"{biomarker} for {patient} already rounded !")

    def get_rounded_cercare(self, patient: str, biomarker: str):

        if biomarker not in constants.DICT_CERCARE_P.keys():
            raise ValueError(f"Biomarker {biomarker} not supported to be rounded ! "
                             f"Supported biomarkers are {constants.DICT_CERCARE_P.keys()} !")

        path_rounded_biomarker = (self.dir_hard_drive
                                  / "AIDREAM DATA"
                                  / "CERCARE DATA"
                                  / "ROUNDED CERCARE"
                                  / patient
                                  / fr"{patient}_{biomarker}_rounded_p{constants.DICT_CERCARE_P[biomarker]}.nii.gz")

        if not path_rounded_biomarker.exists():
            self.round_cercare(patient, biomarker)

        return ants.image_read(str(path_rounded_biomarker))

    def resample_cercare(self, patient: str, biomarker: str, interpolator: str, overwrite: bool = False):

        if biomarker not in constants.LIST_CERCARE_MAPS:
            raise ValueError(f"Biomarker {biomarker} not supported !")
        if interpolator not in constants.LIST_INTERPOLATORS:
            raise ValueError(f"Interpolator {interpolator} not supported !"
                             f"Supported interpolators are {constants.LIST_INTERPOLATORS} !")

        if biomarker == "brainmask" and interpolator != "genericLabel":
            print(f"Interpolation method for brainmask should be genericLabel, not {interpolator}.")
            interpolator = "genericLabel"

        # Resample the CERCARE biomarker :
        path_resampled_biomarker = (self.dir_hard_drive
                                    / "AIDREAM DATA"
                                    / "CERCARE DATA"
                                    / "RESAMPLED CERCARE TO T1"
                                    / patient
                                    / interpolator
                                    / fr"{patient}_{biomarker}_resampled_{interpolator}.nii.gz")

        if not path_resampled_biomarker.exists() or overwrite:

            # Load the T1 image :
            ants_t1 = self.native_loader.load_mri(patient, "pre_RT", "T1")

            # Load the CERCARE biomarker :
            to_round = (biomarker in constants.DICT_CERCARE_P.keys()
                        and interpolator in ["genericLabel", "nearestNeighbor"])
            ants_biomarker = self.get_rounded_cercare(patient, biomarker) if to_round else self.native_loader.load_biomarker(patient, biomarker)

            # Warp the CERCARE biomarker using the identity transform :
            ants_warped_biomarker = ants.apply_transforms(fixed=ants_t1,
                                                          moving=ants_biomarker,
                                                          transformlist=[get_id_transform()],
                                                          interpolator=interpolator)

            ants.image_write(ants_warped_biomarker, str(path_resampled_biomarker))
            print(f"Resampling {biomarker} for {patient} successful !")

        else:
            print(f"{biomarker} for {patient} already resampled !")

    def get_resampled_cercare(self, patient: str, biomarker: str, interpolator: str):

        if biomarker not in constants.LIST_CERCARE_MAPS:
            raise ValueError(f"Biomarker {biomarker} not supported !")
        if interpolator not in constants.LIST_INTERPOLATORS:
            raise ValueError(f"Interpolator {interpolator} not supported !"
                             f"Supported interpolators are {constants.LIST_INTERPOLATORS} !")

        if biomarker == "brainmask" and interpolator != "genericLabel":
            raise ValueError(f"Interpolation method for brainmask should be genericLabel, not {interpolator}.")

        path_resampled_biomarker = (self.dir_hard_drive
                                    / "AIDREAM DATA"
                                    / "CERCARE DATA"
                                    / "RESAMPLED CERCARE TO T1"
                                    / patient
                                    / interpolator
                                    / fr"{patient}_{biomarker}_resampled_{interpolator}.nii.gz")

        if not path_resampled_biomarker.exists():
            self.resample_cercare(patient, biomarker, interpolator)

        return ants.image_read(str(path_resampled_biomarker))

    def register_cercare(self, patient: str, biomarker: str, interpolator: str, overwrite: bool = False):

        if biomarker not in constants.LIST_CERCARE_MAPS:
            raise ValueError(f"Biomarker {biomarker} not supported !")
        if interpolator not in constants.LIST_INTERPOLATORS:
            raise ValueError(f"Interpolator {interpolator} not supported !"
                             f"Supported interpolators are {constants.LIST_INTERPOLATORS} !")

        if biomarker == "brainmask" and interpolator != "genericLabel":
            print(f"Interpolation method for brainmask should be genericLabel, not {interpolator}.")
            interpolator = "genericLabel"

        path_registered_biomarker = (self.dir_hard_drive
                                     / "AIDREAM DATA"
                                     / "CERCARE DATA"
                                     / "REGISTERED CERCARE BY PADDING"
                                     / patient
                                     / interpolator
                                     / fr"{patient}_{biomarker}_registered_by_padding_{interpolator}.nii.gz")

        if not path_registered_biomarker.exists() or overwrite:

            # Load the ATLAS T1 image :
            ants_atlas_t1 = self.atlas_loader.load_mri(patient, "pre_RT", "T1")

            # Load the CERCARE biomarker :
            to_round = (biomarker in constants.DICT_CERCARE_P.keys()
                        and interpolator in ["genericLabel", "nearestNeighbor"])
            ants_biomarker = self.get_rounded_cercare(patient, biomarker) if to_round else self.native_loader.load_biomarker(patient, biomarker)

            # Warp the CERCARE biomarker to the ATLAS T1 using the transform matrix of T1 to ATLAS T1 :
            path_transform = self.atlas_loader.get_mri_transform(patient, "pre_RT", "T1")
            ants_warped_biomarker = ants.apply_transforms(fixed=ants_atlas_t1,
                                                          moving=ants_biomarker,
                                                          transformlist=[path_transform],
                                                          interpolator=interpolator)

            ants.image_write(ants_warped_biomarker, str(path_registered_biomarker))
            print(f"Registering {biomarker} for {patient} successful !")

        else:
            print(f"{biomarker} for {patient} already registered !")

    def get_registered_cercare(self, patient: str, biomarker: str, interpolator: str):

        if biomarker not in constants.LIST_CERCARE_MAPS:
            raise ValueError(f"Biomarker {biomarker} not supported !")
        if interpolator not in constants.LIST_INTERPOLATORS:
            raise ValueError(f"Interpolator {interpolator} not supported !"
                             f"Supported interpolators are {constants.LIST_INTERPOLATORS} !")

        if biomarker == "brainmask" and interpolator != "genericLabel":
            raise ValueError(f"Interpolation method for brainmask should be genericLabel, not {interpolator}.")

        path_registered_biomarker = (self.dir_hard_drive
                                     / "AIDREAM DATA"
                                     / "CERCARE DATA"
                                     / "REGISTERED CERCARE BY PADDING"
                                     / patient
                                     / interpolator
                                     / fr"{patient}_{biomarker}_registered_by_padding_{interpolator}.nii.gz")

        if not path_registered_biomarker.exists():
            self.register_cercare(patient, biomarker, interpolator)

        return ants.image_read(str(path_registered_biomarker))

