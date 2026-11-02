const grid=document.getElementById('projectGrid');
function render(filter='all'){grid.innerHTML='';const items=PROJECTS.filter(p=>filter==='all'||p.category===filter);items.forEach((p,i)=>{const el=document.createElement('article');el.className='project-card';el.innerHTML=`<div class="card-top"><span>MISSION ${String(i+1).padStart(2,'0')}</span><span class="tag">${p.tag}</span></div><h3>${p.title}</h3><p>${p.problem}</p><button class="expand" aria-expanded="false">Explore the story <span>↗</span></button><div class="details"><h4>Approach</h4><p>${p.approach}</p><h4>Evidence so far</h4><p>${p.evidence}</p><h4>Limitations</h4><p>${p.limits}</p><h4>Where next?</h4><p>${p.next}</p></div>`;const evidence=(window.PROJECT_EVIDENCE&&window.PROJECT_EVIDENCE[p.id])||[];if(evidence.length){const gallery=document.createElement('div');gallery.className='evidence-gallery';gallery.innerHTML='<h4>Original project evidence</h4><p class="evidence-note">Original report pages are shown as submitted; open an image to inspect it at full size. Captions identify the source report and page.</p>'+evidence.map(v=>`<figure><a href="${v.src}" target="_blank" rel="noopener noreferrer"><img loading="lazy" src="${v.src}" alt="${v.caption}"></a><figcaption>${v.caption}<br><a href="${v.source}" target="_blank" rel="noopener noreferrer">Open original report ↗</a></figcaption></figure>`).join('');el.querySelector('.details').appendChild(gallery)}const links=document.createElement('p');links.className='project-links';links.innerHTML=`<a href="https://github.com/Vijeth-ML/vijeth-ml.github.io/tree/main/projects/${p.id}" target="_blank" rel="noopener noreferrer">View project source and documentation ↗</a>`;el.querySelector('.details').appendChild(links);el.querySelector('.expand').addEventListener('click',e=>{const open=el.classList.toggle('expanded');e.currentTarget.setAttribute('aria-expanded',open)});grid.appendChild(el)})}
render();document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-filter]').forEach(x=>x.classList.remove('active'));b.classList.add('active');render(b.dataset.filter)}));
const panel=document.getElementById('chatPanel');function openChat(){panel.classList.add('visible');panel.setAttribute('aria-hidden','false');document.getElementById('chatInput').focus()}function closeChat(){panel.classList.remove('visible');panel.setAttribute('aria-hidden','true')}document.getElementById('chatOpen').onclick=openChat;document.getElementById('chatClose').onclick=closeChat;
const messages=document.getElementById('chatMessages');function bubble(text,who='bot',html=false){const d=document.createElement('div');d.className='bubble '+who;if(html)d.innerHTML=text;else d.textContent=text;messages.appendChild(d);messages.scrollTop=messages.scrollHeight}
const stopwords=new Set(['what','which','where','when','who','how','does','did','your','you','the','and','for','about','with','from','tell','show','explain','project','projects','can','could','would','was','are','is','this','that','have','has','into','next','some','any']);
let lastDiscussedProject = null;

