// Generate groups info to be downloaded
async function generateGroupsInfo() {
    let jsonObj = {};
    const groups = WAPI.getAllGroups();
    const getParticipantsIDs = groups.map((group) => WAPI.getGroupParticipantIDs(group.id));
    const allParticipantsIDs = await Promise.all(getParticipantsIDs);
    console.log(groups.length, allParticipantsIDs.length);
    groups.forEach((group, index) => {
        let groupObj = {};
        groupObj["group_name"] = group.name;
        groupObj["participants"] = allParticipantsIDs[index].map(p => p.user);
        jsonObj[group.id._serialized] = groupObj;
    });
    return jsonObj;
}

// Generate contacts info to be downloaded
async function getContactsInfo() {
    const contacts = WAPI.getMyContacts();
    let jsonObj = {};

    for (const contact of contacts) {
        jsonObj[contact.id.user] = contact.name;
    }

    return jsonObj;
}

// Download given content as file with filename
function download(content, fileName, contentType) {
    var a = document.createElement("a");
    var file = new Blob([content], { type: contentType });
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
}

// The scraper's main function
async function run() {
    console.log("Downloading contacts...");
    const contacts = await getContactsInfo();
    console.log(contacts);
    download(JSON.stringify(contacts, null, 4), 'contacts.json', 'application/json');

    console.log("Generating JSON...");
    const data = await generateGroupsInfo();
    console.log(data);
    download(JSON.stringify(data, null, 4), 'data.json', 'application/json');

}

run().then(() => console.log("Downloaded all info!"));