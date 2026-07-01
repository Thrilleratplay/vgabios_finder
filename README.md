# VGA BIOS finder

Find VGA BIOS blobs from [UEFITool's UEFIExtract](https://github.com/LongSoft/UEFITool) dumps.  Adapted from [chrisf4lc0n's blog](https://coreboot.f4lc0n-industries.co.uk/w541.html#53-extract-the-nvidia-k1100m-vga-rom-and-intel-vbt-using-uefiextract)

## Requirements

`uefiextract` must be run on the image file before executing this script.

## Usage

Extracted file names will be in the format of `vgabios_<VENDER NAME>_<VENDOR ID>_<DEVICE ID>.bin`.  Use a site like [PCI Lookup](https://pcilookup.com/) to reference the device's model name to find the VGA BIOS relevant to your system.

```sh
usage: vgabios_finder.py [-h] [-d DESTINATION_PATH] [--intel-only] [--nvidia-only] [--via-only] [--amd-only] [--device-id DEVICE_ID] path

Find VGA ROM within extracted UEFI.

positional arguments:
  path                  Path to extracted UEFI data dump

options:
  -h, --help            show this help message and exit
  -d, --destination-path DESTINATION_PATH
                        Destination path VGA ROM(s) will be copied to. If not provided, current directory is used
  --intel-only          Find only Intel VGA Roms
  --nvidia-only         Find only NVIDIA VGA Roms
  --via-only            Find only VIA VGA Roms
  --amd-only            Find only AMD/ATI VGA Roms
  --device-id DEVICE_ID
                        Filter based on the hexadecimal device Id
```

## Examples

```sh
$> python vgabios_finder.py  -d ./dest/ w530_12m_full.bin.dump                                                                                       [15:34:16]
w530_12m_full.bin.dump/3 BIOS region/1 7A9354D9-0468-444A-81CE-0BF617D890DF/0 4A538818-5AE0-4EB2-B2EB-488B23657022/0 Compressed section/1 Volume image section/0 7A9354D9-0468-444A-81CE-0BF617D890DF/347 0AFCDD7A-345E-415E-926D-C5971B580400/0 FC1BCDB0-7D31-49AA-936A-A4600D9DD083/0 Raw section/body.bin  vendor=0x8086 device=0x0106 size=65536 bytes
  >>> EXTRACTED to ./dest/vgabios_Intel_8086_0106.bin
w530_12m_full.bin.dump/3 BIOS region/1 7A9354D9-0468-444A-81CE-0BF617D890DF/0 4A538818-5AE0-4EB2-B2EB-488B23657022/0 Compressed section/1 Volume image section/0 7A9354D9-0468-444A-81CE-0BF617D890DF/348 09D7A900-3333-421D-B217-71A7D87857BC/0 FC1BCDB0-7D31-49AA-936A-A4600D9DD083/0 Raw section/body.bin  vendor=0x10de device=0x0ffc size=90624 bytes
  >>> EXTRACTED to ./dest/vgabios_NVIDIA_10de_0ffc.bin
w530_12m_full.bin.dump/3 BIOS region/1 7A9354D9-0468-444A-81CE-0BF617D890DF/0 4A538818-5AE0-4EB2-B2EB-488B23657022/0 Compressed section/1 Volume image section/0 7A9354D9-0468-444A-81CE-0BF617D890DF/349 9781FA9D-5A3B-431A-AD59-2748C9A170EC/0 FC1BCDB0-7D31-49AA-936A-A4600D9DD083/0 Raw section/body.bin  vendor=0x10de device=0x0ffb size=90624 bytes
  >>> EXTRACTED to ./dest/vgabios_NVIDIA_10de_0ffb.bin
```


```sh
$> python vgabios_finder.py  --intel-only -d ./dest/ w530_12m_full.bin.dump                                                                            [15:34:48]
w530_12m_full.bin.dump/3 BIOS region/1 7A9354D9-0468-444A-81CE-0BF617D890DF/0 4A538818-5AE0-4EB2-B2EB-488B23657022/0 Compressed section/1 Volume image section/0 7A9354D9-0468-444A-81CE-0BF617D890DF/347 0AFCDD7A-345E-415E-926D-C5971B580400/0 FC1BCDB0-7D31-49AA-936A-A4600D9DD083/0 Raw section/body.bin  vendor=0x8086 device=0x0106 size=65536 bytes
  >>> EXTRACTED to ./dest/vgabios_Intel_8086_0106.bin
```

```sh
$> python vgabios_finder.py  --device-id 0x0ffb  -d ./dest/ w530_12m_full.bin.dump                                                                     [15:35:40]
w530_12m_full.bin.dump/3 BIOS region/1 7A9354D9-0468-444A-81CE-0BF617D890DF/0 4A538818-5AE0-4EB2-B2EB-488B23657022/0 Compressed section/1 Volume image section/0 7A9354D9-0468-444A-81CE-0BF617D890DF/349 9781FA9D-5A3B-431A-AD59-2748C9A170EC/0 FC1BCDB0-7D31-49AA-936A-A4600D9DD083/0 Raw section/body.bin  vendor=0x10de device=0x0ffb size=90624 bytes
  >>> EXTRACTED to ./dest/vgabios_NVIDIA_10de_0ffb.bin
```
