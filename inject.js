async function generateGroupsInfo() {
    const groups = WAPI.getAllGroups();
    let jsonObj = {};
    for (group of groups)
    {
        let groupObj = {};
        let participants = await WAPI.getGroupParticipantIDs(group.id);
        
        groupObj["group_name"] = group.name;
        groupObj["participants"] = participants.map(p => p.user);

        jsonObj[group.id._serialized] = groupObj;
    }

    return jsonObj;
}

function download(content, fileName, contentType) {
    var a = document.createElement("a");
    var file = new Blob([content], {type: contentType});
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
}

async function run()
{
    console.log("Generating JSON...");
    const data = await generateGroupsInfo();
    console.log(data);
    download(JSON.stringify(data, null, 4), 'data.json', 'application/json');
    
}

run().then(() => console.log("Generated JSON!"));