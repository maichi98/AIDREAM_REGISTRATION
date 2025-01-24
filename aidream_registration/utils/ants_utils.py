import shutil

from aidream_registration import constants

from pathlib import Path
import numpy as np
import ants


def get_id_transform():

    if not constants.PATH_IDENTITY_TRANSFORM.exists():

        identity_transform = ants.create_ants_transform(transform_type='AffineTransform', dimension=3)
        ants.write_transform(identity_transform, str(constants.PATH_IDENTITY_TRANSFORM))

    return str(constants.PATH_IDENTITY_TRANSFORM)


def create_empty_label():

    path_atlas = constants.PATH_SPGR_ATLAS
    assert path_atlas.exists(), f"Atlas {path_atlas} doesn't exist !"

    atlas = ants.image_read(str(path_atlas))
    empty_label = ants.from_numpy(np.zeros(atlas.shape, dtype=np.uint8), origin=atlas.origin,
                                  spacing=atlas.spacing, direction=atlas.direction)

    return empty_label


def save_as_empty_label(path_empty_label: Path | str):

    if not constants.PATH_EMPTY_LABEL.exists():

        ants_empty_label = create_empty_label()
        ants.image_write(ants_empty_label, str(constants.PATH_EMPTY_LABEL))

    shutil.copy2(src=str(constants.PATH_EMPTY_LABEL),
                 dst=str(path_empty_label))
