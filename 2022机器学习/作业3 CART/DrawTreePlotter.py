import treePlotter

def NT_To_DD(NameList, NameTuple):
    DDict = {}
    for i in NameList[::-1]:
        Dict = {}
        if not DDict:
            if i.branch != "无分支":
                Dict[i.node] = {i.branch: NameTuple[0],
                                 "other": NameTuple[1]}
            else:
                Dict[i.node] = {NameTuple[1]: "NULL"}
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
