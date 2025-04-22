from aidream_registration.utils.ants_utils import get_id_transform, get_atlas
from aidream_registration.dataloaders import AtlasImagingNiftiLoader
from aidream_registration import constants

from pathlib import Path
import ants


class VentricleRegByPadding:

    def __init__(self,
                 dir_hard_drive: Path = constants.DIR_DEFAULT_HARD_DRIVE):

        self.dir_hard_drive = dir_hard_drive
        assert self.dir_hard_drive.exists(), f"Missing {str(self.dir_hard_drive)} !"

        self.atlas_loader = AtlasImagingNiftiLoader(self.dir_hard_drive, source_mri="PIPELINE_SS")

    def get_pre_rt_t1_segmentation(self, patient: str):

        path_seg = (self.dir_hard_drive
                    / "AIDREAM DATA"
                    / "VENTRICLES SEGMENTATION"
                    / "NIFTI FREESURFER SEGMENTATION ON PRE_RT T1"
                    / fr"{patient}_pre_RT_T1_seg.nii.gz")

        if not path_seg.exists():
            raise FileNotFoundError(f"Missing {path_seg} !")

        return ants.image_read(str(path_seg))

    def get_ventricle_segmentation(self, patient: str):

        path_ventricle_seg = (self.dir_hard_drive
                              / "AIDREAM DATA"
                              / "VENTRICLES SEGMENTATION"
                              / "SEGMENTED VENTRICLES"
                              / fr"{patient}_pre_RT_T1_ventricle_seg.nii.gz")

        if not path_ventricle_seg.exists():
            self.create_ventricle_segmentation(patient, overwrite=False)

        return ants.image_read(str(path_ventricle_seg))

    def create_ventricle_segmentation(self, patient: str, overwrite: bool):

        path_ventricle_seg = (self.dir_hard_drive
                              / "AIDREAM DATA"
                              / "VENTRICLES SEGMENTATION"
                              / "SEGMENTED VENTRICLES"
                              / fr"{patient}_pre_RT_T1_ventricle_seg.nii.gz")

        if path_ventricle_seg.exists() and not overwrite:
            print(fr"Ventricle segmentation already exists for {patient} !")

        else:
            # Load the FREESURFER segmentation :
            ants_seg = self.get_pre_rt_t1_segmentation(patient)

            ants_ventricle_seg = ((ants_seg == 4) +
                                  (ants_seg == 43) +
                                  (ants_seg == 5) +
                                  (ants_seg == 44) +
                                  (ants_seg == 14) +
                                  (ants_seg == 15))

            # Apply identity transform to the segmentation so it matches the patient's T1 :
            t1 = self.atlas_loader.load_mri(patient, "pre_RT", "T1")

            ants_ventricle_seg = ants.apply_transforms(
                fixed=t1,
                moving=ants_ventricle_seg,
                transformlist=[get_id_transform()],
                interpolator="genericLabel"
            )

            ants.image_write(ants_ventricle_seg, str(path_ventricle_seg))
            print(fr"Ventricle segmentation created for {patient} !")
