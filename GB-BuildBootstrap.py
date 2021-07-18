import sublime, sublime_plugin, string, random
from datetime import date
today = date.today()

# Define HTML code snippets
snippets = {
    "Accordion":
        {
        "Start": '\n<div class="clearfix container-fluid"></div>\n<!-- Start of Accordion, ID = {r}, date = {t} --> <div class="accordion" id="accordion-{r}">',
        "Repeat": '\n\n<!-- Start of Item {i} --> <div class="card"> <div class="card-header" id="heading-{i}-{r}"> <h5 class="mb-0"> <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse-{i}-{r}" aria-expanded="false" aria-controls="collapse-{i}-{r}"> {a} </button> </h5> </div> <div id="collapse-{i}-{r}" class="collapse" aria-labelledby="heading-{i}-{r}" data-parent="#accordion-{r}"> <div class="card-body">{b}</div> </div> </div> \n<!-- End of Item {i} --> ',
        "End": '</div> \n<!-- End of Accordion, ID = {r}, date = {t} --> \n\n'
        },
    "V-tabs":
    {
        "Start": '\n<div class="clearfix container-fluid"></div>\n<!-- Start of Vertical tabs, ID = {r}, date = {t} --> <div class="row"> <div class="col-3 no-gutters">',
        "Nav-Start": '<div class="nav flex-column nav-pills" id="vtabs-{r}" role="tablist" aria-orientation="vertical">',
        "Nav-Repeat": '<a class="nav-link{c}" id="vtabs-{i}-{r}-tab" data-toggle="pill" href="#vtabs-{i}-{r}" role="tab" aria-controls="vtabs-{i}-{r}" aria-selected="{f}">{a}</a>',
        "Nav-End": '</div> </div> <div class="col-9 no-gutters"> <div class="tab-content" id="v-tabs-tabContent">',
        "Repeat": '\n\n<!-- Start of Item {i} --> <div class="tab-pane card p-3 fade{c}" id="vtabs-{i}-{r}" role="tabpanel" aria-labelledby="vtabs-{i}-{r}"> <h4>{a}</h4> {b} </div> \n<!-- End of Item {i} --> ',
        "End": '</div> </div> </div> \n<!-- End of Vertical tabs, ID = {r}, date = {t} --> \n\n'
    },
    "H-tabs":
    {
        "Start": '\n<div class="clearfix container-fluid"></div>\n<!-- Start of Horizontal tabs, ID = {r}, date = {t} -->',
        "Nav-Start": '<ul class="nav nav-pills mb-0" id="htabs-{r}" role="tablist">',
        "Nav-Repeat": '<li class="nav-item"><a class="nav-link{c}" id="htabs-{i}-{r}-tab" data-toggle="pill" href="#htabs-{i}-{r}" role="tab" aria-controls="htabs-{i}-{r}" aria-selected="{f}">{a}</a></li>',
        "Nav-End": '</ul><div class="tab-content card" id="pills-tabContent">',
        "Repeat": '\n\n<!-- Start of Item {i} --> <div class="tab-pane p-3 fade{c}" id="htabs-{i}-{r}" role="tabpanel" aria-labelledby="htabs-{i}-{r}"> <h4>{a}</h4> {b} </div> \n<!-- End of Item {i} --> ',
        "End": '</div> \n<!-- End of Horizontal tabs, ID = {r}, date = {t} --> \n\n'
    },
    "Cards":
    {
        "Start": '\n<div class="clearfix container-fluid"></div>\n<!-- Start of Card Group, ID = {r}, date = {t} --> <div class="card-group">',
        "Repeat": '\n\n<!-- Start of card {i} --> <div class="card"> <div class="card-header"> <h5>{a}</h5> </div> <div class="card-body">{b}</div> </div> \n<!-- End of card {i} --> ',
        "End": '</div> \n<!-- End of Card Group, ID = {r}, date = {t} -->\n\n'
    },
    "Deck":
    {
        "Start": '\n<div class="clearfix container-fluid"></div>\n<!-- Start of Card Deck, ID = {r}, date = {t} --> <div class="card-deck">',
        "Repeat": '\n\n<!-- Start of card {i} --> <div class="card"> <div class="card-header"> <h5>{a}</h5> </div> <div class="card-body">{b}</div> </div> \n<!-- End of card {i} --> ',
        "End": '</div> \n<!-- End of Card Deck, ID = {r}, date = {t} -->\n\n'
    },
    "Rainbow":
    {
        "Start": '\n<div class="clearfix container-fluid"></div>\n<!-- Start of Rainbow Card Deck, ID = {r}, date = {t} --> <div class="card-deck">',
        "Repeat": '\n\n<!-- Start of card {i} --> <div class="card text-white {c}> <div class="card-header"> <h5 class="text-white">{a}</h5> </div> <div class="card-body">{b}</div> </div> \n<!-- End of card {i} --> ',
        "End": '</div> \n<!-- End of Rainbow Card Deck, ID = {r}, date = {t} -->\n\n'
    },
    "Columns":
    {
        "Start": '\n<div class="clearfix container-fluid"></div>\n<!-- Start of Card Column, ID = {r}, date = {t} --> <div class="card-columns">',
        "Repeat": '\n\n<!-- Start of card {i} --> <div class="card"> <div class="card-header"> <h5>{a}</h5> </div> <div class="card-body">{b}</div> </div> \n<!-- End of card {i} --> ',
        "End": '</div> \n<!-- End of Card Column, ID = {r}, date = {t} -->\n\n'
    },
    "Show":
    {
        "Start": '\n\n<!-- Start of Show/Hide interface, ID = {r}, date = {t} -->',
        "Repeat": '<p> <a class="btn btn-primary" data-toggle="collapse" href="#show-{r}" role="button" aria-expanded="false" aria-controls="show-{r}"> More - {a} </a> </p>\n<div class="collapse" id="show-{r}"> <div class="card card-body"><h5>{a}</h5>\n{b} <small><a class="btn-block btn btn-sm btn-light" class="text-center" data-toggle="collapse" href="#show-{r}" role="button" aria-expanded="false" aria-controls="show-{r}">Hide</a></small> </div> </div>',
        "End": ' \n<!-- End of Show/Hide interface, ID = {r}, date = {t} -->\n\n'
    }
}

