const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');

const client = new Client({
    authStrategy: new LocalAuth()
});


client.on('qr', qr => {
    qrcode.generate(qr, {small: true});
});

client.on('ready', async () => {
    console.log('Client is ready!');

    // Get all contacts
    const contacts = (await client.getContacts()).filter(contact => contact.isMyContact);

    // Create a JSON object with all contacts mapped by their ID
    const contactsMap = contacts.reduce((acc, contact) => {
        acc[contact.id.user] = contact.name;
        return acc;
    }, {});

    // Write the JSON object to a file
    fs.writeFileSync('contacts.json', JSON.stringify(contactsMap, null, 2));
    console.log("Saved contacts info to contacts.json");

    const chats = await client.getChats();

    // Filter only group chats
    const groups = chats.filter(chat => chat.isGroup);


    // Get all participants in each group
    const groups_info = {};
    await Promise.all(groups.map(async group => {
        groups_info[group.id._serialized] = {
            group_name: group.name,
            participants: group.participants.map(participant => participant.id.user),
            admins: group.participants.filter(participant => participant.isAdmin).map(participant => participant.id.user)
        };
    }));

    // Save the groups info to a file
    fs.writeFileSync('groups.json', JSON.stringify(groups_info, null, 2));
    console.log("Saved groups info to groups.json");

    // End the session
    await client.destroy();
});

client.initialize();
