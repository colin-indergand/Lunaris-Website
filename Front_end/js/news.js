let posts = [];
let currentIndex = 0;
let cardElements = [];

async function loadPosts() {
  const res = await fetch(postsUrl);
  const allPosts = await res.json();
  posts = allPosts.slice(0, 5); // ✅ nur die 5 neuesten Beiträge laden

  if (posts.length < 3) return;

  cardElements = Array.from(document.querySelectorAll('.carousel-card'));
  updateCarousel();
  attachListeners();
}


function attachListeners() {
  cardElements[0].addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + posts.length) % posts.length;
    updateCarousel();
  });
  cardElements[2].addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % posts.length;
    updateCarousel();
  });
}

function updateCarousel() {
  const leftIdx = (currentIndex - 1 + posts.length) % posts.length;
  const rightIdx = (currentIndex + 1) % posts.length;

  const indices = [leftIdx, currentIndex, rightIdx];

  cardElements.forEach((card, i) => {
    const data = posts[indices[i]];
    card.className = 'carousel-card';
    if (i === 0) card.classList.add('left');
    if (i === 1) card.classList.add('center');
    if (i === 2) card.classList.add('right');
    card.innerHTML = `
      <h3>${data.title}</h3>
      <p>${data.text}</p>
    `;
  });
}

loadPosts();
