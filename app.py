import streamlit as st
import streamlit.components.v1 as components
import hashlib
import json
import tempfile
from pathlib import Path
import os


# -----------------------------------------------------------------------------
# URAFITE MULTILINGUAL INTERFACE: English, Kinyarwanda and French
# User selection is kept in Streamlit session state and can be changed anytime.
# -----------------------------------------------------------------------------
LANGUAGE_TEXT = {
    "Kinyarwanda": {
        "Home": "Ahabanza", "RECOVER": "Gukira", "REBUILD": "Kwiyubaka",
        "RECONNECT": "Kongera guhuza n'amahirwe", "AI Companion": "Hiro – Ubufasha mu gukira no kwiyubaka",
        "Professional Support": "Ubufasha bw'inzobere", "Navigate": "Ahantu ho kujya",
        "Reclaim Your Future": "Subirana ejo hazaza hawe",
        "A new pathway towards a better future": "Inzira nshya igana ku hazaza heza",
        "Three pathways. One renewed future.": "Inzira eshatu. Ejo hazaza hashya.",
        "You are more than your past experiences.": "Uri umuntu urenze ibyo wanyuzemo kera.",
        "1. How are you feeling today?": "1. Umeze ute uyu munsi?",
        "Choose the description closest to how you feel.": "Hitamo amagambo asobanura uko wiyumva.",
        "Very overwhelmed": "Ndaremerewe cyane", "Anxious": "Mfite impungenge",
        "Discouraged": "Nacitse intege", "Okay": "Ni byiza", "Hopeful": "Mfite icyizere",
        "Motivated": "Mfite imbaraga zo gukomeza", "Positive": "Numva meze neza",
        "2. Understand what you are experiencing": "2. Sobanukirwa n'ibyo urimo kunyuramo",
        "How strong is your urge to gamble right now?": "Ushaka gukina urusimbi ku rugero rungana iki ubu?",
        "3. What would you like to work on today?": "3. Ni iki wifuza kwitaho uyu munsi?",
        "Reflect on my responses": "Tekereza ku bisubizo byanjye",
        "Thank you for taking this moment for yourself. Recognizing what you are experiencing is meaningful.": "Urakoze gufata aka kanya ko kwiyitaho. Kumenya ibyo urimo kunyuramo ni intambwe ikomeye.",
        "Your personal reflection": "Ibyo watekerejeho",
        "Your past financial struggles do not define your future.": "Ibibazo wagize mu bijyanye n'amafaranga ntibigena ejo hazaza hawe.",
        "1. Understand your monthly finances": "1. Sobanukirwa n'amafaranga ukoresha buri kwezi",
        "Your monthly income (RWF)": "Amafaranga winjiza buri kwezi (RWF)",
        "Food and essential needs (RWF)": "Ibiribwa n'ibikenewe by'ibanze (RWF)",
        "Accommodation (RWF)": "Ubukode cyangwa icumbi (RWF)", "Transport (RWF)": "Ingendo (RWF)",
        "Education and personal development (RWF)": "Uburezi no kwiteza imbere (RWF)",
        "Other expenses (RWF)": "Andi mafaranga ukoresha (RWF)",
        "Money you have actually saved (RWF)": "Amafaranga wamaze kuzigama (RWF)",
        "Review my financial plan": "Reba gahunda yanjye y'imari",
        "2. Your financial picture": "2. Uko imari yawe ihagaze",
        "Monthly income": "Amafaranga winjiza buri kwezi", "Monthly expenses": "Amafaranga ukoresha buri kwezi",
        "Remaining income": "Amafaranga asigara", "Actual savings recorded": "Amafaranga wazigamye",
        "3. Your personal savings journey": "3. Urugendo rwawe rwo kuzigama",
        "4. What are you rebuilding towards?": "4. Ni iki wifuza kugeraho wiyubaka?",
        "Choose a goal that matters to you.": "Hitamo intego ifite agaciro kuri wowe.",
        "Your past does not determine your future.": "Ibyo wanyuzemo ntibigena ejo hazaza hawe.",
        "1. Discover your future": "1. Menya amahirwe y'ejo hazaza hawe",
        "Tell us what you would like to work towards. You can select more than one interest.": "Tubwire ibyo wifuza kugeraho. Ushobora guhitamo ibirenze kimwe.",
        "What opportunities interest you?": "Ni ayahe mahirwe agushishikaje?",
        "Scholarships and further education": "Buruse n'amashuri yisumbuyeho",
        "Digital skills and technology": "Ubumenyi mu ikoranabuhanga",
        "Vocational and technical training": "Amahugurwa y'imyuga n'ubumenyingiro",
        "Employment and internships": "Akazi na za stage",
        "Entrepreneurship and business": "Kwihangira imirimo n'ubucuruzi",
        "Personal development and leadership": "Kwiteza imbere n'ubuyobozi",
        "What is your current education or career stage?": "Urwego ugezeho mu mashuri cyangwa mu kazi ni uruhe?",
        "University graduate": "Warangije kaminuza", "University student": "Umunyeshuri wa kaminuza",
        "Secondary school student": "Umunyeshuri w'amashuri yisumbuye",
        "Currently seeking employment": "Ushaka akazi", "Working professional": "Usanzwe ukora",
        "What would you most like to achieve?": "Ni iki wifuza kugeraho kurusha ibindi?",
        "Continue my education": "Gukomeza amashuri", "Develop employable skills": "Kunguka ubumenyi bwamfasha kubona akazi",
        "Find an internship or job": "Kubona stage cyangwa akazi", "Start or grow a business": "Gutangira cyangwa guteza imbere ubucuruzi",
        "Become financially independent": "Kwigira mu by'imari", "Build confidence and personal growth": "Kwiyubakamo icyizere no kwiteza imbere",
        "Discover my opportunities": "Menya amahirwe yanjye", "2. Opportunities for your next chapter": "2. Amahirwe y'intambwe ikurikira",
        "3. Turn an opportunity into action": "3. Hindura amahirwe igikorwa",
        "My next step": "Intambwe ikurikira", "Save my next step": "Bika intambwe yanjye ikurikira",
        "🎯 My personal action plan": "🎯 Gahunda y'ibikorwa byanjye",
        "4. A message for your journey": "4. Ubutumwa bugutera imbaraga",
        "Your past losses do not define your worth.": "Igihombo wagize ntikigena agaciro kawe.",
        "Your mistakes do not erase your potential.": "Amakosa yawe ntakuraho ubushobozi ufite.",
        "🤖 URAFITE AI Companion": "🤖 Umufasha wa URAFITE ukoresha AI",
        "A safe space to reflect, rebuild and move forward.": "Ahantu hatekanye ho gutekereza, kwiyubaka no gukomeza.",
        "💬 Your conversation": "💬 Ikiganiro cyawe",
        "Share what is on your mind...": "Sangiza ibikuri ku mutima...",
        "🗑️ Start a new conversation": "🗑️ Tangira ikiganiro gishya",
        "🤝 Professional Support": "🤝 Ubufasha bw'inzobere",
        "Access information about qualified human support.": "Menya aho wabonera ubufasha bw'inzobere.",
        "Language / Ururimi / Langue": "Ururimi / Language / Langue",
        "Choose your preferred language": "Hitamo ururimi ukunda gukoresha",
    },
    "Français": {
        "Home": "Accueil", "RECOVER": "SE RÉTABLIR", "REBUILD": "RECONSTRUIRE",
        "RECONNECT": "RENOUER AVEC LES POSSIBILITÉS", "AI Companion": "Hiro – Votre guide de rétablissement",
        "Professional Support": "Soutien professionnel", "Navigate": "Navigation",
        "Reclaim Your Future": "Reprenez votre avenir",
        "A new pathway towards a better future": "Un nouveau chemin vers un avenir meilleur",
        "Three pathways. One renewed future.": "Trois parcours. Un avenir renouvelé.",
        "You are more than your past experiences.": "Vous êtes bien plus que vos expériences passées.",
        "1. How are you feeling today?": "1. Comment vous sentez-vous aujourd'hui ?",
        "Choose the description closest to how you feel.": "Choisissez la description qui correspond le mieux à votre état.",
        "Very overwhelmed": "Très dépassé(e)", "Anxious": "Anxieux / anxieuse",
        "Discouraged": "Découragé(e)", "Okay": "Ça va", "Hopeful": "Plein(e) d'espoir",
        "Motivated": "Motivé(e)", "Positive": "Positif / positive",
        "2. Understand what you are experiencing": "2. Comprendre ce que vous vivez",
        "How strong is your urge to gamble right now?": "Quelle est l'intensité de votre envie de jouer actuellement ?",
        "3. What would you like to work on today?": "3. Sur quoi souhaitez-vous travailler aujourd'hui ?",
        "Reflect on my responses": "Réfléchir à mes réponses",
        "Thank you for taking this moment for yourself. Recognizing what you are experiencing is meaningful.": "Merci d'avoir pris ce moment pour vous. Reconnaître ce que vous vivez est une étape importante.",
        "Your personal reflection": "Votre réflexion personnelle",
        "Your past financial struggles do not define your future.": "Vos difficultés financières passées ne définissent pas votre avenir.",
        "1. Understand your monthly finances": "1. Comprendre vos finances mensuelles",
        "Your monthly income (RWF)": "Vos revenus mensuels (RWF)",
        "Food and essential needs (RWF)": "Alimentation et besoins essentiels (RWF)",
        "Accommodation (RWF)": "Logement (RWF)", "Transport (RWF)": "Transport (RWF)",
        "Education and personal development (RWF)": "Études et développement personnel (RWF)",
        "Other expenses (RWF)": "Autres dépenses (RWF)",
        "Money you have actually saved (RWF)": "Épargne réellement constituée (RWF)",
        "Review my financial plan": "Examiner mon plan financier",
        "2. Your financial picture": "2. Votre situation financière",
        "Monthly income": "Revenus mensuels", "Monthly expenses": "Dépenses mensuelles",
        "Remaining income": "Revenu restant", "Actual savings recorded": "Épargne réellement enregistrée",
        "3. Your personal savings journey": "3. Votre parcours d'épargne personnel",
        "4. What are you rebuilding towards?": "4. Vers quel objectif souhaitez-vous vous reconstruire ?",
        "Choose a goal that matters to you.": "Choisissez un objectif qui compte pour vous.",
        "Your past does not determine your future.": "Votre passé ne détermine pas votre avenir.",
        "1. Discover your future": "1. Découvrez votre avenir",
        "Tell us what you would like to work towards. You can select more than one interest.": "Dites-nous ce que vous souhaitez accomplir. Vous pouvez choisir plusieurs centres d'intérêt.",
        "What opportunities interest you?": "Quelles possibilités vous intéressent ?",
        "Scholarships and further education": "Bourses et études supérieures",
        "Digital skills and technology": "Compétences numériques et technologie",
        "Vocational and technical training": "Formation professionnelle et technique",
        "Employment and internships": "Emploi et stages",
        "Entrepreneurship and business": "Entrepreneuriat et affaires",
        "Personal development and leadership": "Développement personnel et leadership",
        "What is your current education or career stage?": "Quel est votre niveau d'études ou votre situation professionnelle ?",
        "University graduate": "Diplômé(e) universitaire", "University student": "Étudiant(e) universitaire",
        "Secondary school student": "Élève du secondaire",
        "Currently seeking employment": "En recherche d'emploi", "Working professional": "En activité professionnelle",
        "What would you most like to achieve?": "Que souhaitez-vous accomplir en priorité ?",
        "Continue my education": "Poursuivre mes études", "Develop employable skills": "Développer des compétences professionnelles",
        "Find an internship or job": "Trouver un stage ou un emploi", "Start or grow a business": "Créer ou développer une entreprise",
        "Become financially independent": "Devenir financièrement indépendant(e)", "Build confidence and personal growth": "Renforcer ma confiance et mon développement personnel",
        "Discover my opportunities": "Découvrir mes possibilités", "2. Opportunities for your next chapter": "2. Des possibilités pour votre prochain chapitre",
        "3. Turn an opportunity into action": "3. Transformer une possibilité en action",
        "My next step": "Ma prochaine étape", "Save my next step": "Enregistrer ma prochaine étape",
        "🎯 My personal action plan": "🎯 Mon plan d'action personnel",
        "4. A message for your journey": "4. Un message pour votre parcours",
        "Your past losses do not define your worth.": "Vos pertes passées ne définissent pas votre valeur.",
        "Your mistakes do not erase your potential.": "Vos erreurs n'effacent pas votre potentiel.",
        "🤖 URAFITE AI Companion": "🤖 Assistant IA URAFITE",
        "A safe space to reflect, rebuild and move forward.": "Un espace sûr pour réfléchir, se reconstruire et avancer.",
        "💬 Your conversation": "💬 Votre conversation",
        "Share what is on your mind...": "Exprimez ce que vous avez à l'esprit...",
        "🗑️ Start a new conversation": "🗑️ Commencer une nouvelle conversation",
        "🤝 Professional Support": "🤝 Soutien professionnel",
        "Access information about qualified human support.": "Accédez aux informations sur l'accompagnement par des professionnels qualifiés.",
        "Language / Ururimi / Langue": "Langue / Ururimi / Language",
        "Choose your preferred language": "Choisissez votre langue préférée",
    }
}


