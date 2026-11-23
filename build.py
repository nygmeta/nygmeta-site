"""Builds the static nygmeta.com site from the content below. Run: python3 build.py"""
import os, html, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "docs")
os.makedirs(OUT, exist_ok=True)

NAV = [("index.html", "Home"), ("lab-automation.html", "Lab Automation"),
       ("openlabai.html", "OpenLabAI"), ("humanoids.html", "Humanoids"), ("nur-lighting.html", "Nur Lighting"),
       ("robotics.html", "Robotics"), ("spiderharp.html", "SpiderHarp"),
       ("art.html", "Art"), ("about.html", "About")]

CSS = """
:root{--bg:#fbfaf8;--fg:#1d1d1f;--muted:#5f6368;--accent:#b4532a;--card:#fff;--line:#e7e3de}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#121212;--fg:#ececec;--muted:#a3a3a3;--accent:#e08a5f;--card:#1c1c1c;--line:#2c2c2c}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.65 Inter,system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
a{color:var(--accent)}img{max-width:100%;height:auto;display:block;border-radius:10px}
header{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.bar{max-width:1080px;margin:0 auto;padding:12px 16px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.brand{font-weight:700;letter-spacing:.02em;text-decoration:none;color:var(--fg);margin-right:auto}
nav{display:flex;flex-wrap:wrap;gap:4px 16px}nav a{color:var(--muted);text-decoration:none;font-size:15px;white-space:nowrap}nav a.on,nav a:hover{color:var(--fg)}
main{max-width:860px;margin:0 auto;padding:40px 16px 80px}
h1{font-size:clamp(30px,5vw,44px);line-height:1.15;margin:0 0 12px}h2{font-size:26px;margin:48px 0 12px}h3{font-size:20px;margin:32px 0 8px}
.lede{font-size:20px;color:var(--muted);margin:0 0 28px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin:24px 0}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:18px;margin:28px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;text-decoration:none;color:var(--fg);transition:transform .15s}
.card:hover{transform:translateY(-3px)}.card img{border-radius:0;aspect-ratio:4/3;object-fit:cover;width:100%}
.card div{padding:12px 14px}.card b{display:block}.card span{color:var(--muted);font-size:14px}
.hero{display:grid;grid-template-columns:220px 1fr;gap:28px;align-items:center;margin-bottom:24px}.hero img{aspect-ratio:1;object-fit:cover;border-radius:50%}@media (max-width:640px){.hero{grid-template-columns:1fr}.hero img{width:160px}}
.cols{columns:3 200px;font-size:15px;color:var(--muted)}.cols li{break-inside:avoid}
blockquote{border-left:3px solid var(--accent);margin:32px 0;padding:4px 18px;font-size:20px}
.video{position:relative;padding-top:56.25%;margin:24px 0}.video iframe{position:absolute;inset:0;width:100%;height:100%;border:0;border-radius:10px}
.steps{list-style:none;counter-reset:s;padding:0;margin:24px 0}
.steps li{counter-increment:s;position:relative;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px 14px 58px;margin:0 0 10px}
.steps li::before{content:counter(s);position:absolute;left:16px;top:14px;width:28px;height:28px;border-radius:50%;background:var(--accent);color:var(--bg);font-weight:700;font-size:15px;display:grid;place-items:center}
.steps b{display:block}.steps span{color:var(--muted);font-size:16px}
.flow{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:24px 0;font-size:15px}
.flow div{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px 12px}
.flow div.gate{border-color:var(--accent);color:var(--accent);font-weight:600}.flow i{color:var(--muted);font-style:normal}
.tablewrap{overflow-x:auto;margin:20px 0}table{border-collapse:collapse;width:100%;font-size:16px}
th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line)}th{color:var(--muted);font-weight:600;font-size:14px}
code{background:var(--card);border:1px solid var(--line);border-radius:5px;padding:1px 5px;font-size:.88em}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:14px;text-align:center;padding:24px 16px}
@media (max-width:640px){.bar{gap:6px}nav{gap:2px 14px}}
"""

