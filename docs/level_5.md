# Level 5

Our start on final level 5 differs a bit to the previous levels.
Before we used our previous implementations to extend the behavior.
Now we would like to start with a scaffholding and implement our previous learnings.

## Goal

Our goal is to have a working tipi pipeline by utelizing the scaffholding of the package.
Our currently still very script like approach will be transformed into custom `permanences` and
`pipeline_processes`.

## Before / After

{{ previous }}

{{ after }}

## Tasks

1. Create from template
2. Get familiar with the structure
3. Transfer `level_4`
4. Add Pipeline
5. Run Pipeline

### Create from Template

To create a new pipeline project we utelize the cli of `tipi`.

> Execute
>
> ```bash
> uv run tipi --help
> ```
>
> To get a hint what commands the cli provides

To create a new pipeline with the cli as `level_5` enter:

```bash
#                 project name    template    description
#           command    |  location   |            |
#             |        |     |       |            |
#             v		   v     v       v            v
uv run tipi create level_5 -l . -e full -d "Tutorial Level 5"
```

This command will create the example code from template and prints the structure to terminal.

### Get familiar with the strcuture

> Currently, the template is based on a deprecated version of tipi (1.2.4)
> It includes some deperecated informations about WandB Logger.
> This isn't an issue to complete level_5

It is the main idea of a tipi pipeline to seperate parts which are constant available trough 
the process and parts which actually execute something.

Inside the project folder the package `level_5` provides modules for each of them.

A Permanence needs always implement:

- `cleanup`

A Process needs always implement:

- `execute`
- `skip`

> If you like you can now skip [Transfer `level_4`](#transfer-level_4) and test the template by following the steps of
> [Add Pipeline](#add-pipeline) and [Run Pipeline](#run-pipeline)

The central part which glues both together is the `configs/pipeline_config.py`.

It does not only provides the config options of the core permanences and processes,
it is also the place to configure the pipelines own permanences and processes.

The currently provided and configured tipi permanences and processes are dummy implementations.
They execute, but doesn't provide any meaningful purpose, only an idea what could be implemented
as each other.

### Transfer `level_4`

We start with the datasets.
Instead of splitting them we change the implementation of allready provided `DataPermanence`.
We utelize a python trick with `getattr` to make a few decision dynamic to load them from 
the config file.

Following parameters needs to be provided via config and this new permanence:

- root
- data_set
- transform
- download
- prevent_deletion

> We can now execute the pipeline again if we did before, and check if it fails with:
>
> ```bash
> Error: 'DataPermanence' object has no attribute 'get_data'
> Caused by: AttributeError: 'DataPermanence' object has no attribute 'get_data'
> ```
>
> This demonstrates that the tipi [`builder`](https://github.com/tensorimgpipeline/TensorImgPipeline/blob/main/tipi/core/builder.py) was able to create an object of `DataPermanence`.


### Add Pipeline

Instead of running our implementations directly we utilize `tipi` itself.
`Tipi` provides the user with a central location to execute our pipelines from everywhere.

By default the locations is `~/.config/tipi/` which is split into `projects` and `configs` and
symbolic links our configs and projects directly.

to add our `level_5` to this place, we simply run:

```bash
uv run tipi add level_5
```

If we would like to get all added projects we can run:

```bash
uv run tipi list
```

### Run Pipeline

If we added our project as desribed before the only thing left to do:

```bash
uv run tipi run level_5
```

## Result

{{ results }}

## Troubleshooting

If you had issues to recreate this level, please provide informations via [troubleshoot form](https://github.com/tensorimgpipeline/Tutorial/issues/new?template=LEVEL_TROUBLESHOOT.yml)

{{ troubleshooting }}
