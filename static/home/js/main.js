import { fetchBloggers } from "./api.js";
import { renderBloggers, calcTotals } from "./render.js";
import { setupNameInput, renderSelectedTags, applyFilters } from "./filters.js";

const filterNameInput = document.getElementById("filterName");
const filterIdInput = document.getElementById("filterId");

setupNameInput(filterNameInput);
renderSelectedTags(filterNameInput, filterIdInput);

async function loadBloggers() {
  const bloggers = await fetchBloggers();
  if (!bloggers || !Array.isArray(bloggers)) return;
  renderBloggers(bloggers);
  calcTotals(bloggers);
}

loadBloggers();

document.getElementById('resetFiltersBtn').addEventListener('click', async () => {
  const bloggers = await fetchBloggers();
  renderBloggers(bloggers);
  calcTotals(bloggers);
});
