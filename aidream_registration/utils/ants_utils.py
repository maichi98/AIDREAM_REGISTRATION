from aidream_registration import constants

import ants


def get_id_transform():

    if not constants.PATH_IDENTITY_TRANSFORM.exists():

        identity_transform = ants.create_ants_transform(transform_type='AffineTransform', dimension=3)
        ants.write_transform(identity_transform, str(constants.PATH_IDENTITY_TRANSFORM))

    return str(constants.PATH_IDENTITY_TRANSFORM)
