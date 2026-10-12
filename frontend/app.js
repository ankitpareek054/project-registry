const API_URL = "/api/projects";

const form = document.querySelector("#project-form");
const nameInput = document.querySelector("#project-name");
const descriptionInput = document.querySelector("#project-description");
const statusInput = document.querySelector("#project-status");
const filterInput = document.querySelector("#filter-status");
const projectList = document.querySelector("#project-list");
const submitButton = document.querySelector("#submit-button");
const cancelButton = document.querySelector("#cancel-edit");
const formTitle = document.querySelector("#form-title");
const message = document.querySelector("#message");

let editingProjectId = null;


async function loadProjects() {
    const status = filterInput.value;

    const url = status
        ? `${API_URL}?status=${encodeURIComponent(status)}`
        : API_URL;

    const response = await fetch(url);
    const projects = await response.json();

    renderProjects(projects);
}


function renderProjects(projects) {
    projectList.replaceChildren();

    if (projects.length === 0) {
        const empty = document.createElement("p");
        empty.textContent = "No projects found.";

        projectList.appendChild(empty);
        return;
    }

    for (const project of projects) {
        const card = document.createElement("article");
        card.className = "project-card";

        const title = document.createElement("h3");
        title.textContent = `${project.id}: ${project.name}`;

        const description = document.createElement("p");
        description.textContent =
            project.description || "No description";

        const status = document.createElement("p");
        status.className = "status";
        status.textContent = `Status: ${project.status}`;

        const actions = document.createElement("div");
        actions.className = "project-actions";

        const editButton = document.createElement("button");
        editButton.textContent = "Edit";
        editButton.addEventListener(
            "click",
            () => startEditing(project),
        );

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.addEventListener(
            "click",
            () => deleteProject(project.id),
        );

        actions.append(
            editButton,
            deleteButton,
        );

        card.append(
            title,
            description,
            status,
            actions,
        );

        projectList.appendChild(card);
    }
}


function startEditing(project) {
    editingProjectId = project.id;

    nameInput.value = project.name;
    descriptionInput.value = project.description;
    statusInput.value = project.status;

    formTitle.textContent =
        `Edit Project ${project.id}`;

    submitButton.textContent =
        "Save Changes";

    cancelButton.hidden = false;
}


function resetForm() {
    editingProjectId = null;

    form.reset();
    statusInput.value = "planned";

    formTitle.textContent =
        "Create Project";

    submitButton.textContent =
        "Create Project";

    cancelButton.hidden = true;
}


async function deleteProject(projectId) {
    const confirmed = window.confirm(
        "Delete this project?"
    );

    if (!confirmed) {
        return;
    }

    const response = await fetch(
        `${API_URL}/${projectId}`,
        {
            method: "DELETE",
        },
    );

    if (!response.ok) {
        message.textContent =
            "Could not delete project.";

        return;
    }

    message.textContent =
        "Project deleted.";

    await loadProjects();
}


form.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        const payload = {
            name: nameInput.value,
            description: descriptionInput.value,
            status: statusInput.value,
        };

        const editing =
            editingProjectId !== null;

        const url = editing
            ? `${API_URL}/${editingProjectId}`
            : API_URL;

        const method = editing
            ? "PATCH"
            : "POST";

        const response = await fetch(
            url,
            {
                method,
                headers: {
                    "Content-Type":
                        "application/json",
                },
                body: JSON.stringify(payload),
            },
        );

        if (!response.ok) {
            const error = await response.json();

            console.error(error);

            message.textContent =
                "Request failed.";

            return;
        }

        message.textContent = editing
            ? "Project updated."
            : "Project created.";

        resetForm();

        await loadProjects();
    },
);


cancelButton.addEventListener(
    "click",
    resetForm,
);


filterInput.addEventListener(
    "change",
    loadProjects,
);


loadProjects();