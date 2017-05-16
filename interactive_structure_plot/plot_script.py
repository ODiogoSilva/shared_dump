#!/usr/bin/python

from plotly.offline import iplot, init_notebook_mode
import plotly.graph_objs as go
import numpy as np

# You don't need this next line. It's just to display plots in the notebook
init_notebook_mode(connected=True)

# You can import the file directly from the web or download it and import as a local file
qvals = np.genfromtxt("https://github.com/ODiogoSilva/shared_dump/raw/master/interactive_structure_plot/HvFullSample_ingroup_v1_MM50_mafRandSNP.5.meanQ")

indarray = np.genfromtxt("https://github.com/ODiogoSilva/shared_dump/raw/master/interactive_structure_plot/indfile.txt",
                         dtype="|U20")

index = indarray[:, 1]
index_array = np.c_[index, qvals]
sorted_qvals = index_array[index_array[:, 0].argsort()]
sorted_qvals = sorted_qvals[:,1:].astype(np.float64)
sorted_qvals_transposed = sorted_qvals.T
sorted_indarray = indarray[indarray[:,1].argsort()]
sorted_individuals = sorted_indarray[:,0]

from collections import OrderedDict, Counter

# Get sorted unique list of populations
# E.g.: ['Pop1', 'Pop2', 'Pop3', 'Pop4']
pops = sorted(list(OrderedDict.fromkeys(indarray[:, 1])))

# Get cumulative sums of individuals in each population
# E.g.: [ 72  81  91 101]
# Meaning that the first population has 72 individuals, the second has 9, etc.
pop_sums = np.cumsum([np.count_nonzero(indarray == x)
                                      for x in pops])

# Get the number of individuals in each population
pop_counts = Counter(indarray[:, 1])

# Create list with the ranges for each population
pop_ranges = []
# Create list with the xpos of each population label
pop_xpos = []
for counter, pop in enumerate(pops):
    pop_ranges.append((pop_sums[counter] - pop_counts[pop], pop_sums[counter]))
    pop_xpos.append(pop_sums[counter] - pop_counts[pop] / 2)
    
import colorlover as cl

data = []

# Create color pallete for 12 colors
# More color pallets available on https://plot.ly/ipython-notebooks/color-scales/
cp = cl.scales["12"]["qual"]["Set3"]

for k, ar in enumerate(sorted_qvals_transposed):
    
    current_bar = go.Bar(
        x = sorted_individuals,
        y = ar,
        name = "K {}".format(k),
        text=["Assignment: {}%".format(x * 100) for x in ar],
        marker = dict(
            color=cp[k],
            line=dict(
                color="grey",
                width=1,
            )
        )
    )
    
    data.append(current_bar)

number_individuals = len(sorted_individuals)

shape_list = [
    {"type": "line", "x0": - .5, "y0": 0,
     "x1": number_individuals - .5, "y1": 0,
     "line": {"width": 2}},
    {"type": "line", "x0": - .5, "y0": 0, "x1": -.5, "y1": 1,
     "line": {"width": 3}},
    {"type": "line", "x0": - .5, "y0": 1,
     "x1": number_individuals - .5, "y1": 1,
     "line": {"width": 3}},
    {"type": "line", "x0": number_individuals -.5, "y0": 0,
     "x1": number_individuals - .5, "y1": 1,
     "line": {"width": 3}}
]

pop_lines = list(
    OrderedDict.fromkeys([x for y in pop_ranges for x in y]))[1:-1]
for xpos in pop_lines:
    shape_list.append(
         {"type": "line",
          "x0": xpos - .5,
          "y0": 0,
          "x1": xpos - .5,
          "y1": 1,
          "line": {"width":3}}
    )
    
layout = go.Layout(
    title="Interactive structure plot",
    barmode='stack',
    margin={"t":40},
    bargap="0",
    shapes=shape_list,
    legend={"x":1, "y":0.5},
    yaxis={
        "showticklabels":False
    },
    xaxis={
        # Disable the xticks with individual names
        "ticks": "",
        "showticklabels": True,
        # Provide your custom tick labels
        "ticktext": pops,
        # And their positions
        "tickvals": pop_xpos,
        "tickangle":-45,
        "tickfont": dict(size=22,
                        color="black")
    }
)


fig = go.Figure(data=data, layout=layout)

iplot(fig)