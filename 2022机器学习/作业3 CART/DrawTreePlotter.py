import treePlotter

def NT_To_DD(NameList, NameTuple):
    DDict = {}
    for i in NameList:
        Dict = {}
        if not DDict:
            Dict[i.node] = {i.branch: NameTuple[0],
                             "other": NameTuple[1]}
            DDict = Dict
        else:
            Dict[i.node] = {i.branch: NameTuple[0],
                             "other": DDict}
            DDict = Dict
    return DDict

def DrawIT(GET):
    DDICT = NT_To_DD(GET[0], GET[1])
    treePlotter.createPlot(DDICT)

if __name__ == "__main__":
    pass