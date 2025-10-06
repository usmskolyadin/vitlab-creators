import { getPlatformIcon } from "./get_platform_icon.js";

export function calcTotals(bloggers) {
    let totalLikes = 0, totalComments = 0, totalVideos = 0, totalViews = 0, totalSubscribers = 0;
    bloggers.forEach(b => {
        for (const s of Object.values(b.stats)) {
        totalLikes += s.likes;
        totalComments += s.comments;
        totalVideos += s.videos;
        totalViews += s.views;
        totalSubscribers += s.subscribers || 0;
        }
    });
    document.getElementById("totalLikes").textContent = totalLikes;
    document.getElementById("totalComments").textContent = totalComments;
    document.getElementById("totalVideos").textContent = totalVideos;
    document.getElementById("totalViews").textContent = totalViews;
    document.getElementById("totalSubscribers").textContent = totalSubscribers;
    }


export function renderBloggers(bloggers) {
  const container = document.getElementById("bloggerList");
  container.innerHTML = "";

  bloggers.forEach(b => {
    const avatar = b.avatar_url
      ? `<img src="${b.avatar_url}" class="w-16 h-16 rounded-full object-cover">`
      : `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="64" height="64">
          <!-- фон -->
          <circle cx="12" cy="12" r="12" fill="#f5eee8"/>
          <!-- силуэт -->
          <path fill="#e4ccb4" d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
        </svg>
        `;

    let totalLikes = 0, totalComments = 0, totalVideos = 0, totalViews = 0, totalSubscribers = 0;
    for (const s of Object.values(b.stats)) { 
      totalLikes += s.likes;
      totalComments += s.comments;
      totalVideos += s.videos;
      totalViews += s.views;
      totalSubscribers += s.subscribers || 0;
    }

    const statsSummary = `
      <div class="grid lg:grid-cols-5 grid-cols-3 gap-4 text-center text-sm">
        <div class="p-2 rounded-2xl">
          <p class="text-[10px] uppercase text-[#6B7280] font-medium">Подписчики</p> 
          <p class="font-bold  text-black">${totalSubscribers}</p>
        </div>
        <div class="p-2 rounded-2xl">
          <p class="text-[10px] uppercase text-[#6B7280] font-medium">Просмотры</p>
          <p class="font-bold  text-black">${totalViews}</p>
        </div>
        <div class="p-2 rounded-2xl">
          <p class="text-[10px] uppercase text-[#6B7280] font-medium">Видео</p>
          <p class="font-bold  text-black">${totalVideos}</p>
        </div>
        <div class="p-2 rounded-2xl">
          <p class="text-[10px] uppercase text-[#6B7280] font-medium">Лайки</p>
          <p class="font-bold  text-black">${totalLikes}</p>
        </div>
        <div class="p-2 rounded-2xl">
          <p class="text-[10px] uppercase text-[#6B7280] font-medium">Комментарии</p>
          <p class="font-bold  text-black">${totalComments}</p>
        </div>

      </div>
    `;

    const div = document.createElement("div");
    div.className = "bg-white  border border-[#E5E7EB] p-4 transition hover:bg-gray-100 rounded-3xl  hover:-md transition";

    div.innerHTML = `
      <div class="lg:flex items-center justify-between gap-4 cursor-pointer blogger-header">
        <div class="flex items-center gap-4">
          ${avatar} 
          <div class=" ">
            <h3 class="flex items-center z-20 text-lg font-semibold text-gray-800">${b.name} • 
              <a class="hover:scale-105" href="${b.telegram_url}">
              <svg width="25px" height="25px" class="ml-2" viewBox="0 0 256 256" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" preserveAspectRatio="xMidYMid">
                  <g>
                      <path d="M128,0 C57.307,0 0,57.307 0,128 L0,128 C0,198.693 57.307,256 128,256 L128,256 C198.693,256 256,198.693 256,128 L256,128 C256,57.307 198.693,0 128,0 L128,0 Z" fill="#40B3E0">

                  </path>
                          <path d="M190.2826,73.6308 L167.4206,188.8978 C167.4206,188.8978 164.2236,196.8918 155.4306,193.0548 L102.6726,152.6068 L83.4886,143.3348 L51.1946,132.4628 C51.1946,132.4628 46.2386,130.7048 45.7586,126.8678 C45.2796,123.0308 51.3546,120.9528 51.3546,120.9528 L179.7306,70.5928 C179.7306,70.5928 190.2826,65.9568 190.2826,73.6308" fill="#FFFFFF">

                  </path>
                          <path d="M98.6178,187.6035 C98.6178,187.6035 97.0778,187.4595 95.1588,181.3835 C93.2408,175.3085 83.4888,143.3345 83.4888,143.3345 L161.0258,94.0945 C161.0258,94.0945 165.5028,91.3765 165.3428,94.0945 C165.3428,94.0945 166.1418,94.5735 163.7438,96.8115 C161.3458,99.0505 102.8328,151.6475 102.8328,151.6475" fill="#D2E5F1">

                  </path>
                          <path d="M122.9015,168.1154 L102.0335,187.1414 C102.0335,187.1414 100.4025,188.3794 98.6175,187.6034 L102.6135,152.2624" fill="#B5CFE4">

                  </path>
                  </g>
              </svg>
              </a>
              </h3>
            <h3 class="text-md font-medium text-[#636b80]">Creator № 234</h3>
          </div>
        </div>
        ${statsSummary}
      </div>
      <div class="blogger-stats hidden mt-4"></div>
    `;

    div.querySelector(".blogger-header").addEventListener("click", () => {
      const statsContainer = div.querySelector(".blogger-stats");
      if (statsContainer.classList.contains("hidden")) {
        showBloggerStats(b, statsContainer);
      } else {
        statsContainer.classList.add("hidden");
        statsContainer.innerHTML = "";
      }
    });

    container.appendChild(div);
  });
}
export function showBloggerStats(blogger, container) {
  container.innerHTML = "";
  showBloggerHistory(blogger.id, container);
  const header = document.createElement("div");
  header.className = "grid grid-cols-6 gap-4 font-medium text-gray-100 p-3 pb-2 mb-2";
  header.innerHTML = `
    <div class="text-[#6B7280] text-center">📱 Соц. сеть</div>
    <div class="text-[#6B7280] text-center">📊 Подписчики</div>
    <div class="text-[#6B7280] text-center">📷 Просмотры</div>
    <div class="text-[#6B7280] text-center">📈 Видео</div>
    <div class="text-[#6B7280] text-center">♥️ Лайки</div>
    <div class="text-[#6B7280] text-center">💬 Комментарии</div>
  `;
  container.appendChild(header);

  for (const [platform, stats] of Object.entries(blogger.stats)) {
    const row = document.createElement("div");
    row.className = "grid grid-cols-6 gap-4 items-center bg-gray-[#F9FAFB] p-2 rounded-xl  mb-2";
    row.innerHTML = `
      <div class="font-bold  p-3 mr-2 text-gray-800 flex items-center">
        <a href="${stats.url || '#'}" target="_blank" class="flex hover:text-blue-500 transition items-center gap-2">
          ${getPlatformIcon(platform)}
          ${platform.toUpperCase()}
        </a>
      </div>
      <div class="text-center text-lg font-medium">${stats.subscribers}</div>
      <div class="text-center text-lg font-medium">${stats.views}</div>
      <div class="text-center text-lg font-medium">${stats.videos}</div>
      <div class="text-center text-lg font-medium">${stats.likes}</div>
      <div class="text-center text-lg font-medium">${stats.comments}</div>
    `;
    container.appendChild(row);
  }

  container.classList.remove("hidden");
}
export async function showBloggerHistory(bloggerId, container) {
  const res = await fetch(`/blogger_history/${bloggerId}/`);
  const history = await res.json();

  const table = document.createElement("div");
  table.className = "overflow-x-auto bg-gray-[#F9FAFB] p-3 rounded-2xl";

  // Создаем заголовки: Дата, Имя, TikTok, Instagram, YouTube, VK
  let html = `

  `;

  history.forEach(dayRow => {
    const day = dayRow.day;
const bloggerName = Object.values(dayRow.stats)[0]?.name || "-";

    // Формируем колонки с данными по соцсетям
    const platforms = ["tiktok", "instagram", "youtube", "vk"];
    const statsRow = platforms.map(p => {
      if (dayRow.stats[p]) {
        const s = dayRow.stats[p];
        return `Видео: ${s.videos}`;
      } else {
        return "-";
      }
    }).join("</td><td class='p-2'>");

    html += `

    `;
  });

  html += "</tbody></table>";
  table.innerHTML = html;
  container.appendChild(table);
}
