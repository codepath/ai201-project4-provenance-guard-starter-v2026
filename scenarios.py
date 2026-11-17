"""
What your test runs.

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "plain human writing",
        "criterion": 1,
        # Target: at most 1 of 10 labelled high-confidence AI, in every trial.
        # ⚠️ These ten are the PLAIN list from calibration.py and were drafted
        # with Claude's help, not written from scratch by me. Swap in ten of
        # my own pieces before relying on this criterion.
        "texts": [
            'I went to the store after school. I bought milk and bread. The line was long so I waited. Then I walked home. My mom made dinner and we ate together. After that I did my homework and went to bed.',
            'My favorite food is pizza. I like cheese pizza the most. I eat it with my friends on Friday. It is a good way to end the week. Sometimes we also get ice cream. I think everyone likes pizza.',
            'Last summer we went to the lake. The water was cold but we swam anyway. We made a fire and cooked hot dogs. My brother fell in the water. It was funny. I want to go back next year.',
            'I think school should start later in the day. Many students are tired in the morning. When we are tired it is hard to learn. A later start would help us pay attention. It would also help us feel better. I hope the school thinks about it.',
            'My dog is named Max. He is brown and he is very friendly. Every day we go for a walk in the park. He likes to chase the ball. When we get home he drinks a lot of water. Then he sleeps on the couch.',
            'The new library is a good place to study. It has big tables and quiet rooms. The people who work there are helpful. I go there after class most days. I can finish my work and read a book. I am glad it is close to my house.',
            'I started a new job last month. The people are nice and the work is not too hard. I get up early and take the train. At lunch I eat with my coworkers. I am learning a lot. I think I made a good choice.',
            'Soccer is my favorite sport. I play on a team every weekend. We practice twice a week. Our coach is kind and he teaches us a lot. Last week we won our game. I was very happy.',
            'Our town has a farmers market on Saturday. People sell fruit, bread, and flowers. I like to go with my father. We buy apples and sometimes honey. The music is nice too. It is a good way to spend the morning.',
            'I am learning to cook. First I made eggs. Then I made soup, and it was not bad. My family said they liked it. I want to learn to bake bread next. It looks hard but I will try.',
        ],
    },
    {
        "name": "clearly AI",
        "criterion": 2,
        # Criterion 2 compares this group's mean combined score with the next.
        "texts": [
            'Artificial intelligence is transforming the way organizations operate in the modern world. It is important to note that this technology offers numerous benefits across a wide range of industries. Additionally, it enables businesses to improve efficiency and make data-driven decisions. Overall, the integration of artificial intelligence represents a significant opportunity for growth and innovation.',
            'Climate change is one of the most pressing challenges facing humanity today. It is caused by the increase of greenhouse gases in the atmosphere, which leads to rising global temperatures. Furthermore, it has a significant impact on ecosystems, economies, and communities around the world. Therefore, it is essential that governments and individuals work together to address this important issue.',
            'Effective communication is a key factor in the success of any team. It allows team members to share ideas, resolve conflicts, and work toward common goals. In addition, strong communication skills help to build trust and foster a positive work environment. Consequently, organizations should prioritize the development of these skills among their employees.',
            'Regular exercise provides a wide variety of benefits for both physical and mental health. It helps to strengthen the heart, improve mood, and reduce the risk of chronic diseases. Moreover, it can enhance sleep quality and increase overall energy levels. For these reasons, it is important to incorporate physical activity into your daily routine.',
            "The importance of education cannot be overstated in today's society. It provides individuals with the knowledge and skills needed to succeed in their careers and personal lives. Additionally, education promotes critical thinking and encourages lifelong learning. As a result, investing in education is essential for building a prosperous and equitable future.",
        ],
    },
    {
        "name": "clearly human",
        "criterion": 2,
        "texts": [
            "I burned the toast again. Third time this week! Honestly, I think the toaster hates me - or maybe I just can't stop reading my phone while it's going. Anyway, the smoke alarm went off, the dog lost his mind, and my neighbor (the one with the leaf blower) waved at me through the window like nothing was wrong.",
            "My grandmother kept a jar of buttons she never used. Hundreds. Brass, bone, one shaped like a tiny strawberry. When she died we found out she'd sewn exactly zero things in forty years; she just liked how they sounded when she shook the jar. I took the strawberry one. It's on my desk now, next to a cold coffee.",
            "Look, the bus was late, again; that's not news. What got me was the driver, who apologized to every single person as they climbed on - even the guy who yelled. Weird how that stuck with me all day? I kept thinking about it during the meeting, which, by the way, could have been an email.",
            "We lost to Dunmore 3-2 on Saturday. Rain, mud, a ref who clearly needed glasses. Marcus scored in the 88th and then slipped on the celebration (face first, honestly spectacular). Coach said nothing for ten minutes, then bought everyone fries. That's why I love this team.",
            'Nobody tells you how loud a newborn is at 3 a.m. Or how quiet the house gets right after. I stood in the hallway holding her, not daring to move, and listened to the fridge hum; strange, but it was the best minute of that whole week.',
        ],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        # 12 texts across the range: 3 AI, 3 human, 3 plain, 3 edited AI.
        # Each of human / unsure / ai must appear at least once, none above 9.
        "texts": [
            'Artificial intelligence is transforming the way organizations operate in the modern world. It is important to note that this technology offers numerous benefits across a wide range of industries. Additionally, it enables businesses to improve efficiency and make data-driven decisions. Overall, the integration of artificial intelligence represents a significant opportunity for growth and innovation.',
            'Climate change is one of the most pressing challenges facing humanity today. It is caused by the increase of greenhouse gases in the atmosphere, which leads to rising global temperatures. Furthermore, it has a significant impact on ecosystems, economies, and communities around the world. Therefore, it is essential that governments and individuals work together to address this important issue.',
            'Effective communication is a key factor in the success of any team. It allows team members to share ideas, resolve conflicts, and work toward common goals. In addition, strong communication skills help to build trust and foster a positive work environment. Consequently, organizations should prioritize the development of these skills among their employees.',
            "I burned the toast again. Third time this week! Honestly, I think the toaster hates me - or maybe I just can't stop reading my phone while it's going. Anyway, the smoke alarm went off, the dog lost his mind, and my neighbor (the one with the leaf blower) waved at me through the window like nothing was wrong.",
            "My grandmother kept a jar of buttons she never used. Hundreds. Brass, bone, one shaped like a tiny strawberry. When she died we found out she'd sewn exactly zero things in forty years; she just liked how they sounded when she shook the jar. I took the strawberry one. It's on my desk now, next to a cold coffee.",
            "Look, the bus was late, again; that's not news. What got me was the driver, who apologized to every single person as they climbed on - even the guy who yelled. Weird how that stuck with me all day? I kept thinking about it during the meeting, which, by the way, could have been an email.",
            'I went to the store after school. I bought milk and bread. The line was long so I waited. Then I walked home. My mom made dinner and we ate together. After that I did my homework and went to bed.',
            'My favorite food is pizza. I like cheese pizza the most. I eat it with my friends on Friday. It is a good way to end the week. Sometimes we also get ice cream. I think everyone likes pizza.',
            'Last summer we went to the lake. The water was cold but we swam anyway. We made a fire and cooked hot dogs. My brother fell in the water. It was funny. I want to go back next year.',
            "AI is changing how companies work these days. Honestly it's a big deal for a lot of industries - it helps businesses cut costs and make decisions with data. But not everything about it is great, and some folks worry about jobs. Still, it's a real chance to grow; I guess we'll see.",
            'Teams that talk to each other do better, simple as that. Sharing ideas, sorting out fights, pulling the same direction - it all depends on talking. And trust? It grows from good communication (usually). So companies ought to teach it.',
            'Exercise is good for you. Really good - heart, mood, sleep, the lot. It cuts the risk of nasty long-term illness too. So find something you like and just do it every day, even a little.',
        ],
    },
    {
        "name": "appeal path",
        "criterion": 4,
        # `appeal: True` makes run_eval.py appeal every content_id that comes
        # back, read the status back through GET /content/<id>, and finish with
        # one appeal against an id that doesn't exist (must 404, record nothing).
        # Ten texts, because criterion 4 says 10 of 10 appeals.
        "appeal": True,
        "texts": [
            "I burned the toast again. Third time this week! Honestly, I think the toaster hates me - or maybe I just can't stop reading my phone while it's going. Anyway, the smoke alarm went off, the dog lost his mind, and my neighbor (the one with the leaf blower) waved at me through the window like nothing was wrong.",
            "My grandmother kept a jar of buttons she never used. Hundreds. Brass, bone, one shaped like a tiny strawberry. When she died we found out she'd sewn exactly zero things in forty years; she just liked how they sounded when she shook the jar. I took the strawberry one. It's on my desk now, next to a cold coffee.",
            "Look, the bus was late, again; that's not news. What got me was the driver, who apologized to every single person as they climbed on - even the guy who yelled. Weird how that stuck with me all day? I kept thinking about it during the meeting, which, by the way, could have been an email.",
            "We lost to Dunmore 3-2 on Saturday. Rain, mud, a ref who clearly needed glasses. Marcus scored in the 88th and then slipped on the celebration (face first, honestly spectacular). Coach said nothing for ten minutes, then bought everyone fries. That's why I love this team.",
            'Nobody tells you how loud a newborn is at 3 a.m. Or how quiet the house gets right after. I stood in the hallway holding her, not daring to move, and listened to the fridge hum; strange, but it was the best minute of that whole week.',
            'Artificial intelligence is transforming the way organizations operate in the modern world. It is important to note that this technology offers numerous benefits across a wide range of industries. Additionally, it enables businesses to improve efficiency and make data-driven decisions. Overall, the integration of artificial intelligence represents a significant opportunity for growth and innovation.',
            'Climate change is one of the most pressing challenges facing humanity today. It is caused by the increase of greenhouse gases in the atmosphere, which leads to rising global temperatures. Furthermore, it has a significant impact on ecosystems, economies, and communities around the world. Therefore, it is essential that governments and individuals work together to address this important issue.',
            'Effective communication is a key factor in the success of any team. It allows team members to share ideas, resolve conflicts, and work toward common goals. In addition, strong communication skills help to build trust and foster a positive work environment. Consequently, organizations should prioritize the development of these skills among their employees.',
            'Regular exercise provides a wide variety of benefits for both physical and mental health. It helps to strengthen the heart, improve mood, and reduce the risk of chronic diseases. Moreover, it can enhance sleep quality and increase overall energy levels. For these reasons, it is important to incorporate physical activity into your daily routine.',
            "The importance of education cannot be overstated in today's society. It provides individuals with the knowledge and skills needed to succeed in their careers and personal lives. Additionally, education promotes critical thinking and encourages lifelong learning. As a result, investing in education is essential for building a prosperous and equitable future.",
        ],
    },
    {
        "name": "bad input",
        "criterion": 5,
        # Target: 0 responses with a 5xx. (A bare-list body and non-UTF-8 bytes
        # can't be written as a dict body here; the malformed-request attacks
        # cover those.)
        "bodies": [
            {"creator_id": "eval_bad_missing"},
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "   \n  ", "creator_id": "eval_bad_blank"},
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": 12345, "creator_id": "eval_bad_number"},
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
