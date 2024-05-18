// grab everything we need
const btn = document.querySelector(".mobile-menu-button");
const sidebar = document.querySelector(".sidebar");
let isSidebarOpen = false;

// add our event listener for the click
btn.addEventListener("click", () => {
  sidebar.classList.toggle("-translate-x-full");
});

// close sidebar if user clicks outside of the sidebar
document.addEventListener("click", (event) => {
  const isButtonClick = btn === event.target && btn.contains(event.target);
  const isOutsideClick =
    sidebar !== event.target && !sidebar.contains(event.target);

  // bail out if sidebar isnt open
  if (sidebar.classList.contains("-translate-x-full")) return;

  // if the user clicks the button, then toggle the class
  if (isButtonClick) {
    console.log("does not contain");
    sidebar.classList.toggle("-translate-x-full");
    return;
  }

  // check to see if user clicks outside the sidebar
  if (!isButtonClick && isOutsideClick) {
    console.log("outside click");
    sidebar.classList.add("-translate-x-full");
    return;
  }
});
