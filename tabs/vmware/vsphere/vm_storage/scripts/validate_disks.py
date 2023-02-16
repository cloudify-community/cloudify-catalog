# Stdlib imports

# Third party imports
from fabric2 import task

# Cloudify imports
from cloudify import ctx
from cloudify.exceptions import NonRecoverableError

# This package imports

@task
def configure(connection):
    # In case of connection related retries, see if we need to scan+mkfs
    # This will still fail in some circumstances
    # (e.g. conn failure after rescan)
    ctx.logger.info('Seeing if we need to initialise the disk..')
    mounted = connection.sudo('mount').splitlines()
    mounted_paths = [mount.split()[0] for mount in mounted]
    if '/mnt' in mounted_paths:
        ctx.logger.info('Device already initialised and mounted')
    else:
        scsi_id = connection.env['scsi_id']
        ctx.logger.info('Scanning SCSI host bus')
        connection.sudo('for host in /sys/class/scsi_host/*; '
            'do echo "- - -" > ${host}/scan; '
            'done')
        ctx.logger.info(
            'Getting target device with SCSI ID: {scsi_id}'.format(
                scsi_id=scsi_id,
            )
        )
        scsi_candidates = connection.sudo(
            'lsscsi *:{scsi_id}:*'.format(scsi_id=scsi_id),
        ).splitlines()
        scsi_candidates = [
            candidate for candidate in scsi_candidates
            if 'vmware' in candidate.lower() and
            'virtual disk' in candidate.lower()
        ]

        if len(scsi_candidates) != 1:
            raise NonRecoverableError(
                'Could not find a single candidate device. '
                'Found: {devices}'.format(devices=scsi_candidates)
            )
        else:
            # lsscsi output example:
            # [0:0:1:0]    disk    VMware   Virtual disk     1.0   /dev/sdb
            target_device = scsi_candidates[0].split()[-1]
            ctx.logger.info('Target device is {target}'.format(
                            target=target_device))

        ctx.logger.info('Formatting device as ext4...')
        connection.sudo('mkfs.ext4 -F {device}'.format(device=target_device))
        connection.sudo('mount {device} /mnt'.format(device=target_device))
        ctx.logger.info('Device formatted and mounted on /mnt')

    ctx.logger.info('Attempting to create file on device...')
    connection.sudo('touch /mnt/testfile')
    ctx.logger.info('Successfully created test file on device')

if __name__ == "__main__":
    pass