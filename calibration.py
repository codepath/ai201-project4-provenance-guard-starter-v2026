"""
Calibration inputs: texts whose true origin I know, so I can see where the two
signals and the combined score actually land. Run:

    python calibration.py            # both signals + combined + label
    python calibration.py --style    # style signal only (instant, no model)

The groups:
  ai        clearly machine-written
  human     clearly human, lumpy and specific
  plain     plain, conventional human writing (the group signal one over-reads)
  edited    AI text with light human edits
"""

import sys

AI = [
    "Artificial intelligence is transforming the way organizations operate in the modern world. It is important to note that this technology offers numerous benefits across a wide range of industries. Additionally, it enables businesses to improve efficiency and make data-driven decisions. Overall, the integration of artificial intelligence represents a significant opportunity for growth and innovation.",
    "Climate change is one of the most pressing challenges facing humanity today. It is caused by the increase of greenhouse gases in the atmosphere, which leads to rising global temperatures. Furthermore, it has a significant impact on ecosystems, economies, and communities around the world. Therefore, it is essential that governments and individuals work together to address this important issue.",
    "Effective communication is a key factor in the success of any team. It allows team members to share ideas, resolve conflicts, and work toward common goals. In addition, strong communication skills help to build trust and foster a positive work environment. Consequently, organizations should prioritize the development of these skills among their employees.",
    "Regular exercise provides a wide variety of benefits for both physical and mental health. It helps to strengthen the heart, improve mood, and reduce the risk of chronic diseases. Moreover, it can enhance sleep quality and increase overall energy levels. For these reasons, it is important to incorporate physical activity into your daily routine.",
    "The importance of education cannot be overstated in today's society. It provides individuals with the knowledge and skills needed to succeed in their careers and personal lives. Additionally, education promotes critical thinking and encourages lifelong learning. As a result, investing in education is essential for building a prosperous and equitable future.",
]

HUMAN = [
    "I burned the toast again. Third time this week! Honestly, I think the toaster hates me - or maybe I just can't stop reading my phone while it's going. Anyway, the smoke alarm went off, the dog lost his mind, and my neighbor (the one with the leaf blower) waved at me through the window like nothing was wrong.",
    "My grandmother kept a jar of buttons she never used. Hundreds. Brass, bone, one shaped like a tiny strawberry. When she died we found out she'd sewn exactly zero things in forty years; she just liked how they sounded when she shook the jar. I took the strawberry one. It's on my desk now, next to a cold coffee.",
    "Look, the bus was late, again; that's not news. What got me was the driver, who apologized to every single person as they climbed on - even the guy who yelled. Weird how that stuck with me all day? I kept thinking about it during the meeting, which, by the way, could have been an email.",
    "We lost to Dunmore 3-2 on Saturday. Rain, mud, a ref who clearly needed glasses. Marcus scored in the 88th and then slipped on the celebration (face first, honestly spectacular). Coach said nothing for ten minutes, then bought everyone fries. That's why I love this team.",
    "Nobody tells you how loud a newborn is at 3 a.m. Or how quiet the house gets right after. I stood in the hallway holding her, not daring to move, and listened to the fridge hum; strange, but it was the best minute of that whole week.",
]

PLAIN = [
    "I went to the store after school. I bought milk and bread. The line was long so I waited. Then I walked home. My mom made dinner and we ate together. After that I did my homework and went to bed.",
    "My favorite food is pizza. I like cheese pizza the most. I eat it with my friends on Friday. It is a good way to end the week. Sometimes we also get ice cream. I think everyone likes pizza.",
    "Last summer we went to the lake. The water was cold but we swam anyway. We made a fire and cooked hot dogs. My brother fell in the water. It was funny. I want to go back next year.",
    "I think school should start later in the day. Many students are tired in the morning. When we are tired it is hard to learn. A later start would help us pay attention. It would also help us feel better. I hope the school thinks about it.",
    "My dog is named Max. He is brown and he is very friendly. Every day we go for a walk in the park. He likes to chase the ball. When we get home he drinks a lot of water. Then he sleeps on the couch.",
    "The new library is a good place to study. It has big tables and quiet rooms. The people who work there are helpful. I go there after class most days. I can finish my work and read a book. I am glad it is close to my house.",
    "I started a new job last month. The people are nice and the work is not too hard. I get up early and take the train. At lunch I eat with my coworkers. I am learning a lot. I think I made a good choice.",
    "Soccer is my favorite sport. I play on a team every weekend. We practice twice a week. Our coach is kind and he teaches us a lot. Last week we won our game. I was very happy.",
    "Our town has a farmers market on Saturday. People sell fruit, bread, and flowers. I like to go with my father. We buy apples and sometimes honey. The music is nice too. It is a good way to spend the morning.",
    "I am learning to cook. First I made eggs. Then I made soup, and it was not bad. My family said they liked it. I want to learn to bake bread next. It looks hard but I will try.",
]

EDITED = [
    "AI is changing how companies work these days. Honestly it's a big deal for a lot of industries - it helps businesses cut costs and make decisions with data. But not everything about it is great, and some folks worry about jobs. Still, it's a real chance to grow; I guess we'll see.",
    "Teams that talk to each other do better, simple as that. Sharing ideas, sorting out fights, pulling the same direction - it all depends on talking. And trust? It grows from good communication (usually). So companies ought to teach it.",
    "Exercise is good for you. Really good - heart, mood, sleep, the lot. It cuts the risk of nasty long-term illness too. So find something you like and just do it every day, even a little.",
    "Education matters, a lot. It gives people skills for work and life, and it teaches them to think. Plus learning never really stops, right? Putting money into schools pays off for everybody in the end.",
]

GROUPS = {"ai": AI, "human": HUMAN, "plain": PLAIN, "edited": EDITED}

if __name__ == "__main__":
    import stylometry
    style_only = "--style" in sys.argv
    if not style_only:
        import detector
        import scoring
    for name, texts in GROUPS.items():
        print(f"\n== {name} ==")
        tot = []
        for i, t in enumerate(texts, 1):
            st = stylometry.style_signal(t)
            if style_only:
                print(f"  {i:>2}  style={st:.3f}")
            else:
                m = detector.model_signal(t)
                c = scoring.combine_signals(m, st)
                g, _ = scoring.score_to_label(c)
                tot.append(c)
                print(f"  {i:>2}  model={m:.3f}  style={st:.3f}  combined={c:.3f}  -> {g}")
        if tot:
            print(f"  mean combined = {sum(tot)/len(tot):.3f}")
