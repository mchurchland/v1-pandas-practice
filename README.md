# V1 Pandas Practice

Six small pandas quests using **real mouse V1 calcium traces** and paired spike
events. The data is already in this repository (about 550 KB), so a fresh clone
can start without downloading a research archive or running a simulation.

## Start in one go

You need [Conda](https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html).
From this repository's directory, run:

```bash
./start.sh
```

The script creates the `v1-pandas-practice` conda environment on first use,
installs this package, and displays the quests. No GPU is required. Then:

```bash
./start.sh data            # peek at the observations
# edit practice.py         # fill in the six functions
./start.sh check           # get a score and hints
./start.sh check spikes_by_cell  # check just one quest
```

The first launch needs an internet connection for Conda packages. Later runs
use the local environment and the bundled data. If you already have pandas
installed, you can also use `pip install -e .` and
`python -m v1_pandas_practice`.

## Your quest book

Edit [practice.py](practice.py). Its six functions teach filtering, grouping,
sorting, time bins, rolling windows, and conditional summaries. The checker
compares your returned pandas objects with reference results and gives a hint
for each unfinished quest. For example, after implementing `spikes_by_cell`,
run `./start.sh check spikes_by_cell` to see your progress.

You can also explore in a notebook or Python shell:

```python
from v1_pandas_practice import load_traces

traces = load_traces()
print(traces.head())
```

## What is in the CSV?

[`src/v1_pandas_practice/data/v1_calcium_traces.csv`](src/v1_pandas_practice/data/v1_calcium_traces.csv)
contains 3,600 consecutive frames (about 60 seconds) from the first segment
of each of four V1 cells. Each row is one fluorescence frame for one cell:

| Column | Meaning |
| --- | --- |
| `cell_id` | Source cell label; these recordings do not specify an inhibitory subtype |
| `frame` | Zero-based frame within the selected segment |
| `time_s` | Fluorescence frame time, in seconds |
| `dff` | Recorded fractional fluorescence change (ΔF/F) |
| `spike_count` | Simultaneously recorded spikes assigned to this frame |

`spike_count` is formed by binning `events_AP / 10,000` between fluorescence
frame midpoints, following the upstream CascadeTorch loader. The CSV rounds
times and fluorescence values to nine decimal places. These are measured V1
calcium/ephys observations, not GLIF simulation output, and they have no
locomotion or stimulus labels. The four cells make a compact practice sample;
the exercises are descriptive and should not be treated as population results.

## Data provenance and license

The excerpt comes from the public
[CascadeTorch ground-truth dataset](https://github.com/PTRRupprecht/CascadeTorch/tree/a2c6130375f199345e2d1f3985609444cd312ecd/Ground_truth/DS09-GCaMP6f-m-V1)
at commit `a2c6130375f199345e2d1f3985609444cd312ecd`. Source files are
`CAttached_Chen2013_GC6f_cell1_mini.mat`,
`CAttached_Chen2013_GC6f_cell4C_mini.mat`,
`CAttached_Chen2013_GC6f_cell5C_mini.mat`, and
`CAttached_Chen2013_GC6f_cell7C_full_mini.mat` in that directory.
The source repository identifies its license as GPL-3.0; this derived excerpt
and this practice package are distributed under the same license, copied in
[LICENSE](LICENSE). The original MATLAB files are not bundled here.

To rebuild the CSV from a CascadeTorch checkout:

```bash
python3 -m pip install 'scipy>=1.11' numpy
python3 scripts/build_dataset.py --source-dir /path/to/CascadeTorch/Ground_truth
```