# Complete language coverage for all user-facing text in the current MVP.
# Internal values remain English for calculations and conditional logic;
# format_func and display wrappers translate only what the user sees.
EXTRA_LANGUAGE_TEXT = {
"Kinyarwanda": {
    "A fresh start begins here": "Intangiriro nshya itangirira hano",
    "Your future is worth more than your next bet. Find support, rebuild your financial confidence, and reconnect with opportunities that move your life forward.": "Ejo hazaza hawe hafite agaciro kurusha indi nshuro wagera. Shaka ubufasha, ongera wubake icyizere mu micungire y'amafaranga, kandi wongere uhuze n'amahirwe yagufasha gutera imbere.",
    "A practical pathway towards a stronger future": "Inzira ifatika igana ku hazaza heza",
    "URAFITE is a youth-centred support platform designed to help people affected by harmful gambling take practical steps towards wellbeing, financial stability and new opportunities. You choose where to begin, and you can move between the pathways at your own pace.": "URAFITE ni urubuga rugenewe gufasha urubyiruko rwahuye n'ingaruka z'urusimbi gufata ingamba zifatika zo kubungabunga imibereho myiza, kongera gutekana mu by'imari no kubona andi mahirwe. Ni wowe uhitamo aho utangirira, kandi ushobora gukurikiza izi nzira uko ubyifuza.",
    "Three pathways. One renewed future.": "Inzira eshatu. Ejo hazaza hashya.",
    "01 · wellbeing": "01 · Imibereho myiza", "02 · financial confidence": "02 · Icyizere mu by'imari", "03 · new opportunities": "03 · Amahirwe mashya",
    "Pause, reflect on urges and triggers, build coping strategies, and identify when human support may help.": "Fata akaruhuko, tekereza ku byifuzo byo gutega n'ibibitera, wige uburyo bwo kubyitwaramo kandi umenye igihe ubufasha bw'umuntu bushobora kugufasha.",
    "Understand your income and expenses, set realistic savings goals, and take manageable financial steps.": "Sobanukirwa amafaranga winjiza n'ayo ukoresha, shyiraho intego zifatika zo kuzigama kandi ufate intambwe zoroheje mu micungire y'amafaranga.",
    "Turn your interests into an action plan for learning, skills development, employment or enterprise.": "Hindura ibyo ukunda gahunda y'ibikorwa bijyanye no kwiga, kongera ubumenyi, kubona akazi cyangwa kwihangira imirimo.",
    "Explore RECOVER →": "Jya kuri RECOVER →", "Explore REBUILD →": "Jya kuri REBUILD →", "Explore RECONNECT →": "Jya kuri RECONNECT →",
    "Start with one small step": "Tangira n'intambwe imwe nto", "You do not need to solve everything today. Choose the area that feels most important right now.": "Ntugomba gukemura byose uyu munsi. Hitamo ikintu wumva ari ingenzi kurusha ibindi muri aka kanya.",
    "Begin with a personal check-in": "Tangira wisuzuma uko umeze", "A message to carry with you": "Ubutumwa wahorana mu rugendo rwawe",
    "Your past losses do not define your worth. Your next decision can help shape a different future.": "Igihombo wagize mu gihe cyashize ntikigena agaciro kawe. Icyemezo ufata uyu munsi gishobora kugufasha kubaka ejo hazaza hatandukanye.",
    "URAFITE MVP · A developing support prototype": "URAFITE MVP · Verisiyo ikiri gutezwa imbere",
    "URAFITE complements, but does not replace, qualified professional care. This prototype does not provide clinical diagnosis, crisis monitoring or emergency response.": "URAFITE yunganira ubufasha bw'inzobere ariko ntibusimbura. Iyi verisiyo ntisuzuma indwara, ntikurikirana ibibazo by'ihutirwa kandi ntitanga ubutabazi bwihuse.",
    "Welcome to a judgment-free space. You do not have to have everything figured out today. Take a moment to understand how you are feeling and what you need.": "Urakaza neza ahantu utacirwa urubanza. Ntugomba kuba ufite ibisubizo byose uyu munsi. Fata akanya usobanukirwe n'uko wiyumva n'icyo ukeneye.",
    "Your responses are used to provide supportive reflections. This exercise is not a clinical assessment or a diagnosis.": "Ibisubizo utanga bifasha kuguha ibitekerezo bigushyigikira. Iyi myitozo si isuzuma ry'ubuvuzi kandi ntitanga isuzuma ry'indwara.",
    "Choose the description closest to how you feel.": "Hitamo amagambo asobanura neza uko wiyumva.",
    "What situations or feelings may be influencing you?": "Ni ibihe bihe cyangwa ibyiyumvo bishobora kuba bikugiraho ingaruka?",
    "Choose options": "Hitamo amahitamo",
    "Choose an option": "Hitamo kimwe",
    "Financial pressure": "Ihungabana ry'amafaranga", "Stress or anxiety": "Guhangayika cyangwa kugira impungenge", "Boredom or loneliness": "Kurambirwa cyangwa kwigunga", "Friends or social influence": "Inshuti cyangwa igitutu cy'abandi", "Gambling advertisements": "Kwamamaza urusimbi", "Trying to recover previous losses": "Kugerageza kugaruza amafaranga yatakaye", "Feeling disappointed in myself": "Kumva ntanyuzwe n'ibyo nakoze", "Excitement or the hope of winning": "Ibyishimo cyangwa icyizere cyo gutsinda", "Other": "Ikindi", "I am not sure": "Sindabyizeye neza",
    "Choose what matters most to you right now.": "Hitamo ikintu kikubangamiye cyangwa kikuraje ishinga kurusha ibindi ubu.",
    "I want to manage my gambling urges.": "Ndashaka kumenya uko nahangana n'ibyifuzo byo gukina urusimbi.", "I want to understand my gambling behaviour.": "Ndashaka gusobanukirwa n'imyitwarire yanjye ku bijyanye n'urusimbi.", "I want to regain control of my finances.": "Ndashaka kongera gucunga neza amafaranga yanjye.", "I want to focus on my education or career.": "Ndashaka kwibanda ku mashuri cyangwa ku kazi kanjye.", "I want to rebuild my confidence.": "Ndashaka kongera kwiyubakamo icyizere.", "I would like to speak with a professional.": "Ndifuza kuganira n'inzobere.",
    "I would like information about professional support.": "Ndifuza amakuru ku bufasha butangwa n'inzobere.",
    "Thank you for taking this moment for yourself. Recognizing what you are experiencing is meaningful.": "Urakoze gufata aka kanya ko kwiyitaho. Kumenya ibyo urimo kunyuramo ni intambwe ifite akamaro.",
    "Your personal reflection": "Ibyo watekerejeho ku buzima bwawe", "You described feeling **": "Uvuze ko wiyumva **", " today.": "** uyu munsi.",
    "**You are experiencing a strong gambling urge.**": "**Ufite icyifuzo gikomeye cyo gukina urusimbi.**", "**You have noticed a moderate gambling urge.**": "**Wabonye ko ufite icyifuzo cyo gukina urusimbi kiri ku rugero ruciriritse.**", "**You have reported a relatively low gambling urge.**": "**Ugaragaje ko icyifuzo cyo gukina urusimbi kiri hasi.**",
    "Situations you identified:": "Ibihe cyangwa impamvu wagaragaje:", "A small step towards change": "Intambwe nto igana ku mpinduka", "Your chosen priority: ": "Icyo wahisemo gushyira imbere: ",
    "You do not have to act on an urge immediately. Consider stepping away from gambling applications or advertisements, moving to a different environment, and contacting someone you trust.": "Ntugomba guhita ukurikiza icyifuzo cyo gutega. Gerageza kuva kuri porogaramu cyangwa amatangazo y'urusimbi, ujye ahandi hantu kandi uvugishe umuntu wiringira.",
    "This could be a useful moment to pause and reflect before making a decision. Try identifying what you are feeling and choose an activity that supports your personal goals.": "Iki ni igihe cyiza cyo guhagarara gato no gutekereza mbere yo gufata icyemezo. Gerageza kumenya uko wiyumva, uhitemo igikorwa kigufasha kugera ku ntego zawe.",
    "Use this moment to strengthen habits that support your well-being and the future you want to build.": "Koresha aka kanya kugira ngo ukomeze ingeso nziza zifasha imibereho yawe n'ejo hazaza wifuza.",
    "Try delaying any gambling decision for 15 minutes. During that time, move away from gambling content and do something that helps you feel grounded.": "Gerageza gusubika icyemezo cyo gutega nibura iminota 15. Muri icyo gihe, jya kure y'ibijyanye n'urusimbi maze ukore ikintu kigufasha gutuza.",
    "Start by identifying one essential financial priority. You can use REBUILD to create a realistic budget and work towards it.": "Tangira ugaragaze ikintu kimwe cy'ingenzi mu by'amafaranga. Ushobora gukoresha REBUILD kugira ngo utegure ingengo y'imari ifatika kandi uyikurikize.",
    "Seeking professional support is a positive step. You deserve to be heard and supported by someone qualified to help.": "Gusaba ubufasha bw'inzobere ni intambwe nziza. Ukwiriye kumvwa no gushyigikirwa n'umuntu ubifitiye ubumenyi.",
    "You deserve support": "Ukwiriye gufashwa", "If you are experiencing severe distress, thoughts of suicide, or immediate danger, do not rely on this check-in. Contact emergency services, a qualified professional, or someone you trust who can help you access immediate care.": "Niba ufite agahinda gakabije, ibitekerezo byo kwiyahura cyangwa uri mu kaga kihutirwa, ntukishingikirize kuri iri suzuma. Hamagara ubutabazi bwihutirwa, inzobere cyangwa umuntu wiringira wagufasha kubona ubufasha ako kanya.",
    "Your past financial struggles do not define your future.": "Ibibazo wagize mu bijyanye n'amafaranga ntibigena ejo hazaza hawe.", "You do not need to recover everything at once. Start by understanding your finances, setting realistic goals, and taking small steps towards financial stability.": "Ntugomba kugaruza cyangwa gukemura byose icyarimwe. Tangira usobanukirwe n'imari yawe, ushyireho intego zifatika kandi utere intambwe nto zigana ku mutekano w'amafaranga.",
    "This is a personal budgeting and goal-tracking tool, not professional financial advice.": "Iki ni igikoresho kigufasha gutegura ingengo y'imari no gukurikirana intego zawe; ntigisimbura inama z'inzobere mu by'imari.",
    "Your monthly income (RWF)": "Amafaranga winjiza buri kwezi (RWF)", "Your essential and personal expenses": "Amafaranga y'ibikenewe n'ibindi ukoresha", "Food and essential needs (RWF)": "Ibiribwa n'ibikenewe by'ibanze (RWF)", "Accommodation (RWF)": "Icumbi cyangwa ubukode (RWF)", "Transport (RWF)": "Ingendo (RWF)", "Education and personal development (RWF)": "Amashuri no kwiteza imbere (RWF)", "Other expenses (RWF)": "Andi mafaranga ukoresha (RWF)", "Money you have actually saved (RWF)": "Amafaranga usanzwe warazigamye (RWF)", "Your financial recovery goal": "Intego yawe yo kongera gutekana mu by'imari", "How much would you like to save? (RWF)": "Ni amafaranga angahe wifuza kuzigama? (RWF)", "When would you like to achieve this goal?": "Wifuza kugera kuri iyi ntego ryari?", "1 month": "Ukwezi 1", "3 months": "Amezi 3", "6 months": "Amezi 6", "12 months": "Amezi 12", "Review my financial plan": "Reba gahunda yanjye y'imari",
    "Your recorded expenses exceed your income. This may be a good opportunity to review your financial priorities and consider additional support.": "Amafaranga wanditse ukoresha aruta ayo winjiza. Ibi bishobora kukwereka ko ukwiriye kongera gusuzuma ibyo ushyira imbere mu gukoresha amafaranga no gushaka ubundi bufasha.", "Understanding your finances is an important step towards making informed decisions.": "Gusobanukirwa n'imari yawe ni intambwe ikomeye igufasha gufata ibyemezo bishingiye ku makuru.", "Actual savings recorded": "Amafaranga wazigamye koko", "Remaining income is not automatically counted as savings. Only money you have actually saved is recorded here.": "Amafaranga asigaye ntiyihita abarwa nk'ayo wazigamye. Habarwa gusa amafaranga washyize ku ruhande koko.", "Your personal savings journey": "Urugendo rwawe rwo kuzigama", "Your goal: **": "Intego yawe: **", " within **": " mu gihe cya **", "You have achieved ": "Umaze kugeraho ", "% of your savings goal.": "% by'intego yawe yo kuzigama.", "Amount remaining: **": "Amafaranga asigaye: **", "Set a savings target whenever you feel ready.": "Ishyirireho intego yo kuzigama igihe uzaba witeguye.", "What are you rebuilding towards?": "Ni iyihe ntego wifuza kugeraho wiyubaka?", "Choose a goal that matters to you.": "Hitamo intego ifite akamaro kuri wowe.", "Paying my education fees": "Kwishyura amafaranga y'ishuri", "Building personal savings": "Kongera amafaranga nizigamiye", "Starting a small business": "Gutangira ubucuruzi buto", "Developing my professional skills": "Kongera ubumenyi bw'umwuga", "Achieving financial independence": "Kwigira mu by'imari", "Supporting my family": "Gufasha umuryango wanjye", "Another personal goal": "Indi ntego yanjye bwite", "Your chosen priority: ": "Icyo wahisemo gushyira imbere: ", "A reminder from URAFITE": "Ubutumwa buguturutse kuri URAFITE", "Your financial situation today does not determine your financial future. You do not have to rebuild everything immediately. Every realistic step towards your goals matters.": "Uko imari yawe ihagaze uyu munsi si byo bigena uko izaba imeze mu gihe kizaza. Ntugomba kongera kwiyubaka byose ako kanya. Buri ntambwe ifatika igana ku ntego zawe ifite agaciro.", "Demonstration version: financial information is held in the current Streamlit session and is not yet stored in a permanent personal account.": "Iyi ni verisiyo y'igerageza: amakuru y'imari abikwa gusa mu gihe iyi porogaramu iri gukora; ntarabikwa kuri konti bwite ihoraho.",
    "A fresh start is not just about leaving harmful habits behind. It is also about discovering new opportunities, developing your potential, and building a future you can be proud of.": "Gutangira bundi bushya ntibivuga kureka ingeso mbi gusa. Binavuga kumenya andi mahirwe, guteza imbere ubushobozi bwawe no kubaka ejo hazaza uzishimira.", "Your future is still full of possibilities. Let's identify one meaningful step you can take today.": "Ejo hazaza hawe haracyarimo amahirwe menshi. Reka tumenye intambwe imwe ifite akamaro ushobora gutera uyu munsi.", "Discover your future": "Menya amahirwe y'ejo hazaza hawe", "Tell us what you would like to work towards. You can select more than one interest.": "Tubwire ibyo wifuza kugeraho. Ushobora guhitamo ibirenze kimwe.", "What opportunities interest you?": "Ni ayahe mahirwe agushishikaje?", "What is your current education or career stage?": "Urwego ugezeho mu mashuri cyangwa mu kazi ni uruhe?", "Vocational training student": "Umunyeshuri w'amahugurwa y'imyuga", "What would you most like to achieve?": "Ni iki wifuza kugeraho kurusha ibindi?", "Discover my opportunities": "Menya amahirwe ashobora kungirira akamaro", "Opportunities for your next chapter": "Amahirwe y'intambwe ikurikira", "Your current goal: ": "Intego yawe ubu: ", "Your education or career stage: ": "Urwego ugezeho mu mashuri cyangwa mu kazi: ", "The opportunities below are illustrative examples for the MVP. They are not verified live vacancies, scholarships, or open programmes.": "Amahirwe akurikira ni ingero zashyizwe muri iyi verisiyo y'igerageza. Ntabwo ari imyanya y'akazi, buruse cyangwa gahunda byemejwe ko bigifunguye.", "Scholarship Discovery": "Gushakisha buruse", "Explore scholarship pathways, admission requirements, application preparation, and opportunities for further study.": "Shakisha buruse, ibisabwa kugira ngo wemererwe kwiga, uko wategura ubusabe n'andi mahirwe yo gukomeza amashuri.", "Prepare a list of three programmes I would like to explore.": "Tegura urutonde rwa gahunda eshatu nifuza kumenya kurushaho.", "Digital Skills Development": "Kongera ubumenyi mu ikoranabuhanga", "Build practical skills in programming, data analysis, digital tools, and other areas of technology.": "Ongera ubumenyi bufatika muri porogaramu za mudasobwa, isesengura ry'amakuru, ibikoresho by'ikoranabuhanga n'ibindi bijyanye na tekinolojiya.", "Choose one digital skill and identify a learning resource.": "Hitamo ubumenyi bumwe bw'ikoranabuhanga ushaka kwiga maze ushake aho wabwigira.", "Vocational Skills Pathway": "Inzira yo kwiga imyuga", "Explore practical and technical training that can support employment or self-employment.": "Shakisha amahugurwa y'imyuga n'ubumenyingiro ashobora kugufasha kubona akazi cyangwa kwihangira imirimo.", "Identify one vocational skill relevant to my interests.": "Menya umwuga umwe ujyanye n'ibyo nshishikajwe na byo.", "Employment Readiness": "Kwitegura kubona akazi", "Strengthen your CV, prepare for interviews, and explore internship and employment pathways.": "Ongera kunoza umwirondoro wawe w'akazi (CV), witegure ibazwa kandi ushake amahirwe ya stage n'akazi.", "Update my CV and identify one opportunity to apply for.": "Vugurura CV yanjye kandi menye amahirwe imwe nshobora gusabira.", "Entrepreneurship Journey": "Urugendo rwo kwihangira imirimo", "Explore business ideas, entrepreneurship training, financial planning, and enterprise development.": "Shakisha ibitekerezo by'ubucuruzi, amahugurwa yo kwihangira imirimo, igenamigambi ry'imari no guteza imbere ikigo.", "Write down one business idea and the problem it addresses.": "Andika igitekerezo kimwe cy'ubucuruzi n'ikibazo cyakemura.", "Leadership and Personal Growth": "Ubuyobozi no kwiteza imbere", "Explore mentorship, leadership development, communication, and personal growth opportunities.": "Shakisha ubujyanama, amahugurwa y'ubuyobozi, itumanaho n'amahirwe yo kwiteza imbere.", "Identify one personal development goal for this month.": "Hitamo intego imwe yo kwiteza imbere muri uku kwezi.", "You have not selected any interests yet. Please select at least one interest above to discover suggested opportunities.": "Nta cyo wahisemo kirakwerekeye. Hitamo nibura ikintu kimwe hejuru kugira ngo ubone amahirwe ashobora kukugirira akamaro.", "Turn an opportunity into action": "Hindura amahirwe igikorwa", "Big changes begin with small, realistic steps. Choose one action you are willing to take.": "Impinduka zikomeye zitangirira ku ntambwe nto kandi zishoboka. Hitamo igikorwa kimwe witeguye gukora.", "My next step": "Intambwe yanjye ikurikira", "Save my next step": "Bika intambwe yanjye ikurikira", "Your next step has been added to your action plan.": "Intambwe ikurikira yongewe muri gahunda yawe y'ibikorwa.", "My personal action plan": "Gahunda yanjye bwite y'ibikorwa", "You do not have to change everything today. Focus on taking this one step forward.": "Ntugomba guhindura byose uyu munsi. Wibande kuri iyi ntambwe imwe igana imbere.", "A message for your journey": "Ubutumwa bugutera imbaraga mu rugendo rwawe", "Your past mistakes do not erase your potential.": "Amakosa wakoze mu gihe cyashize ntakuraho ubushobozi ufite.", "Every meaningful new beginning starts with one step. Keep moving forward.": "Intangiriro nshya ifite akamaro itangirana n'intambwe imwe. Komeza utere imbere.", "Your next chapter starts with a decision. Select your interests above to discover possible pathways.": "Intambwe nshya itangirana n'icyemezo. Hitamo ibyo ukunda hejuru kugira ngo umenye inzira zishoboka.",
    "You deserve support from a real person.": "Ukwiriye gufashwa n'umuntu nya muntu.", "Digital tools can help you reflect, but some situations need human care. A qualified counsellor, mental-health professional or healthcare provider can listen, help you consider your options and guide you towards appropriate support.": "Ibikoresho by'ikoranabuhanga bishobora kugufasha gutekereza, ariko hari ibihe bisaba ubufasha bw'umuntu. Umujyanama ubifitiye ubumenyi, inzobere mu buzima bwo mu mutwe cyangwa umukozi w'ubuzima ashobora kukumva, kugufasha gusuzuma amahitamo yawe no kukuyobora ku bufasha bukwiye.", "URAFITE has not yet verified a directory of local referral providers. We will not display unconfirmed phone numbers, organisations or emergency contacts.": "URAFITE ntiragenzura urutonde rw'abatanga ubufasha bo mu karere. Ntabwo tuzerekana nimero za telefoni, imiryango cyangwa aho wahamagara mu gihe cyihutirwa bitaremezwa.", "When to seek support": "Igihe ukwiriye gushaka ubufasha", "Ongoing support": "Ubufasha buhoraho", "Consider speaking with a qualified professional if gambling, stress, debt, sleep problems or emotional distress are affecting your daily life.": "Tekereza kuganira n'inzobere ibifitiye ubumenyi niba urusimbi, imihangayiko, imyenda, ibibazo byo gusinzira cyangwa agahinda bikubuza gukora neza mu buzima bwa buri munsi.", "Immediate danger": "Akaga kihutirwa", "If you may hurt yourself or someone else, or cannot keep yourself safe, seek immediate in-person help through local emergency services or the nearest hospital.": "Niba ushobora kwigirira nabi cyangwa kugirira undi nabi, cyangwa udashobora kwirinda akaga, shaka ubufasha bw'umuntu ako kanya binyuze mu butabazi bwihutirwa cyangwa ku bitaro bikwegereye.",
    "Professional Support": "Ubufasha bw'inzobere", "AI-assisted recovery and opportunity support": "Ubufasha bwo kwiyubaka no kubona amahirwe bwunganirwa n'ikoranabuhanga", "Navigate": "Ahantu ho kujya", "Choose your preferred language": "Hitamo ururimi wifuza gukoresha", "Language / Ururimi / Langue": "Ururimi", "Share what is on your mind...": "Sangiza ibikuri ku mutima...", "Start a new conversation": "Tangira ikiganiro gishya", "You can switch the interface language in the sidebar. Avoid sharing passwords, ID numbers or other highly sensitive information.": "Ushobora guhindura ururimi ukoresheje ahabugenewe ku ruhande. Irinde gutanga ijambo ry'ibanga, nimero ndangamuntu cyangwa andi makuru akomeye y'ibanga.", "Responses are predefined and may not understand every message. For urgent or complex needs, seek help from a qualified person.": "Ibisubizo byateguwe mbere kandi bishobora kutumva ubutumwa bwose. Ku kibazo cyihutirwa cyangwa gikomeye, saba ubufasha bw'umuntu ubifitiye ubumenyi.", "Privacy: conversation history exists only in this active Streamlit session in this prototype. Secure accounts, retention controls and deployment privacy safeguards are not yet implemented.": "Ibanga: amateka y'ikiganiro aboneka gusa mu gihe iyi verisiyo ya Streamlit iri gukora. Konti zifite umutekano, uburyo bwo kugenzura igihe amakuru abikwa n'uburyo bwo kurinda ibanga mbere yo gutangaza urubuga ntibirashyirwaho.",
},
"Français": {
    "A fresh start begins here": "Un nouveau départ commence ici",
    "Your future is worth more than your next bet. Find support, rebuild your financial confidence, and reconnect with opportunities that move your life forward.": "Votre avenir vaut davantage que votre prochain pari. Trouvez du soutien, retrouvez confiance dans votre gestion financière et renouez avec des possibilités qui vous feront avancer.",
    "A practical pathway towards a stronger future": "Un parcours concret vers un avenir plus solide",
    "URAFITE is a youth-centred support platform designed to help people affected by harmful gambling take practical steps towards wellbeing, financial stability and new opportunities. You choose where to begin, and you can move between the pathways at your own pace.": "URAFITE est une plateforme d'accompagnement destinée aux jeunes touchés par les conséquences négatives des jeux d'argent. Elle les aide à prendre des mesures concrètes pour leur bien-être, leur stabilité financière et l'accès à de nouvelles possibilités. Vous choisissez par où commencer et avancez à votre rythme.",
    "01 · wellbeing": "01 · Bien-être", "02 · financial confidence": "02 · Confiance financière", "03 · new opportunities": "03 · Nouvelles possibilités",
    "Pause, reflect on urges and triggers, build coping strategies, and identify when human support may help.": "Faites une pause, réfléchissez aux envies de jouer et à leurs déclencheurs, développez des stratégies pour y faire face et identifiez les moments où une aide humaine peut être utile.",
    "Understand your income and expenses, set realistic savings goals, and take manageable financial steps.": "Comprenez vos revenus et vos dépenses, fixez des objectifs d'épargne réalistes et avancez par étapes financières accessibles.",
    "Turn your interests into an action plan for learning, skills development, employment or enterprise.": "Transformez vos centres d'intérêt en plan d'action pour les études, le développement des compétences, l'emploi ou l'entrepreneuriat.",
    "Explore RECOVER →": "Découvrir RECOVER →", "Explore REBUILD →": "Découvrir REBUILD →", "Explore RECONNECT →": "Découvrir RECONNECT →",
    "Start with one small step": "Commencez par une petite étape", "You do not need to solve everything today. Choose the area that feels most important right now.": "Vous n'avez pas à tout résoudre aujourd'hui. Choisissez le domaine qui vous semble le plus important pour le moment.", "Begin with a personal check-in": "Commencer par un bilan personnel", "A message to carry with you": "Un message à garder en tête",
    "Your past losses do not define your worth. Your next decision can help shape a different future.": "Vos pertes passées ne définissent pas votre valeur. Votre prochaine décision peut contribuer à construire un avenir différent.", "URAFITE MVP · A developing support prototype": "URAFITE MVP · Prototype d'accompagnement en développement", "URAFITE complements, but does not replace, qualified professional care. This prototype does not provide clinical diagnosis, crisis monitoring or emergency response.": "URAFITE complète l'accompagnement professionnel qualifié, mais ne le remplace pas. Ce prototype ne fournit ni diagnostic clinique, ni surveillance des crises, ni intervention d'urgence.",
    "Welcome to a judgment-free space. You do not have to have everything figured out today. Take a moment to understand how you are feeling and what you need.": "Bienvenue dans un espace sans jugement. Vous n'avez pas besoin d'avoir toutes les réponses aujourd'hui. Prenez un moment pour comprendre ce que vous ressentez et ce dont vous avez besoin.", "Your responses are used to provide supportive reflections. This exercise is not a clinical assessment or a diagnosis.": "Vos réponses servent à proposer des pistes de réflexion et de soutien. Cet exercice ne constitue ni une évaluation clinique ni un diagnostic.",
    "Choose the description closest to how you feel.": "Choisissez la description qui correspond le mieux à votre ressenti.",
    "What situations or feelings may be influencing you?": "Quelles situations ou émotions peuvent avoir une influence sur vous ?",
    "Choose options": "Choisir des options",
    "Choose an option": "Choisir une option", "Financial pressure": "Pression financière", "Stress or anxiety": "Stress ou anxiété", "Boredom or loneliness": "Ennui ou solitude", "Friends or social influence": "Influence des amis ou de l'entourage", "Gambling advertisements": "Publicités pour les jeux d'argent", "Trying to recover previous losses": "Essayer de récupérer des pertes précédentes", "Feeling disappointed in myself": "Déception envers moi-même", "Excitement or the hope of winning": "Excitation ou espoir de gagner", "Other": "Autre", "I am not sure": "Je ne sais pas",
    "Choose what matters most to you right now.": "Choisissez ce qui compte le plus pour vous en ce moment.", "I want to manage my gambling urges.": "Je souhaite mieux gérer mes envies de jouer.", "I want to understand my gambling behaviour.": "Je souhaite mieux comprendre mon comportement de jeu.", "I want to regain control of my finances.": "Je souhaite reprendre le contrôle de mes finances.", "I want to focus on my education or career.": "Je souhaite me concentrer sur mes études ou ma carrière.", "I want to rebuild my confidence.": "Je souhaite retrouver confiance en moi.", "I would like to speak with a professional.": "Je souhaite parler à un professionnel.", "I would like information about professional support.": "Je souhaite obtenir des informations sur l'accompagnement professionnel.",
    "Thank you for taking this moment for yourself. Recognizing what you are experiencing is meaningful.": "Merci d'avoir pris ce moment pour vous. Reconnaître ce que vous traversez est une étape importante.", "Your personal reflection": "Votre réflexion personnelle", "You described feeling **": "Vous avez indiqué vous sentir **", " today.": "** aujourd'hui.", "**You are experiencing a strong gambling urge.**": "**Vous ressentez une forte envie de jouer.**", "**You have noticed a moderate gambling urge.**": "**Vous avez remarqué une envie de jouer modérée.**", "**You have reported a relatively low gambling urge.**": "**Vous indiquez ressentir une envie de jouer relativement faible.**", "Situations you identified:": "Situations que vous avez identifiées :", "A small step towards change": "Une petite étape vers le changement", "Your chosen priority: ": "Votre priorité : ",
    "You do not have to act on an urge immediately. Consider stepping away from gambling applications or advertisements, moving to a different environment, and contacting someone you trust.": "Vous n'êtes pas obligé d'agir immédiatement sur cette envie. Éloignez-vous des applications et publicités de jeux d'argent, changez d'environnement et contactez une personne de confiance.", "This could be a useful moment to pause and reflect before making a decision. Try identifying what you are feeling and choose an activity that supports your personal goals.": "C'est peut-être le bon moment pour faire une pause et réfléchir avant de décider. Essayez d'identifier ce que vous ressentez et choisissez une activité qui soutient vos objectifs personnels.", "Use this moment to strengthen habits that support your well-being and the future you want to build.": "Profitez de ce moment pour renforcer les habitudes qui favorisent votre bien-être et l'avenir que vous souhaitez construire.", "Try delaying any gambling decision for 15 minutes. During that time, move away from gambling content and do something that helps you feel grounded.": "Essayez de reporter toute décision de jouer de 15 minutes. Pendant ce temps, éloignez-vous des contenus liés aux jeux d'argent et faites une activité qui vous aide à retrouver votre calme.", "Start by identifying one essential financial priority. You can use REBUILD to create a realistic budget and work towards it.": "Commencez par identifier une priorité financière essentielle. Vous pouvez utiliser REBUILD pour établir un budget réaliste et avancer vers cet objectif.", "Seeking professional support is a positive step. You deserve to be heard and supported by someone qualified to help.": "Demander l'aide d'un professionnel est une démarche positive. Vous méritez d'être écouté et accompagné par une personne qualifiée.", "You deserve support": "Vous méritez du soutien", "If you are experiencing severe distress, thoughts of suicide, or immediate danger, do not rely on this check-in. Contact emergency services, a qualified professional, or someone you trust who can help you access immediate care.": "Si vous traversez une détresse intense, avez des pensées suicidaires ou êtes en danger immédiat, ne comptez pas uniquement sur ce bilan. Contactez les services d'urgence, un professionnel qualifié ou une personne de confiance qui pourra vous aider à obtenir une aide immédiate.",
    "You do not need to recover everything at once. Start by understanding your finances, setting realistic goals, and taking small steps towards financial stability.": "Vous n'avez pas à tout récupérer d'un seul coup. Commencez par comprendre vos finances, fixer des objectifs réalistes et avancer par petites étapes vers la stabilité financière.", "This is a personal budgeting and goal-tracking tool, not professional financial advice.": "Cet outil aide à établir un budget personnel et à suivre des objectifs. Il ne remplace pas les conseils d'un professionnel de la finance.", "Your essential and personal expenses": "Vos dépenses essentielles et personnelles", "Food and essential needs (RWF)": "Alimentation et besoins essentiels (RWF)", "Accommodation (RWF)": "Logement (RWF)", "Transport (RWF)": "Transport (RWF)", "Education and personal development (RWF)": "Études et développement personnel (RWF)", "Other expenses (RWF)": "Autres dépenses (RWF)", "Money you have actually saved (RWF)": "Épargne réellement constituée (RWF)", "Your financial recovery goal": "Votre objectif de reconstruction financière", "How much would you like to save? (RWF)": "Quel montant souhaitez-vous épargner ? (RWF)", "When would you like to achieve this goal?": "Quand souhaitez-vous atteindre cet objectif ?", "1 month": "1 mois", "3 months": "3 mois", "6 months": "6 mois", "12 months": "12 mois", "Review my financial plan": "Examiner mon plan financier", "Your recorded expenses exceed your income. This may be a good opportunity to review your financial priorities and consider additional support.": "Les dépenses que vous avez indiquées dépassent vos revenus. Vous pourriez revoir vos priorités financières et envisager un accompagnement complémentaire.", "Understanding your finances is an important step towards making informed decisions.": "Comprendre vos finances est une étape importante pour prendre des décisions éclairées.", "Actual savings recorded": "Épargne réellement enregistrée", "Remaining income is not automatically counted as savings. Only money you have actually saved is recorded here.": "Le revenu restant n'est pas automatiquement considéré comme une épargne. Seules les sommes réellement mises de côté sont enregistrées ici.", "Your personal savings journey": "Votre parcours d'épargne", "Your goal: **": "Votre objectif : **", " within **": " en **", "You have achieved ": "Vous avez atteint ", "% of your savings goal.": "% de votre objectif d'épargne.", "Amount remaining: **": "Montant restant : **", "Set a savings target whenever you feel ready.": "Fixez un objectif d'épargne lorsque vous vous sentirez prêt.", "What are you rebuilding towards?": "Quel objectif souhaitez-vous atteindre ?", "Choose a goal that matters to you.": "Choisissez un objectif qui compte pour vous.", "Paying my education fees": "Payer mes frais de scolarité", "Building personal savings": "Constituer une épargne personnelle", "Starting a small business": "Créer une petite entreprise", "Developing my professional skills": "Développer mes compétences professionnelles", "Achieving financial independence": "Atteindre l'indépendance financière", "Supporting my family": "Soutenir ma famille", "Another personal goal": "Un autre objectif personnel", "Your chosen priority: ": "Votre priorité : ", "A reminder from URAFITE": "Un rappel d'URAFITE", "Your financial situation today does not determine your financial future. You do not have to rebuild everything immediately. Every realistic step towards your goals matters.": "Votre situation financière actuelle ne détermine pas votre avenir financier. Vous n'avez pas à tout reconstruire immédiatement. Chaque étape réaliste vers vos objectifs compte.", "Demonstration version: financial information is held in the current Streamlit session and is not yet stored in a permanent personal account.": "Version de démonstration : les informations financières restent dans la session Streamlit en cours et ne sont pas encore enregistrées dans un compte personnel permanent.",
    "A fresh start is not just about leaving harmful habits behind. It is also about discovering new opportunities, developing your potential, and building a future you can be proud of.": "Un nouveau départ ne consiste pas seulement à abandonner des habitudes néfastes. Il s'agit aussi de découvrir de nouvelles possibilités, de développer votre potentiel et de construire un avenir dont vous serez fier.", "Your future is still full of possibilities. Let's identify one meaningful step you can take today.": "Votre avenir reste plein de possibilités. Identifions une étape utile que vous pouvez franchir aujourd'hui.", "Discover your future": "Découvrez votre avenir", "Tell us what you would like to work towards. You can select more than one interest.": "Indiquez ce que vous souhaitez accomplir. Vous pouvez sélectionner plusieurs centres d'intérêt.", "What opportunities interest you?": "Quelles possibilités vous intéressent ?", "What is your current education or career stage?": "Quel est votre niveau d'études ou votre situation professionnelle ?", "Vocational training student": "En formation professionnelle", "What would you most like to achieve?": "Que souhaitez-vous accomplir en priorité ?", "Discover my opportunities": "Découvrir mes possibilités", "Opportunities for your next chapter": "Des possibilités pour votre prochain chapitre", "Your current goal: ": "Votre objectif actuel : ", "Your education or career stage: ": "Votre niveau d'études ou votre situation professionnelle : ", "The opportunities below are illustrative examples for the MVP. They are not verified live vacancies, scholarships, or open programmes.": "Les possibilités ci-dessous sont des exemples illustratifs du MVP. Il ne s'agit pas d'offres d'emploi, de bourses ou de programmes actuellement ouverts et vérifiés.", "Scholarship Discovery": "Recherche de bourses", "Explore scholarship pathways, admission requirements, application preparation, and opportunities for further study.": "Explorez les possibilités de bourses, les conditions d'admission, la préparation des candidatures et les possibilités de poursuivre vos études.", "Prepare a list of three programmes I would like to explore.": "Préparer une liste de trois programmes à examiner.", "Digital Skills Development": "Développement des compétences numériques", "Build practical skills in programming, data analysis, digital tools, and other areas of technology.": "Développez des compétences pratiques en programmation, analyse de données, outils numériques et autres domaines technologiques.", "Choose one digital skill and identify a learning resource.": "Choisir une compétence numérique et trouver une ressource pour l'apprendre.", "Vocational Skills Pathway": "Parcours de formation professionnelle", "Explore practical and technical training that can support employment or self-employment.": "Découvrez des formations pratiques et techniques qui peuvent favoriser l'emploi ou l'activité indépendante.", "Identify one vocational skill relevant to my interests.": "Identifier une compétence professionnelle correspondant à mes intérêts.", "Employment Readiness": "Préparation à l'emploi", "Strengthen your CV, prepare for interviews, and explore internship and employment pathways.": "Améliorez votre CV, préparez vos entretiens et explorez les possibilités de stage et d'emploi.", "Update my CV and identify one opportunity to apply for.": "Mettre à jour mon CV et identifier une possibilité à laquelle postuler.", "Entrepreneurship Journey": "Parcours entrepreneurial", "Explore business ideas, entrepreneurship training, financial planning, and enterprise development.": "Explorez des idées d'entreprise, des formations en entrepreneuriat, la planification financière et le développement d'activités.", "Write down one business idea and the problem it addresses.": "Décrire une idée d'entreprise et le problème auquel elle répond.", "Leadership and Personal Growth": "Leadership et développement personnel", "Explore mentorship, leadership development, communication, and personal growth opportunities.": "Découvrez le mentorat, le développement du leadership, la communication et les possibilités de développement personnel.", "Identify one personal development goal for this month.": "Définir un objectif de développement personnel pour ce mois.", "You have not selected any interests yet. Please select at least one interest above to discover suggested opportunities.": "Vous n'avez pas encore sélectionné de centre d'intérêt. Choisissez-en au moins un ci-dessus pour découvrir des pistes adaptées.", "Turn an opportunity into action": "Transformer une possibilité en action", "Big changes begin with small, realistic steps. Choose one action you are willing to take.": "Les grands changements commencent par de petites étapes réalistes. Choisissez une action que vous êtes prêt à entreprendre.", "My next step": "Ma prochaine étape", "Save my next step": "Enregistrer ma prochaine étape", "Your next step has been added to your action plan.": "Votre prochaine étape a été ajoutée à votre plan d'action.", "My personal action plan": "Mon plan d'action personnel", "You do not have to change everything today. Focus on taking this one step forward.": "Vous n'avez pas à tout changer aujourd'hui. Concentrez-vous sur cette étape.", "A message for your journey": "Un message pour votre parcours", "Your past mistakes do not erase your potential.": "Vos erreurs passées n'effacent pas votre potentiel.", "Every meaningful new beginning starts with one step. Keep moving forward.": "Tout nouveau départ important commence par une étape. Continuez d'avancer.", "Your next chapter starts with a decision. Select your interests above to discover possible pathways.": "Votre prochain chapitre commence par une décision. Sélectionnez vos centres d'intérêt ci-dessus pour découvrir des parcours possibles.",
    "You deserve support from a real person.": "Vous méritez le soutien d'une personne réelle.", "Digital tools can help you reflect, but some situations need human care. A qualified counsellor, mental-health professional or healthcare provider can listen, help you consider your options and guide you towards appropriate support.": "Les outils numériques peuvent vous aider à réfléchir, mais certaines situations nécessitent un accompagnement humain. Un conseiller qualifié, un professionnel de la santé mentale ou un prestataire de soins peut vous écouter, examiner les options avec vous et vous orienter vers un soutien adapté.", "URAFITE has not yet verified a directory of local referral providers. We will not display unconfirmed phone numbers, organisations or emergency contacts.": "URAFITE n'a pas encore vérifié de répertoire de prestataires locaux. Nous n'afficherons aucun numéro de téléphone, organisme ou contact d'urgence non confirmé.", "When to seek support": "Quand demander de l'aide", "Ongoing support": "Accompagnement régulier", "Consider speaking with a qualified professional if gambling, stress, debt, sleep problems or emotional distress are affecting your daily life.": "Envisagez de consulter un professionnel qualifié si les jeux d'argent, le stress, les dettes, les troubles du sommeil ou la détresse émotionnelle affectent votre vie quotidienne.", "Immediate danger": "Danger immédiat", "If you may hurt yourself or someone else, or cannot keep yourself safe, seek immediate in-person help through local emergency services or the nearest hospital.": "Si vous risquez de vous faire du mal ou de faire du mal à quelqu'un, ou si vous ne pouvez pas assurer votre sécurité, demandez immédiatement une aide en personne auprès des services d'urgence locaux ou de l'hôpital le plus proche.",
    "AI-assisted recovery and opportunity support": "Accompagnement au rétablissement et aux possibilités avec l'aide de l'IA", "Choose your preferred language": "Choisissez votre langue préférée", "Language / Ururimi / Langue": "Langue", "Share what is on your mind...": "Exprimez ce que vous avez à l'esprit...", "Start a new conversation": "Commencer une nouvelle conversation", "You can switch the interface language in the sidebar. Avoid sharing passwords, ID numbers or other highly sensitive information.": "Vous pouvez changer la langue de l'interface dans la barre latérale. Évitez de partager vos mots de passe, numéros d'identification ou autres informations très sensibles.", "Responses are predefined and may not understand every message. For urgent or complex needs, seek help from a qualified person.": "Les réponses sont prédéfinies et peuvent ne pas comprendre tous les messages. Pour les situations urgentes ou complexes, demandez l'aide d'une personne qualifiée.", "Privacy: conversation history exists only in this active Streamlit session in this prototype. Secure accounts, retention controls and deployment privacy safeguards are not yet implemented.": "Confidentialité : dans ce prototype, l'historique de conversation existe uniquement pendant la session Streamlit active. Les comptes sécurisés, les contrôles de conservation et les protections nécessaires au déploiement ne sont pas encore mis en place.",
}
}
for _lang_name, _translations in EXTRA_LANGUAGE_TEXT.items():
    LANGUAGE_TEXT[_lang_name].update(_translations)

