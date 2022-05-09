# Dementia_detection_using_AI


[![forthebadge](https://forthebadge.com/images/badges/built-by-developers.svg)](http://forthebadge.com)   [![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)      [![forthebadge](https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg)](https://forthebadge.com)

<!--
[![Gem Version](https://badge.fury.io/rb/colorls.svg)](https://badge.fury.io/rb/colorls)
[![CI](https://github.com/athityakumar/colorls/actions/workflows/ruby.yml/badge.svg)](https://github.com/athityakumar/colorls/actions/workflows/ruby.yml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=shields)](http://makeapullrequest.com)
-->
The project is about creating a model which predicts the flight fare price based on factors like distance, number of stops, total hours of flight as well as the type of seat

Here are the screenshots of working example on an AWS Linux Instance.


<!-- #`oh-my-zsh` with `powerlevel9k` theme and `powerline nerd-font + awesome-config` font with the `Solarized Dark` color theme. 

 ![image](https://user-images.githubusercontent.com/17109060/32149040-04f3125c-bd25-11e7-8003-66fd29bc18d4.png)

*If you're interested in knowing the powerlevel9k configuration to get this prompt, have a look at [this gist](https://gist.github.com/athityakumar/1bd5e9e24cd2a1891565573a893993eb).*

-->

# Table of contents

- [Usage](#usage)
- [Installation](#installation)
- [Recommended configurations](#recommended-configurations)
- [Custom configurations](#custom-configurations)
- [Updating](#updating)
- [Uninstallation](#uninstallation)
- [Contributing](#contributing)
- [Future Scope](#future-scope)

</br></br>

# Usage

[(Back to top)](#table-of-contents)

Man pages have been added. Checkout `man colorls`.


# Installation


[(Back to top)](#table-of-contents)

1. Install git (preferably, version >= 2.0) and python (preferably, version >=3.6)
 [(windows)](https://www.maketecheasier.com/install-git-bash-on-windows/)
 For Linux :
 ```bash
    sudo yum instal git -y
    sudo yum install python -y
 ```
 
2. Copy the github url from the repository : 

 ```bash
 https://github.com/SiddharthaShandilya/air_quality_index_prediction.git
 ```

3. Select a Directory in local system and use 

  ```bash 
  git clone https://github.com/SiddharthaShandilya/air_quality_index_prediction.git           
  ```

    *Note for `git clone command`  Please make sure that you have proper internet connection. *

    *Note for `python` Please try to anaconda for running the app.*  

4. Create a seperate virtual environment to avoid conflict between python libraries :
```bash
    python3 -m venv new-env 
```

5. Activate the virtual env: 👉 [(click Here)](https://www.programshelp.com/help/python/activate_virtual_environment_python_windows_10.html)
6. Install all the libraries for the application.
```bash
pip3 install -r requirements.txt
```

6. Have a look at [Recommended configurations](#recommended-configurations) and [Custom configurations](#custom-configurations).


</br></br>


# Recommended configurations

[(Back to top)](#table-of-contents)

<!--

1. To add some short command (say, `lc`) with some flag options (say, `-l`, `-A`, `--sd`) by default, add this to your shell configuration file (`~/.bashrc`, `~/.zshrc`, etc.) :
    ```sh
    alias lc='colorls -lA --sd'
    ```

2. For changing the icon(s) to other unicode icons of choice (select icons from [here](https://nerdfonts.com/)), change the YAML files in a text editor of your choice (say, `subl`)

    ```sh
    subl $(dirname $(gem which colorls))/yaml
    ```

</br></br>
-->
<!--

# Custom configurations

[(Back to top)](#table-of-contents)

<!--
You can overwrite the existing icons and colors mapping by copying the yaml files from `$(dirname $(gem which colorls))/yaml` into `~/.config/colorls`, and changing them.

- To overwrite color mapping :

  Please have a look at the [list of supported color names](https://github.com/sickill/rainbow#color-list). You may also use a color hex code as long as it is quoted within the YAML file and prefaced with a `#` symbol.

  Let's say that you're using the dark color scheme and would like to change the color of untracked file (`??`) in the `--git-status` flag to yellow. Copy the defaut `dark_colors.yaml` and change it.

  ```sh
  cp $(dirname $(gem which colorls))/yaml/dark_colors.yaml ~/.config/colorls/dark_colors.yaml
  ```

  In the `~/.config/colorls/dark_colors.yaml` file, change the color set for `untracked` from `darkorange` to `yellow`, and save the change.

  ```
  untracked: yellow
  ```

  Or, using hex color codes:

  ```
  untracked: '#FFFF00'
  ```

- To overwrite icon mapping :

  Please have a look at the [list of supported icons](https://nerdfonts.com/). Let's say you want to add an icon for swift files. Copy the default `files.yaml` and change it.

  ```sh
  cp $(dirname $(gem which colorls))/yaml/files.yaml ~/.config/colorls/files.yaml`
  ```

  In the `~/.config/colorls/files.yaml` file, add a new icon / change an existing icon, and save the change.


  ```
  swift: "\uF179"
  ```

- User contributed alias configurations :

  - [@rjhilgefort](https://gist.github.com/rjhilgefort/51ea47dd91bcd90cd6d9b3b199188c16)


</br></br>

# Updating

[(Back to top)](#table-of-contents)

Want to update to the latest version of `chat_app`?

<!--
```sh
gem update colorls
```



</br></br>

# Uninstallation

[(Back to top)](#table-of-contents)

Want to uninstall and revert back to the old style? No issues (sob). Please feel free to open an issue regarding how we can enhance `chat_app`.

<!--
```sh
gem uninstall colorls
```


</br></br>

# Contributing

[(Back to top)](#table-of-contents)

Your contributions are always welcome! Please have a look at the [contribution guidelines](CONTRIBUTING.md) first. :tada:


</br>

# Future Scope
[(Back to top)](#table-of-contents)

Adding Voice chat app will make it more user friendly





-->
