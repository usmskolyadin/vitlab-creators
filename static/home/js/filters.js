import { fetchBloggers } from "./api.js";
import { renderBloggers } from "./render.js";

export let selectedBloggers = [];
export let selectedIds = [];

export function applyFilters() {
  const filters = {};
  if (selectedBloggers.length) filters.name = selectedBloggers;
  if (selectedIds.length) filters.blogger_id = selectedIds;

  fetchBloggers(filters).then(bloggers => {
    renderBloggers(bloggers);
  });
}


export function renderSelectedTags(nameInput, idInput) {
  let nameContainer = nameInput.parentNode.querySelector(".tag-container.names");
  if (!nameContainer) {
    nameContainer = document.createElement("div");
    nameContainer.className = "tag-container names flex flex-wrap gap-2 mt-2";
    nameInput.parentNode.appendChild(nameContainer);
  }
  nameContainer.innerHTML = "";
  selectedBloggers.forEach(name => {
    const tag = document.createElement("span");
    tag.className = "bg-green-100 text-green-700 px-3 py-1 rounded-xl text-sm flex items-center gap-1";
    tag.innerHTML = `${name} <button class="ml-1 text-red-500">&times;</button>`;
    tag.querySelector("button").addEventListener("click", () => {
      selectedBloggers = selectedBloggers.filter(n => n !== name);
      renderSelectedTags(nameInput, idInput);
      applyFilters();
    });
    nameContainer.appendChild(tag);
  });

  // контейнер для ID
  let idContainer = idInput.parentNode.querySelector(".tag-container.ids");
  if (!idContainer) {
    idContainer = document.createElement("div");
    idContainer.className = "tag-container ids flex flex-wrap gap-2 mt-2";
    idInput.parentNode.appendChild(idContainer);
  }
  idContainer.innerHTML = "";
  selectedIds.forEach(id => {
    const tag = document.createElement("span");
    tag.className = "bg-blue-100 text-blue-700 px-3 py-1 rounded-xl text-sm flex items-center gap-1";
    tag.innerHTML = `${id} <button class="ml-1 text-red-500">&times;</button>`;
    tag.querySelector("button").addEventListener("click", () => {
      selectedIds = selectedIds.filter(i => i !== id);
      renderSelectedTags(nameInput, idInput);
      applyFilters();
    });
    idContainer.appendChild(tag);
  });
}

export function setupNameInput(filterNameInput) {
  const suggestionsList = document.createElement("ul");
  suggestionsList.className = "absolute bg-white border rounded shadow-md mt-1 z-50 w-full hidden";
  filterNameInput.parentNode.appendChild(suggestionsList);

  filterNameInput.addEventListener("input", async () => {
    const query = filterNameInput.value.trim();
    if (!query) {
      suggestionsList.classList.add("hidden");
      return;
    }

    try {
      const res = await fetch(`/bloggers_list/?name=${encodeURIComponent(query)}`);
      const data = await res.json();
      suggestionsList.innerHTML = "";

      if (!data.length) {
        suggestionsList.classList.add("hidden");
        return;
      }

      data.forEach(b => {
        const li = document.createElement("li");
        li.textContent = b.name;
        li.className = "px-3 py-2 hover:bg-gray-100 cursor-pointer";
        li.addEventListener("click", () => {
          if (!selectedBloggers.includes(b.name)) selectedBloggers.push(b.name);
          renderSelectedTags(filterNameInput, filterNameInput.nextElementSibling);
          applyFilters();
          filterNameInput.value = "";
          suggestionsList.classList.add("hidden");
        });
        suggestionsList.appendChild(li);
      });

      suggestionsList.classList.remove("hidden");
    } catch (e) {
      console.error("Ошибка загрузки подсказок:", e);
    }
  });

  filterNameInput.addEventListener("keydown", e => {
    if (e.key === "Enter") {
      e.preventDefault();
      const val = filterNameInput.value.trim();
      if (val && !selectedBloggers.includes(val)) selectedBloggers.push(val);
      renderSelectedTags(filterNameInput, filterNameInput.nextElementSibling);
      applyFilters();
      filterNameInput.value = "";
      suggestionsList.classList.add("hidden");
    }
  });

  document.addEventListener("click", e => {
    if (!filterNameInput.contains(e.target) && !suggestionsList.contains(e.target)) {
      suggestionsList.classList.add("hidden");
    }
  });
}