# ----------------------------------------------------------------------------
# LANGUAGE AUDIT PATCH: complete visible UI coverage for all three languages.
# Keep internal option values in English; translate only their presentation.
# ----------------------------------------------------------------------------
_LANGUAGE_AUDIT = {
    "Kinyarwanda": {
        "Could not initialise the Supabase connection. Check your project URL and publishable key.": "Ntibyashobotse guhuza na Supabase. Genza aderesi ya project n'urufunguzo rwa publishable.",
        "URAFITE needs its Supabase connection settings before you can sign in.": "URAFITE ikeneye amakuru yo kuyihuza na Supabase mbere y'uko winjira.",
        "Create `.streamlit/secrets.toml` using the supplied `secrets.toml.example` file, then add your Project URL and publishable key. Never use the Supabase secret/service-role key here.": "Kora dosiye `.streamlit/secrets.toml` uhereye kuri `secrets.toml.example`, wongeremo Project URL n'urufunguzo rwa publishable. Ntukigere ukoresha secret key cyangwa service-role key ya Supabase hano.",
        "Your session could not be verified. Please sign in again.": "Ntitwashoboye kwemeza ko winjiye. Ongera winjire.",
        "Return to sign in": "Subira ku kwinjira",
        "Your account is active. Your profile permissions are being prepared. Please refresh in a moment or contact the URAFITE administrator if this continues.": "Konti yawe irakora. Uburenganzira bwa konti burimo gutegurwa. Ongera ufungure urupapuro nyuma y'akanya; niba bikomeje, vugana n'umuyobozi wa URAFITE.",
        "Super Administrator": "Umuyobozi mukuru wa sisitemu",
        "Administrator": "Umuyobozi",
        "Sign out": "Sohoka",
        "### Three pathways. One renewed future.": "### Inzira eshatu. Ejo hazaza hashya.",
        "#### A message to carry with you": "#### Ubutumwa wahorana mu rugendo rwawe",
        "> Your past losses do not define your worth. Your next decision can help shape a different future.": "> Igihombo wagize ntikigena agaciro kawe. Icyemezo ufata gikurikira gishobora kugufasha kubaka ejo hazaza hatandukanye.",
        "**Situations you identified:**": "**Ibihe cyangwa impamvu wagaragaje:**",
        "Consider reflecting on what happened before your last gambling session. What were you feeling, and what were you hoping gambling would change?": "Tekereza ku byabaye mbere y'uko uheruka gukina urusimbi. Wari wiyumva ute, kandi wifuzaga ko urusimbi ruhindura iki?",
        "Think about one educational or professional goal you would like to pursue. Visit RECONNECT to explore possible opportunities.": "Tekereza ku ntego imwe y'amashuri cyangwa y'akazi wifuza kugeraho. Jya muri RECONNECT urebe amahirwe ashoboka.",
        "Write down one ability, achievement, or personal quality you value about yourself. Your past difficulties do not define your worth.": "Andika ubushobozi bumwe, ibyo wagezeho cyangwa imico myiza wishimira kuri wowe. Ibibazo wanyuzemo ntibigena agaciro kawe.",
        "You can seek support from a qualified mental-health professional or counsellor. Open Professional Support in the sidebar for available support information.": "Ushobora gusaba ubufasha inzobere mu buzima bwo mu mutwe cyangwa umujyanama ubifitiye ubumenyi. Fungura ahitwa Ubufasha bw'inzobere mu rutonde rwo ku ruhande kugira ngo umenye amakuru ahari.",
        "**Remember:** You do not need to rebuild your entire life in one day. One thoughtful decision can be the beginning of a different direction.": "**Wibuke:** Ntugomba kongera kubaka ubuzima bwawe bwose mu munsi umwe. Icyemezo kimwe gifashwe utekereje gishobora kuba intangiriro y'icyerekezo gishya.",
        "These reflections are based on predefined guidance, not an AI clinical assessment. They do not determine your mental-health or suicide risk.": "Ibi bitekerezo bishingiye ku butumwa bwateguwe mbere; si isuzuma ry'ubuvuzi rikozwe na AI. Ntibipima ibyago bijyanye n'ubuzima bwo mu mutwe cyangwa kwiyahura.",
        "**Your essential and personal expenses**": "**Amafaranga y'ibikenewe by'ibanze n'ibindi ukoresha**",
        "**Your financial recovery goal**": "**Intego yawe yo kongera gutunganya imari**",
        "### A reminder from URAFITE": "### Ubutumwa URAFITE ikwibutsa",
        "### 🎯 My personal action plan": "### 🎯 Gahunda y'ibikorwa byanjye",
        "URAFITE — Reclaim Your Future.": "URAFITE — Subirana ejo hazaza hawe.",
        "Prototype transparency: responses are selected from predefined guidance. The companion may misunderstand messages and cannot monitor your safety or replace a qualified professional.": "Ibisobanuro ku cyitegererezo: ibisubizo bitoranywa mu butumwa bwateguwe mbere. Umufasha ashobora kutumva neza ubutumwa bwawe; ntashobora gukurikirana umutekano wawe cyangwa gusimbura inzobere.",
        "### 💬 Your conversation": "### 💬 Ikiganiro cyawe",
        "### When to seek support": "### Igihe wakwiriye gusaba ubufasha",
        "#### 🌿 Ongoing support": "#### 🌿 Ubufasha buhoraho",
        "#### 🆘 Immediate danger": "#### 🆘 Akaga kihutirwa",
        "### Preparing to speak with someone": "### Kwitegura kuganira n'umuntu",
        "You may find it helpful to:": "Dore ibyo ushobora gusanga bigufasha:",
        "- Describe what has been happening, in your own words.\n- Explain how it is affecting your finances, relationships, studies or wellbeing.\n- Ask about confidentiality, costs and available support options.\n- Take a trusted person with you if that would make the conversation easier.": "- Sobanura mu magambo yawe ibyakubayeho.\n- Vuga uko bigira ingaruka ku mafaranga, imibanire, amasomo cyangwa imibereho yawe.\n- Baza ibijyanye n'ibanga, ikiguzi n'ubufasha bushoboka.\n- Niba byagufasha, jyana n'umuntu wiringira.",
        "Before public launch, URAFITE should add a locally reviewed and verified referral directory, with clear consent and safeguarding procedures.": "Mbere yo gushyirwa ku mugaragaro, URAFITE igomba kongeramo urutonde rw'abatanga ubufasha rwagenzuwe n'inzobere zo mu karere, hamwe n'uburyo busobanutse bwo kwemera no kurinda abakoresha.",
        "English": "Icyongereza", "Kinyarwanda": "Ikinyarwanda", "Français": "Igifaransa",
        "Speech playback is not supported by this browser.": "Iyi mushakisha ntishobora gusoma igisubizo mu ijwi.",
        "0 means no urge; 10 means an extremely strong urge.": "0 bivuze ko nta cyifuzo gihari; 10 bivuze ko icyifuzo gikomeye cyane.",
        "Use the navigation menu to open ": "Koresha urutonde rwo kujyamo kugira ngo ufungure ",
    },
    "Français": {
        "Could not initialise the Supabase connection. Check your project URL and publishable key.": "Impossible d'établir la connexion à Supabase. Vérifiez l'URL du projet et la clé publishable.",
        "URAFITE needs its Supabase connection settings before you can sign in.": "URAFITE a besoin de ses paramètres de connexion à Supabase avant que vous puissiez vous connecter.",
        "Create `.streamlit/secrets.toml` using the supplied `secrets.toml.example` file, then add your Project URL and publishable key. Never use the Supabase secret/service-role key here.": "Créez `.streamlit/secrets.toml` à partir du fichier fourni `secrets.toml.example`, puis ajoutez l'URL du projet et la clé publishable. N'utilisez jamais ici la clé secrète ou la clé service_role de Supabase.",
        "Your session could not be verified. Please sign in again.": "Votre session n'a pas pu être vérifiée. Veuillez vous reconnecter.",
        "Return to sign in": "Retour à la connexion",
        "Your account is active. Your profile permissions are being prepared. Please refresh in a moment or contact the URAFITE administrator if this continues.": "Votre compte est actif. Les autorisations de votre profil sont en cours de préparation. Actualisez la page dans un instant ou contactez l'administrateur URAFITE si le problème persiste.",
        "Super Administrator": "Super administrateur",
        "Administrator": "Administrateur",
        "Sign out": "Se déconnecter",
        "### Three pathways. One renewed future.": "### Trois parcours. Un avenir renouvelé.",
        "#### A message to carry with you": "#### Un message à garder avec vous",
        "> Your past losses do not define your worth. Your next decision can help shape a different future.": "> Vos pertes passées ne définissent pas votre valeur. Votre prochaine décision peut contribuer à construire un avenir différent.",
        "**Situations you identified:**": "**Situations que vous avez identifiées :**",
        "Consider reflecting on what happened before your last gambling session. What were you feeling, and what were you hoping gambling would change?": "Prenez un moment pour réfléchir à ce qui s'est passé avant votre dernière session de jeu. Que ressentiez-vous et qu'espériez-vous changer en jouant ?",
        "Think about one educational or professional goal you would like to pursue. Visit RECONNECT to explore possible opportunities.": "Pensez à un objectif d'études ou de carrière que vous aimeriez poursuivre. Consultez RECONNECT pour explorer les possibilités.",
        "Write down one ability, achievement, or personal quality you value about yourself. Your past difficulties do not define your worth.": "Notez une compétence, une réussite ou une qualité personnelle que vous appréciez chez vous. Vos difficultés passées ne définissent pas votre valeur.",
        "You can seek support from a qualified mental-health professional or counsellor. Open Professional Support in the sidebar for available support information.": "Vous pouvez demander l'aide d'un professionnel qualifié de la santé mentale ou d'un conseiller. Ouvrez Soutien professionnel dans le menu latéral pour consulter les informations disponibles.",
        "**Remember:** You do not need to rebuild your entire life in one day. One thoughtful decision can be the beginning of a different direction.": "**À retenir :** vous n'avez pas à reconstruire toute votre vie en une journée. Une décision réfléchie peut marquer le début d'une nouvelle direction.",
        "These reflections are based on predefined guidance, not an AI clinical assessment. They do not determine your mental-health or suicide risk.": "Ces réflexions reposent sur des conseils prédéfinis et non sur une évaluation clinique par IA. Elles ne déterminent pas votre niveau de risque en matière de santé mentale ou de suicide.",
        "**Your essential and personal expenses**": "**Vos dépenses essentielles et personnelles**",
        "**Your financial recovery goal**": "**Votre objectif de rétablissement financier**",
        "### A reminder from URAFITE": "### Un rappel d'URAFITE",
        "### 🎯 My personal action plan": "### 🎯 Mon plan d'action personnel",
        "URAFITE — Reclaim Your Future.": "URAFITE — Reprenez votre avenir.",
        "Prototype transparency: responses are selected from predefined guidance. The companion may misunderstand messages and cannot monitor your safety or replace a qualified professional.": "Transparence du prototype : les réponses sont sélectionnées parmi des conseils prédéfinis. L'assistant peut mal comprendre vos messages et ne peut ni surveiller votre sécurité ni remplacer un professionnel qualifié.",
        "### 💬 Your conversation": "### 💬 Votre conversation",
        "### When to seek support": "### Quand demander de l'aide",
        "#### 🌿 Ongoing support": "#### 🌿 Accompagnement continu",
        "#### 🆘 Immediate danger": "#### 🆘 Danger immédiat",
        "### Preparing to speak with someone": "### Se préparer à parler avec quelqu'un",
        "You may find it helpful to:": "Les démarches suivantes peuvent vous aider :",
        "- Describe what has been happening, in your own words.\n- Explain how it is affecting your finances, relationships, studies or wellbeing.\n- Ask about confidentiality, costs and available support options.\n- Take a trusted person with you if that would make the conversation easier.": "- Décrivez ce qui se passe, avec vos propres mots.\n- Expliquez les effets sur vos finances, vos relations, vos études ou votre bien-être.\n- Posez des questions sur la confidentialité, les coûts et les possibilités d'accompagnement.\n- Si cela vous aide, faites-vous accompagner par une personne de confiance.",
        "Before public launch, URAFITE should add a locally reviewed and verified referral directory, with clear consent and safeguarding procedures.": "Avant son lancement public, URAFITE devrait ajouter un répertoire d'orientation vérifié et examiné localement, avec des procédures claires de consentement et de protection.",
        "English": "Anglais", "Kinyarwanda": "Kinyarwanda", "Français": "Français",
        "Speech playback is not supported by this browser.": "La lecture audio n'est pas prise en charge par ce navigateur.",
        "0 means no urge; 10 means an extremely strong urge.": "0 signifie aucune envie ; 10 signifie une envie extrêmement forte.",
        "Use the navigation menu to open ": "Utilisez le menu de navigation pour ouvrir ",
    }
}