def page(fname, title, body):
    nav = "".join(f'<a href="{h}"{" class=on" if h == fname else ""}>{t}</a>' for h, t in NAV)
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | Ainur Nygmet</title>
<meta name="description" content="Ainur Nygmet: mechanical engineer and robotics founder building intelligent physical systems.">
<link rel="stylesheet" href="style.css"></head><body>
<header><div class="bar"><a class="brand" href="index.html">AINUR NYGMET</a><nav>{nav}</nav></div></header>
<main>{body}</main>
<footer>© Ainur Nygmet · <a href="https://www.linkedin.com/in/nygmetainur">LinkedIn</a> · <a href="https://github.com/nygmeta/OpenLabAI">OpenLabAI on GitHub</a></footer>
</body></html>"""
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(doc)

def imgs(prefix):
    files = sorted(glob.glob(os.path.join(OUT, "images", prefix + "-*")),
                   key=lambda p: int(p.rsplit("-", 1)[1].split(".")[0]))
    return [os.path.relpath(p, OUT) for p in files]

def gallery(paths):
    return '<div class="grid">' + "".join(f'<a href="{p}"><img src="{p}" loading="lazy" alt=""></a>' for p in paths) + "</div>"

def ps(*paras):
    return "".join(f"<p>{p}</p>" for p in paras)

# ---------- Home ----------
home = imgs("home")
cards = [("lab-automation.html", home[1], "Lab Automation at Hexagon Bio", "50+ Hamilton methods for drug discovery"),
         ("humanoids.html", home[2], "Humanoids for the Lab", "Raised VC funding for lab automation"),
         ("nur-lighting.html", home[3], "Nur Lighting", "Semi-finalist, Women Entrepreneurship competition"),
         ("nur-lighting.html#ozone", imgs("nur")[-1], "Balancing Ozone", "2nd place in physics, Paris, at 14"),
         ("spiderharp.html", home[5], "SpiderHarp", "Turning mechanical vibrations into music"),
         ("robotics.html", home[4], "Mechanical Engineering Projects", "Aero design, robots, capstone"),
         ("art.html", home[6], "Art", "Painting, poetry and drawing")]
page("index.html", "Portfolio", f"""
<div class="hero"><img src="{home[0]}" alt="Ainur Nygmet"><div><h1>Engineering Physical Intelligence</h1>
<p class="lede">I am a mechanical engineer and robotics founder focused on building intelligent physical systems.</p></div></div>
{ps("Over the past decade I have worked across laboratory automation, humanoid robotics, and scientific infrastructure. I have automated workflows used by scientists at Genentech, Guardant Health, Personalis, and Hexagon Bio, and recently led development of humanoid teleoperation systems for laboratory environments.",
    "My interests lie at the intersection of robotics, AI, automation, and manufacturing: building machines that extend human capability and accelerate scientific and industrial progress.")}
