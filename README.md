# V3rmillion Archive Explorer
**V3rmillion** was a large forum that existed for about 12 years. It was dedicated to scripts, exploits, and the technical community around the game `Roblox`. Unfortunately, the forum was closed in 2023. As far as i remember, these factors contributed to its shutdown:
- The administration became tired of maintaining the site (banning scammers; constantly removing malware uploaded by users such as phishing disguised as "Free Robux generator", malicious Luau scripts, RATs, stealers, miners; moderating millions of messages, etc.)
- A new Roblox anti-cheat called `Hyperion` by Byfron Technologies was released
- The developers of `Synapse X` (the largest Roblox exploit at the time) joined Roblox

That year, enough things happened for everything to start falling apart. i say this as someone who witnessed those events and was affected by them in some way. To be honest, i was never a member of the v3rmillion community itself. So i apologize if someone dislikes the fact that i decided to make this project.

You can learn more about v3rmillion [here](https://logos.fandom.com/wiki/V3rmillion) or [here](https://theprogamers-experiment.fandom.com/wiki/V3rmillion)

As mentioned above, the forum was closed in 2023. However, an [archive](https://archive.org/download/v3rmillion) containing all threads and users of the community was later published. The only problem - i could not find a way to actually use this archive. Here are some reasons why:
1. It is impossible to find threads by title (there is no search system)
2. HTML pages of the threads reference the original v3rmillion website and cannot be opened properly
3. Reading HTML pages through raw source code is very difficult

Because of this, i decided to create an Explorer that helps search, extract all posts, and build a clearer reply history (surprisingly, this was not implemented very well on v3rmillion itself).

## Why would anyone need old posts from a deleted forum?
- A large number of highly valuable threads remain there - you can find guides and knowledge that even ChatGPT may not teach, and that are difficult or impossible to find elsewhere on the internet. Even today, there is no forum where you could find even 5% of the information that once existed on v3rmillion.
- History. Some people may simply want to know: "How was it back then?" - v3rmillion preserves that.

# Download
**The prebuilt search index will be downloaded automatically on first main.py run.**

Choose a folder where you want to download the project, open a terminal there, and run:
```sh
git clone https://github.com/64kun/V3rmillion-Archive-Explorer.git
```

# Usage
Go to the project directory:
```sh
cd V3rmillion-Archive-Explorer
```

Simple usage example:
```sh
python main.py path-to-v3rmillion-archive -r "request 1"
```

You can specify the maximum number of results (default value is 10):
```sh
python main.py path-to-v3rmillion-archive -r "request 1" 20
```

You can also search using multiple requests at once:
```sh
python main.py path-to-v3rmillion-archive -r "request 1" "request 2" 15 "request 3" 5
```

After execution, all results will be saved into the `parsed/` folder inside the project.

*Currently only saving threads in JSON format is supported. Generating custom HTML pages is planned, but it is unknown when i will have time to implement it.*