from aidream_registration import constants
from aidream_registration.dataloaders import AtlasImagingNiftiLoader
from aidream_registration.utils.ants_utils import save_as_empty_label

from pathlib import Path
import ants


class NativeLabelRegistration:

    def __init__(self,
                 dir_hard_drive: Path = constants.DIR_DEFAULT_HARD_DRIVE,
                 overwrite: bool = False):

        self.dir_hard_drive = dir_hard_drive
        assert self.dir_hard_drive.exists(), f"{self.dir_hard_drive} doesn't exist !"

        self.overwrite = overwrite
        self.atlas_loader = AtlasImagingNiftiLoader(dir_hard_drive=self.dir_hard_drive, source_mri="PIPELINE_SS")

    def apply_affine_transformation_to_labels(self, patient: str, stage: str, reference: str, list_labels: list[str]):

        if stage not in ["pre_RT", "Rechute"]:
            raise ValueError(f"Stage {stage} not supported !")

        # Load the ATLAS pre_RT T1 which serves as reference :
        print(fr'Loading {patient} ATLAS pre_RT T1...')
        ants_reference = self.atlas_loader.load_mri(patient=patient, stage="pre_RT", imaging="T1")

        # Warping the labels using the Affine transformation:
        for label in list_labels:

            path_warped_label = (self.dir_hard_drive
                                 / "AIDREAM DATA"
                                 / "LABELS DATA"
                                 / "REGISTERED LABELS ON PRE_RT T1"
                                 / stage
                                 / reference
                                 / patient
                                 / "Affine"
                                 / fr"{patient}_{stage}_{label}_Affine.nii.gz")
            path_warped_label.parent.mkdir(parents=True, exist_ok=True)

            if path_warped_label.exists() and not self.overwrite:
                print(fr"Affine {label} already exists for {patient} !")

            else:

                # Load the label :
                path_label = (self.dir_hard_drive
                              / "AIDREAM DATA"
                              / "LABELS DATA"
                              / "REFACTORED LABELS NIFTI"
                              / patient
                              / stage
                              / fr"{patient}_{stage}_{label}.nii.gz")
                if not path_label.exists():

                    print(f"Patient {patient} doesn't have {stage} {label}, saving empty label !")
                    save_as_empty_label(path_empty_label=path_warped_label)

                else:

                    # Load the label :
                    ants_label = ants.image_read(str(path_label))

                    # Apply the affine transformation :
                    print(fr"Applying affine transformation to {label} for {patient} {stage} ...")

                    path_affine_transform = self.atlas_loader.get_mri_transform(patient=patient,
                                                                                stage=stage,
                                                                                imaging="T1CE")
                    ants_warped_label = ants.apply_transforms(fixed=ants_reference,
                                                              moving=ants_label,
                                                              transformlist=[str(path_affine_transform)],
                                                              interpolator="genericLabel")

                    # Save the warped label :
                    ants.image_write(ants_warped_label, str(path_warped_label))