# Administration module translations (user-facing labels).
_ADMIN_TRANSLATIONS = {'Kinyarwanda': {'Administration': 'Ubuyobozi', 'Impact & Evidence': 'Ingaruka n‟Ibimenyetso', 'Opportunity Manager': 'Imicungire y‟Amahirwe', 'Heal and Learn Centre Manager': 'Imicungire y‟Ikigo cyo Gukira no Kwigira', 'Grant & Programme Tracker': 'Gukurikirana Inkunga na Porogaramu', 'Overview': 'Incamake', 'Registered accounts': 'Konti zanditswe', 'Published opportunities': 'Amahirwe yatangajwe', 'Published learning resources': 'Ibikoresho byo kwiga byatangajwe', 'Recorded platform events': 'Ibikorwa byanditswe ku rubuga', 'Recent registrations': 'Abiyandikishije vuba', 'Activity by type': 'Ibikorwa hakurikijwe ubwoko', 'No activity records yet.': 'Nta bikorwa biranditswe kugeza ubu.', 'This dashboard reports platform activity, not clinical recovery outcomes.': 'Iyi mibare igaragaza imikoreshereze y’urubuga, si ibipimo byemeza ko umuntu yakize.', 'Add an opportunity': 'Ongeraho amahirwe', 'Title': 'Umutwe', 'Category': 'Icyiciro', 'Organisation': 'Umuryango cyangwa ikigo', 'Country': 'Igihugu', 'Description': 'Ibisobanuro', 'Eligibility': 'Ibisabwa kugira ngo umuntu abyemererwe', 'Application URL': 'Aho gusabira', 'Deadline': 'Itariki ntarengwa', 'Save opportunity': 'Bika amahirwe', 'Opportunity saved.': 'Amahirwe yabitswe.', 'Current opportunities': 'Amahirwe ahari', 'No opportunities found.': 'Nta mahirwe araboneka.', 'Add a learning resource': 'Ongeraho igikoresho cyo kwiga', 'Resource type': 'Ubwoko bw’igikoresho', 'Language': 'Ururimi', 'Contributor name': 'Amazina y’uwatanze igikoresho', 'Professional credentials': 'Impamyabumenyi n’uburambe by’umwuga', 'Content URL': 'Aho igikoresho kiri', 'Submit for review': 'Ohereza kugira ngo gisuzumwe', 'Resource submitted for review.': 'Igikoresho cyo kwiga cyoherejwe kugira ngo gisuzumwe.', 'Current learning resources': 'Ibikoresho byo kwiga bihari', 'No learning resources found.': 'Nta bikoresho byo kwiga biraboneka.', 'Add a grant or programme': 'Ongeraho inkunga cyangwa porogaramu', 'Funder': 'Utanga inkunga', 'Project name': 'Izina ry’umushinga', 'Award amount (RWF)': 'Amafaranga yatanzwe (RWF)', 'Start date': 'Itariki yo gutangira', 'End date': 'Itariki yo kurangira', 'Target participants': 'Abagenerwabikorwa bateganyijwe', 'Reporting deadline': 'Itariki ntarengwa yo gutanga raporo', 'Save grant record': 'Bika amakuru y’inkunga', 'Grant record saved.': 'Amakuru y’inkunga yabitswe.', 'Grant and programme records': 'Amakuru y’inkunga na porogaramu', 'No grant records yet.': 'Nta makuru y’inkunga arahari.', 'Export activity summary (CSV)': 'Kuramo incamake y’ibikorwa (CSV)', 'Export grants (CSV)': 'Kuramo amakuru y’inkunga (CSV)', 'Status': 'Imiterere', 'Draft': 'Inyandiko itaratangazwa', 'Published': 'Byatangajwe', 'Pending review': 'Bitegereje gusuzumwa', 'Video': 'Video', 'Article': 'Ingingo', 'Post': 'Ubutumwa', 'Mentoring': 'Ubujyanama', 'Scholarship': 'Buruse', 'Employment': 'Akazi', 'Internship': 'Stage', 'Training': 'Amahugurwa', 'Entrepreneurship': 'Kwihangira imirimo', 'Mentorship': 'Ubujyanama', 'Other': 'Ibindi', 'Select a category': 'Hitamo icyiciro', 'Select a language': 'Hitamo ururimi', 'English': 'Icyongereza', 'Kinyarwanda': 'Ikinyarwanda', 'French': 'Igifaransa', 'Monthly / quarterly reporting should be based on verified records.': 'Raporo za buri kwezi cyangwa igihembwe zigomba gushingira ku makuru yagenzuwe.'}, 'Français': {'Administration': 'Administration', 'Impact & Evidence': 'Impact et preuves', 'Opportunity Manager': 'Gestion des opportunités', 'Heal and Learn Centre Manager': 'Gestion du Heal and Learn Centre', 'Grant & Programme Tracker': 'Suivi des subventions et programmes', 'Overview': 'Vue d’ensemble', 'Registered accounts': 'Comptes inscrits', 'Published opportunities': 'Opportunités publiées', 'Published learning resources': 'Ressources pédagogiques publiées', 'Recorded platform events': 'Activités enregistrées sur la plateforme', 'Recent registrations': 'Inscriptions récentes', 'Activity by type': 'Activité par catégorie', 'No activity records yet.': 'Aucune activité enregistrée pour le moment.', 'This dashboard reports platform activity, not clinical recovery outcomes.': 'Ce tableau présente l’utilisation de la plateforme, et non des résultats cliniques de rétablissement.', 'Add an opportunity': 'Ajouter une opportunité', 'Title': 'Titre', 'Category': 'Catégorie', 'Organisation': 'Organisation', 'Country': 'Pays', 'Description': 'Description', 'Eligibility': 'Critères d’éligibilité', 'Application URL': 'Lien de candidature', 'Deadline': 'Date limite', 'Save opportunity': 'Enregistrer l’opportunité', 'Opportunity saved.': 'Opportunité enregistrée.', 'Current opportunities': 'Opportunités actuelles', 'No opportunities found.': 'Aucune opportunité trouvée.', 'Add a learning resource': 'Ajouter une ressource pédagogique', 'Resource type': 'Type de ressource', 'Language': 'Langue', 'Contributor name': 'Nom du contributeur', 'Professional credentials': 'Qualifications professionnelles', 'Content URL': 'Lien du contenu', 'Submit for review': 'Soumettre pour examen', 'Resource submitted for review.': 'Ressource soumise pour examen.', 'Current learning resources': 'Ressources pédagogiques actuelles', 'No learning resources found.': 'Aucune ressource pédagogique trouvée.', 'Add a grant or programme': 'Ajouter une subvention ou un programme', 'Funder': 'Organisme financeur', 'Project name': 'Nom du projet', 'Award amount (RWF)': 'Montant accordé (RWF)', 'Start date': 'Date de début', 'End date': 'Date de fin', 'Target participants': 'Nombre de participants visé', 'Reporting deadline': 'Date limite du rapport', 'Save grant record': 'Enregistrer la subvention', 'Grant record saved.': 'Subvention enregistrée.', 'Grant and programme records': 'Dossiers des subventions et programmes', 'No grant records yet.': 'Aucun dossier de subvention pour le moment.', 'Export activity summary (CSV)': 'Exporter le résumé des activités (CSV)', 'Export grants (CSV)': 'Exporter les subventions (CSV)', 'Status': 'Statut', 'Draft': 'Brouillon', 'Published': 'Publié', 'Pending review': 'En attente de validation', 'Video': 'Vidéo', 'Article': 'Article', 'Post': 'Publication', 'Mentoring': 'Mentorat', 'Scholarship': 'Bourse', 'Employment': 'Emploi', 'Internship': 'Stage', 'Training': 'Formation', 'Entrepreneurship': 'Entrepreneuriat', 'Mentorship': 'Mentorat', 'Other': 'Autre', 'Select a category': 'Choisir une catégorie', 'Select a language': 'Choisir une langue', 'English': 'Anglais', 'Kinyarwanda': 'Kinyarwanda', 'French': 'Français', 'Monthly / quarterly reporting should be based on verified records.': 'Les rapports mensuels et trimestriels doivent reposer sur des données vérifiées.'}}
for _lang, _items in _ADMIN_TRANSLATIONS.items():
    LANGUAGE_TEXT[_lang].update(_items)
for _lang, _items in {'Kinyarwanda': {'Heal and Learn Centre': 'Ikigo cyo Gukira no Kwigira', 'All categories': 'Ibyiciro byose', 'Filter by category': 'Shungura hakurikijwe icyiciro', 'Open resource': 'Fungura igikoresho', 'Contributor': 'Uwagitanze', 'Learning resources are temporarily unavailable.': 'Ibikoresho byo kwiga ntibiboneka muri aka kanya.', 'No approved resources are available in your selected language yet.': 'Nta bikoresho byemejwe biri mu rurimi wahisemo kugeza ubu.', 'You do not have permission to access this area.': 'Nta burenganzira ufite bwo kugera aha.', 'Could not retrieve this information from Supabase.': 'Ntibyashobotse kubona aya makuru muri Supabase.', 'Your role': 'Uruhare rwawe', 'Use the administration pages in the navigation menu to manage opportunities, learning resources, grants and impact reports.': 'Koresha ibice by’ubuyobozi biri ku rutonde kugira ngo ucunge amahirwe, ibikoresho byo kwiga, inkunga na raporo.', 'Title and description are required.': 'Umutwe n’ibisobanuro birakenewe.', 'Could not save the opportunity. Check the database migration and permissions.': 'Ntibyashobotse kubika amahirwe. Genza niba imbonerahamwe n’uburenganzira byateguwe neza.', 'Select an opportunity to update': 'Hitamo amahirwe ushaka kuvugurura', 'New status': 'Imiterere mishya', 'Update opportunity status': 'Vugurura imiterere y’amahirwe', 'Opportunity status updated.': 'Imiterere y’amahirwe yavuguruwe.', 'Could not update opportunity.': 'Ntibyashobotse kuvugurura amahirwe.', 'Title, category and description are required.': 'Umutwe, icyiciro n’ibisobanuro birakenewe.', 'Could not submit the resource. Check database permissions.': 'Ntibyashobotse kohereza igikoresho. Genza uburenganzira bwo kugera ku makuru.', 'Select a resource to review': 'Hitamo igikoresho cyo gusuzuma', 'Review decision': 'Icyemezo cyo gusuzuma', 'Save review decision': 'Bika icyemezo cyo gusuzuma', 'Resource status updated.': 'Imiterere y’igikoresho yavuguruwe.', 'Could not update resource.': 'Ntibyashobotse kuvugurura igikoresho.', 'Funder and project name are required.': 'Utanga inkunga n’izina ry’umushinga birakenewe.', 'Could not save grant record. Run the latest database migration.': 'Ntibyashobotse kubika amakuru y’inkunga. Banza ukoreshe SQL migration iheruka.'}, 'Français': {'Heal and Learn Centre': 'Centre Heal and Learn', 'All categories': 'Toutes les catégories', 'Filter by category': 'Filtrer par catégorie', 'Open resource': 'Ouvrir la ressource', 'Contributor': 'Contributeur', 'Learning resources are temporarily unavailable.': 'Les ressources pédagogiques sont temporairement indisponibles.', 'No approved resources are available in your selected language yet.': 'Aucune ressource approuvée n’est encore disponible dans la langue sélectionnée.', 'You do not have permission to access this area.': 'Vous n’êtes pas autorisé à accéder à cette section.', 'Could not retrieve this information from Supabase.': 'Impossible de récupérer ces informations depuis Supabase.', 'Your role': 'Votre rôle', 'Use the administration pages in the navigation menu to manage opportunities, learning resources, grants and impact reports.': 'Utilisez les pages d’administration pour gérer les opportunités, les ressources pédagogiques, les subventions et les rapports d’impact.', 'Title and description are required.': 'Le titre et la description sont obligatoires.', 'Could not save the opportunity. Check the database migration and permissions.': 'Impossible d’enregistrer l’opportunité. Vérifiez la migration et les autorisations de la base de données.', 'Select an opportunity to update': 'Sélectionner une opportunité à modifier', 'New status': 'Nouveau statut', 'Update opportunity status': 'Mettre à jour le statut', 'Opportunity status updated.': 'Statut de l’opportunité mis à jour.', 'Could not update opportunity.': 'Impossible de mettre à jour l’opportunité.', 'Title, category and description are required.': 'Le titre, la catégorie et la description sont obligatoires.', 'Could not submit the resource. Check database permissions.': 'Impossible de soumettre la ressource. Vérifiez les autorisations de la base de données.', 'Select a resource to review': 'Sélectionner une ressource à examiner', 'Review decision': 'Décision de validation', 'Save review decision': 'Enregistrer la décision', 'Resource status updated.': 'Statut de la ressource mis à jour.', 'Could not update resource.': 'Impossible de mettre à jour la ressource.', 'Funder and project name are required.': 'Le financeur et le nom du projet sont obligatoires.', 'Could not save grant record. Run the latest database migration.': 'Impossible d’enregistrer la subvention. Exécutez la dernière migration SQL.'}}.items():
    LANGUAGE_TEXT[_lang].update(_items)

for _language_name, _audit_dictionary in _LANGUAGE_AUDIT.items():
    LANGUAGE_TEXT[_language_name].update(_audit_dictionary)


def _urafite_translate(value):
    """Translate visible text while keeping internal option values unchanged."""
    if not isinstance(value, str):
        return value
    language = st.session_state.get("urafite_language", "English")
    if language == "English":
        return value
    dictionary = LANGUAGE_TEXT.get(language, {})
    # Exact matches first, then replace known phrases inside longer Markdown/HTML text.
    if value in dictionary:
        return dictionary[value]
    for english, translated in sorted(dictionary.items(), key=lambda item: len(item[0]), reverse=True):
        value = value.replace(english, translated)
    return value

# Translate common Streamlit display functions without changing application logic.
def _patch_display_function(function_name):
    original = getattr(st, function_name)
    def translated_function(*args, **kwargs):
        args = tuple(_urafite_translate(arg) if isinstance(arg, str) else arg for arg in args)
        for _text_kwarg in ("label", "help", "placeholder"):
            if isinstance(kwargs.get(_text_kwarg), str):
                kwargs[_text_kwarg] = _urafite_translate(kwargs[_text_kwarg])
        return original(*args, **kwargs)
    setattr(st, function_name, translated_function)

for _function_name in [
    "title", "header", "subheader", "write", "markdown", "info", "success",
    "warning", "error", "caption", "text", "chat_input", "button",
    "text_input", "text_area", "number_input", "slider", "checkbox",
    "form_submit_button", "audio_input"
]:
    _patch_display_function(_function_name)

# Translate tab labels and metric labels/help text as well.
_original_tabs = st.tabs
def _translated_tabs(labels, *args, **kwargs):
    return _original_tabs([_urafite_translate(label) for label in labels], *args, **kwargs)
st.tabs = _translated_tabs

_original_metric = st.metric
def _translated_metric(label, value, *args, **kwargs):
    if isinstance(kwargs.get("help"), str):
        kwargs["help"] = _urafite_translate(kwargs["help"])
    return _original_metric(_urafite_translate(label), value, *args, **kwargs)
st.metric = _translated_metric

# Translate sidebar controls too; Streamlit sidebar methods are separate from st.*.
for _sidebar_method in ["title", "header", "subheader", "write", "markdown", "info", "success", "warning", "error", "caption", "text", "button", "selectbox", "radio"]:
    _original_sidebar_method = getattr(st.sidebar, _sidebar_method)
    if _sidebar_method in ["selectbox", "radio"]:
        def _make_sidebar_choice(original):
            def _wrapped(label, options, *args, **kwargs):
                kwargs.setdefault("format_func", _urafite_translate)
                return original(_urafite_translate(label), options, *args, **kwargs)
            return _wrapped
        setattr(st.sidebar, _sidebar_method, _make_sidebar_choice(_original_sidebar_method))
    else:
        def _make_sidebar_display(original):
            def _wrapped(*args, **kwargs):
                args = tuple(_urafite_translate(arg) if isinstance(arg, str) else arg for arg in args)
                if isinstance(kwargs.get("label"), str):
                    kwargs["label"] = _urafite_translate(kwargs["label"])
                return original(*args, **kwargs)
            return _wrapped
        setattr(st.sidebar, _sidebar_method, _make_sidebar_display(_original_sidebar_method))

# Translate widget labels and displayed choices, but retain original English values
# internally so existing conditions and calculations continue to work.
def _patch_choice_widget(function_name):
    original = getattr(st, function_name)
    def translated_widget(label, options, *args, **kwargs):
        kwargs.setdefault("format_func", _urafite_translate)
        return original(_urafite_translate(label), options, *args, **kwargs)
    setattr(st, function_name, translated_widget)

for _function_name in ["selectbox", "multiselect", "radio", "select_slider"]:
    _patch_choice_widget(_function_name)


