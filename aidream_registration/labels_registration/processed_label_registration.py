from aidream_registration import constants
from aidream_registration.dataloaders import AtlasImagingNiftiLoader
from aidream_registration.utils.ants_utils import save_as_empty_label

from pathlib import Path
import ants


class ProcessedLabelRegistration:

    def __init__(self,
                 dir_hard_drive: Path = constants.DIR_DEFAULT_HARD_DRIVE):

        self.dir_hard_drive = dir_hard_drive
        assert self.dir_hard_drive.exists(), f"{self.dir_hard_drive} doesn't exist !"

        self.atlas_loader = AtlasImagingNiftiLoader(dir_hard_drive=self.dir_hard_drive, source_mri="PIPELINE_SS")

    def apply_affine_transformation_to_labels(self, patient: str, stage: str, reference: str, list_labels: list[str]):

        if stage not in ["pre_RT", "Rechute"]:
            raise ValueError(fr"Stage {stage} not supported !")

        # Load the ATLAS pre_RT T1 which serves as reference :
        print(fr'Loading {patient} ATLAS pre_RT T1...')
        ants_reference = self.atlas_loader.load_mri(patient=patient, stage="pre_RT", imaging="T1")

        # Registering the labels' source imaging on the ATLAS pre_RT T1 using an affine transformation :
        prefix_affine_transform = (self.dir_hard_drive
                                   / "AIDREAM DATA"
                                   / "LABELS DATA"
                                   / "REGISTERED LABELS ON PRE_RT T1"
                                   / stage
                                   / reference
                                   / patient
                                   / "transforms"
                                   / fr"{patient}_Affine_")
        prefix_affine_transform.parent.mkdir(exist_ok=True, parents=True)

        path_affine_transform = prefix_affine_transform.parent / fr"{patient}_Affine_0GenericAffine.mat"
        if path_affine_transform.exists():
            print(fr"the source imaging is already Affine registered on the ATLAS pre_RT T1 !")

        else:
            # Load the labels' source imaging :
            print(fr'Loading {patient} {stage} source imaging...')
            path_source_imaging = (self.dir_hard_drive
                                   / "AIDREAM DATA"
                                   / "LABELS DATA"
                                   / "NIFTI"
                                   / patient
                                   / stage
                                   / "SOURCE IMAGING"
                                   / fr"{patient}_{stage}_T1CE.nii.gz")
            assert path_source_imaging.exists(), f"SOURCE IMAGING doesn't exist for {patient} !"

            ants_source_imaging = ants.image_read(str(path_source_imaging))

            print("Registering the source imaging on the ATLAS pre_RT T1...")
            my_tx = ants.registration(fixed=ants_reference,
                                      moving=ants_source_imaging,
                                      type_of_transform='Affine',
                                      outprefix=str(prefix_affine_transform))

            # Warp the labels' source imaging using the affine transformation:
            print("Warping the source imaging using the affine transformation...")
            ants_warped_source_imaging = ants.apply_transforms(fixed=ants_reference,
                                                               moving=ants_source_imaging,
                                                               transformlist=my_tx['fwdtransforms'],
                                                               interpolator='bSpline')

            # Save the warped source imaging:
            path_warped_source_imaging = (self.dir_hard_drive
                                          / "AIDREAM DATA"
                                          / "LABELS DATA"
                                          / "REGISTERED LABELS ON PRE_RT T1"
                                          / stage
                                          / reference
                                          / patient
                                          / "REGISTERED SOURCE IMAGING"
                                          / fr"{patient}_{stage}_T1CE_Affine.nii.gz")
            path_warped_source_imaging.parent.mkdir(parents=True, exist_ok=True)

            ants.image_write(ants_warped_source_imaging, str(path_warped_source_imaging))

        # Warping the labels using the Affine transformation :
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

            if path_warped_label.exists():
                print(fr"Affine {stage} {label} already exists for {patient} !")

            else:

                # Load the label, if it doesn't exist, save an empty label :
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
                    ants_label = ants.image_read(str(path_label))

                    # Apply the affine transformation :
                    print(fr"Applying affine transformation to {label} for {patient} {stage} ...")
                    ants_warped_label = ants.apply_transforms(fixed=ants_reference,
                                                              moving=ants_label,
                                                              transformlist=[str(path_affine_transform)],
                                                              interpolator="genericLabel")

                    # Save the warped label :
                    ants.image_write(ants_warped_label, str(path_warped_label))

    def apply_syn_transformation_to_labels(self, patient: str, stage: str, reference: str, list_labels: list[str]):

        if stage not in ["pre_RT", "Rechute"]:
            raise ValueError(fr"Stage {stage} not supported !")

        # Load the ATLAS pre_RT T1CE which serves as reference :
        print(fr'Loading {patient} ATLAS pre_RT T1CE...')
        ants_reference = self.atlas_loader.load_mri(patient=patient, stage="pre_RT", imaging="T1CE")

        # Registering the labels' affine registered source imaging on the ATLAS pre_RT T1CE using a SyN transformation :
        prefix_syn_transform = (self.dir_hard_drive
                                / "AIDREAM DATA"
                                / "LABELS DATA"
                                / "REGISTERED LABELS ON PRE_RT T1"
                                / stage
                                / reference
                                / patient
                                / "transforms"
                                / fr"{patient}_SyN_")
        prefix_syn_transform.parent.mkdir(exist_ok=True, parents=True)

        path_syn_transform = prefix_syn_transform.parent / fr"{patient}_SyN_0GenericAffine.mat"
        if path_syn_transform.exists():
            print(fr"the source imaging is already SyN registered on the ATLAS pre_RT T1CE !")

        else:
            # Load the labels' source imaging :
            print(fr'Loading {patient} {stage} Affine registered source imaging...')
            path_source_imaging = (self.dir_hard_drive
                                   / "AIDREAM DATA"
                                   / "LABELS DATA"
                                   / "REGISTERED LABELS ON PRE_RT T1"
                                   / stage
                                   / reference
                                   / patient
                                   / "REGISTERED SOURCE IMAGING"
                                   / fr"{patient}_{stage}_T1CE_Affine.nii.gz")
            assert path_source_imaging.exists(), f"SOURCE IMAGING doesn't exist for {patient} !"

            ants_source_imaging = ants.image_read(str(path_source_imaging))

            print("Registering the source imaging on the ATLAS pre_RT T1CE...")
            my_tx = ants.registration(fixed=ants_reference,
                                      moving=ants_source_imaging,
                                      type_of_transform='SyN',
                                      outprefix=str(prefix_syn_transform))

            # Warp the labels' source imaging using the SyN transformation:
            print("Warping the source imaging using the SyN transformation...")
            ants_warped_source_imaging = ants.apply_transforms(fixed=ants_reference,
                                                               moving=ants_source_imaging,
                                                               transformlist=my_tx['fwdtransforms'],
                                                               interpolator='bSpline')

            # Save the warped source imaging:
            path_warped_source_imaging = (self.dir_hard_drive
                                          / "AIDREAM DATA"
                                          / "LABELS DATA"
                                          / "REGISTERED LABELS ON PRE_RT T1"
                                          / stage
                                          / reference
                                          / patient
                                          / "REGISTERED SOURCE IMAGING"
                                          / fr"{patient}_{stage}_T1CE_SyN.nii.gz")
            path_warped_source_imaging.parent.mkdir(parents=True, exist_ok=True)

            ants.image_write(ants_warped_source_imaging, str(path_warped_source_imaging))

        # Warping the labels using the SyN transformation :
        for label in list_labels:

            path_warped_label = (self.dir_hard_drive
                                 / "AIDREAM DATA"
                                 / "LABELS DATA"
                                 / "REGISTERED LABELS ON PRE_RT T1"
                                 / stage
                                 / reference
                                 / patient
                                 / "SyN"
                                 / fr"{patient}_{stage}_{label}_SyN.nii.gz")
            path_warped_label.parent.mkdir(parents=True, exist_ok=True)

            if path_warped_label.exists():
                print(fr"SyN {stage} {label} already exists for {patient} !")

            else:

                # Load the label, if it doesn't exist, save an empty label :
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

                    ants_label = ants.image_read(str(path_label))

                    path_affine_transform = path_syn_transform.parent / fr"{patient}_Affine_0GenericAffine.mat"

                    # Apply the SyN transformation :
                    print(fr"Applying SyN transformation to {label} for {patient} {stage} ...")
                    ants_warped_label = ants.apply_transforms(fixed=ants_reference,
                                                              moving=ants_label,
                                                              transformlist=[str(path_affine_transform),
                                                                             str(path_syn_transform)],
                                                              interpolator="genericLabel")

                    # Save the warped label :
                    ants.image_write(ants_warped_label, str(path_warped_label))
