# Table of Contents

1. [Overview](#org2d0cc27)
2. [Installation](#orgf5b5fca)
   1. [Docker Install](#org799d599)
   2. [Installation On Unraid](#org7baa9c1)
3. [Commands](#orgacd88a9)



# Overview

This is a simple Discord bot that sends a daily devotional message to a designated channel. It is built using Python, Docker, and the discord.py library. The bot allows users to set a channel for automatic devotional messages and also provides a manual command to retrieve the day's devotional. This bot can be self-hosted on an Unraid server or any machine with Docker support. I manually compiled all the quotes for each day of the year. I made this from a Classical Protestant perspective so you'll see anyone from St. Ephraim to a Puritan like Thomas Watson and so forth.



# Installation



## Docker Install

1. Pull the Docker image:

   ```
   docker pull sticio/evotional-bot:latest
   ```

2. Run the bot with your token:

   ```
   docker run -e DISCORD_TOKEN="your-token-here" sticio/evotional-bot:latest
   ```



## Installation On Unraid

1. Open the **Unraid Web UI**.
2. Go to the **Docker** tab and click **Add Container**.
3. Set the **Repository** to: `sticio/devotion-bot:latest`
4. Under **Environment Variables**, add:
   - **Key**: `DISCORD_TOKEN`
   - **Value**: `your-bot-token-here`
5. Click **Apply** and start the container.



# Commands

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Command</th>
<th scope="col" class="org-left">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-left">!setchannel</td>
<td class="org-left">Sets the channel for daily devotion quotes</td>
</tr>

<tr>
<td class="org-left">!devotional</td>
<td class="org-left">Manually sends the devotion quote of the day</td>
</tr>