<h2>Projects</h2>
<div class="cards">{"".join(f'<a class="card" href="{h}"><img src="{i}" alt="" loading="lazy"><div><b>{t}</b><span>{s}</span></div></a>' for h, i, t, s in cards)}</div>
""")

# ---------- Lab automation (Hexagon) ----------
lab = imgs("lab")
methods = {
 "Cell Culture": ["Dilution Plating", "Electroporation Transformation", "Plasmid Prep", "Plating"],
 "Chemical Genetics": ["Aliquotting", "Colony Hitpicking", "Glycerol Stock and Pooling", "Growth Plate Hitpicking", "Inoculation from Omnitrays", "PCR Setup", "Pooling", "qPCR Dilution and Setup"],
 "Chemistry": ["LCMS Multiplex Hitpicking"],
 "Drug Discovery": ["NPL Dilution", "NPL Hitpicking", "NPL Onboarding"],
 "Forward Genetics": ["6 Cell Dispense", "24 Well Cell Dispense", "24 Well Compound Dispense"],
 "Whole Genome Sequencing": ["gDNA Normalization", "Library Amplification Hitpicking", "Library Normalization", "Library Pooling", "qPCR Dilution"],
 "Fungen": ["gDNA Extraction", "Index Primer", "Index Primer Stamp"],
 "Frag Prep": ["Amplicon Normalization", "Bead Purification", "Lightbench Size Selection", "PCR Setup (plates)", "FragAmp", "Channel-based Bead Purification", "Lightbench Analytics"],
 "Next-Generation Sequencing": ["DNA Addition", "Double Sided Bead Clean", "High Volume Bead Purification", "Normalization", "Pooling (384)", "Pooling"],
 "PlasMod": ["Deletion Hitpicking", "Ligation", "Plasmid Pick and Norm"],
 "PlasMORE": ["Dilution 1:100 Preparation", "Dilution Plating", "Fragment Batch Normalization", "Hitpicking (384)", "Hitpicking", "PCR to VB Dilution Hitpicking", "Plate CherryPick", "Plate Dilution", "Plate Resuspension", "Resuspension"],
 "Quantification": ["Lunatic Stamp"],
 "Reagent Prep": ["PCR Bead Dispense", "Yeast Plasmid Extraction"],
 "Standard Parts": ["Normalization and Aliquot", "Post PCR Pooling", "Secondary Pooling"],
 "Synthetic DNA": ["Consolidation Normalization", "Dilution", "Resuspension"],
 "Tools": ["Glycerol Stock Prep", "IDT VB Plate Processing", "IDT VB Plate Stamping", "Lightbench Quantification", "Pico Hitpicking", "Plate to Tube Hitpick Transfer", "Reagent Dispense", "Tip Consolidation", "Volume QC", "Volume Verification"],
 "Yeast": ["Amplicon Hitpicking", "Backbone Digestion", "Backbone Heat Shock", "Backbone Normalization and Aliquot", "Bead Extraction", "Transformation"],
}
mlist = "".join(f"<li><b>{html.escape(k)}</b>: {html.escape(', '.join(v))}</li>" for k, v in methods.items())
page("lab-automation.html", "Lab Automation", f"""
<h1>Lab Automation at Hexagon Bio</h1>
<p class="lede">Scientist-centric design: more than 50 custom Hamilton methods and 200+ deck layouts for drug discovery.</p>
<img src="{lab[0]}" alt="">
<h2>Scientist-Centric Design</h2>
{ps("In my role as a Lab Automation Engineer, I developed over 50 custom methods and edited more than 200 deck images. These methods were crafted with a singular goal in mind: to create solutions centered around scientists' needs and workflows. Each deck image, the first thing a scientist sees when they power on the robot, serves as a visual guide showing where to place reagents and which labware to use. Every deck image was paired with the Hamilton methods I developed in close collaboration with the scientists themselves.",
    "Through interviews and observations, I tailored each method to align with their physical setups, operational habits, and workflows. Beyond functionality, safety was paramount: I arranged reagents and plates to minimize risks, so accidents like finger injuries in the lab were virtually eliminated.")}
{gallery(lab[1:9])}
<h2>Safety and Training</h2>
{ps("I prioritized safety around lab automation equipment so that all users could operate the systems confidently and without risk. I trained over 40 scientists and research associates to use Hamilton robotics systems safely, emphasizing proper handling techniques and safety protocols, including step-by-step guidance running the methods I developed for them. I also replaced HEPA filters on the Hamilton equipment to maintain a sterile environment when working with BSL-2 microbes, protecting both the experiments and the scientists.")}
<h2>Workcells, XY Filler and Mantis</h2>
{ps("At Hexagon, as at other companies I worked for, we ran a workcell: robotic hardware integrated with automation systems to streamline repetitive tasks, improve precision, and keep workflows safe. Most workcells, even at companies like Ginkgo Bioworks, use HighRes Biosolutions hardware with Cellario software, which I am certified to operate.",
    "To verify that the XY filler dispensed the correct volume, I tested it on more than 1,000 bottles with different types of media. I then taught the next step on a Hamilton robot, developed a method to move media from bottles into plates, and ran it with real samples. I also worked with the Mantis, a micro-dispenser well suited to mRNA vaccine workflows.",
    "I have given workshops on lab automation at BioPunk Society in San Francisco and at the SilkRoad Innovation Hub in Palo Alto during TechCrunch week. I enjoy teaching people how to use robots.")}
{gallery(lab[9:])}
<h2>Methods I Developed</h2>
<ul class="cols">{mlist}</ul>
""")

# ---------- OpenLabAI ----------
layers = [
 ("Structured tools, never raw hardware",
  "The agent can only call a fixed set of tools, such as <code>read_deck</code>, <code>create_protocol</code>, <code>upload_protocol</code> and <code>start_run</code>. It has no other way to reach an instrument."),
 ("The request is validated before a file is written",
  "Protocol names, well references, step types, volumes, mix cycles and deck slots are each checked. Volumes are compared with the pipette's capacity. If anything is off, nothing is written."),
 ("The protocol is checked before anything moves",
  "On the Opentrons OT-2, uploading sends the protocol to the robot for its own analysis and creates a run that sits idle. A second check compares the analysed commands with deck limits. With PyLabRobot, the plan is first simulated with tip and volume tracking, which catches aspirating liquid that is not there or reusing a tip."),
 ("A person approves every motion",
  "Any tool that moves the robot refuses unless it is called with <code>confirm=true</code>, which stands for a named person approving that specific run. Pause and stop are never gated, because they only make the robot safer. In Slack, the approver's identity is recorded and a lab can require a second person."),
 ("Checks fail closed",
  "If the robot's analysis timed out, produced no commands, or the constraint checks could not load, the answer is \"do not start\". A check that could not run never counts as a check that passed."),
 ("The approval is tied to the exact protocol",
  "The PyLabRobot connector's approval token is a hash of the plan and of the commands it generates, so what was approved is what runs. The OT-2 path records the SHA-256 of the uploaded file."),
 ("Every action is written to an audit log",
  "Home, start, pause, resume and stop are logged with the operator and the protocol hash, so a result can be traced back to exactly what ran and who approved it."),
 ("Monitoring and recovery go through a person",
  "<code>get_run_status</code> reports the robot's errors and the safe next actions for the run's state. After a failure it sends someone to look at the deck. It never retries on its own."),
]
status = [
 ("Opentrons OT-2", "Opentrons HTTP API", "Plan, validate, upload, robot analysis, approve, run, monitor", "Partly verified on a physical OT-2; execution path tested against a simulated robot"),
 ("Hamilton STAR / STARlet", "PyLabRobot", "Generate a protocol and simulate it", "Simulation only; not yet run on a physical Hamilton"),
 ("Beckman Biomek", "COM automation", "Read the deck and generate a method file for review", "Not verified on hardware"),
 ("HighRes Cellario", "Cellario API", "Schedule runs and read device and queue status", "Not verified on hardware"),
]
page("openlabai.html", "OpenLabAI", f"""
<h1>OpenLabAI: how the guardrails work</h1>
<p class="lede">An open-source framework that lets an AI agent plan an experiment and run it on lab robots, without ever letting the agent move hardware on its own.</p>
{ps("Scientists often wait on an automation engineer for every protocol change, or have to learn each vendor's software. I was that engineer for years. OpenLabAI lets a scientist describe an experiment in plain language; an agent turns it into a protocol, and a set of guardrails decides whether and when the robot moves.",
    "The design rule is simple: the agent can plan anything, but it can only act through tools that validate the request, check it against the robot, wait for a person to approve, and record what ran.")}
