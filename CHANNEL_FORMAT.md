# Channel Message Format Example

When a user submits a project, the channel will receive:

## 1. Forwarded File
```
📄 essay.pdf
or
🎵 song.mp3
or  
🖼️ artwork.jpg
etc.
```

## 2. Reply with User Data (formatted)
```
📋 Ishtirokchi ma'lumotlari:

👤 Ism: Aliyev Vali Akramovich
📍 Viloyat: Toshkent shahri
🏘 Tuman: Chilonzor tumani
🏘 Mahalla: Yangi hayot mahallasi
🏢 Ish joyi: Toshkent davlat universiteti
📅 Tug'ilgan sana: 01.01.2000
🆔 Pasport: AD1654502
📱 Telefon: +998991234567
🎨 Loyiha turi: ✍️ Maqola yoki esse
```

## Message URL Structure
```
https://t.me/your_channel/123
             └─ channel   └─ message_id
```

This URL is saved to `projects.project_url` in the database.

## Channel Setup Checklist

- [ ] Create a public or private channel
- [ ] Add bot as admin
- [ ] Give bot permission to post messages
- [ ] Copy channel username (with @)
- [ ] Add to .env: `CHANNEL_ID=@your_channel`
- [ ] Test by submitting a project

## Benefits of This Structure

✅ **Organized** - All submissions in one place
✅ **Linked** - User data attached to each submission
✅ **Trackable** - URL for each submission
✅ **Reviewable** - Easy for judges to review
✅ **Archivable** - Permanent record in channel
✅ **Searchable** - Can search by name, passport, etc.

## For Private Channels

If your channel is private, the bot can still forward messages there.
However, the URLs will only work for people who have access to the channel.

Format for private channels:
```
https://t.me/c/1234567890/123
           └─ channel_id └─ message_id
```

Note: You may need to adjust the URL generation logic if using a private channel.
