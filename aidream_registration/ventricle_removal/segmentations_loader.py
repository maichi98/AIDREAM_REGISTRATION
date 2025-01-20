from pathlib import Path
import ants
import SimpleITK as sitk

from aidream_registration import constants


class HammerSmithSegLoader:

    dir_data = constants.DIR_DATA / "hammersmith"
    assert dir_data.exists(), f"Directory {dir_data} does not exist"

    def get_ants_hammersmith(self):

        path_hammersmith = self.dir_data / "T1w_ICBM_skullstripped.nii.gz"
        assert path_hammersmith.exists(), f"File {path_hammersmith} does not exist"

        ants_hammersmith = ants.image_read(str(path_hammersmith))
        return ants_hammersmith

    def get_sitk_hammersmith(self):

        path_hammersmith = self.dir_data / "T1w_ICBM_skullstripped.nii.gz"
        assert path_hammersmith.exists(), f"File {path_hammersmith} does not exist"

        sitk_hammersmith = sitk.ReadImage(str(path_hammersmith))
        return sitk_hammersmith

    def get_mask_hammersmith(self):

        ants_hammersmith = self.get_ants_hammersmith()
        mask_hammersmith = ants_hammersmith > 0
        return mask_hammersmith

    def get_dict_ants_segmentations(self):

        dict_segmentations = {
            path_seg.name.removesuffix(".nii.gz"): ants.image_read(str(path_seg)) > 0
            for path_seg in self.dir_data.glob("*.nii.gz")
            if path_seg.name != "T1w_ICBM_skullstripped.nii.gz"
        }

        return dict_segmentations