<div class="flow"><div>Scientist's request</div><i>→</i><div>Agent plans</div><i>→</i><div>Validate</div><i>→</i><div>Robot analysis or simulation</div><i>→</i><div class="gate">Human approval</div><i>→</i><div>Robot runs</div><i>→</i><div>Audit log</div></div>
<h2>The eight layers</h2>
<ol class="steps">{"".join(f"<li><b>{t}</b><span>{d}</span></li>" for t, d in layers)}</ol>
<h2>What works on which instrument</h2>
{ps("I would rather be exact about this than impressive. The table says what each connector does today and how far it has been verified.")}
<div class="tablewrap"><table><tr><th>Instrument</th><th>Connection</th><th>What the agent can do</th><th>Verification</th></tr>
{"".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in status)}</table></div>
<h2>What the guardrails do not do</h2>
<ul><li><b>They do not know the biology.</b> They check volumes, tips and deck layout. Whether a run is scientifically right is still decided by the scientist's acceptance criteria.</li>
<li><b>The approval flag is passed by the agent.</b> The next step is approval the server verifies from outside the agent, such as the Slack button, so the agent cannot approve its own run.</li>
<li><b>Some layers are in review.</b> Fail-closed checks, request validation and the gates on homing and resuming are in an open pull request, not yet merged.</li></ul>
<h2>Code</h2>
{ps('OpenLabAI is MIT-licensed and tested in CI on every change: <a href="https://github.com/nygmeta/OpenLabAI">github.com/nygmeta/OpenLabAI</a>. The guardrail changes described above are in <a href="https://github.com/nygmeta/OpenLabAI/pull/3">pull request 3</a>.')}
""")

# ---------- Humanoids ----------
page("humanoids.html", "Humanoids", f"""
<h1>Humanoid Robots for the Lab</h1>
<h2>What</h2>
{ps("I am building humanoid robotics systems for laboratory environments. The approach starts with human teleoperation to perform real-world laboratory tasks and generate high-quality datasets that can be used to develop increasingly autonomous robotic capabilities.")}
<h2>Why</h2>
{ps("Scientists spend a significant portion of their time on repetitive, manual, and sometimes hazardous tasks. Humanoid robots can operate within existing laboratory infrastructure, improving safety, reducing operational bottlenecks, and letting researchers focus on higher-value scientific work.")}
<blockquote>“Ad astra per aspera.”<br><small>Through hardships to the stars.</small></blockquote>
<img src="{imgs('humanoid')[0]}" alt="">
""")

# ---------- Nur Lighting + Ozone ----------
nur = imgs("nur")
comps = [("LED Current Control", "Regulates the current flowing to the LEDs using transistors and a current-sense amplifier (INA180B), keeping illumination stable for plant growth."),
         ("Light Meter", "A photoresistor or light sensor measures ambient light so the microcontroller can adjust LED intensity to the sunlight available."),
         ("36 V to 12 V Buck Converter", "Steps a 36 V input down to a stable 12 V supply, improving efficiency and protecting components from overvoltage."),
         ("Fan Control", "Drives cooling fans with transistors, adjusting speed from temperature readings to prevent overheating."),
         ("One-Wire Temperature Sensors (DS18B20)", "Monitor temperature inside the greenhouse so lighting and environment stay in the ideal range."),
         ("On/Off Timer Control", "Automates LED timing so plants get the light they need each day, calculating supplemental light from natural exposure."),
         ("ISP Header and UART", "The ISP header programs the Arduino microcontroller; UART provides serial communication for logging and debugging."),
         ("Reset Button and Voltage Sensing", "A manual reset plus a voltage-sensing circuit that monitors power levels to catch anomalies.")]
page("nur-lighting.html", "Nur Lighting", f"""
<h1>Nur Lighting</h1>
<p class="lede">A smart greenhouse lighting controller, designed from sophomore to senior year. <a href="https://nurlightingsystems.weebly.com/">Original project site</a></p>
{ps("As a sophomore, I came up with Nur Lighting to address a problem I observed in a greenhouse at Oak Creek. Tomato seedlings need at least 16 hours of light a day, and during the dim month of February the greenhouse lights had to run the full duration regardless of how much natural light was available. Club members turned the lamps off by hand when there was enough sun, but this was inconsistent and often harmed the plants.",
    "I designed a smarter system: a photoresistor senses light outside the greenhouse, and a microcontroller tracks the natural light received and calculates how much supplemental light the plants still need. If seedlings received only 3 hours of sun on a cloudy day, the system runs the LEDs for another 13 hours, lowering energy costs and removing manual work.",
    "I developed the idea with advice from Professor James Cassidy, Senior Instructor in Soil Physics and Organic Agriculture, and visited the Oak Creek greenhouse to study the existing setup. I kept refining the project through senior year, and it became a semi-finalist in the Smith College Women Entrepreneurship competition.",
    "My prototype was damaged in transit from Oregon to Boston. Five minutes before the competition began, I pulled a wire from an LED bracelet to repair it, and it worked just in time.")}
{gallery(nur[:3])}
<h2>Key Components</h2>
<ul>{"".join(f"<li><b>{a}.</b> {b}</li>" for a, b in comps)}</ul>
<h3>Sketches of Nur integrated with AI</h3>
{gallery(nur[3:6])}
<h2 id="ozone">Balancing Ozone Levels</h2>
<p class="lede">This project won 2nd place in an international physics competition in Paris.</p>
{ps("Ozone shields Earth from UV in the stratosphere but is a harmful pollutant near the ground. This uneven distribution causes two problems: depletion, which increases UV exposure, and excess, which causes air pollution and health risks.",
    "For excess ozone, fine water mists can capture and reduce local ozone concentrations in offices and cities, alongside public awareness: limiting outdoor activity on hot, windless days and sharing timely information.",
    "The project went further with a device to redistribute ozone where it is lacking: a steel capsule holding a porous catalyst such as silica gel, with heating and cooling, that converts oxygen into ozone when exposed to external radiation. The challenges are the need for high-energy radiation and environmental safety, so the design focused on simplifying the process and lowering cost while keeping efficiency high, which also makes it useful for wastewater treatment, air purification, and drinking water.")}
{gallery(nur[6:])}
""")

# ---------- Robotics ----------
rob = imgs("robotics")
page("robotics.html", "Robotics", f"""
<h1>Mechanical Engineering Projects</h1>
<h2>Aero Design Project</h2>
<p class="lede">Oregon State University · Instructor: Dr. Nancy Squires</p>
<ul><li><b>Focus:</b> fundamentals of aerodynamics, stability, and control</li>
<li><b>Outcome:</b> a scale model aircraft concept with a mid-mounted wing, streamlined fuselage, and tail fin optimized for directional stability</li>
<li><b>Skills:</b> CAD modeling and aerodynamic analysis; balancing lift, drag, and structure; iterative team design</li></ul>
{gallery(rob[:2])}
<h2>ME 250: Hole Puncher</h2>
{ps("In this introductory manufacturing and design course, I designed, prototyped, and built a mechanical hole puncher from scratch, using a CNC mill for precision drilling, a manual lathe for shaping metal rods, and bench tools such as a drill press and band saw. Selecting materials, holding tolerances, and troubleshooting design flaws sparked my passion for manufacturing.")}
{gallery(rob[2:4])}
<h2>ME 382: Mechanical Systems Design</h2>
{ps("Our team designed and built a remote-controlled robot within a 50 × 50 × 50 cm box and under $200 in materials to complete five tasks: sprint 5 m and back, climb three 5 cm steps, throw a ping-pong ball, kick a ball as far as possible, and retrieve a ball 5 m away. We integrated chassis, propulsion, and lifting mechanisms with motors and remote-control electronics, while managing time and budget. It was my real introduction to how mechanical, electrical, and control systems come together.")}
{gallery(rob[4:7])}
<h2>Senior Capstone: Robotic Drawer</h2>
{ps("As part of a larger Oregon State effort to build a humanoid testing lab, our team developed a robotic drawer with interchangeable handles and integrated sensors for testing how a humanoid robot opens drawers. We gathered stakeholder requirements, applied design for manufacturing and assembly, and built a working prototype that met the specifications.")}
{gallery(rob[7:])}
""")

# ---------- SpiderHarp ----------
sp = imgs("spider")
page("spiderharp.html", "SpiderHarp", f"""
<h1>SpiderHarp</h1>
<p class="lede">Undergraduate robotics research: turning mechanical vibrations into music.</p>
{ps("I studied mechanical engineering at Oregon State University from 2014 to 2018, one of a few students from Kazakhstan selected from 500 applicants for a scholarship, and earned more than $100,000 in scholarships over four years.",
    "After my freshman year I joined Professor Ross Hatton's lab. Orb-weaving spiders see poorly and rely on web vibrations to locate prey, predators, and mates, so web geometry and composition shape their behavior. We built artificial webs and computer models to understand how web structure affects vibration transmission.")}