colours = ('bg-primary', 'bg-secondary', 'bg-success', 'bg-danger', 'bg-info', 'bg-light', 'bg-warning', 'bg-dark')

class BuildBootstrapCommand(sublime_plugin.TextCommand):
    def run(self, edit, type):
        view = self.view
        for region in view.sel():
            if not region.empty():
                s = view.substr(region) # string of selected region
                t = bs_parser(s,type) # send string to parser
                view.replace(edit, region, t) # Update page content
                # self.view.run_command("select_all")
                # self.view.run_command("htmlprettify")
                # self.view.sel().clear()

def bs_parser(string, type):
    items = string.split('<h5>')
    # if I chose cards or deck and there are more than 3 cards, change to column view
    if (type == "Cards" or type == "Deck") and len(items) > 4:
        type = 'Columns'
    new_str = items[0] # Content prior to first <h5>
    # Create random ID
    r = random_key(6)
    # loop thorough items (as defind by <h5>)
    for idx, item in enumerate(items):
        i = str (idx)
        if idx == 0:
            # Built starting BS HTML
            new_str += snippets[type]['Start'].format(r=r,t=today)
            # If I have top level nav (V-tabs or H-tabs)
            if "Nav-Start" in snippets[type].keys():
                new_str += snippets[type]['Nav-Start'].format(r=r)
                for idx, item in enumerate(items):
                    i = str (idx)
                    c = ''
                    f = 'false'
                    sub_items = item.split('</h5>')
                    if idx == 1: # If I'm the first item
                        c = ' active show'
                        f = 'true'
                    if idx > 0:
                        new_str += snippets[type]['Nav-Repeat'].format(r=r, i=i, a=sub_items[0], f=f,c=c)
                new_str += snippets[type]['Nav-End'].format(r=r)
        else:
            # Build repeating items
            sub_items = item.split('</h5>')
            c = ''
            if idx == 1: # If I'm the first item
                c = ' active show'
            # rainbow items
            if type == 'Rainbow':
                print("type: ", type)
                n = idx%len(colours) - 1
                print("n: ", n)
                colour = colours[n]
                print("colour: ", colour)

            new_str += snippets[type]['Repeat'].format(r=r, i=i, a=sub_items[0], b=sub_items[1], c=c)
    new_str += snippets[type]['End'].format(r=r,t=today)
    return new_str

def random_key(length):
    key = ''
    for i in range(length):
        key += random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
    return key