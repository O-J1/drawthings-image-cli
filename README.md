# DrawThings Image CLI

The DrawThings Image CLI (*dtcli*) is a command-line tool that is used to generate images on devices running the Mac and IOS app [DrawThings](https://apps.apple.com/us/app/draw-things-ai-generation/id6444050820). 

This tool is built using Python and the Click library, making it easy to use and configure. This was my first real Python project so there may be some lumps 😆

## Installation

To install the DrawThings Image CLI  you have 2 options, follow these steps:

### Option 1
1. Clone this repository to your local machine.
2. Install poetry [(refer to their documentation)](https://python-poetry.org/docs/#installation)
2. Navigate to the project directory and open the terminal at said location:
3. Install the required dependencies using the followping:

   ```
   poetry install
   ```
### Option 2 
1. Install `pipx` [via their simple documentation](https://github.com/pypa/pipx#on-windows-install-via-pip-requires-pip-190-or-later)
2. Run `pipx install git+https://github.com/O-J1/drawthings-image-cli.git`
3. If everything goes well you will see:

    `These apps are now globally available — dtcli.exe done! ✨ 🌟 ✨`

This means that dtcli is now a proper command line tool that you can use independently of Poetry and is isnt polluting your global python install thanks to pipx!

## Usage

The DrawThings Image CLI provides just one command and many optional "options" for generating images. Here's how you can use it:

### Basic Command

To generate an image using default settings, run the following command:

```
poetry run dtcli
```

P.S Please note that this project will output into a folder named "DrawThings Output" that is under the current working directory that the CLI command is executed at.

The order of priority for options are as follows:

`CLI inputs > dt_config.toml > default values from constants.py`

### Options

You can customize the image generation process using various options:

- `-u`, `--url`: Specify the target device URL for image generation.
- `-p`, `--prompt`: Set the prompt for the image generation.
- `-n`, `--negative_prompt`: Specify the negative prompt for the image generation.
- `-m`,`--model`: Specify what diffusion model to use, you may use the file name or the display name seen in the app


For example:

```
poetry run dtcli --url "192.168.1.100:7860" --prompt "landscape, fantasy" -n "low quality, worst quality, monochrome"
```

Poetry run can be excluded if you went with option 2 for install.

### Advanced Commands

The DrawThings Image CLI provides more advanced commands:

- `-c`,`--config`: If you choose to not use the .toml created in the current working directory you may specify a path
- `-s`, `--steps`: Adjust the steps, however it already uses the reccomended value of 30, in the large majority of cases there should be no need to adjust
- `--seed`: Set the seed for noise generation, defaults to random
- `--sampler`: Adjust the sampler. Consider using only Euler a, DPM++ 2M Karras and DPM++ SDE Karras with the latter needing only 20 steps. Defaults to Euler A
- `-bsize`, `--batch_size`: Adjusts the concurrent image generation (max of 4)
- `-bcount`, `--batch_count`: Adjusts the consecutive image generation, think of it like a loop (max of 100)

### Configuration

You can configure default options by edit the `dt_config.toml` file created in the current working directory or manually creating it somewhere on your PC and passing the path via `-c` or `--config`. Here's an example of the contents:

```[options]
url = "http://192.168.1.100:7860"
timeout = 120
prompt = "(limited palette blue black:1.1), creative (command line interface CLI:1.3) connected to a (blue magical tesseract glowing cube:1.2), no humans"
negative_prompt = "human, man, woman, child, simple background, (low quality, worst quality, normal quality:1.4), hand"
seed = -1
steps = 30
sampler = "Euler a"
batch_size = 1
batch_count = 1
guidance_scale = 7
hires_fix = false
default_model_list = [
    "Generic (Stable Diffusion v1.5)",
    "SDXL Base (v1.0)",
]
manual_model_list = []
```

You can read more about TOML syntax here: https://toml.io/en/ 

Its a good middle ground between INI and JSON.

## Contributing

Contributions to this project are welcome! If you find issues or have improvements, feel free to create a pull request.

## License

This project is licensed under [AGPL_V3](https://www.gnu.org/licenses/agpl-3.0.en.html).

## Acknowledgments

This project interfaces with [DrawThings](https://example.com/drawthings) for remote image generation. We are just a shell/client for this great tool.

Special thanks to the following individuals:
- Inspiriation from Bob K's edit of the A111 API script
- Scyren for assistance for providing me with some good hints on resolving some of moderate callback issues
- Huge thanks to L3viathan who without their help I couldnt have easily patched the arg parser for click
- Tachyondecay for pointing me in the right direction for click documentation
- Liu Liu for the work on the DrawThings app. Read more about some of the work he has done @ https://engineering.drawthings.ai/
- Clarityai engeering for their guide on using poetry + pipx to create a CLI tool @ https://medium.com/clarityai-engineering/how-to-create-and-distribute-a-minimalist-cli-tool-with-python-poetry-click-and-pipx-c0580af4c026

