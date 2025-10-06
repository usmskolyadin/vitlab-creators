export let bloggers = [];

export async function fetchBloggers(filters = {}) {
  document.getElementById("loader").classList.remove("hidden");
  try {
    let url = new URL("/bloggers_list/", window.location.origin);
    Object.keys(filters).forEach(key => {
      if (Array.isArray(filters[key])) {
        filters[key].forEach(v => url.searchParams.append(key, v));
      } else if (filters[key]) {
        url.searchParams.append(key, filters[key]);
      }
    });

    const res = await fetch(url);
    if (!res.ok) throw new Error(`${res.status}: ${res.statusText}`);
    const data = await res.json();  // <- возвращаем данные
    return data;
  } catch (e) {
    console.error("Ошибка загрузки:", e);
    return [];
  } finally {
    document.getElementById("loader").classList.add("hidden");
  }
}

export async function fetchBloggerHistory(bloggerId) {
  const res = await fetch(`/blogger_history/${bloggerId}/`);
  return await res.json();
}
