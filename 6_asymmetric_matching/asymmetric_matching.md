# Asymmetric matching, with pre-rendered stimuli

## Overview
```mermaid
graph LR;
    setup --> next_block --> run_block
    next_block <--> incomplete_blocks <--> incomplete_trials
    next_block <--> generate_design

    run_block <--> run_trial
    run_trial <--> define
    run_trial <--> field
    run_trial --> display --> capture --> adjust --> run_trial
    run_trial --> save_trial
    run_block --> exit

    generate_design <--> generate_block

    subgraph data_management.py
        incomplete_blocks
        incomplete_trials

        next_block

        save_trial
    end

    subgraph design.py
        generate_design
        generate_block
    end


    subgraph HRL
        display
        capture[capture participant response]
    end

    subgraph stimuli.py
        define[load stimulus]
    end



    subgraph asymmetric_matching.py
        field[matching field]
    end

    subgraph experiment_logic.py
        run_trial
    end

    subgraph adjustment.py
        adjust[adjust matching field value]
    end

    subgraph run_experiment.py
        setup

        run_block

        exit[cleanup & exit]
    end

```

## Installation
This demo uses:
- [pandas](https://pandas.pydata.org/), to manage data
- [Pillow (PIL)](https://pillow.readthedocs.io/en/stable/), for text and image(loading)
- [HRL](https://github.com/computational-psychology/hrl)

```bash
python -m pip install pandas, Pillow
python -m pip install https://github.com/computational-psychology/hrl/archive/master.zip
```