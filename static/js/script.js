const indicator = document.querySelector(".nav-indicator");
const items = document.querySelectorAll(".info-link");
const blocks = document.querySelectorAll(".blocks");
const anchors = document.querySelectorAll('.info-link[href^="#"]');
const swiperWrapper = document.querySelector(".swiper-wrapper");
let active_item;

for (let anchor of anchors) {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const blockID = anchor.getAttribute("href");
    document.querySelector("" + blockID).scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  });
}

document.addEventListener("DOMContentLoaded", function () {
  var blocks = document.querySelectorAll("#animated-block");
  function revealBlocks() {
    blocks.forEach(function (block, index) {
      setTimeout(function () {
        block.style.opacity = 1;
        block.style.transform = "translateY(0)";
      }, index * 150);
    });
  }

  window.addEventListener("DOMContentLoaded", function () {
    revealBlocks();
    window.removeEventListener("DOMContentLoaded", arguments.callee);
  });
});

function handleIndicator(el) {
  items.forEach((item) => {
    item.classList.remove("is-active");
    item.removeAttribute("style");
  });

  indicator.style.width = `${el.offsetWidth}px`;
  indicator.style.left = `${el.offsetLeft}px`;
  active_item = el;
  el.classList.add("is-active");
}

items.forEach((item, index) => {
  item.addEventListener("click", (e) => {
    handleIndicator(e.target);
  });
  item.classList.contains("is-active") && handleIndicator(item);
});

var swiper_main = new Swiper(".swiper-prj", {
  on: {
    slideNextTransitionStart: function () {
      if (swiper_main.isEnd) {
        swiper_vertical.slideTo(1);
        swiper_main.slideTo(0);
      }
    },
  },
  grabCursor: true,
  slidesPerView: 1,
  initialSlide: 0,
  spaceBetween: 40,
  speed: 1000,
  keyboard: {
    enabled: true,
  },
  mousewheel: {
    thresholdDelta: 70,
  },
  autoplay: {
    enabled: false,
    delay: 5000,
    pauseOnMouseEnter: true,
    speed: 2000,
  },
  lazy: true,
});

var swiper_device = new Swiper(".swiper-device", {
  on: {
    slideNextTransitionStart: function () {
      if (swiper_device.isEnd) {
        swiper_vertical.slideTo(0);
        swiper_device.slideTo(0);
      }
    },
  },
  grabCursor: true,
  slidesPerView: 2,
  initialSlide: 0,
  spaceBetween: 40,
  speed: 1000,
  keyboard: {
    enabled: true,
  },
  mousewheel: {
    thresholdDelta: 70,
  },
  lazy: true,
  centeredSlides: true,
});

var swiper_vertical = new Swiper(".swiper-v", {
  direction: "vertical",
  grabCursor: true,
  slidesPerView: 1,
  spaceBetween: 60,
  speed: 2000,
  pagination: {
    el: ".swiper-pagination-v",
    clickable: true,
  },
});

function handleIntersection(entries, observer) {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      items.forEach((element) => {
        if (element.name == entry.target.id) {
          handleIndicator(element);
        }
      });
    }
  });
}

const observer = new IntersectionObserver(handleIntersection, {
  threshold: 0.5,
});

blocks.forEach((block) => {
  observer.observe(block);
});

function Change(cards) {
  fetch("/change", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name: cards }),
  })
    .then((response) => response.json())
    .then((data) => {
      updateCardsUI(data.updatedCards, data.updatedDeviceCards);
    });
}

function updateCardsUI(updatedCards, updatedDeviceCards) {
  swiper_main.removeAllSlides();
  swiper_device.removeAllSlides();
  updatedCards.forEach((card) => {
    const slide = `
      <div class="swiper-slide slide-prj" style="${card.style}">
        <div class="slide-text">
        <a href="/information/${
          card.id
        }"  class="details" target="_blank"><span class="arrow-8"></span>${
      card.title
    }</a>
          <p>${card.description}</p>
        </div>
        ${
          card.src.endsWith(".mp4")
            ? `<video controls muted class="slide-image" src="${card.src}"></video>`
            : `<img class="slide-image" src="${card.src}" />`
        }
      </div>
    `;
    swiper_main.appendSlide(slide);
  });
  updatedDeviceCards.forEach((card) => {
    const slide = `
    <div class="swiper-slide slide-device">
      <div class="card device" id="animated-block" style="background-image: url('/${card.src}'); opacity: 1; transform: translateY(0px);">
        <div class="card-content">
            <h1>${card.title}</h1>
            <p>${card.description}</p>
        </div>
        </div>
    </div>
`;
    swiper_device.appendSlide(slide);
  });
  const lastslide = `<div class="swiper-slide"></div>`;
  swiper_device.appendSlide(lastslide);
  swiper_main.appendSlide(lastslide);
  swiper_main.update();
  swiper_device.update();
}
let span = document.getElementById("changeText");

let btn_left = document.querySelector(".prev");
let btn_right = document.querySelector(".next");

btn_left.addEventListener("click", function () {
  if (span.innerHTML == "VR/AR/MR") {
    Change("3D Modeling");
    span.innerHTML = "3D Modeling";
  } else if (span.innerHTML == "AM") {
    Change("VR/AR/MR");
    span.innerHTML = "VR/AR/MR";
  } else if (span.innerHTML == "RI") {
    Change("AM");
    span.innerHTML = "AM";
  } else if (span.innerHTML == "3D Modeling") {
    Change("RI");
    span.innerHTML = "RI";
  }
  swiper_vertical.slideTo(0);
});

btn_right.addEventListener("click", function () {
  if (span.innerHTML == "VR/AR/MR") {
    Change("AM");
    span.innerHTML = "AM";
  } else if (span.innerHTML == "AM") {
    Change("RI");
    span.innerHTML = "RI";
  } else if (span.innerHTML == "RI") {
    Change("3D Modeling");
    span.innerHTML = "3D Modeling";
  } else if (span.innerHTML == "3D Modeling") {
    Change("VR/AR/MR");
    span.innerHTML = "VR/AR/MR";
  }
  swiper_vertical.slideTo(0);
});

window.addEventListener("resize", function () {
  handleIndicator(active_item);
});
