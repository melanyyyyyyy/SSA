const customSelect = document.querySelector(".custom-select");
const optionsList = document.querySelector(".custom-options-list");
const options = document.querySelectorAll(".custom-option");
const nativeSelect = document.getElementById("subject");
const selectSpan = customSelect.querySelector("span");

customSelect.addEventListener("click", () => {
    optionsList.classList.toggle("active");
    const icon = customSelect.querySelector(".angle-down, .angle-up");
    if (optionsList.classList.contains("active")) {
        icon.classList.remove("angle-down");
        icon.classList.add("angle-up");
        const optionHeight = options.length > 0 ? options[0].offsetHeight : 0;
        if (options.length <= 3) {
            optionsList.style.height = (optionHeight * options.length) + "px";
        } else {
            optionsList.style.height = (optionHeight * 3) + "px";
        }
        optionsList.style.border = "1px solid #ced4da";
    } else {
        icon.classList.remove("angle-up");
        icon.classList.add("angle-down");
        optionsList.style.height = "0";
        optionsList.style.border = "none";
    }
});

options.forEach((option) => {
    option.addEventListener("click", () => {
        options.forEach((opt) => { opt.classList.remove('selected') });
        selectSpan.innerHTML = option.innerHTML;
        option.classList.add("selected");
        const selectedValue = option.getAttribute("data-value");
        nativeSelect.value = selectedValue;
        optionsList.classList.remove("active");
        optionsList.style.height = "0";
        optionsList.style.border = "none";
        const icon = customSelect.querySelector(".angle-down, .angle-up");
        if (icon) {
            icon.classList.remove("angle-up");
            icon.classList.add("angle-down");
        }
    });
});

document.addEventListener("click", (e) => {
    if (!customSelect.contains(e.target) && !optionsList.contains(e.target)) {
        optionsList.classList.remove("active");
        optionsList.style.height = "0";
        optionsList.style.border = "none";
        const icon = customSelect.querySelector(".angle-down, .angle-up");
        if (icon) {
            icon.classList.remove("angle-up");
            icon.classList.add("angle-down");
        }
    }
});

function openCancelModal() {
    document.getElementById('cancel-modal').classList.add('modal--show');
}

function closeCancelModal() {
    document.getElementById('cancel-modal').classList.remove('modal--show');
}