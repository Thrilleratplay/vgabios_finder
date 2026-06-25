# CSpell: words UEFI PCIR vgabios

"""Find VGA ROM within extracted UEFI."""
from typing import Union
import sys
import os
from struct import unpack_from
import argparse
import functools


def is_intel(vendor_id: int) -> bool:
    """Is Intel Vendor ID"""
    return vendor_id == 0x8086


def is_nvidia(vendor_id: int) -> bool:
    """Is NVIDIA Vendor ID"""
    return vendor_id == 0x10DE


def is_via(vendor_id: int) -> bool:
    """Is VIA Vendor ID"""
    return vendor_id == 0x1106


def is_amd(vendor_id: int) -> bool:
    """Is AMD/ATI Vendor ID"""
    return vendor_id == 0x1002


# https://pcilookup.com
def name_of_vendor(vendor_id: int) -> str:
    """String Name of a given Vendor ID"""
    if is_intel(vendor_id):
        return 'Intel'
    if is_nvidia(vendor_id):
        return 'NVIDIA'
    if is_via(vendor_id):
        return 'VIA'
    return 'Unknown'


def dir_path(path: str) -> str:
    """Determine if value is valid path."""
    # https://stackoverflow.com/a/54547257
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(
            f"readable_dir:{path} is not a valid path"
        )


def calculate_pcir_offset(data: bytes) -> int:
    """Calculate PCIR offset"""
    # Must start with PCI ROM magic 55 AA
    if len(data) > 0x1a and \
       data[0] == 0x55 and \
       data[1] == 0xAA and \
       data[30:48] == b'IBM VGA Compatible':
        # Pointer to PCI Data Structure is at offset 0x18 (little-endian word)
        offset = unpack_from('<H', data, 0x18)[0]

        if offset + 8 <= len(data) and \
           data[offset:offset+4] == b'PCIR':
            return offset
    return -1


def vendor_filter(
    vendor_id: int,
    intel_only: bool,
    nvidia_only: bool,
    via_only: bool,
    amd_only: bool
) -> bool:
    """Filter by vendor."""
    if intel_only:
        return is_intel(vendor_id)
    if nvidia_only:
        return is_nvidia(vendor_id)
    if via_only:
        return is_via(vendor_id)
    if amd_only:
        return is_amd(vendor_id)
    return True


def vga_rom_find(
    src_path: str,
    dest_path: str,
    intel_only: bool = False,
    nvidia_only: bool = False,
    via_only: bool = False,
    amd_only: bool = False,
    device_id: Union[int, None] = None,
) -> None:
    """Find VGA ROM."""
    # pylint: disable=W0612
    for root, dirs, files in os.walk(src_path):
        for name in files:
            if name == 'body.bin':
                path = os.path.join(root, name)
                try:
                    with open(path, 'rb') as f:
                        data = f.read()
                        offset = calculate_pcir_offset(data)
                        if offset > -1:
                            vendor_id = unpack_from('<H', data, offset+4)[0]

                            if vendor_filter(
                                vendor_id,
                                intel_only,
                                nvidia_only,
                                via_only,
                                amd_only
                            ):
                                vendor_name = name_of_vendor(vendor_id)
                                dev_id = unpack_from('<H', data, offset+6)[0]

                                if (device_id is None or device_id == dev_id):
                                    size = data[2] * 512
                                    print(
                                        f'{path}  vendor=0x{vendor_id:04x} '
                                        f'device=0x{dev_id:04x} '
                                        f'size={size} bytes'
                                    )
                                    outname = os.path.join(
                                        dest_path,
                                        (
                                            'vgabios_'
                                            f'{vendor_name}_'
                                            f'{vendor_id:04x}_'
                                            f'{dev_id:04x}'
                                            '.bin'
                                        )
                                    )
                                    open(outname, 'wb').write(
                                       data[:size] if size else data
                                    )
                                    print(f'  >>> EXTRACTED to {outname}')
                # pylint: disable=W0718
                except BaseException:
                    pass


######################################################################

# Set argparse Arguments
parser = argparse.ArgumentParser(
    description='Find VGA ROM within extracted UEFI.'
)
parser.add_argument(
    'path',
    help='Path to extracted UEFI data dump',
    type=dir_path
)
parser.add_argument(
    '-d',
    '--destination-path',
    help=(
        'Destination path VGA ROM(s) will be copied to.  '
        'If not provided, current directory is used'
    ),
    type=dir_path
)
parser.add_argument(
    '--intel-only',
    help='Find only Intel VGA Roms',
    action='store_true'
)
parser.add_argument(
    '--nvidia-only',
    help='Find only NVIDIA VGA Roms',
    action='store_true'
)
parser.add_argument(
    '--via-only',
    help='Find only VIA VGA Roms',
    action='store_true'
)
parser.add_argument(
    '--amd-only',
    help='Find only AMD/ATI VGA Roms',
    action='store_true'
)
parser.add_argument(
    '--device-id',
    type=functools.wraps(int)(lambda x: int(x, 0)),
    help='Filter based on the hexadecimal device Id'
)
args = parser.parse_args()

######################################################################

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
else:
    destination_path = args.destination_path
    if args.destination_path is None:
        destination_path = os.getcwd()

    vga_rom_find(
        args.path,
        destination_path,
        args.intel_only,
        args.nvidia_only,
        args.via_only,
        args.amd_only,
        args.device_id,
    )
