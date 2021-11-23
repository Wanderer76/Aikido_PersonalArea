let changeButton = document.getElementById("stat-changer");
let ageTable = document.getElementById("age-table");
let rankTable = document.getElementById("rank-table");

let isRankHidden = false;

changeButton.onclick = function () {
    if (isRankHidden) {
        rankTable.classList.remove("hidden");
        ageTable.classList.add("hidden");
        isRankHidden = false
    } else {
        ageTable.classList.remove("hidden");
        rankTable.classList.add("hidden");
        isRankHidden = true;
    }
}