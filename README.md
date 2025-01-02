# DXMT Update Script for Crossover App

A simple Python script to update DXMT files in the Crossover app. Compatible with any path that includes the `dxmt` folder.

## Requirements

- **Python 3.6+**: [Download Python](https://www.python.org/downloads/)
- **Crossover App**: [Crossover](https://www.codeweavers.com/crossover)
- **CXPatcher**: [CXPatcher GitHub](https://github.com/italomandara/CXPatcher)

## Installation

1. **Clone the Repository**

   ```bash
   git clone git@github.com:zqigolden/dxmt_update.git
   cd dxmt_update
   ```

## Usage

1. **Download DXMT Files**

   - **Important:** The script does **not** download DXMT files automatically. You need to download them manually from the [DXMT Releases](https://github.com/3Shain/dxmt/actions) page.

2. **Unzip the Downloaded File**

   - Extract the contents to a preferred location.

3. **(Optional) Rename the Folder**

   - For organization, rename the folder with its CI build number:

     ```bash
     mv build-release build-release-123
     ```

4. **Patch with CXPatcher**

   - Use [CXPatcher](https://github.com/italomandara/CXPatcher) to modify the DXMT files as needed.

5. **Run the Update Script**

   - Execute the script with the path to any parent folder containing the `dxmt` folder.

     ```bash
     python dxmt_update.py /path/to/parent_folder_with_dxmt
     ```

## How It Works

- **Backup Existing Files:** Moves current DXMT-related files to a `backup` folder with timestamps.
- **Replace Files:** Copies new DXMT files to the appropriate Wine directories.
- **Interactive Selection:** Prompts you to select the correct Wine folder and bottle if multiple are found.
