# AutoSign Windows

AutoSign Windows is a program that allows you to easily sign pdf documents on Windows with Custom or Self-Generated Certificates. It is a fork of 
AutoSign and also supports automatic printing of signed documents to the specified printer.

# Installation

To get started you first need to install the required dependencies. You can do this by running the following command in the root of the project by running the <kbd>installer.exe</kbd> file.

**Ensure that Windows Defender or Antivirus is disabled during installation.**

## How to use

Refer to https://github.com/OttomanZ/AutoSign for understanding the usage of main.py script. 

## Getting Printer Names

To get the printer names you can use the following command in PowerShell:

```powershell

.\GetPrinter.exe

```
**Output**:

```bash
[+] Detected Installed Printer: OneNote for Windows 10
[+] Detected Installed Printer: Microsoft XPS Document Writer
[+] Detected Installed Printer: Microsoft Print to PDF
[+] Detected Installed Printer: HP LaserJet MFP M129-M134
[+] Detected Installed Printer: Fax - HP LaserJet MFP M129-M134
[+] Detected Installed Printer: Fax
[+] Detected Installed Printer: AnyDesk Printer
[GOOD-BYE] Utility Developed by Muneeb A. Contact: muneeb@muneeb.co
```

## Generating a Self-Signed Certificate

To generate a self-signed certificate you can edit the configuration file in './certs/cert.conf' and then when you run the main script it will automatically generate that certificate in the root directoty of the project.

```json
{
    'common_name': 'SanjayKumar',
    'country': 'IN',
    'state': 'Karnataka',
    'city': 'New Delhi',
    'org': 'Sanjay Kumar',
    'org_unit': 'IT Department',
}
```

# Windows Tutorial (YouTube)
Check out the following video for a practical Tutorial on how to set it up on a Windows environment.


## System Requirements

```conf
OS: Windows 10 / 11
Python: 3.10
Scoop: 1.0.0
```

Do note that the `installer.exe` script automatically installs all of the required dependencies for you.