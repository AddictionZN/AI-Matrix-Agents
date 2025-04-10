# Miniconda Installation

## Step 1: Initialize Conda
```
conda init zsh
```

## Step 2: Update the Base Environment
```
conda update -n base -c defaults conda
```

## Step 3: Create a New Environment
```
conda create -n <env_name> python=3.12
```

## Step 4: Activate the Environment
```
conda activate <env_name>
```

## Step 5: Install Packages
```
conda install <package_name>
```


## Step 6: Install Packages from a requirements file
```
conda install --file requirements.txt
```

## Other: 
### Disable Auto-Activation of the Base Environment
```
conda config --set auto_activate_base false
conda config --show auto_activate_base
```

### : Deactivate the Environment
```
conda deactivate
```

### List Installed Packages
```
conda list
```

### Remove an Environment
```
conda remove -n <env_name> --all
```