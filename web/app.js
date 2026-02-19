async function fetchState() {
  const res = await fetch("/projects/all");
  const data = await res.json();
  renderProjects(data);
}

function renderProjects(data) {
  const container = document.getElementById("projects");
  container.innerHTML = "";

  const active = data.active_project;

  for (const [name, path] of Object.entries(data.projects)) {
    const item = document.createElement("div");
    item.className = "project-item";

    const info = document.createElement("div");
    info.className = "project-info";

    const nameRow = document.createElement("div");
    nameRow.className = "project-name";
    nameRow.innerText = name;

    if (name === active) {
      const badge = document.createElement("span");
      badge.className = "active-badge";
      badge.innerText = "ACTIVE";
      nameRow.appendChild(badge);
    }

    const pathEl = document.createElement("div");
    pathEl.className = "project-path";
    pathEl.innerText = path;

    info.appendChild(nameRow);
    info.appendChild(pathEl);

    const actions = document.createElement("div");
    actions.className = "actions";

    const activateBtn = document.createElement("button");
    activateBtn.className = "primary";
    activateBtn.innerText = "Activate";
    activateBtn.onclick = () => activateProject(name);

    const deleteBtn = document.createElement("button");
    deleteBtn.className = "danger";
    deleteBtn.innerText = "Delete";
    deleteBtn.onclick = () => deleteProject(name);

    actions.appendChild(activateBtn);
    actions.appendChild(deleteBtn);

    item.appendChild(info);
    item.appendChild(actions);

    container.appendChild(item);
  }
}

async function addProject() {
  response = await fetch("/projects/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: document.getElementById("name").value,
      path: document.getElementById("path").value
    })
  });

  if (!response.ok) {
    alert("one of the fields is missing, Please check your input") 
    return
  }

  fetchState();
}

async function activateProject(name) {
  response = await fetch("/projects/set", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name })
  });

  if (response.ok) {
    alert("Activated "+ name + " successfully")
  }

  fetchState();
}

async function deleteProject(name) {
  response = await fetch(`/projects/${name}`, {
    method: "DELETE"
  });

  if (!response.ok) {
    alert("Invalid request")
  }

  fetchState();
}

fetchState();