# Page configuration
st.set_page_config(
    page_title="URAFITE | Reclaim Your Future",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root {
  --ura-forest: #123C35;
  --ura-green: #1F765F;
  --ura-mint: #E8F3EE;
  --ura-ink: #172B27;
  --ura-muted: #65756F;
  --ura-line: #E3EBE7;
  --ura-surface: #FFFFFF;
}
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #F5F8F6; color: var(--ura-ink); }
[data-testid="stHeader"] { background: rgba(245,248,246,.92); }
.block-container { max-width: 1240px; padding-top: 2.1rem; padding-bottom: 3rem; }
h1, h2, h3 {
  font-family: 'Manrope', sans-serif !important;
  color: #123C35 !important;
  opacity: 1 !important;
  letter-spacing: -0.025em;
}
h1 { font-size: clamp(2rem, 3vw, 2.8rem) !important; font-weight: 800 !important; }
h2 { font-weight: 750 !important; }
h3 { font-weight: 700 !important; }
p, li, label { line-height: 1.65; color: #263A35; opacity: 1; }
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
[data-testid="stMarkdownContainer"] p {
  color: #263A35 !important;
  opacity: 1 !important;
}
.stSelectbox [data-baseweb="select"] *,
.stMultiSelect [data-baseweb="select"] *,
.stTextInput input, .stTextArea textarea {
  color: #263A35 !important;
}
[data-testid="stSidebar"] { background: #FFFFFF; border-right: 1px solid var(--ura-line); }
[data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem; }
[data-testid="stSidebar"] h1 { font-size: 1.55rem !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { padding: .38rem .55rem; border-radius: 9px; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background: var(--ura-mint); }
div[data-testid="stVerticalBlockBorderWrapper"] {
  background: var(--ura-surface); border: 1px solid var(--ura-line);
  border-radius: 16px; box-shadow: 0 3px 14px rgba(18,60,53,.035);
}
div[data-testid="stMetric"] {
  background: white; border: 1px solid var(--ura-line); border-radius: 14px;
  padding: 16px 18px;
}
div[data-testid="stMetricLabel"] { color: var(--ura-muted); }
div[data-testid="stMetricValue"] { color: var(--ura-forest); font-family: 'Manrope', sans-serif; }
.stButton > button, .stFormSubmitButton > button {
  border-radius: 10px; min-height: 2.7rem; font-weight: 700;
  border: 1px solid var(--ura-green); transition: all .18s ease;
}
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
  background: var(--ura-forest) !important;
  color: #FFFFFF !important;
  border-color: var(--ura-forest) !important;
}
.stButton > button[kind="primary"] *,
.stFormSubmitButton > button[kind="primary"] * {
  color: #FFFFFF !important;
  opacity: 1 !important;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
  border-color: var(--ura-green);
  box-shadow: 0 4px 12px rgba(18,60,53,.10);
}
.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover,
.stButton > button[kind="primary"]:focus,
.stFormSubmitButton > button[kind="primary"]:focus,
.stButton > button[kind="primary"]:active,
.stFormSubmitButton > button[kind="primary"]:active {
  background: #174F43 !important;
  color: #FFFFFF !important;
  border-color: #174F43 !important;
}
.stButton > button[kind="primary"]:hover *,
.stFormSubmitButton > button[kind="primary"]:hover *,
.stButton > button[kind="primary"]:focus *,
.stFormSubmitButton > button[kind="primary"]:focus * {
  color: #FFFFFF !important;
  opacity: 1 !important;
}
/* URAFITE: Visible input fields */
div[data-testid="stTextInput"] [data-baseweb="input"],
div[data-testid="stNumberInput"] [data-baseweb="input"],
div[data-testid="stTextArea"] [data-baseweb="textarea"] {
    background-color: #E5F2EA !important;
    border: 1.5px solid #36836B !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}

/* Style the inner input container */
div[data-testid="stTextInput"] [data-baseweb="input"] > div,
div[data-testid="stNumberInput"] [data-baseweb="input"] > div {
    background-color: #E5F2EA !important;
}

/* Actual text-entry fields */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextArea"] textarea {
    background-color: #E5F2EA !important;
    color: #193D32 !important;
    border-radius: 10px !important;
}

/* Highlight focused fields */
div[data-testid="stTextInput"] [data-baseweb="input"]:focus-within,
div[data-testid="stNumberInput"] [data-baseweb="input"]:focus-within,
div[data-testid="stTextArea"] [data-baseweb="textarea"]:focus-within {
    border: 2px solid #176B52 !important;
    box-shadow: 0 0 0 3px rgba(23,107,82,0.12) !important;
}

/* Dropdowns */
.stSelectbox [data-baseweb="select"],
.stMultiSelect [data-baseweb="select"] {
    border-radius: 10px !important;
}

.stSelectbox [data-baseweb="select"],
.stMultiSelect [data-baseweb="select"] {
    border-radius: 10px !important;
}
div[data-testid="stAlert"] { border-radius: 12px; }
hr { border-color: var(--ura-line); }
.ura-hero {
  background: linear-gradient(125deg, #103B33 0%, #1C6552 62%, #2D8067 100%);
  padding: clamp(28px, 5vw, 54px); border-radius: 22px; color: #fff;
  margin: 0 0 26px 0; position: relative; overflow: hidden;
  box-shadow: 0 14px 35px rgba(18,60,53,.13);
}
.ura-hero:after {
  content: ''; position: absolute; width: 260px; height: 260px; right: -75px; top: -100px;
  border: 1px solid rgba(255,255,255,.18); border-radius: 50%;
  box-shadow: 0 0 0 35px rgba(255,255,255,.035), 0 0 0 70px rgba(255,255,255,.025);
}
.ura-hero h1 { color: white !important; margin: 0 0 12px 0; }
.ura-hero p {
    color: #FFFFFF !important;
    font-size: 1.08rem;
    max-width: 720px;
    margin-bottom: 0;
    font-weight: 500;
    line-height: 1.7;
}
.ura-eyebrow { color: #C5E6D8; text-transform: uppercase; letter-spacing: .13em; font-size: .76rem; font-weight: 700; margin-bottom: 12px; }
.ura-card {
  background: white; border: 1px solid var(--ura-line); border-radius: 16px;
  padding: 22px; min-height: 190px; box-shadow: 0 4px 16px rgba(18,60,53,.035);
}
.ura-card h3 { margin-top: 4px; font-size: 1.18rem; }
.ura-card p { color: var(--ura-muted); margin-bottom: 0; }
.ura-step { color: var(--ura-green); font-size: .78rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
.ura-note { color: var(--ura-muted); font-size: .88rem; }
[data-testid="stChatMessage"] { border: 1px solid var(--ura-line); border-radius: 14px; padding: 12px 16px; }
@media (max-width: 700px) {
  .block-container { padding-left: 1rem; padding-right: 1rem; }
  .ura-hero { border-radius: 16px; }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SUPABASE AUTHENTICATION
# Uses the publishable key with Supabase Auth and database RLS.
# No service-role key is used in this Streamlit application.
# -----------------------------------------------------------------------------

def _urafite_supabase_client(project_url: str, publishable_key: str):
    from supabase import create_client
    return create_client(project_url, publishable_key)


def _urafite_get_supabase():
    try:
        project_url = st.secrets.get("SUPABASE_URL", "").strip()
        publishable_key = st.secrets.get("SUPABASE_KEY", "").strip()
    except Exception:
        project_url, publishable_key = "", ""
    if not project_url or not publishable_key:
        return None
    try:
        return _urafite_supabase_client(project_url, publishable_key)
    except Exception as exc:
        st.error("Could not initialise the Supabase connection. Check your project URL and publishable key.")
        st.caption(f"Technical detail: {exc}")
        return None


def _urafite_auth_screen():
    """Render authentication entirely in the language selected before sign-in."""
    st.session_state.setdefault("urafite_language", "English")
    st.session_state.setdefault("urafite_language_user_selected", False)
    def _auth_language_changed():
        st.session_state["urafite_language_user_selected"] = True
    language_options = ["English", "Kinyarwanda", "Français"]
    language_names = {
        "English": {"English": "English", "Kinyarwanda": "Kinyarwanda", "Français": "French"},
        "Kinyarwanda": {"English": "Icyongereza", "Kinyarwanda": "Ikinyarwanda", "Français": "Igifaransa"},
        "Français": {"English": "Anglais", "Kinyarwanda": "Kinyarwanda", "Français": "Français"},
    }
    st.selectbox(
        {"English": "Language", "Kinyarwanda": "Ururimi", "Français": "Langue"}[st.session_state["urafite_language"]],
        language_options,
        key="urafite_language",
        format_func=lambda option: language_names[st.session_state["urafite_language"]][option],
        label_visibility="collapsed",
        on_change=_auth_language_changed,
    )
    language = st.session_state.get("urafite_language", "English")

    auth_copy = {
        "English": {
            "welcome": "Welcome to URAFITE",
            "eyebrow": "A fresh start begins here",
            "intro": "Your future is worth more than your next bet. Sign in or create an account to continue.",
            "signin_tab": "Sign in", "signup_tab": "Create account",
            "email": "Email address", "password": "Password",
            "signin": "Sign in", "display_name": "Display name",
            "confirm_password": "Confirm password", "signup": "Create account",
            "signup_note": "Create an account with your email address. You may be asked to verify your email before signing in.",
            "missing_signin": "Enter your email address and password.",
            "signin_no_session": "Sign-in did not return an active session. Check your email confirmation and try again.",
            "signin_failed": "Sign-in failed. Check your email, password and email verification status.",
            "complete_fields": "Complete all fields before creating your account.",
            "password_mismatch": "The passwords do not match.",
            "password_length": "Use a password with at least 8 characters.",
            "signup_success": "Your account has been created. Welcome to URAFITE!",
            "verify_email": "Account request received. Check your email for a verification link, then return here to sign in.",
            "signup_failed": "We could not create the account. The email may already be registered, or the password may not meet the project requirements.",
        },
        "Kinyarwanda": {
            "welcome": "Murakaza neza kuri URAFITE",
            "eyebrow": "Intangiriro nshya itangiriye hano",
            "intro": "Ejo hazaza hawe hafite agaciro kurusha indi nshuro wakina urusimbi. Injira cyangwa ufungure konti kugira ngo ukomeze.",
            "signin_tab": "Kwinjira", "signup_tab": "Fungura konti",
            "email": "Imeyili", "password": "Ijambo ry'ibanga",
            "signin": "Injira", "display_name": "Amazina agaragara",
            "confirm_password": "Emeza ijambo ry'ibanga", "signup": "Fungura konti",
            "signup_note": "Fungura konti ukoresheje aderesi yawe ya imeyili. Ushobora gusabwa kubanza kwemeza imeyili mbere yo kwinjira.",
            "missing_signin": "Andika aderesi ya imeyili n'ijambo ry'ibanga.",
            "signin_no_session": "Kwinjira ntibyagenze neza. Genza niba wemeje imeyili yawe, wongere ugerageze.",
            "signin_failed": "Kwinjira byanze. Genza imeyili, ijambo ry'ibanga n'uko wemeje imeyili.",
            "complete_fields": "Uzuza ibisabwa byose mbere yo gufungura konti.",
            "password_mismatch": "Amagambo y'ibanga ntahura.",
            "password_length": "Koresha ijambo ry'ibanga rifite nibura inyuguti 8.",
            "signup_success": "Konti yawe yafunguwe. Murakaza neza kuri URAFITE!",
            "verify_email": "Ubusabe bwo gufungura konti bwakiriwe. Reba imeyili yawe kugira ngo wemeze konti, hanyuma ugaruke winjire.",
            "signup_failed": "Ntitwashoboye gufungura konti. Iyi imeyili ishobora kuba isanzwe ikoreshwa cyangwa ijambo ry'ibanga ntiryujuje ibisabwa.",
        },
        "Français": {
            "welcome": "Bienvenue sur URAFITE",
            "eyebrow": "Un nouveau départ commence ici",
            "intro": "Votre avenir vaut plus que votre prochain pari. Connectez-vous ou créez un compte pour continuer.",
            "signin_tab": "Se connecter", "signup_tab": "Créer un compte",
            "email": "Adresse e-mail", "password": "Mot de passe",
            "signin": "Se connecter", "display_name": "Nom affiché",
            "confirm_password": "Confirmer le mot de passe", "signup": "Créer un compte",
            "signup_note": "Créez un compte avec votre adresse e-mail. Vous devrez peut-être confirmer votre adresse avant de vous connecter.",
            "missing_signin": "Saisissez votre adresse e-mail et votre mot de passe.",
            "signin_no_session": "La connexion n'a pas créé de session active. Vérifiez la confirmation de votre e-mail et réessayez.",
            "signin_failed": "Échec de la connexion. Vérifiez votre adresse e-mail, votre mot de passe et la confirmation de votre adresse.",
            "complete_fields": "Veuillez remplir tous les champs avant de créer votre compte.",
            "password_mismatch": "Les mots de passe ne correspondent pas.",
            "password_length": "Utilisez un mot de passe d'au moins 8 caractères.",
            "signup_success": "Votre compte a été créé. Bienvenue sur URAFITE !",
            "verify_email": "Votre demande de création de compte a été reçue. Consultez votre e-mail pour confirmer votre adresse, puis revenez vous connecter.",
            "signup_failed": "Impossible de créer le compte. Cette adresse e-mail est peut-être déjà utilisée ou le mot de passe ne respecte pas les exigences.",
        },
    }
    copy = auth_copy.get(language, auth_copy["English"])

    st.markdown(f"<div class='ura-hero'><div class='ura-eyebrow'>{copy['eyebrow']}</div><h1>{copy['welcome']}</h1><p>{copy['intro']}</p></div>", unsafe_allow_html=True)
    sign_in_tab, sign_up_tab = st.tabs([copy["signin_tab"], copy["signup_tab"]])

    with sign_in_tab:
        with st.form("urafite_signin_form"):
            email = st.text_input(copy["email"], key="signin_email")
            password = st.text_input(copy["password"], type="password", key="signin_password")
            submitted = st.form_submit_button(copy["signin"], type="primary", use_container_width=True)
        if submitted:
            if not email.strip() or not password:
                st.warning(copy["missing_signin"])
            else:
                try:
                    response = _urafite_sb.auth.sign_in_with_password({"email": email.strip(), "password": password})
                    if response.session:
                        st.session_state["urafite_access_token"] = response.session.access_token
                        st.session_state["urafite_refresh_token"] = response.session.refresh_token
                        st.session_state["urafite_user_email"] = response.user.email
                        st.rerun()
                    else:
                        st.error(copy["signin_no_session"])
                except Exception:
                    st.error(copy["signin_failed"])

    with sign_up_tab:
        st.caption(copy["signup_note"])
        with st.form("urafite_signup_form"):
            display_name = st.text_input(copy["display_name"])
            new_email = st.text_input(copy["email"], key="signup_email")
            new_password = st.text_input(copy["password"], type="password", key="signup_password")
            confirm_password = st.text_input(copy["confirm_password"], type="password")
            submitted_signup = st.form_submit_button(copy["signup"], type="primary", use_container_width=True)
        if submitted_signup:
            if not display_name.strip() or not new_email.strip() or not new_password:
                st.warning(copy["complete_fields"])
            elif new_password != confirm_password:
                st.warning(copy["password_mismatch"])
            elif len(new_password) < 8:
                st.warning(copy["password_length"])
            else:
                language_codes = {"English": "en", "Kinyarwanda": "rw", "Français": "fr"}
                try:
                    response = _urafite_sb.auth.sign_up({
                        "email": new_email.strip(),
                        "password": new_password,
                        "options": {
    "email_redirect_to": "https://urafite-eibn9f35u3j4rwgdyqoexx.streamlit.app/",
    "data": {
        "display_name": display_name.strip(),
        "preferred_language": language_codes[language]
    }
}
                    })
                    if response.session:
                        st.session_state["urafite_access_token"] = response.session.access_token
                        st.session_state["urafite_refresh_token"] = response.session.refresh_token
                        st.session_state["urafite_user_email"] = response.user.email
                        st.success(copy["signup_success"])
                        st.rerun()
                    else:
                        st.success(copy["verify_email"])
                except Exception:
                    st.error(copy["signup_failed"])


_urafite_sb = _urafite_get_supabase()
if _urafite_sb is None:
    st.error("URAFITE needs its Supabase connection settings before you can sign in.")
    st.markdown("Create `.streamlit/secrets.toml` using the supplied `secrets.toml.example` file, then add your Project URL and publishable key. Never use the Supabase secret/service-role key here.")
    st.stop()

_urafite_session = None
_access = st.session_state.get("urafite_access_token")
_refresh = st.session_state.get("urafite_refresh_token")
if _access and _refresh:
    try:
        _urafite_session = _urafite_sb.auth.set_session(_access, _refresh).session
        if _urafite_session:
            st.session_state["urafite_access_token"] = _urafite_session.access_token
            st.session_state["urafite_refresh_token"] = _urafite_session.refresh_token
    except Exception:
        st.session_state.pop("urafite_access_token", None)
        st.session_state.pop("urafite_refresh_token", None)

if not _urafite_session:
    _urafite_auth_screen()
    st.stop()

try:
    _urafite_user = _urafite_sb.auth.get_user(_urafite_session.access_token).user
    _urafite_user_id = _urafite_user.id
    _role_response = _urafite_sb.table("user_roles").select("role").eq("user_id", _urafite_user_id).execute()
    _urafite_roles = [row["role"] for row in (_role_response.data or [])]
    if not st.session_state.get("urafite_language_user_selected", False):
        _profile_response = _urafite_sb.table("profiles").select("preferred_language").eq("id", _urafite_user_id).limit(1).execute()
        _profile_rows = _profile_response.data or []
        if _profile_rows:
            _stored_language = {"en": "English", "rw": "Kinyarwanda", "fr": "Français"}.get(_profile_rows[0].get("preferred_language"), "English")
            st.session_state["urafite_language"] = _stored_language
except Exception as exc:
    st.error("Your session could not be verified. Please sign in again.")
    st.caption(f"Technical detail: {exc}")
    if st.button("Return to sign in"):
        st.session_state.pop("urafite_access_token", None)
        st.session_state.pop("urafite_refresh_token", None)
        st.rerun()
    st.stop()

if not _urafite_roles:
    st.info("Your account is active. Your profile permissions are being prepared. Please refresh in a moment or contact the URAFITE administrator if this continues.")
    st.stop()

st.session_state["urafite_authenticated_user_id"] = _urafite_user_id
st.session_state["urafite_authenticated_email"] = _urafite_user.email
st.session_state["urafite_authenticated_roles"] = _urafite_roles

# Sidebar
st.sidebar.title("🌱 URAFITE")
st.sidebar.caption(_urafite_translate("Reclaim Your Future"))
st.sidebar.caption("Signed in: " + str(st.session_state.get("urafite_authenticated_email", "")))
if "super_admin" in st.session_state.get("urafite_authenticated_roles", []):
    st.sidebar.success("Super Administrator")
elif "admin" in st.session_state.get("urafite_authenticated_roles", []):
    st.sidebar.info("Administrator")
if st.sidebar.button("Sign out", use_container_width=True):
    try:
        _urafite_sb.auth.sign_out()
    except Exception:
        pass
    for _key in ["urafite_access_token", "urafite_refresh_token", "urafite_authenticated_user_id", "urafite_authenticated_email", "urafite_authenticated_roles"]:
        st.session_state.pop(_key, None)
    st.rerun()
st.sidebar.divider()

# Language selector: the user can change language at any time.
if "urafite_language" not in st.session_state:
    st.session_state["urafite_language"] = "English"

st.sidebar.markdown("### 🌐 " + _urafite_translate("Language / Ururimi / Langue"))
def _urafite_language_changed():
    """Start a clean conversation and persist the selected interface language."""
    selected_language = st.session_state.get("urafite_language", "English")
    st.session_state["urafite_language_user_selected"] = True
    if st.session_state.get("urafite_authenticated_user_id"):
        try:
            _language_code = {"English": "en", "Kinyarwanda": "rw", "Français": "fr"}[selected_language]
            _urafite_sb.table("profiles").update({"preferred_language": _language_code}).eq(
                "id", st.session_state["urafite_authenticated_user_id"]
            ).execute()
        except Exception:
            # Keep the interface usable even if profile preference saving fails.
            pass
    welcome_messages = {
        "English": "Hello! 🌱 Welcome to URAFITE. How would you like to move forward today?",
        "Kinyarwanda": "Muraho! 🌱 Murakaza neza kuri URAFITE. Ni iki mwifuza gukora uyu munsi kugira ngo mutere imbere?",
        "Français": "Bonjour ! 🌱 Bienvenue sur URAFITE. Que souhaitez-vous entreprendre aujourd'hui pour avancer ?"
    }
    st.session_state["urafite_chat_history"] = [
        {"role": "assistant", "content": welcome_messages.get(selected_language, welcome_messages["English"])}
    ]

_sidebar_language_names = {
    "English": {"English": "English", "Kinyarwanda": "Kinyarwanda", "Français": "French"},
    "Kinyarwanda": {"English": "Icyongereza", "Kinyarwanda": "Ikinyarwanda", "Français": "Igifaransa"},
    "Français": {"English": "Anglais", "Kinyarwanda": "Kinyarwanda", "Français": "Français"},
}
st.sidebar.selectbox(
    _urafite_translate("Choose your preferred language"),
    ["English", "Kinyarwanda", "Français"],
    key="urafite_language",
    format_func=lambda option: _sidebar_language_names[st.session_state["urafite_language"]][option],
    label_visibility="collapsed",
    on_change=_urafite_language_changed
)

def _urafite_nav_label(item):
    # Keep the internal page key for routing, but never expose the old name.
    if item == "AI Companion":
        language = st.session_state.get("urafite_language", "English")
        labels = {
            "English": "🌱 Hiro – Recovery & Support",
            "Kinyarwanda": "🌱 Hiro – Ubufasha mu gukira no kwiyubaka",
            "Français": "🌱 Hiro – Guide de rétablissement",
        }
        return labels.get(language, labels["English"])
    return _urafite_translate(item)

page = st.sidebar.radio(
    _urafite_translate("Navigate"),
    [
        "Home",
        "RECOVER",
        "REBUILD",
        "RECONNECT",
        "AI Companion",
        "Heal and Learn Centre",
        "Professional Support"
    ] + (["Administration", "Impact & Evidence", "Opportunity Manager", "Heal and Learn Centre Manager", "Grant & Programme Tracker"] if any(r in _urafite_roles for r in ["super_admin", "admin"]) else []),
    format_func=_urafite_nav_label,
    key="page_navigation"
)

def _urafite_go_to_page(target):
    st.session_state["page_navigation"] = target

st.sidebar.divider()
st.sidebar.caption(_urafite_translate("AI-assisted recovery and opportunity support"))

# -----------------------------------------------------------------------------
# ADMINISTRATION MODULES
# All writes are protected by Supabase RLS. No service-role key is used.
# -----------------------------------------------------------------------------
def _admin_query(table, columns="*"):
    return _urafite_sb.table(table).select(columns).execute().data or []

def _admin_is_authorised():
    return any(r in _urafite_roles for r in ("super_admin", "admin"))

def _admin_guard():
    if not _admin_is_authorised():
        st.error(_urafite_translate("You do not have permission to access this area."))
        st.stop()

def _safe_admin_rows(table, columns="*"):
    try:
        return _admin_query(table, columns)
    except Exception as exc:
        st.error(_urafite_translate("Could not retrieve this information from Supabase."))
        st.caption(str(exc))
        return []

# Home page
if page == "Home":
    st.markdown("""
    <div class="ura-hero">
      <div class="ura-eyebrow">A fresh start begins here</div>
      <h1>URAFITE — Reclaim Your Future</h1>
      <p>Your future is worth more than your next bet. Find support, rebuild your financial confidence,
      and reconnect with opportunities that move your life forward.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("A practical pathway towards a stronger future")
    st.write(
        "URAFITE is a youth-centred support platform designed to help people affected by harmful "
        "gambling take practical steps towards wellbeing, financial stability and new opportunities. "
        "You choose where to begin, and you can move between the pathways at your own pace."
    )

    st.markdown("### Three pathways. One renewed future.")
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        with st.container(border=True):
            st.markdown('<div class="ura-step">01 · wellbeing</div><h3>🌿 RECOVER</h3><p>Pause, reflect on urges and triggers, build coping strategies, and identify when human support may help.</p>', unsafe_allow_html=True)
            st.button("Explore RECOVER →", key="home_recover", use_container_width=True,
                      on_click=_urafite_go_to_page, args=("RECOVER",))
    with col2:
        with st.container(border=True):
            st.markdown('<div class="ura-step">02 · financial confidence</div><h3>💚 REBUILD</h3><p>Understand your income and expenses, set realistic savings goals, and take manageable financial steps.</p>', unsafe_allow_html=True)
            st.button("Explore REBUILD →", key="home_rebuild", use_container_width=True,
                      on_click=_urafite_go_to_page, args=("REBUILD",))
    with col3:
        with st.container(border=True):
            st.markdown('<div class="ura-step">03 · new opportunities</div><h3>🚀 RECONNECT</h3><p>Turn your interests into an action plan for learning, skills development, employment or enterprise.</p>', unsafe_allow_html=True)
            st.button("Explore RECONNECT →", key="home_reconnect", use_container_width=True,
                      on_click=_urafite_go_to_page, args=("RECONNECT",))

    if st.session_state.get("home_navigation"):
        st.info("Use the navigation menu to open " + st.session_state["home_navigation"] + ".")
        st.session_state["home_navigation"] = None

    st.divider()
    left, right = st.columns([1.35, 1])
    with left:
        st.subheader("Start with one small step")
        st.write("You do not need to solve everything today. Choose the area that feels most important right now.")
        st.button("Begin with a personal check-in", type="primary", use_container_width=True,
                  on_click=_urafite_go_to_page, args=("RECOVER",))
    with right:
        with st.container(border=True):
            st.markdown("#### A message to carry with you")
            st.markdown("> Your past losses do not define your worth. Your next decision can help shape a different future.")

    st.caption("URAFITE MVP · A developing support prototype")
    st.info(
        "URAFITE complements, but does not replace, qualified professional care. "
        "This prototype does not provide clinical diagnosis, crisis monitoring or emergency response."
    )

# Other pages - placeholders for the next development stages

elif page == "RECOVER":
    st.title("🌿 RECOVER")
    st.subheader("You are more than your past experiences.")

    st.write(
        "Welcome to a judgment-free space. You do not have "
        "to have everything figured out today. Take a moment "
        "to understand how you are feeling and what you need."
    )

    st.info(
        "Your responses are used to provide supportive reflections. "
        "This exercise is not a clinical assessment or a diagnosis."
    )

    st.divider()

    st.subheader("1. How are you feeling today?")

    with st.form("recovery_checkin_v2"):

        mood = st.select_slider(
            "Choose the description closest to how you feel.",
            options=[
                "Very overwhelmed",
                "Anxious",
                "Discouraged",
                "Okay",
                "Hopeful",
                "Motivated",
                "Positive"
            ],
            value="Okay"
        )

        st.subheader("2. Understand what you are experiencing")

        urge = st.slider(
            "How strong is your urge to gamble right now?",
            min_value=0,
            max_value=10,
            value=0,
            help="0 means no urge; 10 means an extremely strong urge."
        )

        triggers = st.multiselect(
            "What situations or feelings may be influencing you?",
            [
                "Financial pressure",
                "Stress or anxiety",
                "Boredom or loneliness",
                "Friends or social influence",
                "Gambling advertisements",
                "Trying to recover previous losses",
                "Feeling disappointed in myself",
                "Excitement or the hope of winning",
                "Other",
                "I am not sure"
            ],
            placeholder=_urafite_translate("Choose options")
        )

        st.subheader("3. What would you like to work on today?")

        intention = st.radio(
            "Choose what matters most to you right now.",
            [
                "I want to manage my gambling urges.",
                "I want to understand my gambling behaviour.",
                "I want to regain control of my finances.",
                "I want to focus on my education or career.",
                "I want to rebuild my confidence.",
                "I would like to speak with a professional."
            ]
        )

        professional_request = st.checkbox(
            "I would like information about professional support."
        )

        submitted = st.form_submit_button(
            "Reflect on my responses",
            use_container_width=True
        )

    if submitted:

        st.session_state["recovery_reflection"] = {
            "mood": mood,
            "urge": urge,
            "triggers": triggers,
            "intention": intention,
            "professional_request": professional_request
        }

    if "recovery_reflection" in st.session_state:

        data = st.session_state["recovery_reflection"]

        st.divider()
        st.success(
            "Thank you for taking this moment for yourself. "
            "Recognizing what you are experiencing is meaningful."
        )

        st.subheader("Your personal reflection")

        st.write(
            "You described feeling **" + data["mood"].lower() + "** today."
        )

        if data["urge"] >= 7:
            st.markdown(
                "**You are experiencing a strong gambling urge.**"
            )
            st.write(
                "You do not have to act on an urge immediately. "
                "Consider stepping away from gambling applications "
                "or advertisements, moving to a different environment, "
                "and contacting someone you trust."
            )

        elif data["urge"] >= 4:
            st.markdown(
                "**You have noticed a moderate gambling urge.**"
            )
            st.write(
                "This could be a useful moment to pause and reflect "
                "before making a decision. Try identifying what "
                "you are feeling and choose an activity that supports "
                "your personal goals."
            )

        else:
            st.markdown(
                "**You have reported a relatively low gambling urge.**"
            )
            st.write(
                "Use this moment to strengthen habits that support "
                "your well-being and the future you want to build."
            )

        if data["triggers"]:
            st.markdown("**Situations you identified:**")
            for trigger in data["triggers"]:
                st.write("- " + trigger)

        st.subheader("A small step towards change")

        st.write(
            "Your chosen priority is: **" + data["intention"] + "**"
        )

        if data["intention"] == "I want to manage my gambling urges.":
            st.write(
                "Try delaying any gambling decision for 15 minutes. "
                "During that time, move away from gambling content "
                "and do something that helps you feel grounded."
            )

        elif data["intention"] == "I want to understand my gambling behaviour.":
            st.write(
                "Consider reflecting on what happened before your "
                "last gambling session. What were you feeling, "
                "and what were you hoping gambling would change?"
            )

        elif data["intention"] == "I want to regain control of my finances.":
            st.write(
                "Start by identifying one essential financial "
                "priority. You can use REBUILD to create a realistic "
                "budget and work towards it."
            )

        elif data["intention"] == "I want to focus on my education or career.":
            st.write(
                "Think about one educational or professional goal "
                "you would like to pursue. Visit RECONNECT to explore "
                "possible opportunities."
            )

        elif data["intention"] == "I want to rebuild my confidence.":
            st.write(
                "Write down one ability, achievement, or personal "
                "quality you value about yourself. Your past "
                "difficulties do not define your worth."
            )

        else:
            st.write(
                "Seeking professional support is a positive step. "
                "You deserve to be heard and supported by someone "
                "qualified to help."
            )

        if data["professional_request"] or (
            data["intention"] == "I would like to speak with a professional."
        ):
            st.warning(
                "You can seek support from a qualified mental-health "
                "professional or counsellor. Open Professional Support "
                "in the sidebar for available support information."
            )

        st.divider()

        st.markdown(
            "**Remember:** You do not need to rebuild your entire "
            "life in one day. One thoughtful decision can be "
            "the beginning of a different direction."
        )

        st.caption(
            "These reflections are based on predefined guidance, "
            "not an AI clinical assessment. They do not determine "
            "your mental-health or suicide risk."
        )

    st.divider()

    st.subheader("You deserve support")

    st.write(
        "If you are experiencing severe distress, thoughts of "
        "suicide, or immediate danger, do not rely on this check-in. "
        "Contact emergency services, a qualified professional, "
        "or someone you trust who can help you access immediate care."
    )



elif page == "REBUILD":
    st.title("💚 REBUILD")
    st.subheader("Your past financial struggles do not define your future.")

    st.write(
        "You do not need to recover everything at once. "
        "Start by understanding your finances, setting realistic "
        "goals, and taking small steps towards financial stability."
    )

    st.info(
        "This is a personal budgeting and goal-tracking tool, "
        "not professional financial advice."
    )

    st.divider()

    # Monthly financial overview
    st.subheader("1. Understand your monthly finances")

    with st.form("rebuild_budget_v2"):

        income = st.number_input(
            "Your monthly income (RWF)",
            min_value=0,
            value=100000,
            step=5000
        )

        st.markdown("**Your essential and personal expenses**")

        food = st.number_input(
            "Food and essential needs (RWF)",
            min_value=0,
            value=30000,
            step=1000
        )

        accommodation = st.number_input(
            "Accommodation (RWF)",
            min_value=0,
            value=20000,
            step=1000
        )

        transport = st.number_input(
            "Transport (RWF)",
            min_value=0,
            value=10000,
            step=1000
        )

        education = st.number_input(
            "Education and personal development (RWF)",
            min_value=0,
            value=10000,
            step=1000
        )

        other = st.number_input(
            "Other expenses (RWF)",
            min_value=0,
            value=5000,
            step=1000
        )

        actual_savings = st.number_input(
            "Money you have actually saved (RWF)",
            min_value=0,
            value=0,
            step=1000
        )

        st.markdown("**Your financial recovery goal**")

        savings_goal = st.number_input(
            "How much would you like to save? (RWF)",
            min_value=0,
            value=50000,
            step=5000
        )

        goal_period = st.selectbox(
            "When would you like to achieve this goal?",
            ["1 month", "3 months", "6 months", "12 months"]
        )

        submitted = st.form_submit_button(
            "Review my financial plan",
            use_container_width=True
        )

    if submitted:

        total_expenses = (
            food + accommodation + transport + education + other
        )

        remaining = income - total_expenses

        st.session_state["financial_plan"] = {
            "income": income,
            "expenses": total_expenses,
            "remaining": remaining,
            "savings": actual_savings,
            "goal": savings_goal,
            "period": goal_period
        }

    # Display financial results
    if "financial_plan" in st.session_state:

        plan = st.session_state["financial_plan"]

        st.divider()
        st.subheader("2. Your financial picture")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            _urafite_translate("Monthly income"),
            f"{plan['income']:,.0f} RWF"
        )

        col2.metric(
            _urafite_translate("Monthly expenses"),
            f"{plan['expenses']:,.0f} RWF"
        )

        col3.metric(
            _urafite_translate("Remaining income"),
            f"{plan['remaining']:,.0f} RWF"
        )

        if plan["remaining"] < 0:
            st.error(
                "Your recorded expenses exceed your income. "
                "This may be a good opportunity to review your "
                "financial priorities and consider additional support."
            )
        else:
            st.success(
                "Understanding your finances is an important "
                "step towards making informed decisions."
            )

        st.metric(
            "Actual savings recorded",
            f"{plan['savings']:,.0f} RWF"
        )

        st.caption(
            "Remaining income is not automatically counted as savings. "
            "Only money you have actually saved is recorded here."
        )

        st.divider()
        st.subheader("3. Your personal savings journey")

        st.write(
            f"Your goal: **{plan['goal']:,.0f} RWF** "
            f"within **{plan['period']}**."
        )

        if plan["goal"] > 0:

            progress = min(
                plan["savings"] / plan["goal"], 1.0
            )

            st.progress(progress)

            st.write(
                f"You have achieved {progress * 100:.1f}% "
                "of your savings goal."
            )

            remaining_goal = max(
                plan["goal"] - plan["savings"], 0
            )

            st.write(
                f"Amount remaining: **{remaining_goal:,.0f} RWF**"
            )

        else:
            st.write(
                "Set a savings target whenever you feel ready."
            )

        st.divider()
        st.subheader("4. What are you rebuilding towards?")

        personal_goal = st.radio(
            "Choose a goal that matters to you.",
            [
                "Paying my education fees",
                "Building personal savings",
                "Starting a small business",
                "Developing my professional skills",
                "Achieving financial independence",
                "Supporting my family",
                "Another personal goal"
            ]
        )

        st.session_state["personal_financial_goal"] = personal_goal

        st.success(
            f"Your chosen priority: {personal_goal}"
        )

        st.markdown("### A reminder from URAFITE")

        st.write(
            "Your financial situation today does not determine "
            "your financial future. You do not have to rebuild "
            "everything immediately. Every realistic step towards "
            "your goals matters."
        )

        st.caption(
            "Demonstration version: financial information is "
            "held in the current Streamlit session and is not "
            "yet stored in a permanent personal account."
        )


elif page == "RECONNECT":

    st.title("🌱 RECONNECT")
    st.subheader("Your past does not determine your future.")

    st.write(
        "A fresh start is not just about leaving harmful habits behind. "
        "It is also about discovering new opportunities, developing your "
        "potential, and building a future you can be proud of."
    )

    st.info(
        "Your future is still full of possibilities. "
        "Let's identify one meaningful step you can take today."
    )

    st.markdown("---")

    # 1. DISCOVER YOUR FUTURE

    st.header("1. Discover your future")

    st.write(
        "Tell us what you would like to work towards. "
        "You can select more than one interest."
    )

    with st.form("reconnect_profile_form"):

        interests = st.multiselect(
            "What opportunities interest you?",
            [
                "Scholarships and further education",
                "Digital skills and technology",
                "Vocational and technical training",
                "Employment and internships",
                "Entrepreneurship and business",
                "Personal development and leadership"
            ]
        )

        education = st.selectbox(
            "What is your current education or career stage?",
            [
                "Secondary school student",
                "University student",
                "University graduate",
                "Vocational training student",
                "Currently seeking employment",
                "Working professional",
                "Other"
            ],
            index=None,
            placeholder=_urafite_translate("Choose an option")
        )

        main_goal = st.selectbox(
            "What would you most like to achieve?",
            [
                "Continue my education",
                "Develop employable skills",
                "Find an internship or job",
                "Start or grow a business",
                "Become financially independent",
                "Build confidence and personal growth"
            ]
        )

        submit_profile = st.form_submit_button(
            "Discover my opportunities",
            use_container_width=True
        )

    if submit_profile:

        st.session_state["reconnect_user_profile"] = {
            "interests": interests,
            "education": education,
            "goal": main_goal
        }

        st.session_state["reconnect_action"] = ""

    # 2. OPPORTUNITIES

    profile = st.session_state.get("reconnect_user_profile")

    if profile:

        st.markdown("---")

        st.header("2. Opportunities for your next chapter")

        st.write(
            f"Your current goal: **{profile['goal']}**"
        )

        st.write(
            f"Your education or career stage: **{profile['education']}**"
        )

        st.caption(
            "The opportunities below are illustrative examples for the MVP. "
            "They are not verified live vacancies, scholarships, or open programmes."
        )

        opportunities = [

            {
                "name": "Scholarship Discovery",
                "category": "Scholarships and further education",
                "description": (
                    "Explore scholarship pathways, admission requirements, "
                    "application preparation, and opportunities for further study."
                ),
                "action": (
                    "Prepare a list of three programmes I would like to explore."
                )
            },

            {
                "name": "Digital Skills Development",
                "category": "Digital skills and technology",
                "description": (
                    "Build practical skills in programming, data analysis, "
                    "digital tools, and other areas of technology."
                ),
                "action": (
                    "Choose one digital skill and identify a learning resource."
                )
            },

            {
                "name": "Vocational Skills Pathway",
                "category": "Vocational and technical training",
                "description": (
                    "Explore practical and technical training that can support "
                    "employment or self-employment."
                ),
                "action": (
                    "Identify one vocational skill relevant to my interests."
                )
            },

            {
                "name": "Employment Readiness",
                "category": "Employment and internships",
                "description": (
                    "Strengthen your CV, prepare for interviews, "
                    "and explore internship and employment pathways."
                ),
                "action": (
                    "Update my CV and identify one opportunity to apply for."
                )
            },

            {
                "name": "Entrepreneurship Journey",
                "category": "Entrepreneurship and business",
                "description": (
                    "Explore business ideas, entrepreneurship training, "
                    "financial planning, and enterprise development."
                ),
                "action": (
                    "Write down one business idea and the problem it addresses."
                )
            },

            {
                "name": "Leadership and Personal Growth",
                "category": "Personal development and leadership",
                "description": (
                    "Explore mentorship, leadership development, "
                    "communication, and personal growth opportunities."
                ),
                "action": (
                    "Identify one personal development goal for this month."
                )
            }

        ]

        selected_opportunities = [
            item for item in opportunities
            if item["category"] in profile["interests"]
        ]

        if selected_opportunities:

            for item in selected_opportunities:

                with st.container(border=True):

                    st.subheader(f"✨ {item['name']}")

                    st.write(item["description"])

                    st.caption(
                        f"Suggested first step: {item['action']}"
                    )

        else:

            st.warning(
                "You have not selected any interests yet. "
                "Please select at least one interest above to discover "
                "suggested opportunities."
            )

        # 3. PERSONAL ACTION PLAN

        st.markdown("---")

        st.header("3. Turn an opportunity into action")

        st.write(
            "Big changes begin with small, realistic steps. "
            "Choose one action you are willing to take."
        )

        available_actions = [
            item["action"] for item in selected_opportunities
        ]

        if available_actions:

            selected_action = st.selectbox(
                "My next step",
                available_actions,
                key="reconnect_selected_action"
            )

            if st.button(
                "Save my next step",
                use_container_width=True
            ):

                st.session_state["reconnect_action"] = selected_action

                st.success(
                    "Your next step has been added to your action plan."
                )

        saved_action = st.session_state.get(
            "reconnect_action", ""
        )

        if saved_action:

            st.markdown("### 🎯 My personal action plan")

            st.success(saved_action)

            st.write(
                "You do not have to change everything today. "
                "Focus on taking this one step forward."
            )

        # 4. ENCOURAGEMENT

        st.markdown("---")

        st.header("4. A message for your journey")

        st.markdown(
            """
            > Your past losses do not define your worth.
            >
            > Your mistakes do not erase your potential.
            >
            > You can learn, rebuild, pursue opportunities, and create
            > a different future, one decision at a time.
            """
        )

        st.success(
            "Every meaningful new beginning starts with one step. "
            "Keep moving forward."
        )

        st.caption("URAFITE — Reclaim Your Future.")

    else:

        st.markdown("---")

        st.info(
            "Your next chapter starts with a decision. "
            "Select your interests above to discover possible pathways."
        )

elif page == "AI Companion":
    language = st.session_state.get("urafite_language", "English")
    hiro_copy = {
        "English": {
            "title": "🌱 Hiro – Your recovery and support guide",
            "subtitle": "A friendly place to talk, find support and choose a helpful next step.",
            "intro": "Hiro is here to help you reflect, manage difficult moments and find practical next steps. You can talk about gambling, money, stress, relationships, education or work.",
            "boundary": "Hiro is a digital support guide, not a therapist or emergency service. You can also choose Professional Support to learn when human help may be useful."
        },
        "Kinyarwanda": {
            "title": "🌱 Hiro – Umufasha mu rugendo rwo gukira no kwiyubaka",
            "subtitle": "Ahantu waganirira wisanzuye, ukabona ubufasha kandi ugahitamo intambwe nziza ikurikira.",
            "intro": "Hiro arahari kugira ngo agufashe gutekereza ku byo urimo kunyuramo, guhangana n'ibihe bikomeye no kubona intambwe zifatika wakurikira. Ushobora kuganira ku rusimbi, amafaranga, imihangayiko, imibanire, amashuri cyangwa akazi.",
            "boundary": "Hiro ni umufasha ukoresha ikoranabuhanga; si umuvuzi cyangwa serivisi y'ubutabazi bwihutirwa. Ushobora no guhitamo Ubufasha bw'inzobere kugira ngo umenye igihe ubufasha bw'umuntu wabigize umwuga bukenewe."
        },
        "Français": {
            "title": "🌱 Hiro – Votre guide de rétablissement et de soutien",
            "subtitle": "Un espace bienveillant pour parler, trouver du soutien et choisir une prochaine étape utile.",
            "intro": "Hiro vous aide à réfléchir, à traverser les moments difficiles et à trouver des étapes concrètes. Vous pouvez parler des jeux d'argent, de finances, de stress, de relations, d'études ou de travail.",
            "boundary": "Hiro est un guide numérique de soutien, et non un thérapeute ou un service d'urgence. Vous pouvez également consulter la rubrique Soutien professionnel pour savoir quand une aide humaine peut être utile."
        }
    }
    copy = hiro_copy.get(language, hiro_copy["English"])
    st.title(copy["title"])
    st.subheader(copy["subtitle"])
    st.write(copy["intro"])
    st.caption(copy["boundary"])

    st.info(
        "Prototype transparency: responses are selected from predefined guidance. "
        "The companion may misunderstand messages and cannot monitor your safety or replace a qualified professional."
    )

    language = st.session_state.get("urafite_language", "English")
    if "urafite_chat_history" not in st.session_state:
        welcome = {
            "English": "Hello! 🌱 I'm here to help you think through one next step. You can talk about gambling urges, money, stress, study, work or personal goals.",
            "Kinyarwanda": "Muraho! 🌱 Ndi hano kugira ngo tuganire ku ntambwe imwe yakuganisha imbere. Ushobora kumbwira ibyerekeye urusimbi, amafaranga, imihangayiko, amasomo, akazi cyangwa intego zawe.",
            "Français": "Bonjour ! 🌱 Je suis là pour vous aider à réfléchir à une prochaine étape. Vous pouvez parler des envies de jouer, d'argent, de stress, d'études, de travail ou de vos objectifs."
        }
        st.session_state["urafite_chat_history"] = [{"role": "assistant", "content": welcome.get(language, welcome["English"])}]

    # Reset the conversation if the selected interface language changes.
    if st.session_state.get("chat_language") != language:
        st.session_state["chat_language"] = language
        if len(st.session_state["urafite_chat_history"]) == 1:
            welcome = {
                "English": "Hello! 🌱 I'm here to help you think through one next step. What would you like to focus on?",
                "Kinyarwanda": "Muraho! 🌱 Ndi hano kugufasha gutekereza ku ntambwe ikurikira. Ni iki wifuza kwitaho?",
                "Français": "Bonjour ! 🌱 Je suis là pour vous aider à réfléchir à la prochaine étape. Sur quoi souhaitez-vous vous concentrer ?"
            }
            st.session_state["urafite_chat_history"][0]["content"] = welcome.get(language, welcome["English"])

    def urafite_support_response(message, lang, history):
      """Context-aware, rules-based support. This is not a live AI model."""
      text = (message or "").lower().strip()
      lang = lang if lang in ("English", "Kinyarwanda", "Français") else "English"

      keywords = {
          "crisis": [
              "suicide", "kill myself", "end my life", "want to die",
              "don't want to live", "do not want to live", "hurt myself",
              "self harm", "self-harm", "kwiyahura", "kwica",
              "sinshaka kubaho", "me suicider", "mettre fin à mes jours"
          ],
          "frustration": [
              "stop asking", "don't ask", "do not ask", "you keep asking",
              "leave me alone", "stop repeating", "not helpful", "annoying",
              "shut up", "reka kumbaza", "ntukomeze kumbaza", "bireke",
              "arrête de demander", "ne me demande", "cesse de demander"
          ],
          "gambling": [
              "gambling", "betting", "gamble", "gambl", "bet ", "casino", "sportsbook",
              "chasing losses", "urusimbi", "gutega", "guteza", "parier",
              "jeu d'argent", "jeux d'argent"
          ],
          "money": [
              "money", "debt", "financial", "savings", "salary", "income",
              "broke", "lost money", "expenses", "budget", "phone", "buy",
              "purchase", "amafaranga", "umwenda", "kuzigama", "ikiguzi",
              "téléphone", "argent", "dette", "épargne", "acheter"
          ],
          "opportunity": [
              "education", "school", "university", "scholarship", "study",
              "learning", "career", "job", "employment", "skills", "business",
              "internship", "training", "amashuri", "akazi", "buruse",
              "ubumenyi", "études", "emploi", "bourse", "formation",
              "compétences"
          ],
          "emotion": [
              "sad", "stressed", "stress", "anxious", "anxiety", "lonely",
              "ashamed", "guilty", "hopeless", "overwhelmed", "depressed",
              "failure", "regret", "agahinda", "mpangayitse", "mfite ubwoba",
              "nacitse intege", "triste", "stressé", "angoissé", "honte",
              "désespéré"
          ]
      }

      def detect_topic(value):
          # Safety and user frustration always have priority.
          for topic in ("crisis", "frustration"):
              if any(term in value for term in keywords[topic]):
                  return topic

          # Recognise emotional triggers before general gambling topics.
          for topic in ("emotion", "money", "opportunity", "gambling"):
              if any(term in value for term in keywords[topic]):
                  return topic

          return None

      # Detect the user's current topic.
      category = detect_topic(text)

      # Recognise emotional triggers connected to gambling.
      stress_triggers = (
          "stress", "stressed", "anxiety", "anxious",
          "pressure", "overwhelmed", "mpangayitse",
          "stressé", "angoissé"
      )

      gambling_terms = keywords["gambling"]

      has_stress_trigger = any(term in text for term in stress_triggers)
      mentions_gambling = any(term in text for term in gambling_terms)

      # Crisis and frustration must never be overridden by this shortcut.
      if (
          has_stress_trigger
          and mentions_gambling
          and category not in ("crisis", "frustration")
      ):
          trigger_responses = {
              "English": (
                  "Thank you for recognising this connection. Stress can make "
                  "gambling feel like a temporary escape, but it may create "
                  "more pressure afterwards. When the urge appears, try stepping "
                  "away from betting, taking a short walk, breathing slowly, "
                  "or contacting someone you trust. You can learn to respond "
                  "to stress without placing another bet.\n\n"
                  "Would you like to explore what tends to happen just before the urge?"
              ),
              "Kinyarwanda": (
                  "Urakoze kumenya isano iri hagati y'imihangayiko n'urusimbi. "
                  "Iyo uhangayitse, ushobora kumva ko gutega biguha agahenge "
                  "by'igihe gito, ariko bishobora kongera ibibazo. Iyo wumvise "
                  "ushaka gutega, jya kure y'urusimbi, genda n'amaguru gato, "
                  "humeka buhoro cyangwa uvugishe umuntu wiringira.\n\n"
                  "Wifuza ko turebera hamwe ibikunze kuba mbere y'uko wumva ushaka gutega?"
              ),
              "Français": (
                  "Merci d'avoir identifié ce lien. Le stress peut donner "
                  "l'impression que les jeux d'argent offrent un soulagement "
                  "temporaire, mais ils risquent d'aggraver la pression. "
                  "Lorsque l'envie apparaît, éloignez-vous des paris, "
                  "faites une petite promenade, respirez lentement ou "
                  "contactez une personne de confiance.\n\n"
                  "Souhaitez-vous explorer ce qui se passe généralement juste avant cette envie ?"
              ),
          }

          return trigger_responses[lang]

      # Recognise self-blame and respond without judgment.
      self_blame_phrases = (
          "i am stupid", "i'm stupid", "im stupid",
          "i am a failure", "i'm a failure",
          "i hate myself", "i am useless",
          "i feel worthless", "it is my stupidity",
          "i think i am stupid", "i think i'm stupid",
          "ndi injiji", "ndi igicucu", "ndumva ndi injiji",
          "je suis stupide", "je suis nul",
          "je me déteste", "je ne vaux rien"
      )

      if category not in ("crisis", "frustration") and any(
          phrase in text for phrase in self_blame_phrases
      ):
          self_blame_responses = {
              "English": (
                  "I want you to know that struggling with gambling "
                  "does not mean you are stupid or a failure. Gambling "
                  "can become difficult to manage, especially when "
                  "stress and financial pressure are involved. Instead "
                  "of blaming yourself, let's focus on understanding "
                  "what triggers the behaviour and finding a healthier "
                  "way forward. You deserve support, not judgment."
              ),
              "Kinyarwanda": (
                  "Kugorwa no kureka urusimbi ntibivuze ko uri injiji "
                  "cyangwa ko watsinzwe. Urusimbi rushobora kugorana "
                  "kurucikaho, cyane cyane iyo hari imihangayiko "
                  "n'ibibazo by'amafaranga. Aho kwishinja, reka "
                  "twibande ku kumenya ibigutera gutega no gushaka "
                  "ubundi buryo bwiza bwo kubyitwaramo. Ukwiriye "
                  "ubufasha, si ugucirwa urubanza."
              ),
              "Français": (
                  "Avoir des difficultés avec les jeux d'argent ne "
                  "signifie pas que vous êtes stupide ou incapable. "
                  "Il peut être difficile de changer cette habitude, "
                  "surtout en période de stress ou de difficultés "
                  "financières. Au lieu de vous blâmer, essayons "
                  "de comprendre les déclencheurs et de trouver "
                  "une manière plus saine d'avancer. Vous méritez "
                  "du soutien, pas du jugement."
              )
          }
          return self_blame_responses[lang]

      # Understand requests for practical help in the current conversation.
      action_phrases = (
          "what can i do", "what should i do", "how can i stop",
          "how do i stop", "what can i do now", "what next",
          "how do i deal with this", "what can i do man",
          "none nakora iki", "nakora iki", "nabigenza nte",
          "que puis-je faire", "que dois-je faire",
          "comment arrêter", "comment faire"
      )

      recent_assistant_messages = [
          item.get("content", "").lower()
          for item in history[:-1]
          if item.get("role") == "assistant"
      ][-3:]

      stress_gambling_context = any(
          "stress can make gambling feel like a temporary escape" in item
          or "stress peut donner l'impression que les jeux d'argent" in item
          or "imihangayiko n'urusimbi" in item
          for item in recent_assistant_messages
      )

      # Normalise punctuation in short follow-up requests.
      action_text = text.translate(str.maketrans("", "", ",?.!"))

      # Remember the user's previous messages.
      previous_user_context = " ".join(
          item.get("content", "").lower()
          for item in history[:-1]
          if item.get("role") == "user"
      )

      has_previous_stress_gambling = (
          any(term in previous_user_context for term in stress_triggers)
          and any(term in previous_user_context for term in gambling_terms)
      )

      # Recognise requests for practical help.
      if (
          category not in ("crisis", "frustration")
          and (stress_gambling_context or has_previous_stress_gambling)
          and any(phrase in action_text for phrase in action_phrases)
      ):
          action_responses = {
              "English": (
                  "Let's start with three practical steps. First, "
                  "when stress appears, delay any decision to gamble "
                  "and give yourself 15 minutes away from betting. "
                  "Second, step away from betting apps and protect "
                  "money needed for essentials. Third, try walking, "
                  "slow breathing or talking to someone you trust. "
                  "You do not have to change everything today. "
                  "Start with one step."
              ),
              "Kinyarwanda": (
                  "Reka dutangire ku ntambwe eshatu. Iyo uhangayitse, "
                  "banza utegereze iminota 15 utarafata icyemezo cyo "
                  "gutega. Icya kabiri, jya kure ya porogaramu "
                  "z'urusimbi kandi urinde amafaranga y'ibikenewe. "
                  "Icya gatatu, gerageza kugenda n'amaguru, guhumeka "
                  "buhoro cyangwa kuvugisha umuntu wiringira. "
                  "Tangira ku ntambwe imwe."
              ),
              "Français": (
                  "Commençons par trois étapes pratiques. Lorsque "
                  "le stress apparaît, attendez 15 minutes avant "
                  "toute décision de parier. Ensuite, éloignez-vous "
                  "des applications de paris et protégez l'argent "
                  "nécessaire à vos besoins essentiels. Enfin, "
                  "essayez de marcher, de respirer lentement ou "
                  "de parler à une personne de confiance. "
                  "Commencez par une seule étape."
              )
          }
          return action_responses[lang]

      # Understand short replies using the last assistant question.
      last_assistant_message = next(
          (
              item.get("content", "").lower()
              for item in reversed(history[:-1])
              if item.get("role") == "assistant"
          ),
          ""
      )

      affirmative_replies = {
          "yes", "yeah", "yep", "sure", "okay", "ok",
          "please do", "yego", "yego rwose", "oui",
          "d'accord", "bien sûr"
      }

      negative_replies = {
          "no", "nope", "not now", "not really",
          "oya", "non", "pas maintenant"
      }

      user_reply = text.strip().rstrip(".,!?")
      asked_about_trigger = any(term in last_assistant_message for term in (
          "identify what triggered",
          "identifier ce qui a déclenché",
          "gutera gushaka gutega",
          "what tends to happen just before the urge",
          "ce qui se passe généralement juste avant cette envie",
          "ibikunze kuba mbere y'uko wumva ushaka gutega"
      ))

      # Interpret yes/no only when Hiro has just asked about gambling triggers.
      # Never let a short reply override crisis or frustration handling.
      if (
          category not in ("crisis", "frustration")
          and asked_about_trigger
          and user_reply in affirmative_replies
      ):
          return {
              "English": (
                  "Let's explore what happened before the urge. "
                  "Were you feeling stressed, lonely, bored, or worried "
                  "about money? You can share only what you feel "
                  "comfortable sharing."
              ),
              "Kinyarwanda": (
                  "Reka turebe icyabaye mbere y'uko wumva ushaka gutega. "
                  "Wari uhangayitse, ufite irungu, urambiwe cyangwa "
                  "uhangayikishijwe n'amafaranga? Vuga gusa ibyo "
                  "wumva wisanzuyeho."
              ),
              "Français": (
                  "Essayons de comprendre ce qui s'est passé avant "
                  "cette envie. Étiez-vous stressé, seul, ennuyé "
                  "ou préoccupé par l'argent ? Partagez uniquement "
                  "ce que vous souhaitez."
              )
          }[lang]

      if (
          category not in ("crisis", "frustration")
          and asked_about_trigger
          and user_reply in negative_replies
      ):
          return {
              "English": "That's okay. We can take another direction or pause. You are in control of what you want to discuss.",
              "Kinyarwanda": "Ni sawa. Dushobora kuganira ku kindi cyangwa tukaruhuka. Ni wowe uhitamo ibyo ushaka kuganiraho.",
              "Français": "C'est tout à fait acceptable. Nous pouvons changer de sujet ou faire une pause. Vous choisissez ce que vous souhaitez aborder."
          }[lang]

      # Use the immediately preceding user topic for short follow-ups only.
      # A clearly detected new topic always takes precedence.
      previous_topic = None
      previous_user_messages = [
          item.get("content", "").lower().strip()
          for item in history[:-1]
          if item.get("role") == "user" and item.get("content")
      ]
      if previous_user_messages:
          for earlier_message in reversed(previous_user_messages[-4:]):
              previous_topic = detect_topic(earlier_message)
              if previous_topic:
                  break

      follow_up_phrases = (
          "yes", "yeah", "okay", "ok", "no", "maybe", "that one",
          "tell me more", "what next", "how", "why", "please do",
          "yego", "oya", "birashoboka", "none se", "oui", "non",
          "d'accord", "expliquez", "et ensuite"
      )
      is_short_follow_up = (
          len(text.split()) <= 7
          or any(phrase in text for phrase in follow_up_phrases)
      )
      if category is None and is_short_follow_up and previous_topic:
          category = previous_topic
      if category is None:
          category = "general"

      replies = {
          "English": {
              "crisis": [
                  "I'm really sorry this feels so painful. You deserve immediate support from a real person. If you may act on these thoughts or are in immediate danger, contact local emergency services or go to the nearest hospital emergency department now. If possible, tell someone you trust and ask them to stay with you. I cannot assess risk or provide emergency intervention."
              ],
              "frustration": [
                  "You're right to tell me. I'm sorry this has felt repetitive or unhelpful. I won't keep asking questions. We can pause here, or I can share one practical suggestion without asking you to explain more."
              ],
              "gambling": [
                  "Thank you for telling me. Trying to win back losses can increase financial pressure. For now, consider not placing another bet, stepping away from betting apps and adverts, and asking someone you trust to help you create distance from money you might gamble.",
                  "A difficult urge does not have to become another bet. You could delay any decision, leave the betting environment and contact someone you trust. RECOVER can help you reflect on triggers, while REBUILD can support a practical money plan."
              ],
              "money": [
                  "Let's make this manageable. Protect essentials first: food, housing, transport, education and existing obligations. Then work out what is safe to spend and what you can set aside. Avoid borrowing or betting to try to multiply money; REBUILD can help you organise a budget in RWF.",
                  "Financial pressure can make every decision feel urgent. Start with what must be paid, what can wait and what support is available. A simple plan is safer than trying to recover money through another bet."
              ],
              "opportunity": [
                  "That is a worthwhile direction. Turn it into one manageable action: identify your goal, find one credible programme or employer, check eligibility and deadlines, then prepare the required documents. RECONNECT can help you shape an action plan. Opportunities displayed there are examples unless independently verified.",
                  "You do not need to solve your whole career plan today. Choose one target, check its requirements and deadline, and prepare one part of your application. RECONNECT is designed to help you move from an idea to a practical next step."
              ],
              "emotion": [
                  "Thank you for being open. You do not have to fix everything at once. It may help to pause, take a few slow breaths, move somewhere you feel comfortable, or contact someone you trust. If these feelings persist or become difficult to manage, consider speaking with a qualified counsellor or mental-health professional.",
                  "That sounds like a heavy moment. Try to make the next few minutes gentler: step away from pressure, breathe slowly and reach out to someone you trust. You deserve support, and a qualified professional can help if this keeps feeling difficult."
              ],
              "general": [
                  "I hear you. We can take this one step at a time. I can offer practical guidance about reducing gambling harm, managing money, finding opportunities or handling a difficult moment. You do not need to share anything you would rather keep private.",
                  "Thanks for sharing that with me. I may not understand every detail, but I can help you explore a practical next step around wellbeing, gambling, finances, education or work."
              ]
          },
          "Kinyarwanda": {
              "crisis": [
                  "Mbabajwe n'uko uri kunyura mu bihe bikomeye. Ukwiriye kubona ubufasha bw'umuntu ako kanya. Niba ushobora kwigirira nabi cyangwa uri mu kaga, hamagara ubutabazi bwihutirwa cyangwa ujye ku bitaro bikwegereye ubu. Niba bishoboka, bwira umuntu wiringira agusigarane. Iyi porogaramu ntishobora gusuzuma ibyago cyangwa gutanga ubutabazi bwihutirwa."
              ],
              "frustration": [
                  "Urakoze kumbwira uko ubyumva. Mbabarira niba ibisubizo byanjye byagiye bisubiramo cyangwa bitagufashije. Sinzakomeza kukubaza ibibazo. Dushobora kuruhuka hano cyangwa nkaguha igitekerezo kimwe gifatika utiriwe usobanura byinshi."
              ],
              "gambling": [
                  "Urakoze kubimbwira. Kugerageza kugaruza amafaranga watakaje mu rusimbi bishobora kongera ibibazo by'amafaranga. Ubu gerageza kutongera gutega, wigire kure ya porogaramu n'amatangazo y'urusimbi, kandi usabe umuntu wiringira kugufasha kwirinda gukoresha amafaranga mu gutega.",
                  "Kugira ubushake bwo kongera gutega ntibivuze ko ugomba kubikora. Ushobora kubanza gutegereza, kuva aho bategera no kuvugisha umuntu wiringira. RECOVER yagufasha gutekereza ku bigutera gutega, naho REBUILD ikagufasha gutegura imikoreshereze y'amafaranga."
              ],
              "money": [
                  "Reka tubishyire mu buryo bworoshye. Banza urinde ibikenewe by'ibanze: ibiribwa, icumbi, ingendo, amashuri n'imyenda. Hanyuma uteganye amafaranga ushobora gukoresha n'ayo kuzigama. Irinde gufata umwenda cyangwa gutega kugira ngo wikubire amafaranga. REBUILD yagufasha gutegura ingengo y'imari muri RWF.",
                  "Ibibazo by'amafaranga bishobora gutuma buri cyemezo wumva ko cyihutirwa. Banza wandike ibikenewe kwishyurwa, ibishobora gutegereza n'ubufasha ushobora kubona. Gahunda yoroshye iruta kugerageza kugaruza amafaranga mu rusimbi."
              ],
              "opportunity": [
                  "Icyo ni intego nziza. Yigabanyemo intambwe nto: menya icyo ushaka kugeraho, shaka gahunda cyangwa umukoresha wizewe, reba ibisabwa n'igihe ntarengwa, utegure inyandiko. RECONNECT yagufasha gukora gahunda. Amahirwe agaragara kuri porogaramu ni ingero keretse habanje kugenzurwa ko akiriho.",
                  "Ntugomba gutegura ejo hazaza hawe hose uyu munsi. Hitamo intego imwe, reba ibisabwa n'igihe ntarengwa, hanyuma utegure igice kimwe cy'ubusabe bwawe. RECONNECT yagufasha guhindura igitekerezo intambwe ifatika."
              ],
              "emotion": [
                  "Urakoze kuvuga uko wiyumva. Ntugomba gukemura byose icyarimwe. Fata akanya, uhumeke buhoro, ujye ahantu wumva utuje cyangwa uvugishe umuntu wiringira. Niba ibi byiyumvo bikomeje cyangwa bikurushya, tekereza kuganira n'umujyanama cyangwa inzobere mu buzima bwo mu mutwe.",
                  "Birasa n'aho uri kunyura mu bihe bikuremereye. Gerageza kworoshya iminota mike iri imbere: va mu bintu bikugora, uhumeke buhoro kandi uvugishe umuntu wiringira. Ukwiriye ubufasha; inzobere ishobora kugufasha niba bikomeje kukugora."
              ],
              "general": [
                  "Ndakumva. Dushobora kugenda intambwe ku yindi. Nshobora kugufasha gutekereza ku kugabanya ingaruka z'urusimbi, gucunga amafaranga, gushaka amahirwe cyangwa guhangana n'ibihe bikomeye. Ntugomba kuvuga ibyo wifuza kugumana ibanga.",
                  "Urakoze kubimbwira. Sinshobora kumva buri kantu kose, ariko nshobora kugufasha gutekereza ku ntambwe ikurikira yerekeye ubuzima bwiza, urusimbi, amafaranga, amashuri cyangwa akazi."
              ]
          },
          "Français": {
              "crisis": [
                  "Je suis désolé que vous traversiez une période aussi douloureuse. Vous méritez une aide humaine immédiate. Si vous risquez de passer à l'acte ou êtes en danger immédiat, contactez les services d'urgence locaux ou rendez-vous au service des urgences de l'hôpital le plus proche. Si possible, prévenez une personne de confiance et demandez-lui de rester avec vous. Cette plateforme ne peut pas évaluer le risque ni intervenir en urgence."
              ],
              "frustration": [
                  "Merci de me l'avoir dit. Je suis désolé si mes réponses ont été répétitives ou peu utiles. Je ne vais pas continuer à poser des questions. Nous pouvons faire une pause ou je peux proposer une seule piste concrète sans vous demander davantage d'explications."
              ],
              "gambling": [
                  "Merci de me l'avoir dit. Essayer de récupérer des pertes en rejouant peut aggraver la pression financière. Pour le moment, essayez de ne pas miser à nouveau, éloignez-vous des applications et publicités de paris et demandez à une personne de confiance de vous aider à protéger l'argent que vous pourriez miser.",
                  "Ressentir l'envie de rejouer ne signifie pas que vous devez agir. Vous pouvez attendre avant toute décision, quitter l'environnement de jeu et contacter une personne de confiance. RECOVER aide à réfléchir aux déclencheurs et REBUILD à organiser un plan financier."
              ],
              "money": [
                  "Passons au concret. Protégez d'abord les besoins essentiels : alimentation, logement, transport, études et obligations existantes. Déterminez ensuite ce que vous pouvez dépenser sans risque et ce que vous souhaitez épargner. Évitez d'emprunter ou de parier pour multiplier votre argent. REBUILD peut vous aider à organiser votre budget en RWF.",
                  "La pression financière peut donner l'impression que chaque décision est urgente. Commencez par noter ce qui doit être payé, ce qui peut attendre et les aides possibles. Un plan simple est plus sûr que de tenter de récupérer de l'argent en rejouant."
              ],
              "opportunity": [
                  "C'est un objectif intéressant. Transformez-le en une petite action : précisez votre objectif, trouvez un programme ou un employeur fiable, vérifiez les critères et les délais, puis préparez les documents nécessaires. RECONNECT peut vous aider à établir un plan. Les possibilités affichées sont des exemples tant qu'elles n'ont pas été vérifiées.",
                  "Vous n'avez pas besoin de définir tout votre avenir aujourd'hui. Choisissez un objectif, vérifiez les conditions et la date limite, puis préparez une partie de votre candidature. RECONNECT vous aide à transformer une idée en prochaine étape concrète."
              ],
              "emotion": [
                  "Merci de partager ce que vous ressentez. Vous n'avez pas à tout résoudre aujourd'hui. Faites une pause, respirez lentement, installez-vous dans un endroit où vous vous sentez à l'aise ou contactez une personne de confiance. Si cette détresse persiste, envisagez de parler à un professionnel qualifié.",
                  "Cela semble être un moment difficile. Essayez de rendre les prochaines minutes un peu plus faciles : éloignez-vous de la pression, respirez lentement et contactez une personne de confiance. Vous méritez du soutien et un professionnel qualifié peut vous aider si cela continue."
              ],
              "general": [
                  "Je vous entends. Nous pouvons avancer étape par étape. Je peux proposer des pistes concrètes pour réduire les risques liés aux jeux d'argent, gérer votre budget, trouver des possibilités ou traverser un moment difficile. Vous n'avez pas à partager ce que vous préférez garder privé.",
                  "Merci de me l'avoir confié. Je ne comprends peut-être pas chaque détail, mais je peux vous aider à réfléchir à une prochaine étape concernant le bien-être, les jeux d'argent, les finances, les études ou le travail."
              ]
          }
      }

      # Crisis and frustration always override conversational context.
      options = replies[lang][category]
      recent_assistant = [
          item.get("content", "")
          for item in history[:-1]
          if item.get("role") == "assistant"
      ][-4:]
      # Rotate alternatives to avoid sending the same wording repeatedly.
      response = next(
          (option for option in options if option not in recent_assistant),
          options[0]
      )

      # Add one focused prompt for ordinary support topics, but avoid
      # interrogating someone who is distressed or has asked us to stop.
      prompts = {
          "English": {
              "gambling": ["Would it help to identify what triggered the urge today?", "A useful next step could be making it harder to access betting for the rest of today."],
              "money": ["A useful starting point is separating essential expenses from expenses that can wait.", "You could begin with a simple list of money coming in and essential costs."],
              "opportunity": ["You could start by choosing one opportunity area: study, skills, work or business.", "The next practical step is to check one programme's eligibility and deadline."],
              "emotion": ["For now, consider choosing one small thing that would help you feel supported.", "You might begin by identifying one person you feel comfortable contacting."],
              "general": ["You can tell me which of those areas feels most important right now.", "We can focus on just one issue rather than everything at once."]
          },
          "Kinyarwanda": {
              "gambling": ["Byagufasha gutekereza ku cyaguteye gushaka gutega uyu munsi?", "Intambwe nziza yaba ukugabanya uburyo wageraho porogaramu z'urusimbi uyu munsi."],
              "money": ["Waheraho utandukanya amafaranga y'ibikenewe n'ashobora gutegereza.", "Ushobora gutangira wandika amafaranga winjiza n'ibikenewe kwishyurwa."],
              "opportunity": ["Wahitamo aho uhera: amashuri, ubumenyi, akazi cyangwa ubucuruzi.", "Intambwe ikurikira ni ukureba ibisabwa n'igihe ntarengwa kuri gahunda imwe."],
              "emotion": ["Ubu hitamo ikintu kimwe gito cyatuma wumva ubonye ubufasha.", "Ushobora gutekereza ku muntu umwe wumva wakwiyambaza."],
              "general": ["Wambwira icyiciro wumva cy'ingenzi kuri wowe ubu.", "Dushobora kwibanda ku kibazo kimwe aho kugerageza gukemura byose."]
          },
          "Français": {
              "gambling": ["Souhaitez-vous identifier ce qui a déclenché cette envie aujourd'hui ?", "Une étape utile serait de limiter votre accès aux applications de paris pour le reste de la journée."],
              "money": ["Vous pouvez commencer par distinguer les dépenses essentielles de celles qui peuvent attendre.", "Une première étape consiste à noter vos revenus et vos dépenses indispensables."],
              "opportunity": ["Vous pourriez choisir un domaine prioritaire : études, compétences, emploi ou entrepreneuriat.", "La prochaine étape concrète consiste à vérifier les critères et la date limite d'un programme."],
              "emotion": ["Pour le moment, choisissez une petite chose qui pourrait vous apporter du soutien.", "Vous pourriez penser à une personne que vous vous sentez à l'aise de contacter."],
              "general": ["Vous pouvez me dire quel domaine vous semble le plus important actuellement.", "Nous pouvons nous concentrer sur un seul sujet à la fois."]
          }
      }

      if category not in ("crisis", "frustration"):
          prompt_options = prompts[lang].get(category, [])
          if prompt_options:
              recent_prompts = [p for p in prompt_options if any(p in item for item in recent_assistant)]
              available_prompts = [p for p in prompt_options if p not in recent_prompts]
              prompt = available_prompts[0] if available_prompts else prompt_options[0]
              response = response + "\n\n" + prompt

      return response

    # Text and voice are two interfaces to the same conversation history.
    voice_labels = {
        "English": {"text": "Text conversation", "voice": "Voice conversation", "choose": "Choose how you would like to communicate", "record": "Record a voice message", "listen": "Listen to Hiro's latest response", "voice_note": "Your browser must support microphone access and audio playback. First-time speech recognition setup may take a few minutes.", "install": "Voice transcription needs the optional faster-whisper package. In your terminal, run: pip install faster-whisper", "processing": "Transcribing your message...", "failed": "I could not transcribe that recording. Please try again or use text conversation."},
        "Kinyarwanda": {"text": "Ikiganiro cyanditse", "voice": "Ikiganiro cy'ijwi", "choose": "Hitamo uko wifuza kuganira", "record": "Andika ubutumwa bw'ijwi", "listen": "Umva igisubizo giheruka cya Hiro", "voice_note": "Mudasobwa cyangwa telefoni yawe igomba kwemera gukoresha mikoro no kumva amajwi. Gutegura bwa mbere kumenya amagambo yavuzwe bishobora gufata iminota mike.", "install": "Kugira ngo ijwi rihindurwe inyandiko, shyiramo porogaramu y'inyongera. Koresha: pip install faster-whisper", "processing": "Turimo guhindura ijwi inyandiko...", "failed": "Ntibyashobotse kumva neza amajwi yafashwe. Ongera ugerageze cyangwa ukoreshe ikiganiro cyanditse."},
        "Français": {"text": "Conversation écrite", "voice": "Conversation vocale", "choose": "Choisissez votre mode de communication", "record": "Enregistrer un message vocal", "listen": "Écouter la dernière réponse de Hiro", "voice_note": "Votre navigateur doit autoriser l'accès au microphone et la lecture audio. La première configuration de la reconnaissance vocale peut prendre quelques minutes.", "install": "La transcription vocale nécessite le module optionnel faster-whisper. Dans le terminal, exécutez : pip install faster-whisper", "processing": "Transcription de votre message...", "failed": "Impossible de transcrire cet enregistrement. Réessayez ou utilisez la conversation écrite."}
    }
    voice_copy = voice_labels.get(language, voice_labels["English"])
    mode = st.radio(voice_copy["choose"], [voice_copy["text"], voice_copy["voice"]], horizontal=True, key="urafite_chat_mode")

    st.markdown("### 💬 Your conversation")
    st.caption("You can switch the interface language in the sidebar. Avoid sharing passwords, ID numbers or other highly sensitive information.")

    if mode == voice_copy["voice"]:
        st.info(voice_copy["voice_note"])
        audio_value = st.audio_input(voice_copy["record"], key="urafite_voice_recording")
        if audio_value is not None:
            audio_bytes = audio_value.getvalue()
            audio_digest = hashlib.sha256(audio_bytes).hexdigest()
            if st.session_state.get("urafite_last_audio_digest") != audio_digest:
                try:
                    from faster_whisper import WhisperModel

                    @st.cache_resource
                    def _urafite_get_whisper_model():
                        return WhisperModel("base", device="cpu", compute_type="int8")

                    model = _urafite_get_whisper_model()
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                        temp_audio.write(audio_bytes)
                        audio_path = temp_audio.name
                    try:
                        language_codes = {"English": "en", "Kinyarwanda": "rw", "Français": "fr"}
                        segments, _ = model.transcribe(audio_path, language=language_codes.get(language), vad_filter=True)
                        transcript = " ".join(segment.text.strip() for segment in segments).strip()
                    finally:
                        Path(audio_path).unlink(missing_ok=True)

                    if transcript:
                        st.session_state["urafite_last_audio_digest"] = audio_digest
                        st.session_state["urafite_chat_history"].append({"role": "user", "content": transcript})
                        response = urafite_support_response(transcript, language, st.session_state["urafite_chat_history"])
                        st.session_state["urafite_chat_history"].append({"role": "assistant", "content": response})
                        st.session_state["urafite_pending_voice_reply"] = response
                        st.rerun()
                    else:
                        st.warning(voice_copy["failed"])
                except ImportError:
                    st.session_state.pop("urafite_last_audio_digest", None)
                    st.warning(voice_copy["install"])
                except Exception as exc:
                    st.session_state.pop("urafite_last_audio_digest", None)
                    st.error(voice_copy["failed"])
                    st.caption(f"Technical detail: {exc}")

    for chat_message in st.session_state["urafite_chat_history"]:
        with st.chat_message(chat_message["role"]):
            st.markdown(chat_message["content"])

    if mode == voice_copy["text"]:
        user_message = st.chat_input(
            "Share what is on your mind..." if language == "English"
            else "Sangiza ibikuri ku mutima..." if language == "Kinyarwanda"
            else "Exprimez ce que vous avez à l'esprit...",
            key="urafite_chat_input"
        )
        if user_message:
            st.session_state["urafite_chat_history"].append({"role": "user", "content": user_message})
            response = urafite_support_response(user_message, language, st.session_state["urafite_chat_history"])
            st.session_state["urafite_chat_history"].append({"role": "assistant", "content": response})
    else:
        latest_reply = next((m["content"] for m in reversed(st.session_state["urafite_chat_history"]) if m["role"] == "assistant"), "")
        if latest_reply:
            locale = {"English": "en-US", "Kinyarwanda": "rw-RW", "Français": "fr-FR"}.get(language, "en-US")
            safe_text = json.dumps(latest_reply, ensure_ascii=False)
            safe_locale = json.dumps(locale)
            button_label = json.dumps("🔊 " + voice_copy["listen"], ensure_ascii=False)
            speech_unsupported = json.dumps({"English": "Speech playback is not supported by this browser.", "Kinyarwanda": "Iyi mushakisha ntishobora gusoma igisubizo mu ijwi.", "Français": "La lecture audio n'est pas prise en charge par ce navigateur."}.get(language, "Speech playback is not supported by this browser."), ensure_ascii=False)
            components.html(f'''<html><body style="font-family:sans-serif;">
            <button id="hiro-speak" style="padding:10px 16px;border:0;border-radius:8px;background:#176b45;color:white;font-size:15px;cursor:pointer;"></button>
            <script>
            const speakButton = document.getElementById('hiro-speak');
            speakButton.textContent = {button_label};
            speakButton.addEventListener('click', () => {{
                if (!('speechSynthesis' in window)) {{ alert({speech_unsupported}); return; }}
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance({safe_text});
                utterance.lang = {safe_locale};
                window.speechSynthesis.speak(utterance);
            }});
            </script></body></html>''', height=55)


    col_a, col_b = st.columns([1, 3])
    with col_a:
        if st.button("Start a new conversation", use_container_width=True):
            welcome = {
                "English": "Hello! 🌱 What would you like to focus on today?",
                "Kinyarwanda": "Muraho! 🌱 Ni iki wifuza kwitaho uyu munsi?",
                "Français": "Bonjour ! 🌱 Sur quoi souhaitez-vous vous concentrer aujourd'hui ?"
            }
            st.session_state["urafite_chat_history"] = [{"role": "assistant", "content": welcome.get(language, welcome["English"])}]
            st.rerun()
    with col_b:
        st.caption("Responses are predefined and may not understand every message. For urgent or complex needs, seek help from a qualified person.")

    st.caption("Privacy: conversation history exists only in this active Streamlit session in this prototype. Secure accounts, retention controls and deployment privacy safeguards are not yet implemented.")


elif page == "Heal and Learn Centre":
    st.title("📚 " + _urafite_translate("Heal and Learn Centre"))
    st.write(_urafite_translate("Explore educational videos, articles and mentoring resources reviewed before publication."))
    lang_code = {"English":"en", "Kinyarwanda":"rw", "Français":"fr"}.get(st.session_state.get("urafite_language", "English"), "en")
    try:
        resources = (_urafite_sb.table("learning_resources").select("id,title,resource_type,category,description,content_url,language,contributor_name,professional_credentials,created_at")
                     .eq("status", "published").eq("language", lang_code).order("created_at", desc=True).execute().data or [])
    except Exception:
        resources = []
        st.warning(_urafite_translate("Learning resources are temporarily unavailable."))
    if not resources:
        st.info(_urafite_translate("No approved resources are available in your selected language yet."))
    else:
        categories = sorted({r.get("category", "Other") for r in resources})
        chosen = st.selectbox(_urafite_translate("Filter by category"), [_urafite_translate("All categories")] + categories)
        for resource in resources:
            if chosen != _urafite_translate("All categories") and resource.get("category") != chosen:
                continue
            with st.container(border=True):
                st.subheader(resource.get("title", ""))
                st.caption(f"{resource.get('resource_type','').title()} · {resource.get('category','')}")
                if resource.get("description"):
                    st.write(resource["description"])
                if resource.get("contributor_name"):
                    st.caption(f"{_urafite_translate('Contributor')}: {resource['contributor_name']}")
                if resource.get("content_url"):
                    st.link_button(_urafite_translate("Open resource"), resource["content_url"])

elif page == "Administration":
    _admin_guard()
    st.title("⚙️ " + _urafite_translate("Administration"))
    st.write(_urafite_translate("Manage URAFITE content and monitor verified platform activity."))
    st.info(_urafite_translate("Only authorised administrators can access these management tools."))
    st.subheader(_urafite_translate("Management areas"))
    c1,c2,c3 = st.columns(3)
    with c1:
        st.metric(_urafite_translate("Your role"), _urafite_translate("Super administrator") if "super_admin" in _urafite_roles else _urafite_translate("Administrator"))
    with c2:
        st.metric(_urafite_translate("Registered accounts"), len(_safe_admin_rows("profiles", "id")))
    with c3:
        st.metric(_urafite_translate("Published opportunities"), len(_safe_admin_rows("opportunities", "id")))
    st.write(_urafite_translate("Use the administration pages in the navigation menu to manage opportunities, learning resources, grants and impact reports."))

elif page == "Impact & Evidence":
    _admin_guard()
    st.title("📊 " + _urafite_translate("Impact & Evidence"))
    st.caption(_urafite_translate("This dashboard reports platform activity, not clinical recovery outcomes."))
    profiles = _safe_admin_rows("profiles", "id,created_at,preferred_language")
    opportunities = _safe_admin_rows("opportunities", "id,status,category,created_at")
    resources = _safe_admin_rows("learning_resources", "id,status,resource_type,language,created_at")
    events = _safe_admin_rows("platform_events", "id,event_type,created_at")
    grants = _safe_admin_rows("grant_records", "id,project_name,funder,award_amount,status")
    m1,m2,m3,m4 = st.columns(4)
    m1.metric(_urafite_translate("Registered accounts"), len(profiles))
    m2.metric(_urafite_translate("Published opportunities"), sum(1 for x in opportunities if x.get("status")=="published"))
    m3.metric(_urafite_translate("Published learning resources"), sum(1 for x in resources if x.get("status")=="published"))
    m4.metric(_urafite_translate("Recorded platform events"), len(events))
    st.subheader(_urafite_translate("Activity by type"))
    if events:
        import pandas as pd
        df = pd.DataFrame(events)
        counts = df["event_type"].value_counts().rename_axis("event_type").reset_index(name="count")
        st.bar_chart(counts.set_index("event_type"))
        st.download_button(_urafite_translate("Export activity summary (CSV)"), counts.to_csv(index=False).encode("utf-8-sig"), "urafite_activity_summary.csv", "text/csv")
    else:
        st.info(_urafite_translate("No activity records yet."))
    st.subheader(_urafite_translate("Recent registrations"))
    if profiles:
        import pandas as pd
        reg = pd.DataFrame(profiles)
        if "created_at" in reg:
            reg["created_at"] = pd.to_datetime(reg["created_at"], errors="coerce", utc=True)
            reg = reg.sort_values("created_at", ascending=False)
            reg["registration_date"] = reg["created_at"].dt.strftime("%Y-%m-%d")
        display = reg.groupby("registration_date").size().reset_index(name="registrations") if "registration_date" in reg else reg.head(0)
        if not display.empty:
            st.line_chart(display.set_index("registration_date"))
    st.subheader(_urafite_translate("Grant and programme records"))
    if grants:
        import pandas as pd
        grant_df = pd.DataFrame(grants)
        st.dataframe(grant_df, use_container_width=True, hide_index=True)
        st.download_button(_urafite_translate("Export grants (CSV)"), grant_df.to_csv(index=False).encode("utf-8-sig"), "urafite_grants.csv", "text/csv")
    else:
        st.info(_urafite_translate("No grant records yet."))

elif page == "Opportunity Manager":
    _admin_guard()
    st.title("💼 " + _urafite_translate("Opportunity Manager"))
    with st.expander(_urafite_translate("Add an opportunity"), expanded=True):
        with st.form("admin_add_opportunity"):
            title = st.text_input(_urafite_translate("Title"))
            category = st.selectbox(_urafite_translate("Category"), ["scholarship","employment","internship","training","entrepreneurship","mentorship","other"], format_func=lambda x:_urafite_translate(x.title()))
            organisation = st.text_input(_urafite_translate("Organisation"))
            country = st.text_input(_urafite_translate("Country"))
            description = st.text_area(_urafite_translate("Description"))
            eligibility = st.text_area(_urafite_translate("Eligibility"))
            url = st.text_input(_urafite_translate("Application URL"))
            deadline = st.date_input(_urafite_translate("Deadline"), value=None)
            status = st.selectbox(_urafite_translate("Status"), ["draft","published","closed"], format_func=lambda x:_urafite_translate(x.title()))
            submit = st.form_submit_button(_urafite_translate("Save opportunity"), type="primary")
        if submit:
            if not title.strip() or not description.strip():
                st.warning(_urafite_translate("Title and description are required."))
            else:
                payload = {"title":title.strip(),"category":category,"organisation":organisation.strip(),"country":country.strip(),"description":description.strip(),"eligibility":eligibility.strip(),"application_url":url.strip() or None,"deadline":deadline.isoformat() if deadline else None,"status":status,"created_by":_urafite_user_id}
                try:
                    _urafite_sb.table("opportunities").insert(payload).execute()
                    st.success(_urafite_translate("Opportunity saved.")); st.rerun()
                except Exception as exc:
                    st.error(_urafite_translate("Could not save the opportunity. Check the database migration and permissions.")); st.caption(str(exc))
    st.subheader(_urafite_translate("Current opportunities"))
    rows = _safe_admin_rows("opportunities")
    if rows:
        import pandas as pd
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        choices = {f"{r['title']} ({r['status']})":r["id"] for r in rows}
        selected = st.selectbox(_urafite_translate("Select an opportunity to update"), list(choices))
        new_status = st.selectbox(_urafite_translate("New status"), ["draft","published","closed"], key="opp_new_status")
        if st.button(_urafite_translate("Update opportunity status")):
            try:
                _urafite_sb.table("opportunities").update({"status":new_status}).eq("id",choices[selected]).execute(); st.success(_urafite_translate("Opportunity status updated.")); st.rerun()
            except Exception as exc:
                st.error(_urafite_translate("Could not update opportunity.")); st.caption(str(exc))
    else: st.info(_urafite_translate("No opportunities found."))

elif page == "Heal and Learn Centre Manager":
    _admin_guard()
    st.title("📚 " + _urafite_translate("Heal and Learn Centre Manager"))
    st.caption(_urafite_translate("All professional resources should be reviewed before publication."))
    with st.expander(_urafite_translate("Add a learning resource"), expanded=True):
        with st.form("admin_add_learning_resource"):
            title = st.text_input(_urafite_translate("Title"), key="lr_title")
            resource_type = st.selectbox(_urafite_translate("Resource type"), ["video","article","post","mentoring"], format_func=lambda x:_urafite_translate(x.title()))
            category = st.text_input(_urafite_translate("Category"), value="Recovery")
            description = st.text_area(_urafite_translate("Description"), key="lr_description")
            content_url = st.text_input(_urafite_translate("Content URL"))
            lang = st.selectbox(_urafite_translate("Language"), ["en","rw","fr"], format_func=lambda x:{"en":"English","rw":"Kinyarwanda","fr":"Français"}[x])
            contributor = st.text_input(_urafite_translate("Contributor name"))
            credentials = st.text_input(_urafite_translate("Professional credentials"))
            submitted = st.form_submit_button(_urafite_translate("Submit for review"), type="primary")
        if submitted:
            if not title.strip() or not category.strip() or not description.strip():
                st.warning(_urafite_translate("Title, category and description are required."))
            else:
                payload={"title":title.strip(),"resource_type":resource_type,"category":category.strip(),"description":description.strip(),"content_url":content_url.strip() or None,"language":lang,"contributor_name":contributor.strip(),"professional_credentials":credentials.strip(),"status":"pending_review","created_by":_urafite_user_id}
                try:
                    _urafite_sb.table("learning_resources").insert(payload).execute(); st.success(_urafite_translate("Resource submitted for review.")); st.rerun()
                except Exception as exc:
                    st.error(_urafite_translate("Could not submit the resource. Check database permissions.")); st.caption(str(exc))
    st.subheader(_urafite_translate("Current learning resources"))
    rows=_safe_admin_rows("learning_resources")
    if rows:
        import pandas as pd
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
        choices={f"{r['title']} ({r['status']})":r["id"] for r in rows}
        selected=st.selectbox(_urafite_translate("Select a resource to review"),list(choices))
        new_status=st.selectbox(_urafite_translate("Review decision"),["draft","pending_review","published","rejected"],format_func=lambda x:_urafite_translate(x.replace("_"," ").title()))
        if st.button(_urafite_translate("Save review decision")):
            try:
                _urafite_sb.table("learning_resources").update({"status":new_status}).eq("id",choices[selected]).execute(); st.success(_urafite_translate("Resource status updated.")); st.rerun()
            except Exception as exc:
                st.error(_urafite_translate("Could not update resource.")); st.caption(str(exc))
    else: st.info(_urafite_translate("No learning resources found."))

elif page == "Grant & Programme Tracker":
    _admin_guard()
    st.title("🎯 " + _urafite_translate("Grant & Programme Tracker"))
    with st.expander(_urafite_translate("Add a grant or programme"), expanded=True):
        with st.form("admin_add_grant"):
            funder=st.text_input(_urafite_translate("Funder"))
            project=st.text_input(_urafite_translate("Project name"))
            amount=st.number_input(_urafite_translate("Award amount (RWF)"),min_value=0.0,step=100000.0)
            target=st.number_input(_urafite_translate("Target participants"),min_value=0,step=10)
            start=st.date_input(_urafite_translate("Start date"))
            end=st.date_input(_urafite_translate("End date"))
            report_due=st.date_input(_urafite_translate("Reporting deadline"))
            status=st.selectbox(_urafite_translate("Status"),["planned","active","completed","closed"])
            notes=st.text_area(_urafite_translate("Description"))
            save=st.form_submit_button(_urafite_translate("Save grant record"),type="primary")
        if save:
            if not funder.strip() or not project.strip(): st.warning(_urafite_translate("Funder and project name are required."))
            else:
                payload={"funder":funder.strip(),"project_name":project.strip(),"award_amount":amount,"target_participants":int(target),"start_date":start.isoformat(),"end_date":end.isoformat(),"reporting_deadline":report_due.isoformat(),"status":status,"notes":notes.strip(),"created_by":_urafite_user_id}
                try:
                    _urafite_sb.table("grant_records").insert(payload).execute(); st.success(_urafite_translate("Grant record saved.")); st.rerun()
                except Exception as exc:
                    st.error(_urafite_translate("Could not save grant record. Run the latest database migration.")); st.caption(str(exc))
    grant_rows=_safe_admin_rows("grant_records")
    if grant_rows:
        import pandas as pd
        st.dataframe(pd.DataFrame(grant_rows),use_container_width=True,hide_index=True)
        st.download_button(_urafite_translate("Export grants (CSV)"),pd.DataFrame(grant_rows).to_csv(index=False).encode("utf-8-sig"),"urafite_grants.csv","text/csv")
    else: st.info(_urafite_translate("No grant records yet."))

elif page == "Professional Support":
    st.title("🤝 Professional Support")
    st.subheader("You deserve support from a real person.")
    st.write(
        "Digital tools can help you reflect, but some situations need human care. "
        "A qualified counsellor, mental-health professional or healthcare provider can listen, "
        "help you consider your options and guide you towards appropriate support."
    )
    st.warning(
        "URAFITE has not yet verified a directory of local referral providers. "
        "We will not display unconfirmed phone numbers, organisations or emergency contacts."
    )

    st.markdown("### When to seek support")
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("#### 🌿 Ongoing support")
            st.write("Consider speaking with a qualified professional if gambling, stress, debt, sleep problems or emotional distress are affecting your daily life.")
    with col2:
        with st.container(border=True):
            st.markdown("#### 🆘 Immediate danger")
            st.write("If you may hurt yourself or someone else, or cannot keep yourself safe, seek immediate in-person help through local emergency services or the nearest hospital.")
    st.markdown("### Preparing to speak with someone")
    st.write("You may find it helpful to:")
    st.markdown(
        "- Describe what has been happening, in your own words.\n"
        "- Explain how it is affecting your finances, relationships, studies or wellbeing.\n"
        "- Ask about confidentiality, costs and available support options.\n"
        "- Take a trusted person with you if that would make the conversation easier."
    )
    st.info("Before public launch, URAFITE should add a locally reviewed and verified referral directory, with clear consent and safeguarding procedures.")
