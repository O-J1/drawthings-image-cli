import tomllib
import click
import dtcli.constants as constants
import dtcli.util.log as log
from dtcli.main import process_payload
from dtcli.util.picker import pick_model, image_size_picker


# Load parameters from dt_config.toml file
def load_params(filename=None):
    try:
        if filename is None:
            filename = constants.CONFIG_FILENAME

        with open(filename, "rb") as f:
            data = tomllib.load(f)
            log.success(f"Loaded syntactically valid {filename}")
        return data
    except FileNotFoundError:
        log.error(f"File {filename} not found")
        return {}

# Adjust eagerness so config callback can execute before url or model cb
def patch_parse_args(parser):
    orig_parse_args = parser.parse_args

    def parse_args(*args, **kwargs):
        opts, args, param_order = orig_parse_args(*args, **kwargs)
        param_order.sort(key=lambda p: -getattr(p, "eagerness", 0))
        return opts, args, param_order

    parser.parse_args = parse_args


class OrderableCommand(click.Command):
    def make_parser(self, ctx):
        p = super().make_parser(ctx)
        patch_parse_args(p)
        return p


class EOption(click.Option):
    def __init__(self, *args, eagerness=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.eagerness = eagerness

# Presents picker for model if user does not pass one in via CLI
def modelcb(ctx, opt, model):
    if ctx.get_parameter_source("model") == click.core.ParameterSource.DEFAULT and ctx.obj["options"]["manual_model_list"] != []:
        return pick_model(ctx.obj["final_url_output"], ctx.obj["options"]["manual_model_list"])
    else:
        return model

def imagesizecb(ctx, param, wh):
    if ctx.get_parameter_source("wh") != click.core.ParameterSource.DEFAULT:
        return wh
    else:
        mwh = image_size_picker()
        # print(mwh)
        return mwh

# Set values from TOML as a dict under ctx.obj
def configure(ctx, param, filename):
    if ctx.obj is None:
        ctx.obj = {}
    try:
        if ctx.get_parameter_source("filename") == click.core.ParameterSource.DEFAULT:
        
            # Pull in those from the options section
            ctx.obj["options"] = load_params()["options"]
            # Save the URL from the TOML file in the context object
            ctx.obj["toml_url"] = ctx.obj["options"].get("url")

        elif ctx.get_parameter_source("filename") == click.core.ParameterSource.COMMANDLINE:
            ctx.obj["options"] = load_params(filename)["options"]
            # Save the URL from the TOML file in the context object
            ctx.obj["toml_url"] = ctx.obj["options"].get("url")
        else:
            # Pull in those from the options section
            ctx.obj["options"] = load_params()["options"]
            # Save the URL from the TOML file in the context object
            ctx.obj["toml_url"] = ctx.obj["options"].get("url")
            print(ctx.obj['toml_url'])
    except FileNotFoundError:
        pass

def urlcb(ctx, param, url):
    print(url)
    if ctx.obj is None:
        ctx.obj = {}
    # If a URL is passed via the CLI, use it
    elif ctx.get_parameter_source("url") != click.core.ParameterSource.DEFAULT:
        ctx.obj["final_url_output"] = url
        return ctx.obj["final_url_output"]
    # If a URL is present in the TOML file and not blank, use it
    elif ctx.obj["toml_url"] != '':
        ctx.obj["final_url_output"] = ctx.obj["toml_url"]
        return ctx.obj["final_url_output"]
    else:
        ctx.obj["final_url_output"] = url
        return ctx.obj["final_url_output"]


@click.command(cls=OrderableCommand)
@click.option(
    "--config",
    "-c",
    type=click.Path(dir_okay=False),
    default=constants.CONFIG_FILENAME,
    callback=configure,
    is_eager=True,
    eagerness=2,
    expose_value=False,
    help="Read option defaults from the specified dt_config.toml file (or the one in directory)",
    show_default=True,
    cls=EOption,
)
@click.option("-u",
    "--url",
    help="Which model to generate images on",
    default=constants.CONFIG_TEMPLATE["options"]["url"],
    type=str,
    callback=urlcb,
    is_eager=True,
    eagerness=1,
    cls=EOption,
)
@click.option('-p','--prompt', type=str, help='Prompt', required=True, default=constants.CONFIG_TEMPLATE["options"]["prompt"])
@click.option('-n','--negative_prompt', type=str, help='Negative prompt', required=False, default=constants.CONFIG_TEMPLATE["options"]["negative_prompt"])
@click.option('-s','--steps', type=click.IntRange(5, 150, clamp=True), help='No. of steps to take when generatring', required=False, default=constants.CONFIG_TEMPLATE["options"]["steps"])
@click.option('--seed', type=int, default=constants.CONFIG_TEMPLATE["options"]["seed"], help='Noise seed', required=False)
@click.option('--sampler', type=str, default=constants.CONFIG_TEMPLATE["options"]["sampler"], help='Sampler for generating the noise offset', required=False)
@click.option('-bsize','--batch_size', type=click.IntRange(1, 4, clamp=True), default=constants.CONFIG_TEMPLATE["options"]["batch_size"], help='Batch size', required=False)
@click.option('-bcount','--batch_count', type=click.IntRange(1, 100, clamp=True), default=constants.CONFIG_TEMPLATE["options"]["batch_count"], help='Batch count', required=False)
@click.option('-guide','--guidance_scale', '-cfg', type=click.IntRange(1, 25, clamp=True), default=constants.CONFIG_TEMPLATE["options"]["guidance_scale"], help='Guidance scale for how literally prompt is taken', required=False)
@click.option('-hrf','--hires_fix', type=bool, default=constants.CONFIG_TEMPLATE["options"]["hires_fix"], help='Hi-res fix', required=False)
@click.option(
    '--wh', 
    type=(click.IntRange(128, 2048, clamp=True), click.IntRange(128, 2048, clamp=True)),
    callback=imagesizecb,
    default=(512, 512), 
    help='Image width and height',
    required=False)
@click.option(
    "-m",
    "--model",
    help="Which model to generate images on",
    type=str,
    callback=modelcb,
    default=constants.CONFIG_TEMPLATE["options"]["default_model_list"][0],
)

def cli(**kwargs):
    """Process CLI input and run payload function"""
    print(kwargs)
    process_payload(**kwargs)

if __name__ == '__main__':
    cli()