function answer(q) {
  const s = q.toLowerCase().trim();

  if (/^(hi|hello|hey|good morning|good evening)\b/.test(s)) {
    return 'Hello! Think of me as a friendly guide to this portfolio. I can explain the projects without assuming you know the technical jargon, then go deeper into models, evaluation or future experiments. What would you like to explore?';
  }

  if (/research direction|exoplanet|astronom|kepler|tess|light curve/.test(s)) {
    return 'The research direction described here is robust machine learning for astronomy, especially finding exoplanets in Kepler and TESS light curves. In simple terms, a planet can pass in front of its star and cause a tiny, repeating dip in brightness. The challenge is that stellar activity, instrument noise and other astrophysical events can look similar. A promising next research step is to test whether models trained on one telescope or observing setup still work on another, while measuring uncertainty and false positives.';
  }

  const tokens = s.split(/[^a-z0-9]+/).filter(Boolean);

  // Identify a project explicitly mentioned in the question.
  // Match project titles and IDs, rather than generic technical terms.
  const explicitMatches = PROJECTS.map(p => {
    const identity = (p.title + ' ' + p.id)
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, ' ')
      .split(/\s+/)
      .filter(t => t.length > 2);

    const uniqueIdentity = [...new Set(identity)];
    const matched = uniqueIdentity.filter(t => tokens.includes(t));

    return {
      p,
      score: matched.length,
      total: uniqueIdentity.length
    };
  }).filter(x => x.score > 0)
    .sort((a, b) => b.score - a.score);

  // If the question names a project, use that project.
  let p = null;

  if (explicitMatches.length) {
    const best = explicitMatches[0];

    // Avoid guessing when multiple projects are equally plausible.
    const tied = explicitMatches.filter(x => x.score === best.score);

    if (tied.length > 1) {
      return 'I can help with that, but I found more than one possible project. Could you mention the project name so I can give you the correct information?';
    }

    p = best.p;
  }

  // Recognise questions referring to the previously discussed project.
  const refersToPrevious =
    /\b(it|its|that|this|they|them|their|those|these)\b/.test(s);

  const asksProjectDetail =
    /\b(method|methods|methodology|approach|model|models|algorithm|algorithms|technique|techniques|result|results|accuracy|score|metric|metrics|evidence|limitation|limitations|weakness|weaknesses|challenge|challenges|future|improve|improvement|trained|training|dataset|data|performance|worked|built|used)\b/.test(s);

  const genericFollowUp =
    /^(what about|and|why|how about|limitations?|weaknesses?|future work|next steps?|results?|evidence|approach|methods?|methodology|techniques?|algorithms?|models?|explain more|go deeper|tell me more)\b/.test(s);

  // Use conversation history only when the question does not
  // explicitly identify a different project.
  if (!p && lastDiscussedProject && (refersToPrevious || genericFollowUp) && asksProjectDetail) {
    p = lastDiscussedProject;
  }

  // If no project was identified, search for a meaningful project match.
  if (!p) {
    const stop = new Set([
      'what','which','where','when','who','how','does','did',
      'your','you','the','and','for','about','with','from',
      'tell','show','explain','project','projects','can','could',
      'would','was','are','is','this','that','have','has',
      'into','next','some','any','its','it','they','them',
      'their','method','methods','approach','used','use'
    ]);

    const terms = tokens.filter(t => t.length > 2 && !stop.has(t));

    const ranked = PROJECTS.map(project => {
      const hay = (
        project.title + ' ' + project.id + ' ' + project.tag + ' ' +
        project.problem + ' ' + project.approach + ' ' +
        project.evidence + ' ' + project.limits + ' ' +
        project.next + ' ' + project.keywords
      ).toLowerCase();

      return {
        p: project,
        score: terms.reduce(
          (n, t) => n + (hay.includes(t) ? 1 : 0),
          0
        )
      };
    }).sort((a, b) => b.score - a.score);

    if (ranked[0]?.score > 0) {
      p = ranked[0].p;
    }
  }

  // Handle comparisons separately.
  if (/compare|difference between|similarities/.test(s)) {
    if (/cnn|emnist|character|handwrit/.test(s)) {
      return 'The EMNIST project is the clearest comparison in this archive: it contrasts an MLP, which learns from flattened pixel values, with a CNN, which can learn local spatial patterns such as strokes and edges. The saved notebook reports higher historical test accuracy for the CNN (87.12%) than the MLP (about 84.13%), but these figures are not independently reproduced and the evaluation needs correction. A fair comparison should use the same split, preprocessing and training budget, then compare per-class errors as well as accuracy.';
    }

    return 'I can compare projects when their source material supports it. For example, EMNIST and semantic segmentation are both computer-vision tasks, but EMNIST predicts one label for an image while segmentation predicts a class for each pixel. Which pair would you like me to compare?';
  }

  if (p) {
    // Update the conversation context to the project actually selected.
    lastDiscussedProject = p;

    let section = '';

    if (/limitation|weakness|failure|challenge|risk/.test(s)) {
      section = `The limitations to keep in view: ${p.limits}`;
    } else if (/next|future|improve|progress|research/.test(s)) {
      section = `A possible next step: ${p.next}`;
    } else if (/result|accuracy|score|metric|evidence|performance|worked/.test(s)) {
      section = `What the current record says: ${p.evidence}`;
    } else if (/method|methodology|approach|model|algorithm|technique|how|built|train|training|used/.test(s)) {
      section = `How it was approached: ${p.approach}`;
    } else {
      section =
        `The problem: ${p.problem}\n\n` +
        `The approach: ${p.approach}\n\n` +
        `Evidence: ${p.evidence}\n\n` +
        `Limitations: ${p.limits}\n\n` +
        `Where it could go next: ${p.next}`;
    }

    return `Let's look at ${p.title}.\n\n${section}\n\nYou can ask a follow-up about its methods, evidence, limitations or next experiment.`;
  }

  // Avoid silently assigning an unclear pronoun to an unrelated project.
  if (refersToPrevious && asksProjectDetail && !lastDiscussedProject) {
    return 'Which project are you referring to? Tell me its name and I can explain its methods, results or limitations.';
  }

  return 'I can’t find a grounded answer to that in the project notes I have, and I’d rather be honest than invent details. I can still help with the projects documented here: the mental-health dissertation, EMNIST, semantic segmentation, multi-armed bandits, voting rules, bank-account software, Gym reinforcement learning, binary classification, word-embedding clustering and multilingual-chatbot research.\n\nIf your question is outside this portfolio, these may help: Google Scholar (https://scholar.google.com/), GitHub (https://github.com/Vijeth-ML), or NASA Exoplanet Archive (https://exoplanetarchive.ipac.caltech.edu/).';
}

function send(q){if(!q.trim())return;bubble(q,'user');bubble(answer(q));}document.getElementById('chatForm').addEventListener('submit',e=>{e.preventDefault();const input=document.getElementById('chatInput');send(input.value);input.value=''});document.querySelectorAll('.suggestions button').forEach(b=>b.addEventListener('click',()=>send(b.textContent)));document.addEventListener('keydown',e=>{if(e.key==='Escape')closeChat()});