<h2>2019 Guthman Competition Finalist Performance</h2>
<div class="video"><iframe src="https://www.youtube.com/embed/zdRVBMoHPr4" title="SpiderHarp performance" allowfullscreen loading="lazy"></iframe></div>
<h2>HWeekend: Walking Spider Robot</h2>
{ps("My first robot, built at OSU's Hardware Weekend as a freshman, was a small light-following robot. At the demo, the bright room made it spin in circles, and I didn't place.",
    "Inspired by the Hatton lab, I came back the next year with a plan, recruited mechanical and electrical engineers I had never met, and in 32 hours we built a walking spider robot with Klann-linkage legs from laser-cut and 3D-printed parts. It kept breaking apart, but eventually it walked, and we took 2nd place out of 30 teams.")}
{gallery(sp)}
""")

# ---------- Art ----------
art = imgs("art")
page("art.html", "Art", f"""
<h1>Art</h1>
<img src="{art[0]}" alt="">
<p><em>Atyrau, Kazakhstan, 1998. Both of my grandfathers were history professors. Behind me is the Shezhire, our family's genealogical tree.</em></p>
<h2>Secret Poetry</h2>
{ps("As a teenager I kept a secret poetry blog in Russian on Vkontakte called “Selling Feeling with Poetry.” I wrote poems inspired by the songs I listened to and the photos I stared at, paired with images and music. At that age I was inspired by Ludovico Einaudi.")}
<h2>Painting</h2>
{ps("I have loved drawing since I was a child, on walls, in books, everywhere.",
    "In 2019 I won 2nd place at the Genentech Art Competition in Hillsboro, Oregon, with a painting inspired by Le Petit Prince: the little prince reaching for a rose under a glowing crescent moon, meant to bring back the wonder of seeing the world through a child's eyes.",
    "Another piece depicts the struggle against pollution in our seas. My deepest heartbreak with the Caspian Sea is the helplessness of its animals, unable to save their environment from the pollution we create, so I painted mermaids swimming away in shock.")}
{gallery(art[1:])}
<blockquote>“The meaning of life is to find your gift. The purpose of life is to give it away.”<br><small>Pablo Picasso</small></blockquote>
""")

# ---------- About ----------
ab = imgs("about")
gens = ["Алаш (Alash)", "Жайлхан (Zhaylhan)", "Майхибі (Mayhibi)", "Жен (Zhen)", "Айыр Қалпақ (Aiyr Kalpak)", "Қазақ (Kazakh)", "Бек-Арыс (Bek-Aris)", "Алшын (Alshin)", "Алау-Батыр (Alau-Batyr)", "Құдуар (Kuduar)", "Адам Қожа (Adam Kozha)", "Естай (Estai)", "Беріш (Berish)", "Бейсейт (Beiseit)", "Есен (Esen)", "Женет (Zhenet)", "Өтен (Oten)", "Наурызбай (Nauryzbai)", "Барс (Bars)", "Жантелі (Zhanteli)", "Балуан (Baluan)", "Борібай (Boribay)", "Өлмесек-Божас (Olmesek-Bozhas)", "Иманалы (Imanaly), 1861–1923", "Нығымет (Nygmet), 1901–1960", "Ғинаятолла (Hinayatolla), 1934–2017", "Рустем (Rustem), my father", "Айдарбек (Aidarbek), my brother, and me, Ainur"]
page("about.html", "About", f"""
<h1>About</h1>
<p class="lede">My name, Ai-nur, means “Moon-Light Gift” in Kazakh.</p>
{ps("I am a mechanical engineer specializing in scaling high-throughput laboratories, integrating automation, and optimizing workflows to accelerate science in biotech and pharma. My work bridges engineering, automation, and design.",
    "Beyond engineering, I care about protecting the Caspian Sea's endangered biodiversity and supporting underrepresented communities in STEM. Whether longboarding, writing poetry, or painting, I see creativity as the spark for meaningful change.")}
{gallery(ab[:3])}
<h2>Awards</h2>
<ul><li>First President's Full Tuition Grant, awarded on competitive entry exams in math and physics; top 1% score (116/125) on Kazakhstan's Unified National Test, 2014</li>
<li>Full scholarship to the OSU INTO freshman program, one of 500 students selected across Kazakhstan, 2014</li>
<li>Women in Robotics Scholarship, Society of Women Engineers, 2015</li>
<li>HWeekend engineering and design competition, 2nd place, 2016</li>
<li>Eric and Janice Hoffman Opportunity Scholarship, 2018</li>
<li>Genentech Art Competition, 2nd place, 2019</li></ul>
<h2>Training and Certifications</h2>
<ul><li>Six Sigma Green Belt, Institute of Industrial and Systems Engineers, 2017</li>
<li>SACNAS Leadership Academy, 2018</li>
<li>Qiagen QIAsymphony Training Certificate, 2021</li>
<li>Hamilton Venus Programming, Levels I and II, 2022–2023</li></ul>
{gallery(ab[3:])}
<h2>Twenty-eight generations by the Caspian Sea</h2>
{ps("In Kazakh culture it is essential to remember at least seven generations of ancestors. Thanks to my grandfather, a history professor, our family preserved the names of all 28 generations. The genealogy was written in 1946 by Sultan Rsaluly, chronicler of the Zhenet division, and supplemented in 1960 with the accounts of my great-grandfather Nygmet Imanuly.")}
<ol class="cols">{"".join(f"<li>{html.escape(g)}</li>" for g in gens)}</ol>
""")

with open(os.path.join(OUT, "style.css"), "w") as f:
    f.write(CSS)
print("built", sorted(os.listdir(OUT)))
