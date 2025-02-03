let container = document.querySelector(".container");
let svg = document.getElementById("svg-animation");
let icon = document.querySelector(".icon");

icon.onclick = function () {
  if (container.classList.contains("white")) {
    svg.firstChild.remove();
    changreBGToBlaack();
  } else {
    svg.firstChild.remove();
    changreBGToWhith();
  }
};

function changreBGToWhith() {
  bodymovin.loadAnimation({
    wrapper: document.getElementById("svg-animation"),
    animType: "svg",
    loop: false,
    path: "https://raw.githubusercontent.com/Abdallah-Mohamed-Sayed/some-files/main/toSun",
  });
  setTimeout(() => {
    container.classList.add("white");
    container.classList.remove("black");
  }, 276);
}

function changreBGToBlaack() {
  bodymovin.loadAnimation({
    wrapper: document.getElementById("svg-animation"),
    animType: "svg",
    loop: false,
    path: "https://raw.githubusercontent.com/Abdallah-Mohamed-Sayed/some-files/main/toMoon",
  });
  setTimeout(() => {
    container.classList.add("black");
    container.classList.remove("white");
  }, 276);
}

changreBGToWhith();
