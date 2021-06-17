const discord = require("discord.js");
const ytdl = require("ytdl-core");
const fs = require("fs");

const bot = new discord.Client();

bot.on("ready", () => {
    const guild = bot.guilds.cache.get("832594030264975420");
    const channel = guild.channels.cache.get("832677639944667186");
    
    channel.send("JS Earth is ready and running on discord.js v12.5.3!")
});

bot.on("message", async message => {
    if (!message.guild) return;

    if (message.content === "e.join") {
        if (message.member.voice.channel) {
            await message.member.voice.channel.join()
        } else {
            message.channel.send("<:No:833293106198872094> Join a Voice Channel first.")
        }
    };
    
    if (message.content.startsWith("e.play")) {
        const url = message.content.split(" ")[1];
        if (ytdl.validateURL(url)) {
            if (message.member.voice.channel) {
                const connection = message.member.voice.channel.join();
                connection.play(ytdl.ytdl(url, {filter: "audioonly"}));
    
                const e = new discord.MessageEmbed()
                    .setTitle("Now Playing")
                    .setColor(0x00a8ff)
                    .setAuthor("Earth", "https://this.is-for.me/i/gxe1.png")
                    .setThumbnail(ytdl.getInfo(url).thumbnail.url)
                    .addField("Title", ytdl.getInfo(url).title)
                    .addField("Length in Seconds", ytdl.getInfo(url).lengthSeconds)
                    .setFooter("Earth by Earth Development", "https://this.is-for.me/i/gxe1.png");
                message.channel.send({embed: e})
            } else {
                message.channel.send("<:No:833293106198872094> Join a Voice Channel first.")
            }
        } else {
            message.channel.send("<:No:833293106198872094> This command currently only works with YouTube URLs. This doesn't appear to be a valid YouTube URL.")
        }
    }
});

const tokenfile = fs.readFileSync("./token.json")
const token = JSON.parse(tokenfile);
bot.login(token.token)