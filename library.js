/* Switch Kit AI — shortcut library.
   {for} = who the answer is for (from "Who's at home?"), {style} = how they like answers.
   Every shortcut is plain words the user's own AI receives; nothing is sent to us. */
var CATS = [
  ["meals", "Meals & groceries"],
  ["msgs", "Emails & messages"],
  ["money", "Money & bills"],
  ["trips", "Trips & outings"],
  ["home", "Home & garden"],
  ["family", "Family, friends & gifts"],
  ["learn", "Learning & hobbies"],
  ["health", "Doctor visits & wellbeing"],
  ["work", "Work & business"],
  ["tech", "Phone & tech help"],
  ["switch", "Moving to a different AI"]
];
var LIB = [
  // Meals & groceries
  {id:"m1", c:"meals", t:"Plan 5 easy dinners for this week", p:"Plan 5 easy weeknight dinners {for}. Each one should take 30 minutes or less and use everyday supermarket ingredients. Then give me one shopping list grouped by aisle. {style}"},
  {id:"m2", c:"meals", t:"Cook with what's already in the fridge", p:"Help me make dinner {for} with what I already have, no trip to the store. Ask me what's in my fridge and cupboard, then suggest 3 meals and how to make the best one. {style}"},
  {id:"m3", c:"meals", t:"Cut this week's grocery bill", p:"Help me spend less on groceries {for}. Ask me what I usually buy, then suggest cheaper swaps and a meal plan that uses up leftovers. {style}"},
  {id:"m4", c:"meals", t:"One-pan dinners with hardly any washing up", p:"Give me 4 one-pan or slow-cooker dinners {for} with very little cleanup, plus a shopping list. {style}"},
  {id:"m5", c:"meals", t:"Resize a recipe for more or fewer people", p:"I'll paste a recipe. Rewrite it for the number of people I tell you and give the amounts in cups and spoons. Ask me how many people first. {style}"},
  {id:"m6", c:"meals", t:"Make a favorite recipe a little lighter", p:"I'll paste a recipe I love. Make it a little lighter without losing the flavor, and show me exactly what you changed. {style}"},
  // Emails & messages
  {id:"e1", c:"msgs", t:"Turn my rough note into a polite email", p:"Help me write a short, polite email. Ask me who it's to and what I want to say, then write it in plain, friendly language with a subject line. {style}"},
  {id:"e2", c:"msgs", t:"Say no nicely", p:"Help me turn down a request politely without over-explaining. Ask me what the request is and who it's from, then write two versions: one warm, one firm. {style}"},
  {id:"e3", c:"msgs", t:"Write a complaint that gets results", p:"Help me write a calm, clear complaint to a company. Ask me what happened and what I want them to do, then write it so it's likely to get a quick fix. {style}"},
  {id:"e4", c:"msgs", t:"Reply to a tricky message", p:"I'll paste a message I received. Help me reply kindly and clearly. Give me 3 options, from short to a bit longer. {style}"},
  {id:"e5", c:"msgs", t:"Write a heartfelt thank-you note", p:"Help me write a thank-you note. Ask me who it's for and what they did, then write it warmly but not over the top. {style}"},
  {id:"e6", c:"msgs", t:"Fix my spelling and grammar", p:"I'll paste something I wrote. Fix the spelling and grammar, keep my own voice, and show me what you changed. {style}"},
  {id:"e7", c:"msgs", t:"What to write in a card", p:"Help me write the message inside a card. Ask me the occasion and who it's for, then give me 3 short options. {style}"},
  // Money & bills
  {id:"b1", c:"money", t:"Explain a confusing bill or letter", p:"I'll paste or describe a bill or official letter. Explain in plain English what it says, what I need to do, and whether anything looks unusual. {style}"},
  {id:"b2", c:"money", t:"Find money I'm wasting each month", p:"Help me find money I'm wasting each month {for}. Ask me about my regular bills and subscriptions, then list easy things to cancel, switch or ask to lower. {style}"},
  {id:"b3", c:"money", t:"Set up a simple monthly budget", p:"Help me set up a simple monthly budget {for}. Ask me my rough income and main costs, then lay it out in a small, easy table. {style}"},
  {id:"b4", c:"money", t:"A phone script to lower a bill", p:"Write me a short script for calling my phone, internet or insurance company to ask for a better price. Include what to say if they say no. {style}"},
  {id:"b5", c:"money", t:"Compare two options side by side", p:"Help me decide between two things I'm choosing between. Ask me what they are and what matters most to me, then give me a simple pros and cons table. {style}"},
  {id:"b6", c:"money", t:"Explain a money word in plain English", p:"Explain a money, banking or insurance term in plain English with a real-life example. Ask me which word. {style}"},
  // Trips & outings
  {id:"t1", c:"trips", t:"Plan a weekend away on a budget", p:"Plan a relaxed weekend away {for} on a sensible budget. Ask me where I'm starting from and what I enjoy, then give me 3 ideas with rough costs. {style}"},
  {id:"t2", c:"trips", t:"Find day trips near me", p:"Suggest 5 day trips within 2 hours of where I live, {for}. Ask me my town and what I enjoy. Include what to do and a good place to eat. {style}"},
  {id:"t3", c:"trips", t:"Make my packing list", p:"Make me a packing list. Ask me where I'm going, for how long and the time of year, then group it by suitcase and carry-on. {style}"},
  {id:"t4", c:"trips", t:"Turn my trip into a day-by-day plan", p:"Turn my trip into an easy day-by-day plan with rest breaks and meal ideas, {for}. Ask me where I'm going and for how long. {style}"},
  {id:"t5", c:"trips", t:"Rainy-day ideas", p:"Give me 10 things to do on a rainy day {for}, at home or nearby, mostly free. {style}"},
  {id:"t6", c:"trips", t:"Plan a get-together", p:"Help me host a get-together. Ask me how many people and the occasion, then give me a simple plan: menu, shopping list and a timeline for the day. {style}"},
  // Home & garden
  {id:"h1", c:"home", t:"Something's broken: what to check first", p:"Something at home isn't working. Ask me what it is and what it's doing, then walk me through simple, safe things to check first, and tell me when it's time to call a professional. {style}"},
  {id:"h2", c:"home", t:"A 20-minute-a-day cleaning plan", p:"Make me a realistic weekly cleaning plan {for} that takes about 20 minutes a day. {style}"},
  {id:"h3", c:"home", t:"Declutter one room this weekend", p:"Help me declutter one room this weekend. Ask me which room, then give me a step-by-step plan for what to keep, donate or toss. {style}"},
  {id:"h4", c:"home", t:"What to plant this season", p:"Help me plan what to plant this season. Ask me where I live and how much space and sun I have. Keep it beginner-friendly. {style}"},
  {id:"h5", c:"home", t:"Questions to ask before hiring a contractor", p:"I need someone to do a job at home. Ask me what needs doing, then give me questions to ask contractors and red flags to watch for. {style}"},
  {id:"h6", c:"home", t:"Turn my to-do list into a weekly plan", p:"I'll give you my messy list of chores and errands. Turn it into a simple plan for the week, grouped by day. {style}"},
  // Family, friends & gifts
  {id:"f1", c:"family", t:"Gift ideas for anyone", p:"Give me 10 gift ideas. Ask me who it's for, their age, what they love and my budget. {style}"},
  {id:"f2", c:"family", t:"Plan a birthday celebration", p:"Help me plan a birthday celebration. Ask me who it's for, how many people and the budget, then give me a simple plan. {style}"},
  {id:"f3", c:"family", t:"Cheap weekend activities with kids", k:"kids", p:"Give me 10 easy, cheap things to do with kids this weekend. Ask me their ages and whether we'd rather stay in or go out. {style}"},
  {id:"f4", c:"family", t:"A fun day with the grandkids", k:"grown", p:"Give me ideas for a fun day with my grandkids. Ask me their ages and whether we're staying in or going out. {style}"},
  {id:"f5", c:"family", t:"Write a short toast or speech", p:"Help me write a short toast or speech. Ask me the occasion and a few stories, then keep it under 2 minutes when spoken. {style}"},
  {id:"f6", c:"family", t:"Keep in touch with people I miss", p:"Help me keep in touch with family and old friends. Give me a simple monthly plan and a few easy message ideas. {style}"},
  // Learning & hobbies
  {id:"l1", c:"learn", t:"Learn something new in 10 minutes a day", p:"Teach me something new in 10 minutes a day for a week. Ask me what I'm curious about, then give me day 1. {style}"},
  {id:"l2", c:"learn", t:"Explain something everyone's talking about", p:"Explain a topic I keep hearing about, in plain English with no jargon. Ask me which topic. {style}"},
  {id:"l3", c:"learn", t:"Books or shows I'd enjoy", p:"Recommend 5 books or TV shows I'd enjoy. Ask me about 3 I loved recently first. {style}"},
  {id:"l4", c:"learn", t:"Start a new hobby on a small budget", p:"Help me start a new hobby on a small budget. Ask me what I'm thinking about, then give me a simple first-month plan. {style}"},
  {id:"l5", c:"learn", t:"Start my family tree", p:"Help me start a family tree. Ask me what I already know, then tell me what to write down and where to look next. {style}"},
  {id:"l6", c:"learn", t:"Quiz me on any topic", p:"Quiz me on a topic I choose, one question at a time, and tell me how I did at the end. Ask me the topic. {style}"},
  // Doctor visits & wellbeing (general information only)
  {id:"w1", c:"health", t:"Questions to bring to a doctor's appointment", p:"Help me prepare for a doctor's appointment. Ask me what it's about, then give me a short list of questions to bring. Don't try to diagnose me. {style}"},
  {id:"w2", c:"health", t:"Explain a medical word in plain English", p:"Explain a medical word or test name in plain English. Ask me which one, and remind me to check anything personal with my doctor. {style}"},
  {id:"w3", c:"health", t:"An easy 4-week walking plan", p:"Make me a gentle 4-week walking plan for a beginner. Ask me how much I walk now. {style}"},
  {id:"w4", c:"health", t:"A calm wind-down routine for the evening", p:"Suggest a calm 30-minute evening routine to help me wind down before bed. Keep it simple and free. {style}"},
  // Work & business
  {id:"k1", c:"work", t:"Write a clear email to my boss or a client", p:"Help me write a clear, professional email to my boss or a client. Ask me what it's about and what I need from them. {style}"},
  {id:"k2", c:"work", t:"Turn messy notes into a to-do list", p:"I'll paste messy meeting notes. Turn them into a short summary and a to-do list with who does what and by when. {style}"},
  {id:"k3", c:"work", t:"3 social media posts for my business", p:"Write 3 short social media posts for my small business. Ask me what I sell and who my customers are. {style}"},
  {id:"k4", c:"work", t:"Write a quote or invoice description", p:"Help me write a clear quote or invoice description for a customer. Ask me what the job is and what's included. {style}"},
  {id:"k5", c:"work", t:"Practice a tough conversation", p:"Help me practice a tough conversation or interview. Ask me what it's about, then play the other person and give me feedback after. {style}"},
  {id:"k6", c:"work", t:"Get a spreadsheet to do what I want", p:"Help me with a spreadsheet. Ask me what I'm trying to do, then give me step-by-step instructions for Excel or Google Sheets. {style}"},
  {id:"k7", c:"work", t:"Update my résumé", p:"Help me update my résumé. Ask me about my last few jobs, then write clear, modern bullet points. {style}"},
  // Phone & tech help
  {id:"p1", c:"tech", t:"Walk me through something on my phone", p:"Help me do something on my phone. Ask me whether it's an iPhone or Android and what I'm trying to do, then give me simple numbered steps. {style}"},
  {id:"p2", c:"tech", t:"Is this message a scam?", p:"I'll describe or paste a message, email or call I got. Tell me if it looks like a scam, what the warning signs are, and what to do next. {style}"},
  {id:"p3", c:"tech", t:"Keep my accounts safe", p:"Explain how to keep my online accounts safe, in plain English: good passwords, two-step login, and what I should never share. {style}"},
  {id:"p4", c:"tech", t:"Make my phone easier to read", p:"Walk me through making text bigger and my phone easier to read. Ask me if it's an iPhone or Android. {style}"},
  {id:"p5", c:"tech", t:"Set up a video call with family", p:"Walk me through setting up a video call with family. Ask me what phones or computers we each have. {style}"},
  {id:"p6", c:"tech", t:"Back up and sort my photos", p:"Help me back up and organize the photos on my phone. Ask me if it's an iPhone or Android. {style}"},
  // Moving to a different AI (bonus)
  {id:"s1", c:"switch", t:"See everything ChatGPT knows about you", p:"Write down everything you know about me, from your memories and our past chats, in one block I can copy. Leave out passwords and account numbers."},
  {id:"s2", c:"switch", t:"Check your new AI remembers you", p:"What do you know about me? Answer in a short list."}
];
