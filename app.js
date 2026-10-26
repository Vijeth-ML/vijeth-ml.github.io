const categories = ["All", "Research", "Deep Learning", "Computer Vision", "Reinforcement Learning", "NLP", "Machine Learning", "Unsupervised Learning", "Programming"];
const grid = document.querySelector("#project-grid");
const filterBox = document.querySelector("#filters");
const search = document.querySelector("#search");
const count = document.querySelector("#result-count");
const empty = document.querySelector("#empty-state");
const dialog = document.querySelector("#project-dialog");
let projects = [];
let activeCategory = "All";

function renderFilters() {
  filterBox.innerHTML = categories.map(category =>
    `<button class="filter ${category === activeCategory ? "active" : ""}" type="button" data-category="${category}" aria-pressed="${category === activeCategory}">${category}</button>`
  ).join("");
}
function card(project, index) {
  const tags = project.tags.map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join("");
  return `<article class="project-card">
    <div class="card-top"><span class="category-label">${escapeHtml(project.category)}</span><span class="year-label">${escapeHtml(project.year)}</span></div>
    <h3>${escapeHtml(project.title)}</h3><p>${escapeHtml(project.summary)}</p>
    <div class="tag-list">${tags}</div>
    <button class="card-action" type="button" data-project="${index}" aria-label="Open details for ${escapeHtml(project.title)}"><span>Explore project notes</span><span aria-hidden="true">↗</span></button>
  </article>`;
}
function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
}
function renderProjects() {
  const term = search.value.trim().toLowerCase();
  const matching = projects.map((project, index) => ({project, index})).filter(({project}) => {
    const categoryMatch = activeCategory === "All" || project.category === activeCategory;
    const searchable = [project.title, project.category, project.summary, ...project.tags, project.question].join(" ").toLowerCase();
    return categoryMatch && searchable.includes(term);
  });
  grid.innerHTML = matching.map(({project}, index) => card(project, projects.indexOf(project))).join("");
  count.textContent = `${matching.length} ${matching.length === 1 ? "project" : "projects"} shown`;
  empty.hidden = matching.length !== 0;
  grid.hidden = matching.length === 0;
}
function openProject(project) {
  document.querySelector("#dialog-category").textContent = `${project.category} · ${project.year}`;
  document.querySelector("#dialog-title").textContent = project.title;
  document.querySelector("#dialog-summary").textContent = project.summary;
  document.querySelector("#dialog-question").textContent = project.question;
  document.querySelector("#dialog-approach").textContent = project.approach;
  document.querySelector("#dialog-lessons").textContent = project.lessons;
  document.querySelector("#dialog-status").textContent = project.status;
  dialog.showModal();
}
filterBox.addEventListener("click", event => {
  const button = event.target.closest("button[data-category]");
  if (!button) return;
  activeCategory = button.dataset.category;
  renderFilters(); renderProjects();
});
search.addEventListener("input", renderProjects);
grid.addEventListener("click", event => {
  const button = event.target.closest("button[data-project]");
  if (button) openProject(projects[Number(button.dataset.project)]);
});
document.querySelector("#dialog-close").addEventListener("click", () => dialog.close());
document.querySelector("#dialog-done").addEventListener("click", () => dialog.close());
dialog.addEventListener("click", event => { if (event.target === dialog) dialog.close(); });
document.querySelector("#theme-toggle").addEventListener("click", () => {
  const light = document.documentElement.classList.toggle("light");
  document.querySelector("#theme-toggle").textContent = light ? "☀" : "☾";
  document.querySelector("#theme-toggle").setAttribute("aria-label", light ? "Switch to dark theme" : "Switch to light theme");
});
fetch("projects.json").then(response => {
  if (!response.ok) throw new Error("Could not load projects.json");
  return response.json();
}).then(data => {
  projects = data;
  document.querySelector("#project-count").textContent = projects.length;
  renderFilters(); renderProjects();
}).catch(() => {
  grid.innerHTML = `<p>Project data could not load. Open this site through GitHub Pages or a local web server rather than directly as a file.</p>`;
});
